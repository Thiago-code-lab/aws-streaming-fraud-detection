import json

import pandas as pd

from fraud_detection.config import AppConfig
from fraud_detection.generators.transaction_generator import TransactionGenerator
from fraud_detection.processing.pipeline import run_local_demo


def test_local_pipeline_writes_json_and_parquet(tmp_path) -> None:  # type: ignore[no-untyped-def]
    config = AppConfig.from_env()
    config = AppConfig(
        aws_region=config.aws_region,
        raw_bucket=None,
        processed_bucket=None,
        kinesis_stream_name=None,
        data_dir=tmp_path,
        enable_aws_streaming=False,
        max_aws_retries=1,
        rule_config=config.rule_config,
    )
    transactions = TransactionGenerator(seed=42).generate(25)
    summary = run_local_demo(config, transactions)
    parquet_files = sorted((tmp_path / "processed" / "parquet").rglob("*.parquet"))

    assert summary.transactions_analyzed == 25
    assert summary.output_json_files >= 50
    assert parquet_files
    dataframe = pd.read_parquet(parquet_files[0])
    assert "risk_score" in dataframe.columns
    assert "year=" in str(parquet_files[0])


def test_pipeline_is_idempotent_by_transaction_id(tmp_path) -> None:  # type: ignore[no-untyped-def]
    config = AppConfig.from_env()
    config = AppConfig(
        aws_region=config.aws_region,
        raw_bucket=None,
        processed_bucket=None,
        kinesis_stream_name=None,
        data_dir=tmp_path,
        enable_aws_streaming=False,
        max_aws_retries=1,
        rule_config=config.rule_config,
    )
    tx = TransactionGenerator(seed=42).generate(1)[0]
    summary = run_local_demo(config, [tx, tx])
    assert summary.transactions_analyzed == 1


def test_json_serialization_contains_safe_fields(tmp_path) -> None:  # type: ignore[no-untyped-def]
    config = AppConfig.from_env()
    config = AppConfig(
        aws_region=config.aws_region,
        raw_bucket=None,
        processed_bucket=None,
        kinesis_stream_name=None,
        data_dir=tmp_path,
        enable_aws_streaming=False,
        max_aws_retries=1,
        rule_config=config.rule_config,
    )
    run_local_demo(config, TransactionGenerator(seed=42).generate(1))
    raw_file = next((tmp_path / "raw").rglob("*.json"))
    payload = json.loads(raw_file.read_text(encoding="utf-8"))
    assert payload["masked_card"].startswith("card_****_")
    assert "cliente" not in payload
