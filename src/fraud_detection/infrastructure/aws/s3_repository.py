from __future__ import annotations

import json
import time
from collections.abc import Callable
from typing import Any

from fraud_detection.domain.models import Transaction


class AwsIntegrationError(RuntimeError):
    """Erro emitido quando um adaptador AWS não conclui uma operação controlada."""


class S3Repository:
    def __init__(
        self,
        s3_client: Any,
        raw_bucket: str,
        processed_bucket: str,
        max_retries: int = 3,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.s3_client = s3_client
        self.raw_bucket = raw_bucket
        self.processed_bucket = processed_bucket
        self.max_retries = max_retries
        self.sleep = sleep

    def list_raw_keys(self, prefix: str = "transactions/") -> list[str]:
        try:
            paginator = self.s3_client.get_paginator("list_objects_v2")
            keys: list[str] = []
            for page in paginator.paginate(Bucket=self.raw_bucket, Prefix=prefix):
                keys.extend(item["Key"] for item in page.get("Contents", []) if item["Key"].endswith(".json"))
            return keys
        except Exception as exc:  # boto3 expõe exceções específicas de serviço dinamicamente.
            raise AwsIntegrationError(f"falha ao listar objetos raw no S3: {exc}") from exc

    def put_raw_transaction(self, transaction: Transaction) -> str:
        timestamp = transaction.event_timestamp
        key = (
            "transactions/"
            f"year={timestamp:%Y}/month={timestamp:%m}/day={timestamp:%d}/hour={timestamp:%H}/"
            f"{transaction.transaction_id}.json"
        )
        body = json.dumps(transaction.to_dict(), sort_keys=True).encode("utf-8")
        self._retry(
            lambda: self.s3_client.put_object(
                Bucket=self.raw_bucket,
                Key=key,
                Body=body,
                ContentType="application/json",
            )
        )
        return key

    def _retry(self, operation: Callable[[], Any]) -> Any:
        delay = 0.25
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return operation()
            except Exception as exc:  # boto3 expõe exceções específicas de serviço dinamicamente.
                last_error = exc
                if attempt == self.max_retries:
                    break
                self.sleep(delay)
                delay *= 2
        raise AwsIntegrationError(f"operação AWS falhou após {self.max_retries} tentativas: {last_error}")
