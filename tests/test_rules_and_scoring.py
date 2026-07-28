from datetime import UTC, datetime, timedelta

from fraud_detection.config import FraudRuleConfig
from fraud_detection.domain.models import RiskLevel, Transaction
from fraud_detection.domain.rules import build_default_rules
from fraud_detection.domain.scoring import FraudScorer, classify_risk


def make_tx(**overrides: object) -> Transaction:
    data = {
        "transaction_id": "tx-1",
        "event_timestamp": datetime(2026, 1, 1, 2, 0, tzinfo=UTC),
        "amount": 100.0,
        "state": "SP",
        "device_type": "mobile",
        "customer_id": "cust_1",
        "customer_profile_amount": 100.0,
        "customer_home_state": "SP",
        "customer_usual_device_type": "mobile",
        "masked_card": "card_****_abc123",
        "merchant_category": "grocery",
    }
    data.update(overrides)
    return Transaction(**data)  # type: ignore[arg-type]


def test_risk_classification_thresholds() -> None:
    config = FraudRuleConfig()
    assert classify_risk(10, config) is RiskLevel.LOW
    assert classify_risk(config.medium_risk_threshold, config) is RiskLevel.MEDIUM
    assert classify_risk(config.high_risk_threshold, config) is RiskLevel.HIGH


def test_legitimate_transaction_remains_low_risk() -> None:
    config = FraudRuleConfig(unusual_hours=frozenset())
    scorer = FraudScorer(build_default_rules(config), config)
    assessment = scorer.assess(make_tx(event_timestamp=datetime(2026, 1, 1, 12, tzinfo=UTC)), [])
    assert assessment.risk_level is RiskLevel.LOW
    assert assessment.triggered_rules == []


def test_suspicious_transaction_triggers_multiple_rules() -> None:
    config = FraudRuleConfig()
    scorer = FraudScorer(build_default_rules(config), config)
    tx = make_tx(amount=7_000.0, state="AC", device_type="desktop")
    assessment = scorer.assess(tx, [])
    assert assessment.risk_level is RiskLevel.HIGH
    assert {"high_amount", "profile_amount_mismatch", "risky_location", "device_change"}.issubset(
        set(assessment.triggered_rules)
    )


def test_burst_transaction_rule_uses_history() -> None:
    config = FraudRuleConfig(unusual_hours=frozenset())
    scorer = FraudScorer(build_default_rules(config), config)
    base = make_tx(event_timestamp=datetime(2026, 1, 1, 12, tzinfo=UTC))
    history = [
        make_tx(transaction_id="tx-0", event_timestamp=base.event_timestamp - timedelta(seconds=20)),
        make_tx(transaction_id="tx-00", event_timestamp=base.event_timestamp - timedelta(seconds=40)),
    ]
    assessment = scorer.assess(base, history)
    assert "burst_transactions" in assessment.triggered_rules
