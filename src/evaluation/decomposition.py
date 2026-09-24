"""Phân rã sai số dự báo nhánh B - docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md, Mục 12.2.

    (F_t - G_t)  =  (F_t - W_t)  +  (W_t - G_t)
     sai số tổng    sai số mô hình   độ lệch nguồn

F_t: dự báo của mô hình khớp trên WPP; W_t: ước lượng của chính WPP năm t; G_t: bảng sống
chính thức (GSO) năm t. Ba đại lượng phải cùng thang (nqx theo nhóm tuổi GSO, e0, e60...) -
gộp nhóm bằng `src.demography.age_groups` trước khi gọi.
"""
from __future__ import annotations

import pandas as pd


def decompose_error(forecast: pd.Series, wpp: pd.Series, gso: pd.Series) -> pd.DataFrame:
    """Trả về bảng cột total, model, source (cùng index với đầu vào), total = model + source."""
    return pd.DataFrame({
        "total": forecast - gso,
        "model": forecast - wpp,
        "source": wpp - gso,
    })
