"""Pipeline dữ liệu: raw -> ma trận Dxt, Ext, mx trong data/processed/<dataset>/.

Chạy:  python -m src.data.make_dataset                 # dataset mặc định (wpp_vnm)
       python -m src.data.make_dataset --dataset hmd_jpn

Danh sách dataset khai báo ở `datasets:` trong config/params.yaml.

- WPP: đặt 3 file "Single age life table estimates" (Both sexes / Male / Female) vào
  data/raw/wpp/, tên file đúng như trong data/external/SOURCES.md. Tải tại
  https://population.un.org/wpp/ (mục Life Tables > Single age).
- HMD: đặt Deaths_1x1.txt, Exposures_1x1.txt vào data/raw/hmd/<COUNTRY>/ (xem src/data/hmd.py).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import DATA_RAW, DEFAULT_DATASET, load_params, processed_dir
from src.data.hmd import read_hmd_country
from src.data.validate import validate_matrices
from src.data.wpp import read_wpp_single_age_life_table

WPP_DIR = DATA_RAW / "wpp"
WPP_FILES = {
    "total": "WPP2024_MORT_F06_1_SINGLE_AGE_LIFE_TABLE_ESTIMATES_BOTH_SEXES.xlsx",
    "male": "WPP2024_MORT_F06_2_SINGLE_AGE_LIFE_TABLE_ESTIMATES_MALE.xlsx",
    "female": "WPP2024_MORT_F06_3_SINGLE_AGE_LIFE_TABLE_ESTIMATES_FEMALE.xlsx",
}

# HMD ghi nhận tới tuổi 110+, exposure ở tuổi rất cao có thể bằng 0 - cắt ở 100 cho ma trận
# input (mô hình chỉ fit tới `ages.*.max` = 90).
HMD_MAX_AGE = 100


def build_matrices(df: pd.DataFrame, y0: int, y1: int
                   ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Từ bảng dài (year, age, mx, exposure[, deaths]) dựng ma trận tuổi x năm.

    Có cột `deaths` (HMD) thì dùng số ca tử vong quan sát; không có (WPP) thì
    Dxt = mx * Ext là một GIẢ ĐỊNH (xem giả định về exposure trong src/data/wpp.py).
    """
    sub = df[df["year"].between(y0, y1)]

    def _pivot(col: str) -> pd.DataFrame:
        m = sub.pivot(index="age", columns="year", values=col).sort_index()
        return m[sorted(m.columns)]

    Ext = _pivot("exposure")
    mx = _pivot("mx")
    Dxt = _pivot("deaths") if "deaths" in sub.columns else (mx * Ext).round(2)
    return Dxt, Ext, mx


def _read_long(ds: dict, sex: str) -> pd.DataFrame:
    """Đọc dữ liệu dạng dài của một giới tính theo `source` của dataset."""
    if ds["source"] == "wpp":
        path: Path = WPP_DIR / WPP_FILES[sex]
        if not path.exists():
            raise FileNotFoundError(
                f"Thiếu {path.name} trong data/raw/wpp/. Tải tại https://population.un.org/wpp/ "
                "(Life Tables > Single age life table estimates) rồi đặt vào data/raw/wpp/ "
                "(xem data/external/SOURCES.md)."
            )
        return read_wpp_single_age_life_table(path, iso3=ds["iso3"])
    if ds["source"] == "hmd":
        df = read_hmd_country(ds["country"], sex)
        return df[df["age"] <= HMD_MAX_AGE]
    raise ValueError(
        f"source={ds['source']!r} không dựng được ma trận tuổi đơn x năm "
        "(bảng sống GSO rút gọn, thưa - đọc trực tiếp bằng src.data.gso)"
    )


def main(dataset: str = DEFAULT_DATASET) -> None:
    p = load_params()
    ds = p["datasets"][dataset]
    y0, y1 = p["data"]["years"]["start"], p["data"]["years"]["end"]
    out_dir = processed_dir(dataset)
    out_dir.mkdir(parents=True, exist_ok=True)

    for sex in p["data"]["sexes"]:
        if sex not in WPP_FILES:
            raise KeyError(f"Không có dữ liệu tương ứng cho sex={sex!r}")
        df = _read_long(ds, sex)
        Dxt, Ext, mx = build_matrices(df, y0, y1)
        validate_matrices(Dxt, Ext, mx)

        Dxt.to_csv(out_dir / f"Dxt_{sex}.csv")
        Ext.to_csv(out_dir / f"Ext_{sex}.csv")
        mx.to_csv(out_dir / f"mx_{sex}.csv")
        print(f"[ok] {dataset}/{sex}: {Dxt.shape[0]} tuổi x {Dxt.shape[1]} năm "
              f"-> data/processed/{dataset}/*_{sex}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    main(parser.parse_args().dataset)
