"""Đọc cấu hình trung tâm từ config/params.yaml và quy ước đường dẫn theo dataset."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_EXTERNAL = ROOT / "data" / "external"
MODELS = ROOT / "models"
RESULTS = ROOT / "results"
FIGURES = ROOT / "reports" / "figures"

DEFAULT_DATASET = "wpp_vnm"


def load_params() -> dict:
    with open(ROOT / "config" / "params.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def processed_dir(dataset: str = DEFAULT_DATASET) -> Path:
    """Thư mục ma trận input `Dxt_{sex}.csv`, `Ext_{sex}.csv`, `mx_{sex}.csv` của một dataset."""
    return DATA_PROCESSED / dataset


def results_dir(dataset: str = DEFAULT_DATASET) -> Path:
    """Thư mục output mô hình do R ghi (params, residuals, forecast, backtest) của một dataset."""
    return RESULTS / dataset
