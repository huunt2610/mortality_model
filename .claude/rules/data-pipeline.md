---
paths:
  - "data/**"
  - "src/data/**"
---

# Pipeline dữ liệu

- Luồng đi nghiêm ngặt **raw → interim → processed**, hoàn toàn bằng code, chạy lại được
  từ đầu. Dữ liệu raw là bất biến — không bao giờ sửa tay file Excel gốc.
- `data/raw/` và `data/interim/` bị gitignore (chỉ track `.gitkeep`). File Excel UN WPP
  phải tải thủ công từ https://population.un.org/wpp/ vào `data/raw/` với đúng tên file
  như trong `data/external/SOURCES.md` / `src/data/make_dataset.py::WPP_FILES` trước khi
  `python -m src.data.make_dataset` chạy được — nếu thiếu sẽ raise `FileNotFoundError`
  kèm hướng dẫn.
- Ma trận trong `data/processed/` đặt tên `Dxt_{sex}.csv`, `Ext_{sex}.csv`, `mx_{sex}.csv`
  với sex ∈ {male, female, total}, index theo tuổi (hàng) × năm (cột), tăng dần và liên
  tục — được kiểm tra bởi `src/data/validate.py::validate_matrices`.
- File UN WPP không tách riêng số ca tử vong và exposure: `Dxt = mx * Ext` là một giả
  định, và `Ext` được xấp xỉ từ `L(x,n)`, không phải số liệu quan sát trực tiếp.
- Quy ước loại exposure (nguồn lỗi phổ biến khi fit mô hình): dùng `E^c` (central
  exposure) đi với `m_{x,t}` + link log, hoặc `E^0` (initial exposure) đi với `q_{x,t}` +
  link logit. Trong StMoMo đây là tham số `type = "central"` vs `"initial"`.
- `models/*.rds`/`*.pkl` và `references/*.pdf` cũng bị gitignore — đừng kỳ vọng chúng tồn
  tại sau khi clone mới.
