"""Pipeline dữ liệu: raw (UN WPP) -> ma trận Dxt, Ext trong data/processed.

Chạy:  python -m src.data.make_dataset

Cần đặt 3 file UN WPP "Single age life table estimates" (Both sexes / Male /
Female) vào data/raw/, tên file đúng như trong data/external/SOURCES.md.
Tải tại https://population.un.org/wpp/ (mục Life Tables > Single age).
"""
from pathlib import Path

import pandas as pd

from src.config import DATA_RAW, DATA_PROCESSED, load_params
from src.data.read_raw import read_wpp_single_age_life_table
from src.data.validate import validate_matrices

WPP_FILES = {
    "total": "WPP2024_MORT_F06_1_SINGLE_AGE_LIFE_TABLE_ESTIMATES_BOTH_SEXES.xlsx",
    "male": "WPP2024_MORT_F06_2_SINGLE_AGE_LIFE_TABLE_ESTIMATES_MALE.xlsx",
    "female": "WPP2024_MORT_F06_3_SINGLE_AGE_LIFE_TABLE_ESTIMATES_FEMALE.xlsx",
}


def build_matrices(df: pd.DataFrame, y0: int, y1: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Từ bảng dài (year, age, mx, exposure) dựng ma trận tuổi x năm.

    Dxt = mx * Ext (xem giả định về exposure trong src/data/read_raw.py).
    """
    sub = df[df["year"].between(y0, y1)]
    Ext = sub.pivot(index="age", columns="year", values="exposure").sort_index()
    mx = sub.pivot(index="age", columns="year", values="mx").sort_index()
    Ext = Ext[sorted(Ext.columns)]
    mx = mx[sorted(mx.columns)]
    Dxt = (mx * Ext).round(2)
    return Dxt, Ext


def main() -> None:
    p = load_params()
    y0, y1 = p["data"]["years"]["start"], p["data"]["years"]["end"]

    for sex in p["data"]["sexes"]:
        if sex not in WPP_FILES:
            raise KeyError(f"Không có file UN WPP tương ứng cho sex={sex!r}")
        path: Path = DATA_RAW / WPP_FILES[sex]
        if not path.exists():
            raise FileNotFoundError(
                f"Thiếu {path.name} trong data/raw/. Tải tại https://population.un.org/wpp/ "
                "(Life Tables > Single age life table estimates) rồi đặt vào data/raw/ "
                "(xem data/external/SOURCES.md)."
            )
        df = read_wpp_single_age_life_table(path)
        Dxt, Ext = build_matrices(df, y0, y1)
        validate_matrices(Dxt, Ext)

        Dxt.to_csv(DATA_PROCESSED / f"Dxt_{sex}.csv")
        Ext.to_csv(DATA_PROCESSED / f"Ext_{sex}.csv")
        print(f"[ok] {sex}: {Dxt.shape[0]} tuổi x {Dxt.shape[1]} năm -> data/processed/*_{sex}.csv")


if __name__ == "__main__":
    main()
