---
paths:
  - "src/visualization/**"
  - "reports/figures/**"
---

# Hình vẽ

Mỗi hình trong luận văn được sinh ra bởi một hàm trong `src/visualization/plots.py`, kết
thúc bằng hàm dùng chung `_save(fig, name)` để lưu **PDF ở dpi=300** vào
`reports/figures/` (không phải PNG — đây là lựa chọn có chủ đích).
