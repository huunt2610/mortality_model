"""Đọc cấu hình trung tâm từ config/params.yaml."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"


def load_params() -> dict:
    with open(ROOT / "config" / "params.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)
