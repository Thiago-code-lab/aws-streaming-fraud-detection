from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class CustomerProfile:
    customer_id: str
    home_state: str
    usual_device_type: str
    typical_amount: float


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    event_timestamp: datetime
    amount: float
    state: str
    device_type: str
    customer_id: str
    customer_profile_amount: float
    customer_home_state: str
    customer_usual_device_type: str
    masked_card: str
    merchant_category: str

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("amount deve ser positivo")
        if len(self.state) != 2:
            raise ValueError("state deve ser uma sigla de UF com duas letras")
        if not self.masked_card.startswith("card_"):
            raise ValueError("masked_card deve estar tokenizado")
        if self.event_timestamp.tzinfo is None:
            raise ValueError("event_timestamp deve conter timezone")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["event_timestamp"] = self.event_timestamp.astimezone(UTC).isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Transaction":
        timestamp = data["event_timestamp"]
        parsed_timestamp = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00")).astimezone(UTC)
        return cls(
            transaction_id=str(data["transaction_id"]),
            event_timestamp=parsed_timestamp,
            amount=float(data["amount"]),
            state=str(data["state"]).upper(),
            device_type=str(data["device_type"]),
            customer_id=str(data["customer_id"]),
            customer_profile_amount=float(data["customer_profile_amount"]),
            customer_home_state=str(data["customer_home_state"]).upper(),
            customer_usual_device_type=str(data["customer_usual_device_type"]),
            masked_card=str(data["masked_card"]),
            merchant_category=str(data["merchant_category"]),
        )


@dataclass(frozen=True)
class RuleEvidence:
    rule_id: str
    description: str
    weight: int
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FraudAssessment:
    transaction_id: str
    event_timestamp: datetime
    processed_at: datetime
    amount: float
    state: str
    device_type: str
    risk_score: int
    risk_level: RiskLevel
    triggered_rules: list[str]
    rule_evidence: list[dict[str, Any]]
    rules_version: str
    customer_id: str
    masked_card: str
    merchant_category: str

    @property
    def is_suspicious(self) -> bool:
        return self.risk_level in {RiskLevel.MEDIUM, RiskLevel.HIGH}

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["event_timestamp"] = self.event_timestamp.astimezone(UTC).isoformat()
        data["processed_at"] = self.processed_at.astimezone(UTC).isoformat()
        data["risk_level"] = self.risk_level.value
        return data
