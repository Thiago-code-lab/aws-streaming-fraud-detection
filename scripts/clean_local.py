from __future__ import annotations

import shutil
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    target = (root / "data" / "local").resolve()
    allowed_parent = (root / "data").resolve()
    if target.exists() and target.parent == allowed_parent:
        shutil.rmtree(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
