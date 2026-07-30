"""Làm trơn (smoothing) và graduation cho bảng sống.

- Whittaker-Henderson: làm trơn log m(x,t) theo tuổi, có trọng số theo exposure
  (tuổi có exposure lớn được tin cậy hơn) - phương pháp làm trơn kinh điển trong
  actuarial (Whittaker 1922, Henderson 1924).
- Graduation: chuyển bảng sống nhóm tuổi (vd. GSO, nhóm 5 tuổi) về tuổi đơn bằng
  nội suy spline đơn điệu (PCHIP) trên log(nmx) tại trung điểm mỗi nhóm tuổi -
  đơn giản hơn các công thức Beers/Sprague truyền thống nhưng vẫn giữ được hình
  dạng đơn điệu hợp lý của mx theo tuổi. RỦI RO: với dữ liệu có age heaping
  (làm tròn tuổi) hoặc nhiễu tuổi già như GSO Việt Nam, nội suy có thể khuếch
  đại nhiễu cục bộ thành các đỉnh/đáy giả ở tuổi đơn - xem notebook 03 để có
  bằng chứng cụ thể và lý do nên ưu tiên gộp nhóm (aggregation) thay vì graduation
  khi so sánh với GSO.
- Aggregation (chiều ngược lại): gộp Dxt/Ext tuổi đơn (UN WPP) thành nhóm tuổi
  giống cấu trúc GSO, nMx = sum(D)/sum(E) trong nhóm - không nội suy nên không
  có rủi ro khuếch đại nhiễu, đánh đổi lại là mất độ phân giải tuổi đơn.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator


def whittaker_henderson(y: np.ndarray, weights: np.ndarray, lam: float = 1000.0, d: int = 2) -> np.ndarray:
    """Làm trơn 1 chuỗi `y` (vd. log mx theo tuổi) bằng Whittaker-Henderson.

    Cực tiểu hoá sum(w*(y-z)^2) + lam * sum(diff^d(z)^2) - đánh đổi giữa bám sát
    dữ liệu gốc (trọng số `weights`) và độ mượt (phạt sai phân bậc `d`).
    """
    n = len(y)
    D = np.diff(np.eye(n), n=d, axis=0)
    A = np.diag(weights) + lam * D.T @ D
    return np.linalg.solve(A, weights * y)


def smooth_mx_surface(mx: pd.DataFrame, ext: pd.DataFrame, lam: float = 1000.0, d: int = 2) -> pd.DataFrame:
    """Làm trơn log m(x,t) theo tuổi, mỗi năm (cột) riêng biệt, trọng số = exposure Ext."""
    logmx = np.log(mx)
    smoothed = pd.DataFrame(index=mx.index, columns=mx.columns, dtype=float)
    for year in mx.columns:
        smoothed[year] = whittaker_henderson(logmx[year].to_numpy(), ext[year].to_numpy(), lam=lam, d=d)
    return np.exp(smoothed)


def graduate_abridged_mx(df_abridged: pd.DataFrame, ages: np.ndarray) -> pd.Series:
    """Graduation bảng sống nhóm tuổi (cột `x`, `n`, `nmx`) về tuổi đơn.

    Bỏ qua nhóm tuổi mở (n rỗng, vd. "80+") vì không có trung điểm xác định và
    nqx=1 theo định nghĩa không phản ánh hình dạng mx thật - chỉ graduate trong
    phạm vi các nhóm tuổi đóng, các tuổi ngoài phạm vi này trả về NaN.
    """
    closed = df_abridged.dropna(subset=["n"]).copy()
    # nhóm rộng 1 tuổi (vd. tuổi 0) đã là 1 điểm tuổi đơn - không cộng nửa khoảng
    midpoint = closed["x"] + np.where(closed["n"] > 1, closed["n"] / 2, 0)
    interp = PchipInterpolator(midpoint.to_numpy(), np.log(closed["nmx"].to_numpy()), extrapolate=False)
    return pd.Series(np.exp(interp(ages)), index=ages)


def gso_age_group_edges(df_abridged: pd.DataFrame) -> list[tuple[int, int | None]]:
    """Suy ra danh sách (tuổi bắt đầu, tuổi kết thúc bao gồm - None cho nhóm mở)
    trực tiếp từ cột `x`, `n` của bảng GSO - dùng làm "khuôn mẫu" nhóm tuổi cho
    `aggregate_mx_to_groups`, gắn chặt với đúng cấu trúc GSO thay vì hardcode
    rời rạc dễ lệch nếu file GSO đổi cấu trúc nhóm.
    """
    edges = []
    for x_raw, n in zip(df_abridged["x"], df_abridged["n"]):
        if pd.isna(n):
            edges.append((int(str(x_raw).rstrip("+")), None))
        else:
            start = int(x_raw)
            edges.append((start, start + int(n) - 1))
    return edges


def aggregate_mx_to_groups(Dxt: pd.Series, Ext: pd.Series,
                            edges: list[tuple[int, int | None]]) -> pd.DataFrame:
    """Gộp Dxt/Ext tuổi đơn thành nhóm tuổi (vd. GSO: 0, 1-4, 5-9, ..., 80+).

    nMx = sum(D)/sum(E) trong nhóm - trọng số đúng chuẩn actuarial theo exposure,
    KHÔNG phải trung bình cộng đơn giản của mx từng tuổi (sẽ lệch vì mx thay đổi
    rất nhanh theo tuổi, đặc biệt ở nhóm tuổi nhỏ). `edges`: danh sách
    (tuổi bắt đầu, tuổi kết thúc bao gồm - None cho nhóm mở, vd. (80, None)).
    """
    rows = []
    for start, end in edges:
        if end is None:
            mask = Dxt.index >= start
            label = f"{start}+"
        elif end == start:
            mask = Dxt.index == start
            label = str(start)
        else:
            mask = (Dxt.index >= start) & (Dxt.index <= end)
            label = f"{start}-{end}"
        D, E = Dxt[mask].sum(), Ext[mask].sum()
        rows.append({"group": label, "x": start, "nMx": D / E})
    return pd.DataFrame(rows).set_index("group")
