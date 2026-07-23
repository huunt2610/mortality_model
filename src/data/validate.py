"""Kiểm tra sanity ma trận Dxt/Ext sau khi dựng — chặn lỗi âm thầm lan xuống mô hình."""
import numpy as np
import pandas as pd


def validate_matrices(Dxt: pd.DataFrame, Ext: pd.DataFrame, mx: pd.DataFrame) -> None:
    """Raise ValueError nếu Dxt/Ext không hợp lệ. Không trả gì nếu ổn."""
    if Dxt.shape != Ext.shape:
        raise ValueError(f"Dxt {Dxt.shape} và Ext {Ext.shape} không cùng kích thước")
    if not Dxt.index.equals(Ext.index) or not Dxt.columns.equals(Ext.columns):
        raise ValueError("Dxt và Ext không khớp chỉ số tuổi/năm")

    ages = np.sort(Dxt.index.to_numpy())
    years = np.sort(Dxt.columns.to_numpy())
    if (np.diff(ages) != 1).any():
        raise ValueError("Tuổi không liên tục — thiếu tuổi hoặc trùng lặp")
    if (np.diff(years) != 1).any():
        raise ValueError("Năm không liên tục — thiếu năm hoặc trùng lặp")

    if (Ext.to_numpy() <= 0).any():
        raise ValueError("Ext có giá trị <= 0 — exposure phải dương")

    mx = mx.to_numpy()
    if np.isnan(mx).any():
        raise ValueError("mx có NaN sau khi dựng ma trận (kiểm tra lệch chỉ số age/year)")
    if (mx < 0).any() or (mx > 1.5).any():
        raise ValueError("mx nằm ngoài khoảng hợp lý [0, 1.5] — kiểm tra đơn vị hoặc lỗi parse")
