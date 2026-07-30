"""Phân rã tuổi/năm/thế hệ đơn giản từ mặt log m(x,t) — dùng cho chẩn đoán EDA
(có còn vệt chéo sau khi trừ hiệu ứng tuổi + năm không), KHÔNG thay thế việc fit
mô hình Lee-Carter/Renshaw-Haberman chính thức (xem notebook 04, 05).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def age_period_residual(mx: pd.DataFrame) -> pd.DataFrame:
    """log m(x,t) sau khi trừ hiệu ứng tuổi (trung bình theo tuổi) và hiệu ứng
    năm (trung bình theo năm, sau khi đã trừ hiệu ứng tuổi). Phần dư còn vệt
    chéo (hằng theo cohort c = t-x) là dấu hiệu hiệu ứng thế hệ chưa được hiệu
    ứng tuổi/năm đơn thuần giải thích.
    """
    logmx = np.log(mx)
    age_effect = logmx.mean(axis=1)
    centered = logmx.sub(age_effect, axis=0)
    period_effect = centered.mean(axis=0)
    return centered.sub(period_effect, axis=1)


def cohort_mean_residual(resid: pd.DataFrame, min_obs: int = 15) -> pd.Series:
    """Trung bình residual theo thế hệ (cohort = năm - tuổi), chỉ giữ cohort có
    đủ số quan sát (mặc định >=15 ô tuổi-năm) để tránh nhiễu từ cohort ở rìa dữ
    liệu (chỉ quan sát được vài tuổi trong giai đoạn 1955-2023).
    """
    long = resid.stack()
    long.index = long.index.set_names(["age", "year"])
    cohort = long.index.get_level_values("year") - long.index.get_level_values("age")
    grouped = long.groupby(cohort)
    counts = grouped.size()
    means = grouped.mean()
    return means[counts >= min_obs].rename("mean_residual")
