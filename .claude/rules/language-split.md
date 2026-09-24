# Phân công ngôn ngữ: Python vs R

- **Python** (`src/`, `notebooks/`): thu thập dữ liệu, EDA, đánh giá, vẽ hình.
- **R** (`R/`): fit mô hình bằng `StMoMo`, dự báo, backtest.
- Hai phía chỉ tương tác **qua filesystem**: Python ghi input vào `data/processed/<dataset>/`,
  R ghi output vào `results/<dataset>/` (CSV) và `models/<dataset>/` (.rds) — không chạy
  in-process, không có cầu nối reticulate/rpy2.
- Notebook chỉ nên gọi hàm từ `src/`/`R/`, không chứa logic dài bên trong.
- **Notebook 01–04 đã có nội dung thật** (01 thu thập dữ liệu, 02 EDA, 03 làm trơn/graduation,
  04 Lee-Carter); **05–10 vẫn chỉ là placeholder/stub** (kế hoạch trong cell markdown đầu):
  05 RH+APC, 06 CBD+M7, 07 nhánh A, 08 nhánh B, 09 nhánh C, 10 ứng dụng. Đừng cho rằng notebook
  05–10 đã phản ánh phân tích đang hoạt động. Cách đánh số notebook độc lập với số của script
  `R/` (xem `r-pipeline.md`).
- **Cell output của notebook không tự đồng bộ khi upstream đổi.** Notebook 04 đọc
  `results/wpp_vnm/params_lc_*.csv`/`residuals_lc.csv` (ghi bởi `R/02a_fit_lc.R`) — nếu
  `R/02a_fit_lc.R` hoặc `config/params.yaml::fitting.years` đổi mà không Run All + lưu lại
  notebook, cell markdown "Nhận xét" sẽ trích dẫn số liệu cũ trong khi cell code phía trên đã in
  ra số liệu mới, gây mâu thuẫn ngay trong chính notebook (từng xảy ra thật, xem
  `reports/nhat_ky_nghien_cuu.md`, mục 2026-08-26). Trước khi trích số liệu từ bất kỳ notebook
  nào vào luận văn, kiểm tra thời điểm sửa gần nhất của notebook so với các file CSV nó đọc.
- **Notebook nhiều output ảnh (PNG nhúng base64) có thể vượt giới hạn token của tool Read** —
  từng gặp với `notebooks/02_eda_vietnam_mortality.ipynb` (882KB+, 14 ảnh). Khi Read báo lỗi
  "exceeds maximum allowed tokens" kể cả với `offset`/`limit`, sửa notebook bằng script Python
  đọc/ghi JSON trực tiếp (`json.load`/`json.dump`, giữ `indent=1`, `ensure_ascii=False` khớp
  định dạng gốc do Jupyter lưu), rồi validate bằng `nbformat.validate()` — không dùng tool
  NotebookEdit trong trường hợp này vì nó yêu cầu Read thành công trước.
