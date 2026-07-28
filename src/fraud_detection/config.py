from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{name} deve ser um número") from exc


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} deve ser um inteiro") from exc


@dataclass(frozen=True)
class FraudRuleConfig:
    high_amount_threshold: float = 4_500.0
    profile_amount_multiplier: float = 4.0
    risky_states: frozenset[str] = field(default_factory=lambda: frozenset({"AC", "RR", "RO"}))
    burst_window_seconds: int = 120
    burst_min_transactions: int = 3
    unusual_hours: frozenset[int] = field(default_factory=lambda: frozenset({0, 1, 2, 3, 4, 5}))
    medium_risk_threshold: int = 35
    high_risk_threshold: int = 70
    rules_version: str = "2026-07"


@dataclass(frozen=True)
class AppConfig:
    aws_region: str
    raw_bucket: str | None
    processed_bucket: str | None
    kinesis_stream_name: str | None
    data_dir: Path
    enable_aws_streaming: bool
    max_aws_retries: int
    rule_config: FraudRuleConfig

    @classmethod
    def from_env(cls) -> "AppConfig":
        risky_states = os.getenv("FRAUD_RISKY_STATES", "AC,RR,RO")
        unusual_hours = os.getenv("FRAUD_UNUSUAL_HOURS", "0,1,2,3,4,5")
        rule_config = FraudRuleConfig(
            high_amount_threshold=_env_float("FRAUD_HIGH_AMOUNT_THRESHOLD", 4_500.0),
            profile_amount_multiplier=_env_float("FRAUD_PROFILE_AMOUNT_MULTIPLIER", 4.0),
            risky_states=frozenset(s.strip().upper() for s in risky_states.split(",") if s.strip()),
            burst_window_seconds=_env_int("FRAUD_BURST_WINDOW_SECONDS", 120),
            burst_min_transactions=_env_int("FRAUD_BURST_MIN_TRANSACTIONS", 3),
            unusual_hours=frozenset(int(h.strip()) for h in unusual_hours.split(",") if h.strip()),
            medium_risk_threshold=_env_int("FRAUD_MEDIUM_RISK_THRESHOLD", 35),
            high_risk_threshold=_env_int("FRAUD_HIGH_RISK_THRESHOLD", 70),
            rules_version=os.getenv("FRAUD_RULES_VERSION", "2026-07"),
        )
        return cls(
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
            raw_bucket=os.getenv("FRAUD_RAW_BUCKET"),
            processed_bucket=os.getenv("FRAUD_PROCESSED_BUCKET"),
            kinesis_stream_name=os.getenv("FRAUD_KINESIS_STREAM_NAME"),
            data_dir=Path(os.getenv("FRAUD_DATA_DIR", "data/local")).resolve(),
            enable_aws_streaming=_env_bool("FRAUD_ENABLE_AWS_STREAMING", False),
            max_aws_retries=_env_int("FRAUD_MAX_AWS_RETRIES", 3),
            rule_config=rule_config,
        )
