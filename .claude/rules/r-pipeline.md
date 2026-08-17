---
paths:
  - "R/**"
---

# Pipeline fit mô hình trong R

Các script `R/` có cách đánh số 00–04 riêng (khác với các notebook stub — xem
`language-split.md`) và chạy theo thứ tự, mỗi bước đọc output từ đĩa của bước trước:

1. `R/01_load_data.R` — không chạy trực tiếp; định nghĩa `load_vn_data(series)` đọc
   `data/processed/Dxt_{series}.csv` / `Ext_{series}.csv` thành đối tượng `StMoMoData`.
   Được `source()` bởi các script khác chứ không chạy độc lập.
2. `R/02_fit_models.R` — fit LC, RH, CBD bằng `StMoMo::fit()` trên `fitting.years` và
   phạm vi tuổi riêng cho từng mô hình từ `config/params.yaml`. Ghi ra
   `models/{lc,rh,cbd}_fit.rds`, `data/processed/params_{lc,rh,cbd}_{age,kt,gc}.csv`, và
   `data/processed/residuals_{lc,rh,cbd}.csv`.
3. `R/03_forecast.R` — nạp lại các fit `.rds`, dự báo `kt`/`gc` (RWD/ARIMA theo
   `forecast.kt_model`/`gc_model`), mô phỏng `forecast.n_simulations` đường để tính khoảng
   dự báo. Ghi ra `models/forecasts.rds` và `data/processed/forecast_rates_{lc,rh,cbd}.csv`.
4. `R/04_backtest.R` — với mỗi split trong `backtest.splits`, refit trên
   `years <= train_end` rồi dự báo đến `test_end`, ghi ra
   `data/processed/backtest_lc_{train_end}_{test_end}.csv`.
   **Chỉ nhánh LC được cài đặt** — vòng lặp cho RH/CBD vẫn là `TODO` trong source; đừng
   giả định các file CSV backtest của hai mô hình này đã tồn tại.

`R/utils.R` chứa `plot_residual_heatmap()`, dùng chung cho các bước chẩn đoán ad-hoc trong R.

## Ghi chú khi fit mô hình trong R

- RH dùng `cohortAgeFun = "1"` (β₀=1, theo Haberman & Renshaw 2011) và được khởi tạo từ
  kết quả fit LC; hội tụ chậm (`iterMax = 1e5`), cần kiểm tra `RHfit$conv`.
- Series mặc định là `"total"`, trừ khi cần fit riêng theo giới tính.
