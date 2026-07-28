from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fraud_detection.domain.models import Transaction


class LocalFileRepository:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.raw_dir = self.base_dir / "raw" / "transactions"
        self.processed_json_dir = self.base_dir / "processed" / "json"
        self.processed_parquet_dir = self.base_dir / "processed" / "parquet"

    def write_raw_transactions(self, transactions: list[Transaction]) -> list[Path]:
        written: list[Path] = []
        for transaction in transactions:
            partition = _partition_path(self.raw_dir, transaction.event_timestamp)
            partition.mkdir(parents=True, exist_ok=True)
            path = partition / f"{transaction.transaction_id}.json"
            if path.exists():
                continue
            path.write_text(json.dumps(transaction.to_dict(), sort_keys=True) + "\n", encoding="utf-8")
            written.append(path)
        return written

    def write_processed_assessments(self, rows: list[dict[str, Any]]) -> list[Path]:
        written: list[Path] = []
        for row in rows:
            timestamp = str(row["event_timestamp"])
            partition = self.processed_json_dir / f"date={timestamp[:10]}"
            partition.mkdir(parents=True, exist_ok=True)
            path = partition / f"{row['transaction_id']}.json"
            if path.exists():
                continue
            path.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
            written.append(path)
        return written

    def read_raw_transactions(self) -> list[Transaction]:
        transactions = []
        for path in sorted(self.raw_dir.rglob("*.json")):
            transactions.append(Transaction.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        return transactions


def _partition_path(base_dir: Path, timestamp: datetime) -> Path:
    iso_timestamp = timestamp.isoformat()
    return (
        base_dir
        / f"year={iso_timestamp[:4]}"
        / f"month={iso_timestamp[5:7]}"
        / f"day={iso_timestamp[8:10]}"
        / f"hour={iso_timestamp[11:13]}"
    )
