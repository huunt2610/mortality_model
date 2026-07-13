"""Hình chuẩn cho luận văn. Mỗi hàm lưu 1 hình vào reports/figures (300 dpi)."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.config import FIGURES


def _save(fig, name: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_log_mx_by_age(mx: pd.DataFrame, years: list[int], name: str = "log_mx_by_age"):
    """log m_x theo tuổi, mỗi đường một năm — hình mở đầu chương EDA."""
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


def plot_residual_heatmap(res: pd.DataFrame, model: str):
    """Heatmap residuals — nếu còn vệt chéo nghĩa là mô hình bỏ sót cohort effect."""
    fig, ax = plt.subplots(figsize=(9, 5))
    v = np.nanmax(np.abs(res.values))
    im = ax.pcolormesh(res.columns.astype(int), res.index.astype(int),
                       res.values, cmap="RdBu_r", vmin=-v, vmax=v)
    fig.colorbar(im, ax=ax, label="Deviance residual")
    ax.set_xlabel("Năm t"); ax.set_ylabel("Tuổi x"); ax.set_title(model)
    _save(fig, f"residuals_{model}")
