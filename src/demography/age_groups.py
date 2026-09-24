"""Hài hoà nhóm tuổi: gộp tuổi đơn (WPP, dự báo mô hình) về đúng khuôn nhóm tuổi của bảng
sống GSO (0, 1-4, 5-9, ..., 80+) để so sánh - docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md,
Mục 12.2.

Gộp nhóm (aggregation) không nội suy nên không có rủi ro khuếch đại nhiễu như graduation
(`src.demography.smoothing.graduate_abridged_mx`), đánh đổi lại là mất độ phân giải tuổi
đơn - xem notebook 03 về lý do ưu tiên cách này khi đối chiếu với GSO. Nhóm tuổi mở phải
được xử lý giống nhau ở cả hai phía.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

AgeEdges = list[tuple[int, int | None]]


def gso_age_group_edges(df_abridged: pd.DataFrame) -> AgeEdges:
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


def _group_mask(index: pd.Index, start: int, end: int | None) -> tuple[np.ndarray, str]:
    if end is None:
        return index >= start, f"{start}+"
    if end == start:
        return index == start, str(start)
    return (index >= start) & (index <= end), f"{start}-{end}"


def aggregate_mx_to_groups(Dxt: pd.Series, Ext: pd.Series, edges: AgeEdges) -> pd.DataFrame:
    """Gộp Dxt/Ext tuổi đơn thành nhóm tuổi (vd. GSO: 0, 1-4, 5-9, ..., 80+).

    nMx = sum(D)/sum(E) trong nhóm - trọng số đúng chuẩn actuarial theo exposure,
    KHÔNG phải trung bình cộng đơn giản của mx từng tuổi (sẽ lệch vì mx thay đổi
    rất nhanh theo tuổi, đặc biệt ở nhóm tuổi nhỏ). `edges`: danh sách
    (tuổi bắt đầu, tuổi kết thúc bao gồm - None cho nhóm mở, vd. (80, None)).
    """
    rows = []
    for start, end in edges:
        mask, label = _group_mask(Dxt.index, start, end)
        D, E = Dxt[mask].sum(), Ext[mask].sum()
        rows.append({"group": label, "x": start, "nMx": D / E})
    return pd.DataFrame(rows).set_index("group")


def aggregate_qx_to_groups(qx: pd.Series, edges: AgeEdges) -> pd.DataFrame:
    """Gộp xác suất tử vong tuổi đơn q(x) thành nqx = 1 - prod(1 - q(x+i)) trong nhóm.

    Dùng cho dự báo mô hình (chỉ có tỷ suất, không có exposure tương lai) khi so với
    cột `nqx` của bảng GSO. Nhóm mở: nqx = 1 theo định nghĩa, nên trả về NaN để không
    so sánh nhầm - đối chiếu nhóm mở bằng e(x) thay vì nqx.
    """
    rows = []
    for start, end in edges:
        mask, label = _group_mask(qx.index, start, end)
        nqx = np.nan if end is None else 1 - np.prod(1 - qx[mask].to_numpy())
        rows.append({"group": label, "x": start, "nqx": nqx})
    return pd.DataFrame(rows).set_index("group")
