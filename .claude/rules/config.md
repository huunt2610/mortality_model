---
paths:
  - "config/**"
  - "src/**"
  - "R/**"
  - "notebooks/**"
---

# Cấu hình

`config/params.yaml` là nguồn duy nhất cho dataset, phạm vi tuổi, phạm vi năm, danh sách mô
hình và split train/test — đọc từ đây ở cả Python (`src/config.py::load_params()`) lẫn R
(`R/lib/load_data.R::load_config()`), không hardcode ở nơi khác.

- `datasets:` — mỗi dataset gắn một nhánh thực nghiệm (A: `hmd_*`, B: `wpp_vnm`, C: `gso_vnm`)
  và một thư mục riêng trong `data/processed/`, `models/`, `results/`. `default_dataset` dùng khi
  script không nhận tham số.
- `models:` — mỗi mô hình trỏ tới một khoá trong `ages:` và khai báo `link`. LC/RH/APC dùng
  0–90, CBD/M7 chỉ dùng 55–90 (tập trung tuổi già).
- `fitting.years` = 1990–2008 theo thiết kế nhánh B (bản đồ tri thức Mục 12.2: khớp WPP
  1990–2008, dự báo 2009–2024, kiểm chứng tại 2009/2014/2019/2024). Trước 2026-09-24 là
  1980–2010 — số liệu trong nhật ký nghiên cứu trước ngày đó thuộc cửa sổ cũ. Đổi cửa sổ phải
  refit R, chạy lại notebook 04 và cập nhật số liệu ở `reports/thesis/`.
- Các năm COVID (2020–2022) được đánh dấu qua `backtest.exclude_covid_years`; backtest cần báo
  cáo cả có lẫn không có các năm này.
- `application:` — các giá trị pháp lý (`interest_rate`, ngưỡng CSO 1980) đánh dấu
  `[CẦN KIỂM TRA]`, không tự điền.
