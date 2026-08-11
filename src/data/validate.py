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


def validate_stmomo_window(Dxt: pd.DataFrame, Ext: pd.DataFrame, mx: pd.DataFrame,
                            age_range: tuple[int, int], year_range: tuple[int, int]) -> pd.DataFrame:
    """Kiểm tra cửa sổ tuổi/năm dùng để fit StMoMo (vd. `ages.lc_rh` +
    `fitting.years`/`backtest` trong `config/params.yaml`) sẵn sàng cho R —
    đủ tuổi/năm, không NaN, Ext không có giá trị <=0 (log-link cần dương).

    Khác `validate_matrices` (raise khi build dữ liệu ở `make_dataset.py`):
    hàm này trả về bảng pass/fail từng tiêu chí để hiển thị trong notebook,
    dùng làm bước xác nhận tường minh trước khi fit, không phải cổng chặn lỗi
    khi dựng dữ liệu.
    """
    a0, a1 = age_range
    y0, y1 = year_range
    sub_dxt = Dxt.loc[a0:a1, y0:y1]
    sub_ext = Ext.loc[a0:a1, y0:y1]
    sub_mx = mx.loc[a0:a1, y0:y1]

    expected_ages = set(range(a0, a1 + 1))
    expected_years = set(range(y0, y1 + 1))

    checks = {
        f"Đủ tuổi ({a0}-{a1})": expected_ages.issubset(set(sub_ext.index)),
        f"Đủ năm ({y0}-{y1})": expected_years.issubset(set(sub_ext.columns)),
        "Không NaN trong Dxt": not sub_dxt.isna().to_numpy().any(),
        "Không NaN trong Ext": not sub_ext.isna().to_numpy().any(),
        "Không NaN trong mx": not sub_mx.isna().to_numpy().any(),
        "Ext > 0 (không có giá trị <=0)": bool((sub_ext.to_numpy() > 0).all()),
    }
    return pd.DataFrame({"đạt": checks}).rename_axis("tiêu chí")
