"""Chỉ số đánh giá dự báo — dùng chung cho mọi mô hình."""
import numpy as np


def rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    a, p = np.asarray(actual), np.asarray(predicted)
    return float(np.sqrt(np.nanmean((a - p) ** 2)))


def mape(actual: np.ndarray, predicted: np.ndarray) -> float:
    a, p = np.asarray(actual), np.asarray(predicted)
    return float(np.nanmean(np.abs((a - p) / a)) * 100)


def log_rmse(actual_mx: np.ndarray, predicted_mx: np.ndarray) -> float:
    """RMSE trên thang log — chuẩn trong tài liệu mortality vì mx trải nhiều bậc."""
    return rmse(np.log(actual_mx), np.log(predicted_mx))


def poisson_deviance(D: np.ndarray, D_hat: np.ndarray) -> float:
    """Deviance Poisson: 2*sum[ D*log(D/D_hat) - (D - D_hat) ]."""
    D, D_hat = np.asarray(D, float), np.asarray(D_hat, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        term = np.where(D > 0, D * np.log(D / D_hat), 0.0)
    return float(2 * np.nansum(term - (D - D_hat)))
