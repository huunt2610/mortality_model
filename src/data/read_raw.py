"""Đọc dữ liệu tử vong thô: UN WPP (bảng sống tuổi đơn, .xlsx) và GSO (CSV đã số hoá).

UN WPP xuất file Excel với vài chục dòng metadata phía trên bảng dữ liệu thật,
và tên cột đầy đủ (vd. "Central death rate m(x,n)") có thể lệch nhẹ giữa các
kỳ revision. Thay vì cố định vị trí dòng/cột, ta dò dòng tiêu đề bằng cách tìm
dòng khớp nhiều nhất các nhãn cột mong đợi, rồi khớp cột theo mẫu regex —
chịu được thay đổi nhỏ về định dạng giữa các lần UN cập nhật.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

ISO3_VIETNAM = "VNM"

_HEADER_HINTS: dict[str, re.Pattern] = {
    "iso3": re.compile(r"iso3", re.I),
    "year": re.compile(r"^year$|reference date|mid-period", re.I),
    "age": re.compile(r"age\s*\(x\)|agegrpstart", re.I),
    "mx": re.compile(r"central death rate", re.I),
    "exposure": re.compile(r"person-years lived", re.I),
}


def _find_header_row(raw: pd.DataFrame, max_scan: int = 30, min_hits: int = 4) -> int:
    """Dòng tiêu đề = dòng đầu tiên khớp được >= min_hits / len(_HEADER_HINTS) nhãn cột."""
    for i in range(min(max_scan, len(raw))):
        cells = [str(c) for c in raw.iloc[i].tolist()]
        hits = sum(any(p.search(c) for c in cells) for p in _HEADER_HINTS.values())
        if hits >= min_hits:
            return i
    raise ValueError(
        "Không tìm thấy dòng tiêu đề trong file UN WPP trong "
        f"{max_scan} dòng đầu — kiểm tra lại định dạng file (sheet, số dòng metadata)."
    )


def _match_column(columns: pd.Index, pattern: re.Pattern) -> str:
    for c in columns:
        if pattern.search(str(c)):
            return c
    raise KeyError(f"Không tìm thấy cột khớp mẫu {pattern.pattern!r} trong {list(columns)}")


def read_wpp_single_age_life_table(path: Path) -> pd.DataFrame:
    """Đọc 1 file bảng sống tuổi đơn UN WPP (1 giới tính), lọc riêng Việt Nam.

    Trả về long-format: cột year, age, mx, exposure.

    `exposure` lấy xấp xỉ từ L(x,n) — person-years lived trong bảng sống —
    vì file life table (F06) của UN không tách deaths/exposure dân số thực
    (nằm ở file Population riêng, ngoài phạm vi ở đây). Do đó
    Dxt = mx * Ext là MỘT GIẢ ĐỊNH cần ghi rõ trong luận văn, không phải số
    ca tử vong thực tế đếm được.
    """
    try:
        raw = pd.read_excel(path, sheet_name="Estimates", header=None)
    except ValueError:
        raw = pd.read_excel(path, sheet_name=0, header=None)

    header_row = _find_header_row(raw)
    df = raw.iloc[header_row + 1:].copy()
    df.columns = raw.iloc[header_row]
    df = df.reset_index(drop=True)

    col_iso3 = _match_column(df.columns, _HEADER_HINTS["iso3"])
    col_year = _match_column(df.columns, _HEADER_HINTS["year"])
    col_age = _match_column(df.columns, _HEADER_HINTS["age"])
    col_mx = _match_column(df.columns, _HEADER_HINTS["mx"])
    col_exposure = _match_column(df.columns, _HEADER_HINTS["exposure"])

    vn = df[df[col_iso3].astype(str).str.upper() == ISO3_VIETNAM].copy()
    if vn.empty:
        raise ValueError(f"Không tìm thấy dữ liệu Việt Nam (ISO3={ISO3_VIETNAM}) trong {path.name}")

    out = pd.DataFrame({
        "year": pd.to_numeric(vn[col_year], errors="coerce"),
        "age": pd.to_numeric(vn[col_age], errors="coerce"),
        "mx": pd.to_numeric(vn[col_mx], errors="coerce"),
        "exposure": pd.to_numeric(vn[col_exposure], errors="coerce"),
    }).dropna()
    out["year"] = out["year"].astype(int)
    out["age"] = out["age"].astype(int)
    return out.sort_values(["year", "age"]).reset_index(drop=True)


def read_gso_life_table(path: Path) -> pd.DataFrame:
    """Đọc bảng sống GSO đã số hoá thủ công từ báo cáo TĐT (chỉ dùng đối chiếu).

    Kỳ vọng CSV tối thiểu có cột `age`, `sex`, và `mx` hoặc `qx`. Dữ liệu này
    KHÔNG dùng để fit mô hình (chuỗi năm quá ngắn/thưa), chỉ để kiểm chứng
    chéo với UN WPP ở notebook EDA.
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
