from unittest.mock import Mock

import pytest

from fraud_detection.config import AppConfig
from fraud_detection.generators.transaction_generator import TransactionGenerator
from fraud_detection.infrastructure.aws.s3_repository import AwsIntegrationError, S3Repository


def test_config_reads_environment(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("FRAUD_HIGH_AMOUNT_THRESHOLD", "9000")
    monkeypatch.setenv("FRAUD_RISKY_STATES", "SP,RJ")
    config = AppConfig.from_env()
    assert config.rule_config.high_amount_threshold == 9000
    assert config.rule_config.risky_states == frozenset({"SP", "RJ"})


def test_aws_repository_raises_controlled_error() -> None:
    client = Mock()
    client.put_object.side_effect = RuntimeError("network")
    repository = S3Repository(client, "raw", "processed", max_retries=1, sleep=lambda _: None)
    tx = TransactionGenerator(seed=1).generate(1)[0]
    with pytest.raises(AwsIntegrationError):
        repository.put_raw_transaction(tx)


def test_s3_listing_uses_pagination() -> None:
    paginator = Mock()
    paginator.paginate.return_value = [{"Contents": [{"Key": "transactions/a.json"}, {"Key": "ignore.txt"}]}]
    client = Mock()
    client.get_paginator.return_value = paginator
    repository = S3Repository(client, "raw", "processed")
    assert repository.list_raw_keys() == ["transactions/a.json"]
