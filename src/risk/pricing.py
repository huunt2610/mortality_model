"""Định giá hợp đồng theo bảng tử vong đoàn hệ - docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md,
Mục 14.

    Niên kim trọn đời trả đầu kỳ:  ä_x      = sum_{k>=0} v^k * kp_x
    Bảo hiểm tử kỳ n năm:          A^1_x:n  = sum_{k=0}^{n-1} v^(k+1) * kp_x * q_{x+k}

Định giá niên kim đúng cách phải dùng bảng ĐOÀN HỆ (đi theo đường chéo tuổi-năm của ma trận
dự báo), không phải bảng thời kỳ của một năm lịch - `cohort_qx` lấy đường chéo đó.
Áp dụng cho từng kịch bản mô phỏng thì ä_x, A^1 trở thành biến ngẫu nhiên, phân phối của
chúng đo bằng `src.risk.measures`.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def cohort_qx(qxt: pd.DataFrame, age: int, year: int) -> np.ndarray:
    """q(x+k, t+k), k = 0, 1, ... của người tuổi `age` tại năm `year`, đến khi hết tuổi hoặc
    hết năm trong ma trận `qxt` (index = tuổi, cột = năm)."""
    ages = [a for a in qxt.index if a >= age]
    out = []
    for k, a in enumerate(ages):
        if year + k not in qxt.columns:
            break
        out.append(qxt.loc[a, year + k])
    return np.asarray(out, dtype=float)


def survival_curve(qx: np.ndarray) -> np.ndarray:
    """kp_x, k = 0..len(qx): 0p_x = 1, (k+1)p_x = kp_x * (1 - q_{x+k})."""
    return np.concatenate([[1.0], np.cumprod(1 - np.asarray(qx, dtype=float))])


def annuity_due(qx: np.ndarray, i: float) -> float:
    """ä_x = sum_k v^k kp_x trên đường q(x+k) cho trước (cắt tại độ dài `qx`)."""
    kpx = survival_curve(qx)[:-1]
    v = 1 / (1 + i)
    return float(np.sum(v ** np.arange(len(kpx)) * kpx))


def term_insurance(qx: np.ndarray, i: float, n: int) -> float:
    """A^1_x:n = sum_{k<n} v^(k+1) kp_x q_{x+k}."""
    qx = np.asarray(qx, dtype=float)[:n]
    if len(qx) < n:
        raise ValueError(f"Cần ít nhất {n} giá trị q(x+k), chỉ có {len(qx)}")
    kpx = survival_curve(qx)[:-1]
    v = 1 / (1 + i)
    return float(np.sum(v ** (np.arange(n) + 1) * kpx * qx))
