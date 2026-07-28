from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def write_partitioned_parquet(rows: list[dict[str, Any]], output_dir: Path) -> list[Path]:
    if not rows:
        return []
    output_dir.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(rows)
    dataframe["event_timestamp"] = pd.to_datetime(dataframe["event_timestamp"], utc=True)
    dataframe["processed_at"] = pd.to_datetime(dataframe["processed_at"], utc=True)
    dataframe["year"] = dataframe["event_timestamp"].dt.year.astype(str)
    dataframe["month"] = dataframe["event_timestamp"].dt.month.map(lambda value: f"{value:02d}")
    dataframe["day"] = dataframe["event_timestamp"].dt.day.map(lambda value: f"{value:02d}")
    dataframe["hour"] = dataframe["event_timestamp"].dt.hour.map(lambda value: f"{value:02d}")
    dataframe.to_parquet(
        output_dir,
        engine="pyarrow",
        index=False,
        partition_cols=["year", "month", "day", "hour"],
    )
    return sorted(output_dir.rglob("*.parquet"))
