"""Dựng bảng sống (life table) từ m(x,t) để tính kỳ vọng sống e(x,t).

Giả định lực chết không đổi trong mỗi khoảng tuổi (constant force of
mortality), cùng cách quy đổi q(x) <-> m(x) đã dùng khi đọc bảng sống GSO
(`read_gso_life_table`): q(x) = 1 - exp(-m(x)). Tuổi mở (age cuối) giả định
lực chết không đổi sau tuổi đó nên L(x) = l(x) / m(x).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def build_life_table(mx: pd.Series, radix: int = 100_000) -> pd.DataFrame:
    """Dựng bảng sống 1 năm từ vector m(x) (index = tuổi, tăng dần liên tục).

    Trả về DataFrame cột qx, lx, dx, Lx, Tx, ex, cùng index tuổi với `mx`.
    """
    mx = mx.sort_index()
    ages = mx.index.to_numpy()

    qx = 1 - np.exp(-mx.to_numpy())
    qx[-1] = 1.0

    lx = np.empty(len(ages))
    lx[0] = radix
    for i in range(1, len(ages)):
        lx[i] = lx[i - 1] * (1 - qx[i - 1])

    dx = lx * qx

    Lx = np.empty(len(ages))
    Lx[:-1] = (lx[:-1] + lx[1:]) / 2
    Lx[-1] = lx[-1] / mx.to_numpy()[-1] if mx.to_numpy()[-1] > 0 else lx[-1]

    Tx = np.cumsum(Lx[::-1])[::-1]
    ex = Tx / lx

    return pd.DataFrame(
        {"qx": qx, "lx": lx, "dx": dx, "Lx": Lx, "Tx": Tx, "ex": ex}, index=ages
    )


def life_expectancy_series(mx: pd.DataFrame, age: int, radix: int = 100_000) -> pd.Series:
    """Kỳ vọng sống ở tuổi `age` theo từng năm, từ ma trận mx (index=tuổi, cột=năm).

    Trả về Series index = năm.
    """
    return pd.Series(
        {year: build_life_table(mx[year], radix=radix).loc[age, "ex"] for year in mx.columns},
        name=f"e{age}",
    )
