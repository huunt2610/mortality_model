# Lệnh

```bash
# Cài đặt Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Cài đặt R
Rscript R/00_install_packages.R

# Pipeline dữ liệu
python -m src.data.make_dataset

# Fit từng mô hình (đúng thứ tự - RH đọc lc_fit.rds làm starting values), rồi
# forecast, rồi backtest (mỗi bước đọc output của bước trước)
Rscript R/02a_fit_lc.R
Rscript R/02b_fit_rh.R
Rscript R/02c_fit_cbd.R
Rscript R/03_forecast.R
Rscript R/04_backtest.R

# Test
pytest

# Lint
ruff check .        # Python (config: ruff.toml)
Rscript -e 'lintr::lint_dir("R")'   # R (config: .lintr)
```

Hiện repo này chưa có CI.

`pytest` hiện đang có các test lỗi sẵn (known failures) trong `tests/test_read_raw.py`: các
test gọi `build_matrices()`/`validate_matrices()` theo chữ ký cũ 2 giá trị (`Dxt, Ext`),
nhưng cả hai hàm đã được mở rộng thành chữ ký 3 giá trị `Dxt, Ext, mx` mà test chưa được
cập nhật theo. Đừng vội cho rằng một lần chạy fail là do thay đổi của mình gây ra — kiểm
tra xem lỗi có phải một trong các lỗi có sẵn này trước.
