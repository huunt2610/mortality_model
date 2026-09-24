# Lệnh

```bash
# Cài đặt Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Cài đặt R
Rscript R/00_install_packages.R

# Pipeline dữ liệu (mặc định dataset wpp_vnm; --dataset hmd_jpn cho nhánh A)
python -m src.data.make_dataset

# Fit từng mô hình (RH cần lc_fit.rds làm starting values), rồi forecast, rồi backtest.
# Tham số cuối (tuỳ chọn) là dataset.
Rscript R/02a_fit_lc.R
Rscript R/02b_fit_rh.R
Rscript R/02c_fit_cbd.R
Rscript R/02d_fit_apc.R
Rscript R/02e_fit_m7.R
Rscript R/03_forecast.R
Rscript R/04_backtest.R

# Test
pytest

# Lint
ruff check .        # Python (config: ruff.toml)
Rscript -e 'lintr::lint_dir("R")'   # R (config: .lintr)
```

Hiện repo này chưa có CI. Trên máy Windows của người dùng `Rscript` không nằm trong PATH:
dùng `"/c/Program Files/R/R-4.5.0/bin/Rscript.exe"`. `jupyter nbconvert` chưa được cài.

Toàn bộ `pytest` đang pass (các test lỗi sẵn trong `tests/test_read_raw.py` cũ đã được sửa
khi đổi tên thành `tests/test_data.py`).
