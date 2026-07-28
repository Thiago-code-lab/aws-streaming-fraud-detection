from datetime import UTC, datetime

import pytest

from fraud_detection.domain.models import Transaction
from fraud_detection.processing.validators import validate_transaction_payload


def transaction_payload() -> dict[str, object]:
    return {
        "transaction_id": "tx-1",
        "event_timestamp": "2026-01-01T00:00:00+00:00",
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


def test_transaction_schema_accepts_valid_payload() -> None:
    transaction = validate_transaction_payload(transaction_payload())
    assert transaction.event_timestamp == datetime(2026, 1, 1, tzinfo=UTC)


def test_transaction_schema_rejects_missing_field() -> None:
    payload = transaction_payload()
    del payload["amount"]
    with pytest.raises(ValueError, match="campos obrigatórios"):
        validate_transaction_payload(payload)


def test_transaction_rejects_unmasked_card() -> None:
    payload = transaction_payload() | {"masked_card": "4111111111111111"}
    with pytest.raises(ValueError, match="masked_card"):
        Transaction.from_dict(payload)
