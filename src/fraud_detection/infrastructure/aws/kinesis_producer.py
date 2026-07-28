from __future__ import annotations

import json
from typing import Any

from fraud_detection.domain.models import Transaction
from fraud_detection.infrastructure.aws.s3_repository import AwsIntegrationError


class KinesisProducer:
    def __init__(self, kinesis_client: Any, stream_name: str) -> None:
        self.kinesis_client = kinesis_client
        self.stream_name = stream_name

    def publish(self, transaction: Transaction) -> str:
        try:
            response = self.kinesis_client.put_record(
                StreamName=self.stream_name,
                PartitionKey=transaction.customer_id,
                Data=json.dumps(transaction.to_dict(), sort_keys=True).encode("utf-8"),
            )
        except Exception as exc:
            raise AwsIntegrationError(f"falha ao publicar transação no Kinesis: {exc}") from exc
        return str(response.get("SequenceNumber", ""))
