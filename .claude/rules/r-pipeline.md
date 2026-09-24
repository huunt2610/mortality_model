---
paths:
  - "R/**"
---

# Pipeline fit mô hình trong R

Mọi script chạy từ gốc repo và nhận **dataset** là tham số dòng lệnh đầu tiên
(`Rscript R/02a_fit_lc.R hmd_jpn`); bỏ trống thì dùng `default_dataset` trong
`config/params.yaml` (hiện là `wpp_vnm`). Dataset không có trong `datasets:` → `stop()`.

Đường dẫn theo dataset (định nghĩa trong `R/lib/load_data.R`):
- input: `data/processed/<dataset>/Dxt_{series}.csv`, `Ext_{series}.csv`
- object: `models/<dataset>/<model>_fit.rds`, `forecasts.rds`
- output CSV cho Python: `results/<dataset>/params_<model>_{age,kt,gc}.csv`,
  `residuals_<model>.csv`, `forecast_rates_<model>.csv`, `backtest_<model>_<train_end>_<test_end>.csv`

## `R/lib/` — chỉ `source()`, không chạy trực tiếp

- `load_data.R` — `load_config()`, `get_dataset(cfg)`, `processed_dir/models_dir/results_dir`,
  `load_stmomo_data(dataset, series)` → `StMoMoData` (type `"central"`).
- `models.R` — `model_spec(name)` cho `lc`, `rh`, `apc`, `cbd`, `m7`; `model_ages(name, cfg)`
  (tra `models.<name>.ages` → `ages.<key>`); `fit_years(cfg)`; `fit_model(name, dat, cfg,
  years_fit, start)` dùng chung cho fit chính thức lẫn backtest. `COHORT_MODELS` = rh, apc, m7.
- `export.R` — `save_fit(f, name, dataset)` = saveRDS + `export_params()` + `export_fit_summary()`
  (ghi CSV + in AIC/BIC).
- `diagnostics.R` — `plot_residual_heatmap()` (chẩn đoán ad-hoc; hình luận văn vẽ bằng Python).

## Thứ tự chạy

1. Fit — mỗi mô hình một file, mỗi file chỉ gọi `fit_model()` + `save_fit()`:
   `02a_fit_lc.R` → `02b_fit_rh.R` (cần `models/<dataset>/lc_fit.rds`, dừng sớm với thông báo
   rõ nếu chưa có) ; `02c_fit_cbd.R`, `02d_fit_apc.R`, `02e_fit_m7.R` độc lập.
2. `03_forecast.R` — nạp mọi `<model>_fit.rds` đã có trong `models/<dataset>/`, dự báo (cohort
   bằng ARIMA(1,1,0)), mô phỏng LC `forecast.n_simulations` đường. **CBD/M7 (logit) xuất q(x,t),
   LC/RH/APC xuất m(x,t)** trong `forecast_rates_*.csv`.
3. `04_backtest.R` — mỗi mô hình trong `backtest.models` × mỗi split trong `backtest.splits`:
   refit trên `train_start..train_end`, dự báo đến `test_end`, ghi sai số log. Mô hình logit
   được so với q = 1 − exp(−m). Mặc định `backtest.models: ["lc"]`; đã chạy thử được cả 5 mô hình.
4. `05_fit_llt.R` (nhánh C) và `06_simulate_scenarios.R` (ứng dụng) — **mới là khung**, header
   liệt kê các bước, thân script `stop()`. Đừng giả định output của chúng tồn tại.

## Ghi chú khi fit mô hình

- RH dùng `cohortAgeFun = "1"` (β₀=1, Haberman & Renshaw 2011) + `approxConst = TRUE`, khởi tạo từ
  LC (không refit LC trong `02b_fit_rh.R`); hội tụ chậm (`iterMax = 1e5`), `fit_model()` cảnh báo
  khi `conv` sai.
- RH/APC/M7 dùng `wxt = genWeightMat(ages, years, clip = fitting.cohort_clip)` để loại cohort
  ở rìa Lexis có quá ít quan sát — khác với (và không thay thế) ràng buộc chuẩn hoá của mô hình.
- CBD/M7 trên WPP báo cảnh báo `non-integer #successes in a binomial glm` — do `Dxt = mx * Ext`
  là đại lượng suy ra, không phải số đếm (xem `data-pipeline.md`); không phải lỗi code.
- Series mặc định là `"total"`, trừ khi cần fit riêng theo giới tính.
