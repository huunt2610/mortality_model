---
paths:
  - "src/**"
---

# Bản đồ module Python (`src/`)

- `config.py` — `load_params()` đọc `config/params.yaml`; đồng thời export các hằng
  đường dẫn `DATA_RAW`, `DATA_INTERIM`, `DATA_PROCESSED`, `DATA_EXTERNAL`, `FIGURES`.
- `data/read_raw.py` — `read_wpp_single_age_life_table()` đọc file `.xlsx` UN WPP (dò
  dòng tiêu đề bằng cách khớp mờ (fuzzy) các nhãn cột thay vì cố định vị trí dòng/cột,
  vì các bản revision của UN có thể lệch định dạng nhẹ); `read_gso_life_table()` đọc
  file CSV GSO đã số hoá thủ công và suy ra `mx` từ `qx` khi cần.
- `data/make_dataset.py` — entrypoint của pipeline (`WPP_FILES` map + `build_matrices()`,
  được gọi trong `main()`); xem thêm `data-pipeline.md`.
- `data/validate.py` — `validate_matrices()` (raise cứng, dùng trong `make_dataset.py`)
  so với `validate_stmomo_window()` (trả về bảng đạt/không đạt cho một cửa sổ tuổi/năm
  dùng để fit, dùng để hiển thị trong notebook trước khi đưa dữ liệu sang R).
- `data/smoothing.py` — `whittaker_henderson`/`smooth_mx_surface` (làm trơn 1D theo từng
  năm), `smooth_mx_surface_2d` (P-splines, làm trơn tensor-product B-spline đồng thời
  theo cả tuổi *và* năm), `graduate_abridged_mx` (graduation bằng PCHIP từ bảng sống
  nhóm tuổi về tuổi đơn), và phép ngược lại `aggregate_mx_to_groups`/
  `gso_age_group_edges` (tuổi đơn → nhóm tuổi, dùng để đối chiếu UN WPP với bảng nhóm
  tuổi của GSO — nên ưu tiên hơn graduation cho việc đối chiếu này, xem docstring của
  module để biết lý do).
- `data/life_table.py` — `build_life_table()` dựng bảng sống đầy đủ (`qx, lx, dx, Lx,
  Tx, ex`) từ vector `mx`, giả định lực chết không đổi trong khoảng tuổi;
  `life_expectancy_series()` áp dụng theo từng cột (năm) trên một khoảng năm.
- `evaluation/metrics.py` — `rmse`, `mape`, `log_rmse`, `poisson_deviance`.
- `evaluation/cohort.py` — `age_period_residual()`/`cohort_mean_residual()`: phân rã
  nhanh tuổi+năm của `log m(x,t)` để chẩn đoán trong EDA (có đáng để mô hình hoá hiệu
  ứng thế hệ không?) — không thay thế cho việc fit RH thật trong R.
- `visualization/plots.py` — mỗi hàm ứng với một hình trong luận văn
  (`plot_log_mx_by_age`, `plot_lexis_heatmap`, `plot_mx_sex_comparison`,
  `plot_mortality_improvement_by_age`, `plot_lc_params`, `plot_residual_heatmap`, v.v.),
  tất cả đều đi qua `_save()` — xem `figures.md`.
