"""Đọc dữ liệu Human Mortality Database (HMD) - nhánh A, phòng thí nghiệm so sánh mô hình.

Quần thể tham chiếu: Nhật Bản (JPN), Hàn Quốc (KOR), Đài Loan (TWN) - xem
docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md, Mục 12.1. Việt Nam KHÔNG có trong HMD.

Dữ liệu HMD cần đăng ký tài khoản tại https://www.mortality.org rồi tải thủ công
`Deaths_1x1.txt` và `Exposures_1x1.txt` của từng nước vào `data/raw/hmd/<COUNTRY>/`.
Khác WPP, HMD có số ca tử vong và exposure quan sát thật, nên `Dxt` không phải đại lượng
suy ra.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import DATA_RAW

HMD_DIR = DATA_RAW / "hmd"
_SEX_COLUMNS = {"female": "Female", "male": "Male", "total": "Total"}


def _read_hmd_1x1(path: Path) -> pd.DataFrame:
    """Đọc 1 file HMD dạng 1x1 (2 dòng tiêu đề, phân cách bằng khoảng trắng, tuổi "110+")."""
    df = pd.read_csv(path, sep=r"\s+", skiprows=2, na_values=".")
    df["Age"] = df["Age"].astype(str).str.rstrip("+").astype(int)
    return df


def read_hmd_country(country: str, sex: str, root: Path = HMD_DIR) -> pd.DataFrame:
    """Trả về long-format (year, age, deaths, exposure, mx) cho một nước, một giới tính."""
    col = _SEX_COLUMNS[sex]
    deaths = _read_hmd_1x1(root / country / "Deaths_1x1.txt")
    exposures = _read_hmd_1x1(root / country / "Exposures_1x1.txt")
    df = deaths[["Year", "Age", col]].merge(
        exposures[["Year", "Age", col]], on=["Year", "Age"], suffixes=("_D", "_E")
    )
    out = pd.DataFrame({
        "year": df["Year"].astype(int),
        "age": df["Age"],
        "deaths": df[f"{col}_D"],
        "exposure": df[f"{col}_E"],
    }).dropna()
    out["mx"] = out["deaths"] / out["exposure"]
    return out.sort_values(["year", "age"]).reset_index(drop=True)
