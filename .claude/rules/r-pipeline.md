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
2. Bước fit — **tách riêng mỗi model một file**, chạy theo đúng thứ tự a→b→c (RH đọc
   `models/lc_fit.rds` làm starting values, dừng sớm với thông báo lỗi rõ nếu file này
   chưa tồn tại):
   - `R/02a_fit_lc.R` — fit LC. Ghi `models/lc_fit.rds`, `data/processed/params_lc_*.csv`,
     `residuals_lc.csv`.
   - `R/02b_fit_rh.R` — fit RH, cần `models/lc_fit.rds` đã có sẵn. Ghi `models/rh_fit.rds`,
     `data/processed/params_rh_*.csv`, `residuals_rh.csv`.
   - `R/02c_fit_cbd.R` — fit CBD (độc lập, không phụ thuộc LC/RH). Ghi
     `models/cbd_fit.rds`, `data/processed/params_cbd_*.csv`, `residuals_cbd.csv`.
   - Cả 3 đều đọc `fitting.years` và phạm vi tuổi riêng cho từng model từ
     `config/params.yaml`, và dùng chung `name_cols()`/`export_params()`/
     `export_fit_summary()` trong `R/utils.R` để ghi CSV + in AIC/BIC.
3. `R/03_forecast.R` — nạp lại các fit `.rds`, dự báo `kt`/`gc` (RWD/ARIMA theo
   `forecast.kt_model`/`gc_model`), mô phỏng `forecast.n_simulations` đường để tính khoảng
   dự báo. Ghi ra `models/forecasts.rds` và `data/processed/forecast_rates_{lc,rh,cbd}.csv`.
4. `R/04_backtest.R` — với mỗi split trong `backtest.splits`, refit trên
   `years <= train_end` rồi dự báo đến `test_end`, ghi ra
   `data/processed/backtest_lc_{train_end}_{test_end}.csv`.
   **Chỉ nhánh LC được cài đặt** — vòng lặp cho RH/CBD vẫn là `TODO` trong source; đừng
   giả định các file CSV backtest của hai mô hình này đã tồn tại.

`R/utils.R` chứa `plot_residual_heatmap()` (chẩn đoán ad-hoc) và các hàm xuất kết quả
fit dùng chung cho `R/02a_fit_lc.R`/`02b_fit_rh.R`/`02c_fit_cbd.R` nêu trên.

## Ghi chú khi fit mô hình trong R

- RH dùng `cohortAgeFun = "1"` (β₀=1, theo Haberman & Renshaw 2011) và được khởi tạo từ
  kết quả fit LC (đọc từ `models/lc_fit.rds`, không refit lại trong `02b_fit_rh.R`); hội
  tụ chậm (`iterMax = 1e5`), cần kiểm tra `RHfit$conv`. Ngoài ra dùng `wxt =
  genWeightMat(ages_lc, years_fit, clip = 3)` để loại các cohort ở rìa Lexis diagram có
  quá ít quan sát — khuyến nghị chuẩn trong vignette StMoMo để tránh ước lượng `gc` bất
  ổn ở biên, khác với (và không thay thế) ràng buộc chuẩn hoá nội bộ của `rh()`.
- Series mặc định là `"total"`, trừ khi cần fit riêng theo giới tính.
