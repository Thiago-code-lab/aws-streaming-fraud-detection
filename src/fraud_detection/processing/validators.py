from __future__ import annotations

from fraud_detection.domain.models import Transaction


REQUIRED_TRANSACTION_FIELDS = {
    "transaction_id",
    "event_timestamp",
    "amount",
    "state",
    "device_type",
    "customer_id",
    "customer_profile_amount",
    "customer_home_state",
    "customer_usual_device_type",
    "masked_card",
    "merchant_category",
}


def validate_transaction_payload(payload: dict[str, object]) -> Transaction:
    missing = REQUIRED_TRANSACTION_FIELDS.difference(payload)
    if missing:
        raise ValueError(f"payload da transação está sem campos obrigatórios: {sorted(missing)}")
    return Transaction.from_dict(payload)
