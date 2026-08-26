"""Làm trơn (smoothing) và graduation cho bảng sống.

- Whittaker-Henderson: làm trơn log m(x,t) theo tuổi, có trọng số theo exposure
  (tuổi có exposure lớn được tin cậy hơn) - phương pháp làm trơn kinh điển trong
  actuarial (Whittaker 1922, Henderson 1924). Làm trơn 1D: từng năm riêng biệt,
  không ràng buộc độ mượt giữa năm t và t+1.
- P-splines 2D (Eilers & Marx 1996, mở rộng 2 chiều theo Eilers, Currie & Durban
  2004): làm trơn log m(x,t) đồng thời theo cả tuổi x và năm t bằng basis
  B-spline tensor product + phạt sai phân trên hệ số basis - khắc phục nhược
  điểm của WH 1D là có thể tạo vết giật cục giữa các năm liền kề.
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
from scipy.interpolate import BSpline, PchipInterpolator


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


def _bspline_basis(x: np.ndarray, n_basis: int, degree: int = 3) -> np.ndarray:
    """Ma trận basis B-spline bậc `degree`, `n_basis` hàm cơ sở, nút trong đều
    trên [min(x), max(x)] (basis "mở" - lặp `degree+1` nút ở 2 đầu)."""
    x_min, x_max = x.min(), x.max()
    n_interior = n_basis - degree - 1
    interior = np.linspace(x_min, x_max, n_interior + 2)[1:-1]
    knots = np.concatenate([[x_min] * (degree + 1), interior, [x_max] * (degree + 1)])
    basis = np.zeros((len(x), n_basis))
    for j in range(n_basis):
        coef = np.zeros(n_basis)
        coef[j] = 1.0
        basis[:, j] = BSpline(knots, coef, degree, extrapolate=False)(x)
    # điểm x_max rơi ngoài miền extrapolate=False của B-spline cuối cùng - basis
    # tại đó bằng 0 thay vì đúng giá trị biên, gán lại theo tính chất "partition
    # of unity" (tổng mọi basis tại 1 điểm luôn bằng 1)
    basis[np.isnan(basis)] = 0.0
    row_sum = basis.sum(axis=1, keepdims=True)
    edge = np.isclose(row_sum, 0.0)
    if edge.any():
        basis[edge.ravel(), -1] = 1.0
    return basis


def _fit_pspline_2d(y_vec: np.ndarray, w_vec: np.ndarray, B: np.ndarray, n_basis_age: int,
                     n_basis_year: int, lam_age: float, lam_year: float) -> np.ndarray:
    """Giải hệ phương trình chuẩn (normal equations) của P-splines 2D có trọng
    số cho vector hệ số basis `theta` - dùng chung bởi `smooth_mx_surface_2d`
    và `cv_select_lambda_2d` (basis `B` không đổi giữa các lần gọi, chỉ trọng
    số `w_vec` và `lam_age`/`lam_year` thay đổi khi dò lambda hoặc che ô CV).
    """
    Dx = np.diff(np.eye(n_basis_age), n=2, axis=0)
    Dt = np.diff(np.eye(n_basis_year), n=2, axis=0)
    penalty = (lam_age * np.kron(np.eye(n_basis_year), Dx.T @ Dx)
               + lam_year * np.kron(Dt.T @ Dt, np.eye(n_basis_age)))

    Bw = w_vec[:, None] * B
    A = B.T @ Bw + penalty
    b = B.T @ (w_vec * y_vec)
    return np.linalg.solve(A, b)


def smooth_mx_surface_2d(mx: pd.DataFrame, ext: pd.DataFrame, n_basis_age: int = 20,
                          n_basis_year: int = 15, lam_age: float = 100.0, lam_year: float = 100.0,
                          degree: int = 3) -> pd.DataFrame:
    """Làm trơn log m(x,t) đồng thời theo tuổi và năm bằng P-splines 2D (tensor
    product B-spline + phạt sai phân bậc 2 trên hệ số basis, có trọng số theo
    exposure) - khác WH 1D (`smooth_mx_surface`) ở chỗ ràng buộc độ mượt cả
    theo chiều năm, không chỉ theo tuổi trong từng năm riêng lẻ. `lam_age`/
    `lam_year` nên được chọn bằng `cv_select_lambda_2d` thay vì đoán tay - xem
    notebook 03.
    """
    ages = mx.index.to_numpy(dtype=float)
    years = mx.columns.to_numpy(dtype=float)
    n_age, n_year = len(ages), len(years)

    Bx = _bspline_basis(ages, n_basis_age, degree)
    Bt = _bspline_basis(years, n_basis_year, degree)
    B = np.kron(Bt, Bx)  # (n_age*n_year, n_basis_age*n_basis_year), tuổi biến thiên nhanh nhất

    y_vec = np.log(mx).to_numpy().reshape(-1, order="F")
    w_vec = ext.to_numpy().reshape(-1, order="F")

    theta = _fit_pspline_2d(y_vec, w_vec, B, n_basis_age, n_basis_year, lam_age, lam_year)

    smoothed = (B @ theta).reshape(n_age, n_year, order="F")
    return pd.DataFrame(np.exp(smoothed), index=mx.index, columns=mx.columns)


def cv_select_lambda_2d(mx: pd.DataFrame, ext: pd.DataFrame, lam_grid: list[float],
                         n_basis_age: int = 20, n_basis_year: int = 15, degree: int = 3,
                         k_folds: int = 5, n_repeats: int = 10, random_state: int = 0) -> pd.DataFrame:
    """K-fold cross-validation để chọn lambda cho P-splines 2D (`lam_age =
    lam_year = lam`, một giá trị chung cho cả 2 chiều - khớp cách notebook 03
    dùng `smooth_mx_surface_2d`; nếu cần dò 2 chiều độc lập, gọi `_fit_pspline_2d`
    trực tiếp với lưới (lam_age, lam_year) riêng).

    Với mỗi `lam` trong `lam_grid`: chia ngẫu nhiên các ô (tuổi, năm) có
    exposure > 0 thành `k_folds` phần; lần lượt che trọng số (gán 0) của 1
    phần khi fit trên phần còn lại, rồi đo weighted RMSE giữa log mx dự đoán
    và log mx thật **chỉ trên phần bị che** (ngoài mẫu) - không đo trên tập
    train, vì RSS trong mẫu luôn giảm đơn điệu khi lam giảm về 0 (overfit),
    không dùng được để chọn lam. Trọng số khi tính RMSE là chính exposure gốc,
    nhất quán với cách hàm fit đã weighted theo exposure.

    Lặp lại toàn bộ k-fold `n_repeats` lần với các cách chia ngẫu nhiên khác
    nhau rồi lấy trung bình - với lưới tuổi×năm cỡ trung bình của bài toán
    này, đường cong CV của 1 lần chia dao động seed-to-seed đủ lớn để đổi cả
    lam thắng cuộc (kiểm chứng thực nghiệm: 1 lần chia có thể chọn lam=100
    hoặc lam=1000 tuỳ seed dù chênh lệch score rất nhỏ); lặp lại và lấy trung
    bình cho ước lượng ổn định hơn, `cv_wrmse_std` đo chính độ dao động đó để
    biết đường cong có đủ "nhọn" để tin tưởng vào lam tối ưu hay không.
    """
    ages = mx.index.to_numpy(dtype=float)
    years = mx.columns.to_numpy(dtype=float)

    Bx = _bspline_basis(ages, n_basis_age, degree)
    Bt = _bspline_basis(years, n_basis_year, degree)
    B = np.kron(Bt, Bx)

    y_vec = np.log(mx).to_numpy().reshape(-1, order="F")
    w_vec = ext.to_numpy().reshape(-1, order="F")
    valid_idx = np.flatnonzero(w_vec > 0)  # ô w=0 không mang thông tin để CV

    seed_seq = np.random.SeedSequence(random_state)
    repeat_scores = {lam: [] for lam in lam_grid}
    for child_seed in seed_seq.spawn(n_repeats):
        rng = np.random.default_rng(child_seed)
        shuffled = rng.permutation(valid_idx)
        fold_of = np.arange(len(shuffled)) % k_folds
        for lam in lam_grid:
            se_sum, w_sum = 0.0, 0.0
            for k in range(k_folds):
                holdout = shuffled[fold_of == k]
                w_train = w_vec.copy()
                w_train[holdout] = 0.0
                theta = _fit_pspline_2d(y_vec, w_train, B, n_basis_age, n_basis_year, lam, lam)
                err = y_vec[holdout] - B[holdout] @ theta
                se_sum += np.sum(w_vec[holdout] * err**2)
                w_sum += np.sum(w_vec[holdout])
            repeat_scores[lam].append(np.sqrt(se_sum / w_sum))

    rows = [{"lam": lam, "cv_wrmse_log_mx": np.mean(scores), "cv_wrmse_std": np.std(scores)}
            for lam, scores in repeat_scores.items()]
    return pd.DataFrame(rows).set_index("lam")


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
