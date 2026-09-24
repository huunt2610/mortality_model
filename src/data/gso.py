"""Đọc bảng sống của Tổng cục Thống kê (GSO) đã số hoá thủ công từ các báo cáo tổng điều tra.

Vai trò: dữ liệu kiểm chứng cho nhánh B và dữ liệu khớp cho nhánh C (Lee-Carter kiểu LLT)
- xem docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md, Mục 8.3 và 12.

File số hoá nằm trong `data/external/gso/` (được commit, vì số hoá tay từ PDF nên không tải
lại được). Mỗi thời điểm (1989, 1999, 2009, 2014, 2019, 2024) một file, ghi nguồn trong
`data/external/SOURCES.md`.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DATA_EXTERNAL

GSO_DIR = DATA_EXTERNAL / "gso"
GSO_FILES = {
    2019: "bang_song_tdt2019.csv",
}

_ABRIDGED_COLUMNS = {"sex", "x", "n", "nmx", "nqx"}


def read_gso_abridged(year: int, path: Path | None = None) -> pd.DataFrame:
    """Đọc bảng sống rút gọn GSO (cột sex, x, n, nLx, lx, ndx, nqx, npx, nmx, Tx, ex).

    `x` là tuổi bắt đầu nhóm (nhóm mở ghi dạng "80+"), `n` rỗng ở nhóm mở. Trả về đúng
    cấu trúc gốc để `src.demography.age_groups.gso_age_group_edges` suy ra khuôn nhóm tuổi.
    """
    path = path or GSO_DIR / GSO_FILES[year]
    df = pd.read_csv(path)
    missing = _ABRIDGED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"{path.name} thiếu cột bắt buộc {missing}")
    df["year"] = year
    return df


def read_gso_life_table(path: Path) -> pd.DataFrame:
    """Đọc bảng sống GSO dạng tuổi đơn (cột age, sex, và mx hoặc qx).

    Suy ra `mx = -log(1 - qx)` khi file chỉ có `qx` (giả định lực chết không đổi trong năm).
    """
    df = pd.read_csv(path)
    required = {"age", "sex"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path.name} thiếu cột bắt buộc {missing}")
    if "mx" not in df.columns:
        if "qx" not in df.columns:
            raise ValueError(f"{path.name} cần ít nhất một trong hai cột: mx, qx")
        df["mx"] = -np.log(1 - df["qx"])  # xấp xỉ mx từ qx cho bảng sống rút gọn
    return df
