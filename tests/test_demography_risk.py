import numpy as np
import pandas as pd
import pytest

from src.demography.age_groups import aggregate_qx_to_groups
from src.evaluation.decomposition import decompose_error
from src.evaluation.metrics import coverage
from src.risk.measures import expected_shortfall, risk_capital, value_at_risk
from src.risk.pricing import annuity_due, cohort_qx, term_insurance


def test_aggregate_qx_to_groups_product_rule():
    qx = pd.Series([0.1, 0.2, 0.3, 0.4], index=[0, 1, 2, 3])
    out = aggregate_qx_to_groups(qx, [(0, 0), (1, 2), (3, None)])
    assert out.loc["0", "nqx"] == pytest.approx(0.1)
    assert out.loc["1-2", "nqx"] == pytest.approx(1 - 0.8 * 0.7)
    assert np.isnan(out.loc["3+", "nqx"])


def test_decompose_error_adds_up():
    f, w, g = pd.Series([1.0, 2.0]), pd.Series([0.5, 2.5]), pd.Series([0.0, 1.0])
    out = decompose_error(f, w, g)
    assert np.allclose(out["total"], out["model"] + out["source"])


def test_coverage():
    actual, lo, hi = np.array([1, 2, 5]), np.zeros(3), np.full(3, 3)
    assert coverage(actual, lo, hi) == pytest.approx(2 / 3)


def test_annuity_due_zero_mortality_is_annuity_certain():
    # q = 0 trong 3 năm rồi chết chắc chắn: ä = 1 + v + v^2 + v^3
    i = 0.05
    v = 1 / (1 + i)
    assert annuity_due([0, 0, 0, 1], i) == pytest.approx(1 + v + v**2 + v**3)


def test_term_insurance_one_year():
    assert term_insurance([0.1, 0.2], 0.0, 1) == pytest.approx(0.1)
    with pytest.raises(ValueError):
        term_insurance([0.1], 0.05, 2)


def test_cohort_qx_follows_diagonal():
    qxt = pd.DataFrame([[0.1, 0.11], [0.2, 0.21]], index=[65, 66], columns=[2020, 2021])
    assert list(cohort_qx(qxt, 65, 2020)) == [0.1, 0.21]


def test_risk_measures_ordering():
    v = np.arange(1000, dtype=float)
    assert value_at_risk(v) <= expected_shortfall(v)
    assert risk_capital(v) == pytest.approx(value_at_risk(v) - v.mean())
