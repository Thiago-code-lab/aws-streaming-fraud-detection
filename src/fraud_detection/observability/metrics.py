from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineMetrics:
    transactions_analyzed: int
    suspicious_transactions: int
    top_reasons: dict[str, int]

    @property
    def suspicious_rate(self) -> float:
        if self.transactions_analyzed == 0:
            return 0.0
        return self.suspicious_transactions / self.transactions_analyzed
