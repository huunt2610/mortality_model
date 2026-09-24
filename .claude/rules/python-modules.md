---
paths:
  - "src/**"
---

# Bản đồ module Python (`src/`)

- `config.py` — `load_params()` đọc `config/params.yaml`; hằng đường dẫn `DATA_RAW`,
  `DATA_INTERIM`, `DATA_PROCESSED`, `DATA_EXTERNAL`, `MODELS`, `RESULTS`, `FIGURES`;
  `processed_dir(dataset)` / `results_dir(dataset)` (mặc định `DEFAULT_DATASET = "wpp_vnm"`).

## `data/` — đọc nguồn và dựng ma trận (IO)

- `wpp.py` — `read_wpp_single_age_life_table(path, iso3)` đọc `.xlsx` UN WPP (dò dòng tiêu đề
  bằng khớp mờ nhãn cột thay vì cố định vị trí, vì các revision của UN có thể lệch định dạng).
- `hmd.py` — `read_hmd_country(country, sex)` đọc `Deaths_1x1.txt`/`Exposures_1x1.txt` (nhánh A;
  có số ca tử vong thật).
- `gso.py` — `read_gso_abridged(year)` đọc bảng sống rút gọn số hoá tay trong
  `data/external/gso/` (cột sex, x, n, …, nmx, nqx, ex; map năm → file ở `GSO_FILES`);
  `read_gso_life_table(path)` cho định dạng tuổi đơn (age, sex, mx/qx).
- `make_dataset.py` — entrypoint `python -m src.data.make_dataset [--dataset X]`; `WPP_DIR`,
  `WPP_FILES`, `build_matrices()` trả về `(Dxt, Ext, mx)` (dùng cột `deaths` nếu có, không thì
  `Dxt = mx * Ext`); xem `data-pipeline.md`.
- `validate.py` — `validate_matrices(Dxt, Ext, mx)` (raise cứng, dùng trong `make_dataset.py`)
  so với `validate_stmomo_window()` (bảng đạt/không đạt để hiển thị trong notebook).

## `demography/` — toán bảng sống

- `life_table.py` — `build_life_table()` (`qx, lx, dx, Lx, Tx, ex` từ `mx`, lực chết không đổi
  trong khoảng tuổi); `life_expectancy_series()` theo từng năm.
- `smoothing.py` — `whittaker_henderson`/`smooth_mx_surface` (1D theo năm),
  `smooth_mx_surface_2d` + `cv_select_lambda_2d` (P-splines 2D), `graduate_abridged_mx` (PCHIP
  nhóm tuổi → tuổi đơn).
- `age_groups.py` — hài hoà nhóm tuổi cho nhánh B: `gso_age_group_edges`,
  `aggregate_mx_to_groups` (nMx = ΣD/ΣE), `aggregate_qx_to_groups` (nqx = 1 − Π(1 − q), dùng cho
  dự báo; nhóm mở trả NaN). Ưu tiên gộp nhóm hơn graduation khi đối chiếu với GSO.

## `evaluation/` — tiêu chí đánh giá (bản đồ tri thức Mục 13)

- `metrics.py` — `rmse`, `mape`, `mae`, `log_rmse`, `poisson_deviance`, `coverage`.
- `decomposition.py` — `decompose_error(F, W, G)`: (F−G) = (F−W) + (W−G) (Mục 12.2).
- `cohort.py` — `age_period_residual()`/`cohort_mean_residual()`: chẩn đoán nhanh trong EDA,
  không thay thế fit RH thật trong R.

## `risk/` — ứng dụng (Mục 14)

- `pricing.py` — `cohort_qx(qxt, age, year)` (đường chéo đoàn hệ), `survival_curve`,
  `annuity_due`, `term_insurance`.
- `measures.py` — `value_at_risk`, `expected_shortfall`, `risk_capital` (đuôi phải: giá trị hiện
  tại lớn = tổn thất).

## `visualization/`

- `plots.py` — mỗi hàm ứng với một hình trong luận văn, tất cả đi qua `_save()` — xem `figures.md`.
