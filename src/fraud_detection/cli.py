from __future__ import annotations

import argparse
import json
from pathlib import Path

from fraud_detection.config import AppConfig
from fraud_detection.generators.transaction_generator import TransactionGenerator
from fraud_detection.observability.logging import configure_logging
from fraud_detection.processing.pipeline import run_local_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fraud-detection",
        description="Pipeline educacional de detecção de fraudes",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="Executa a demonstração local determinística sem AWS")
    demo.add_argument("--transactions", type=int, default=1_000)
    demo.add_argument("--seed", type=int, default=42)
    demo.add_argument("--output-dir", type=Path, default=None)

    return parser


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        config = AppConfig.from_env()
        if args.output_dir is not None:
            config = AppConfig(
                aws_region=config.aws_region,
                raw_bucket=config.raw_bucket,
                processed_bucket=config.processed_bucket,
                kinesis_stream_name=config.kinesis_stream_name,
                data_dir=args.output_dir.resolve(),
                enable_aws_streaming=config.enable_aws_streaming,
                max_aws_retries=config.max_aws_retries,
                rule_config=config.rule_config,
            )
        transactions = TransactionGenerator(seed=args.seed).generate(args.transactions)
        summary = run_local_demo(config, transactions)
        print(json.dumps(summary.__dict__, indent=2, sort_keys=True))
        return 0
    return 2
