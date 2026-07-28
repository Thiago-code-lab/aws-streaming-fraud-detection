from __future__ import annotations

import base64
import json
from collections.abc import Iterable
from typing import Any

from fraud_detection.domain.models import Transaction
from fraud_detection.processing.validators import validate_transaction_payload


def parse_kinesis_records(event: dict[str, Any]) -> Iterable[Transaction]:
    for record in event.get("Records", []):
        payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        yield validate_transaction_payload(json.loads(payload))
