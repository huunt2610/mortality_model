---
paths:
  - "config/**"
  - "src/**"
  - "R/**"
  - "notebooks/**"
---

# Cấu hình

`config/params.yaml` là nguồn duy nhất cho phạm vi tuổi, phạm vi năm, và split train/test —
đọc từ đây ở cả Python (`src/config.py::load_params()`) lẫn R (`yaml::read_yaml(...)`),
không hardcode ở nơi khác. Phạm vi tuổi khác nhau theo mô hình: LC/RH dùng 0–90, CBD chỉ
dùng 55–90 (tập trung tuổi già). Các năm COVID (2020–2022) được đánh dấu qua
`exclude_covid_years`; backtest cần báo cáo cả có lẫn không có các năm này.
