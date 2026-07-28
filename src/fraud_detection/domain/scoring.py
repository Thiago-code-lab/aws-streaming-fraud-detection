from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from fraud_detection.config import FraudRuleConfig
from fraud_detection.domain.models import FraudAssessment, RiskLevel, RuleEvidence, Transaction
from fraud_detection.domain.rules import FraudRule


def classify_risk(score: int, config: FraudRuleConfig) -> RiskLevel:
    if score >= config.high_risk_threshold:
        return RiskLevel.HIGH
    if score >= config.medium_risk_threshold:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


class FraudScorer:
    def __init__(self, rules: Sequence[FraudRule], config: FraudRuleConfig) -> None:
        self.rules = list(rules)
        self.config = config

    def assess(
        self,
        transaction: Transaction,
        history: Sequence[Transaction],
        processed_at: datetime | None = None,
    ) -> FraudAssessment:
        evidence = [result for rule in self.rules if (result := rule.evaluate(transaction, history)) is not None]
        score = min(100, sum(item.weight for item in evidence))
        return FraudAssessment(
            transaction_id=transaction.transaction_id,
            event_timestamp=transaction.event_timestamp,
            processed_at=processed_at or datetime.now(UTC),
            amount=transaction.amount,
            state=transaction.state,
            device_type=transaction.device_type,
            risk_score=score,
            risk_level=classify_risk(score, self.config),
            triggered_rules=[item.rule_id for item in evidence],
            rule_evidence=[_evidence_to_dict(item) for item in evidence],
            rules_version=self.config.rules_version,
            customer_id=transaction.customer_id,
            masked_card=transaction.masked_card,
            merchant_category=transaction.merchant_category,
        )


def _evidence_to_dict(evidence: RuleEvidence) -> dict[str, object]:
    return {
        "rule_id": evidence.rule_id,
        "description": evidence.description,
        "weight": evidence.weight,
        "details": evidence.details,
    }
