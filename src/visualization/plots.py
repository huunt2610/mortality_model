"""Hình chuẩn cho luận văn. Mỗi hàm lưu 1 hình vào reports/figures (300 dpi)."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.config import FIGURES


def _save(fig, name: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{name}.pdf", dpi=300, bbox_inches="tight")


def plot_log_mx_by_age(mx: pd.DataFrame, years: list[int], name: str = "log_mx_by_age"):
    """log m_x theo tuổi, mỗi đường một năm."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for y in years:
        ax.plot(mx.index, np.log(mx[y]), label=str(y))
    ax.set_xlabel("Tuổi x"); ax.set_ylabel("log m(x,t)"); ax.legend(title="Năm")
    _save(fig, name)


def plot_lexis_heatmap(mx: pd.DataFrame, name: str = "lexis_heatmap"):
    """Heatmap log m theo (năm, tuổi) — đường chéo lộ rõ hiệu ứng thế hệ."""
    fig, ax = plt.subplots(figsize=(9, 5))
    im = ax.pcolormesh(mx.columns, mx.index, np.log(mx.values), cmap="viridis")
    fig.colorbar(im, ax=ax, label="log m(x,t)")
    ax.set_xlabel("Năm t"); ax.set_ylabel("Tuổi x")
    _save(fig, name)


def plot_mx_sex_comparison(mx_male: pd.DataFrame, mx_female: pd.DataFrame, years: list[int],
                            name: str = "mx_sex_comparison"):
    """So sánh log m(x,t) theo tuổi giữa nam và nữ ở nhiều năm mốc - mỗi năm 1 panel."""
    fig, axes = plt.subplots(1, len(years), figsize=(4 * len(years), 5), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, year in zip(axes, years):
        ax.plot(mx_male.index, np.log(mx_male[year]), label="Nam")
        ax.plot(mx_female.index, np.log(mx_female[year]), label="Nữ")
        ax.set_xlabel("Tuổi x"); ax.set_title(str(year))
    axes[0].set_ylabel("log m(x,t)")
    axes[0].legend(title="Giới tính")
    _save(fig, name)


def plot_mx_ratio_by_age(mx_male: pd.DataFrame, mx_female: pd.DataFrame, years: list[int],
                          name: str = "mx_ratio_by_age"):
    """Tỷ số m(x,t) Nam/Nữ theo tuổi ở nhiều năm mốc - >1 nghĩa là nam tử vong cao hơn."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for year in years:
        ratio = mx_male[year] / mx_female[year]
        ax.plot(ratio.index, ratio.values, label=str(year))
    ax.axhline(1.0, color="grey", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Tuổi x"); ax.set_ylabel("Tỷ số m(x,t) Nam/Nữ"); ax.legend(title="Năm")
    _save(fig, name)


def plot_mortality_improvement_by_age(mx: pd.DataFrame, y0: int, y1: int,
                                       name: str = "mortality_improvement_by_age"):
    """Tốc độ cải thiện tử vong trung bình năm (%) theo tuổi, giữa năm y0 và y1."""
    improvement = (1 - (mx[y1] / mx[y0]) ** (1 / (y1 - y0))) * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(improvement.index, improvement.values)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set_xlabel("Tuổi x")
    ax.set_ylabel(f"Cải thiện tử vong trung bình năm {y0}-{y1} (%)")
    _save(fig, name)


def plot_life_expectancy_trend(series: dict[str, pd.Series], ylabel: str = "Kỳ vọng sống (năm)",
                                name: str = "life_expectancy_trend"):
    """Xu hướng kỳ vọng sống theo thời gian - mỗi entry của `series` (vd. theo giới tính) một đường."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, s in series.items():
        ax.plot(s.index, s.values, label=label)
    ax.set_xlabel("Năm t"); ax.set_ylabel(ylabel); ax.legend()
    _save(fig, name)


def plot_mx_country_comparison(mx_by_country: dict[str, pd.DataFrame], year: int,
                                name: str = "mx_country_comparison"):
    """So sánh log m(x,t) theo tuổi giữa các nước ở một năm cho trước."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for country, mx in mx_by_country.items():
        ax.plot(mx.index, np.log(mx[year]), label=country)
    ax.set_xlabel("Tuổi x"); ax.set_ylabel(f"log m(x,{year})"); ax.legend(title="Quốc gia")
    _save(fig, name)


def plot_smoothing_comparison(mx_raw: pd.DataFrame, mx_smooth: pd.DataFrame, years: list[int],
                               name: str = "smoothing_comparison"):
    """So sánh log m(x,t) trước/sau làm trơn theo tuổi, nhiều năm mốc - mỗi năm 1 panel."""
    fig, axes = plt.subplots(1, len(years), figsize=(4 * len(years), 5), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, year in zip(axes, years):
        ax.plot(mx_raw.index, np.log(mx_raw[year]), label="Gốc", color="tab:blue",
                linewidth=2.5, alpha=0.5)
        ax.plot(mx_smooth.index, np.log(mx_smooth[year]), label="Đã làm trơn", color="tab:orange",
                linewidth=1.2, linestyle="--")
        ax.set_xlabel("Tuổi x"); ax.set_title(str(year))
    axes[0].set_ylabel("log m(x,t)")
    axes[0].legend()
    _save(fig, name)


def plot_named_series_by_age(series: dict[str, pd.Series], ylabel: str, name: str,
                              ref_line: float | None = None):
    """Vẽ nhiều chuỗi (theo tuổi) được đặt tên tuỳ ý trên cùng 1 trục - dùng chung cho
    so sánh nguồn dữ liệu (GSO/WPP), tỷ số theo tuổi, v.v."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, s in series.items():
        ax.plot(s.index, s.values, label=label)
    if ref_line is not None:
        ax.axhline(ref_line, color="grey", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Tuổi x"); ax.set_ylabel(ylabel); ax.legend()
    _save(fig, name)


def plot_cohort_mean_residual(cohort_resid: pd.Series, name: str = "cohort_mean_residual",
                               periods: dict[str, tuple[int, int]] | None = None):
    """Residual trung bình theo năm sinh (cohort) - một vệt trơn dài hạn khác về bản
    chất với việc "nhiễu" ngẫu nhiên qua từng cohort riêng lẻ. `periods` (tuỳ chọn):
    tô nền các giai đoạn lịch sử để đối chiếu trực quan."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(cohort_resid.index, cohort_resid.values)
    ax.axhline(0, color="grey", linewidth=0.8)
    if periods:
        for label, (start, end) in periods.items():
            ax.axvspan(start, end, alpha=0.12, color="red")
            ax.annotate(label, xy=((start + end) / 2, ax.get_ylim()[1]), ha="center", va="top",
                        fontsize=8, rotation=90)
    ax.set_xlabel("Năm sinh (cohort)"); ax.set_ylabel("Residual trung bình log m(x,t)")
    _save(fig, name)


def plot_residual_heatmap(res: pd.DataFrame, model: str, ylabel: str = "Deviance residual"):
    """Heatmap residuals — nếu còn vệt chéo nghĩa là mô hình bỏ sót cohort effect."""
    fig, ax = plt.subplots(figsize=(9, 5))
    v = np.nanmax(np.abs(res.values))
    im = ax.pcolormesh(res.columns.astype(int), res.index.astype(int),
                       res.values, cmap="RdBu_r", vmin=-v, vmax=v)
    fig.colorbar(im, ax=ax, label=ylabel)
    ax.set_xlabel("Năm t"); ax.set_ylabel("Tuổi x"); ax.set_title(model)
    _save(fig, f"residuals_{model}")
