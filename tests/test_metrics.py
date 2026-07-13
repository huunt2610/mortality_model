import numpy as np
from src.evaluation.metrics import rmse, mape, poisson_deviance


def test_rmse_zero_when_equal():
    a = np.array([1.0, 2.0, 3.0])
    assert rmse(a, a) == 0.0


def test_mape_simple():
    assert abs(mape(np.array([100.0]), np.array([110.0])) - 10.0) < 1e-9


def test_deviance_nonnegative():
    D = np.array([[5.0, 10.0]]); Dh = np.array([[6.0, 9.0]])
    assert poisson_deviance(D, Dh) >= 0
