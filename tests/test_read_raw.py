import pandas as pd
import pytest

from src.data.make_dataset import build_matrices
from src.data.read_raw import read_gso_life_table, read_wpp_single_age_life_table
from src.data.validate import validate_matrices

WPP_HEADER = [
    "Index", "Variant", "Region, subregion, country or area *", "Notes",
    "Location code", "ISO3 Alpha-code", "ISO2 Alpha-code", "SDMX code**",
    "Type", "Parent code", "Year", "Age (x)", "AgeGrpSpan",
    "Central death rate m(x,n)", "Probability of dying q(x,n)",
    "Probability of surviving p(x,n)", "Number of survivors l(x)",
    "Number of deaths d(x,n)", "Number of person-years lived L(x,n)",
    "Survivorship ratio S(x,n)", "Number of person-years remaining T(x)",
    "Expectation of life e(x)", "Average number of years lived a(x,n)",
]


def _make_wpp_fixture(tmp_path):
    """Giả lập file UN WPP thật: metadata phía trên, tiêu đề ở dòng 17, có 2 quốc gia."""
    rows = []
    for year in (2020, 2021):
        for age in (0, 1, 2):
            rows.append([1, "Estimates", "Viet Nam", "", 704, "VNM", "VN", "704",
                         "Country/Area", 900, year, age, 1,
                         0.01 + age * 0.001, 0, 0, 0, 0, 1000 - age * 10, 0, 0, 0, 0])
            rows.append([2, "Estimates", "Other Country", "", 1, "OTH", "OT", "1",
                         "Country/Area", 900, year, age, 1,
                         0.5, 0, 0, 0, 0, 1, 0, 0, 0, 0])
    df = pd.DataFrame(rows, columns=WPP_HEADER)

    path = tmp_path / "wpp_sample.xlsx"
    with pd.ExcelWriter(path) as writer:
        pd.DataFrame([["UN WPP 2024 — file mẫu giả lập cho test"]]).to_excel(
            writer, sheet_name="Estimates", header=False, index=False, startrow=0
        )
        df.to_excel(writer, sheet_name="Estimates", index=False, header=True, startrow=16)
    return path


def test_read_wpp_filters_vietnam_and_parses_columns(tmp_path):
    path = _make_wpp_fixture(tmp_path)
    out = read_wpp_single_age_life_table(path)

    assert set(out["year"]) == {2020, 2021}
    assert set(out["age"]) == {0, 1, 2}
    assert len(out) == 6
    # mx của "Other Country" (0.5) không được lẫn vào
    assert (out["mx"] < 0.1).all()
    row = out[(out.year == 2020) & (out.age == 1)].iloc[0]
    assert row["mx"] == pytest.approx(0.011)
    assert row["exposure"] == pytest.approx(990)


def test_read_wpp_missing_country_raises(tmp_path):
    df = pd.DataFrame([[1, "Estimates", "Other Country", "", 1, "OTH", "OT", "1",
                        "Country/Area", 900, 2020, 0, 1, 0.5, 0, 0, 0, 0, 1, 0, 0, 0, 0]],
                       columns=WPP_HEADER)
    path = tmp_path / "no_vn.xlsx"
    with pd.ExcelWriter(path) as writer:
        pd.DataFrame([["meta"]]).to_excel(writer, sheet_name="Estimates", header=False,
                                           index=False, startrow=0)
        df.to_excel(writer, sheet_name="Estimates", index=False, header=True, startrow=16)
    with pytest.raises(ValueError, match="Việt Nam"):
        read_wpp_single_age_life_table(path)


def test_build_matrices_and_validate_roundtrip(tmp_path):
    path = _make_wpp_fixture(tmp_path)
    df = read_wpp_single_age_life_table(path)
    Dxt, Ext = build_matrices(df, 2020, 2021)

    assert list(Dxt.index) == [0, 1, 2]
    assert list(Dxt.columns) == [2020, 2021]
    validate_matrices(Dxt, Ext)  # không raise nghĩa là hợp lệ


def test_validate_matrices_rejects_mismatched_shapes():
    Dxt = pd.DataFrame({2020: [1, 2]}, index=[0, 1])
    Ext = pd.DataFrame({2020: [1, 2, 3]}, index=[0, 1, 2])
    with pytest.raises(ValueError):
        validate_matrices(Dxt, Ext)


def test_validate_matrices_rejects_non_contiguous_ages():
    idx = [0, 1, 3]
    Dxt = pd.DataFrame({2020: [1, 2, 3], 2021: [1, 2, 3]}, index=idx)
    Ext = pd.DataFrame({2020: [10, 20, 30], 2021: [10, 20, 30]}, index=idx)
    with pytest.raises(ValueError, match="Tuổi không liên tục"):
        validate_matrices(Dxt, Ext)


def test_read_gso_life_table_derives_mx_from_qx(tmp_path):
    path = tmp_path / "gso_sample.csv"
    pd.DataFrame({"age": [0, 1], "sex": ["male", "male"], "qx": [0.02, 0.01]}).to_csv(
        path, index=False
    )
    out = read_gso_life_table(path)
    assert "mx" in out.columns
    assert (out["mx"] > 0).all()


def test_read_gso_life_table_missing_columns_raises(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"age": [0, 1]}).to_csv(path, index=False)
    with pytest.raises(ValueError):
        read_gso_life_table(path)
