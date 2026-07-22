# Mortality Forecasting Models for Vietnam

Luận văn Thạc sĩ - Lý thuyết Xác suất và Thống kê Toán học, ĐH KHTN, ĐHQG-HCM.

Xây dựng, hiệu chỉnh và so sánh các mô hình tử vong ngẫu nhiên (Lee-Carter,
Renshaw-Haberman, Cairns-Blake-Dowd) trên dữ liệu Việt Nam, và ứng dụng vào
quản trị rủi ro trong doanh nghiệp bảo hiểm nhân thọ.

## Phân công ngôn ngữ

| Việc | Công cụ |
|---|---|
| Thu thập, tiền xử lý dữ liệu, EDA, vẽ hình | Python (pandas, matplotlib) - `src/`, `notebooks/` |
| Fit mô hình LC / RH / CBD, dự báo, mô phỏng | R (**StMoMo**, demography, forecast) - `R/` |
| Đánh giá, backtest, tổng hợp kết quả | Python + R - `src/evaluation/`, `notebooks/07` |

R fit mô hình rồi export kết quả (tham số, dự báo, residuals) ra CSV trong
`data/processed/` và `models/`; Python đọc lại để phân tích và vẽ hình luận văn.

## Cấu trúc thư mục

```
vn-mortality-models/
├── config/
│   └── params.yaml          # Phạm vi tuổi, năm, split train/test - MỘT nơi duy nhất
├── data/
│   ├── raw/                 # Dữ liệu gốc tải về, KHÔNG BAO GIỜ sửa tay (không commit)
│   ├── external/            # Tài liệu tham chiếu: bảng sống GSO, metadata nguồn
│   ├── interim/             # Dữ liệu trung gian đang xử lý
│   └── processed/           # Ma trận Dxt, Ext sạch - input cho mô hình
├── notebooks/               # Đánh số theo thứ tự pipeline, mỗi notebook ≈ 1 mục luận văn
│   ├── 01_data_collection.ipynb
│   ├── 02_eda_vietnam_mortality.ipynb
│   ├── 03_smoothing_graduation.ipynb
│   ├── 04_lee_carter.ipynb
│   ├── 05_renshaw_haberman.ipynb
│   ├── 06_cbd.ipynb
│   ├── 07_model_comparison_backtest.ipynb
│   └── 08_insurance_applications.ipynb
├── R/
│   ├── 00_install_packages.R
│   ├── 01_load_data.R       # Đọc Dxt/Ext từ data/processed thành StMoMoData
│   ├── 02_fit_models.R      # Fit LC, RH, CBD bằng StMoMo
│   ├── 03_forecast.R        # Dự báo kt, gamma_c bằng ARIMA / RWD, mô phỏng
│   ├── 04_backtest.R        # Out-of-sample: refit trên tập train, dự báo tập test
│   └── utils.R
├── src/                     # Python package
│   ├── data/                # download, làm sạch, dựng ma trận Dxt/Ext
│   ├── evaluation/          # RMSE, MAPE, deviance, so sánh mô hình
│   └── visualization/       # Hình chuẩn cho luận văn (log mx, Lexis heatmap,…)
├── models/                  # Object mô hình đã fit (.rds) + tham số export (không commit file lớn)
├── reports/
│   ├── figures/             # Hình cuối cùng chèn vào luận văn (PDF/PNG 300dpi)
│   └── thesis/              # Bản thảo các chương
├── references/              # PDF papers (không commit nếu có bản quyền)
├── tests/                   # pytest cho src/
├── requirements.txt         # Môi trường Python
└── .gitignore
```

## Nguyên tắc làm việc

1. **Dữ liệu thô là bất biến.** Mọi biến đổi đều bằng code, chạy lại được từ đầu:
   `raw → interim → processed`. Không sửa tay file Excel.
2. **Tham số cấu hình tập trung** ở `config/params.yaml`. Đổi phạm vi tuổi hay
   split train/test ở một chỗ, mọi script đọc từ đó.
3. **Notebook để khám phá và trình bày; logic tái sử dụng nằm trong `src/` và `R/`.**
   Notebook chỉ gọi hàm, không chứa hàm dài.
4. **Mỗi hình trong luận văn sinh ra từ một hàm** trong `src/visualization/`,
   lưu vào `reports/figures/` - sửa được và chạy lại được đến phút chót.
5. Commit thường xuyên, message rõ ràng: `feat: fit RH model with beta0=1 constraint`.

## Nguồn dữ liệu

- **UN World Population Prospects (WPP)** - bảng sống tuổi đơn, 1950–nay, nguồn chính
  (lưu ý trong luận văn: dữ liệu đã được UN làm trơn bằng mô hình).
- **GSO Việt Nam** - bảng sống rút gọn từ Tổng điều tra 2009/2019, điều tra giữa kỳ,
  Niên giám Thống kê: dùng để đối chiếu kiểm chứng.
- **WHO Mortality Database** - dữ liệu VN thưa, chỉ tham khảo.
- Việt Nam **không có** trong Human Mortality Database.

## Khởi động nhanh

```bash
# Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# R
Rscript R/00_install_packages.R

# Chạy pipeline dữ liệu
python -m src.data.make_dataset

# Fit mô hình
Rscript R/02_fit_models.R
```
