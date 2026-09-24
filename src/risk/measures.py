"""Thước đo rủi ro trên phân phối giá trị hiện tại (cách tiếp cận run-off) - Mục 14.

VaR 99,5% là mức Solvency II dùng cho vốn yêu cầu; "vốn rủi ro tuổi thọ" = VaR - kỳ vọng.
Với niên kim, tổn thất lớn ứng với giá trị hiện tại LỚN (sống lâu hơn dự kiến), nên các hàm
dưới đây lấy đuôi phải của phân phối.
"""
from __future__ import annotations

import numpy as np


def value_at_risk(values: np.ndarray, level: float = 0.995) -> float:
    return float(np.quantile(np.asarray(values, dtype=float), level))


def expected_shortfall(values: np.ndarray, level: float = 0.995) -> float:
    """Trung bình các giá trị >= VaR ở mức `level`."""
    v = np.asarray(values, dtype=float)
    return float(v[v >= value_at_risk(v, level)].mean())


def risk_capital(values: np.ndarray, level: float = 0.995) -> float:
    """Vốn rủi ro = VaR(level) - E[giá trị hiện tại]."""
    v = np.asarray(values, dtype=float)
    return value_at_risk(v, level) - float(v.mean())
