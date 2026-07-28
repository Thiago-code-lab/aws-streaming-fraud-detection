from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fraud_detection.config import AppConfig
from fraud_detection.domain.models import FraudAssessment, Transaction
from fraud_detection.domain.rules import build_default_rules
from fraud_detection.domain.scoring import FraudScorer
from fraud_detection.infrastructure.local.file_repository import LocalFileRepository
from fraud_detection.processing.parquet_writer import write_partitioned_parquet


@dataclass(frozen=True)
class PipelineSummary:
    transactions_analyzed: int
    suspicious_transactions: int
    output_json_files: int
    output_parquet_files: int
    top_reasons: dict[str, int]


class FraudPipeline:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.scorer = FraudScorer(build_default_rules(config.rule_config), config.rule_config)

    def process(self, transactions: list[Transaction], repository: LocalFileRepository) -> PipelineSummary:
        seen_ids: set[str] = set()
        history: list[Transaction] = []
        assessments: list[FraudAssessment] = []
        processed_at = max((transaction.event_timestamp for transaction in transactions), default=None)
        for transaction in transactions:
            if transaction.transaction_id in seen_ids:
                continue
            seen_ids.add(transaction.transaction_id)
            assessment = self.scorer.assess(transaction, history, processed_at)
            assessments.append(assessment)
            history.append(transaction)

        raw_files = repository.write_raw_transactions(transactions)
        assessment_rows = [assessment.to_dict() for assessment in assessments]
        processed_json_files = repository.write_processed_assessments(assessment_rows)
        parquet_files = write_partitioned_parquet(assessment_rows, repository.processed_parquet_dir)
        return PipelineSummary(
            transactions_analyzed=len(seen_ids),
            suspicious_transactions=sum(1 for item in assessments if item.is_suspicious),
            output_json_files=len(raw_files) + len(processed_json_files),
            output_parquet_files=len(parquet_files),
            top_reasons=_top_reasons(assessments),
        )


def _top_reasons(assessments: list[FraudAssessment]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for assessment in assessments:
        for rule_id in assessment.triggered_rules:
            counts[rule_id] = counts.get(rule_id, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


def run_local_demo(config: AppConfig, transactions: list[Transaction]) -> PipelineSummary:
    repository = LocalFileRepository(Path(config.data_dir))
    return FraudPipeline(config).process(transactions, repository)
