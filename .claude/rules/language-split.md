# Phân công ngôn ngữ: Python vs R

- **Python** (`src/`, `notebooks/`): thu thập dữ liệu, EDA, đánh giá, vẽ hình.
- **R** (`R/`): fit mô hình bằng `StMoMo`, dự báo, backtest.
- Hai phía chỉ tương tác **qua filesystem** (file CSV trong `data/processed/` và
  `models/`), không chạy in-process — không có cầu nối reticulate/rpy2.
- Notebook chỉ nên gọi hàm từ `src/`/`R/`, không chứa logic dài bên trong.
- **Notebook 03–08 chỉ là placeholder/stub** — chỉ có notebook 01 (thu thập dữ liệu) và
  02 (EDA) có nội dung thật. Đừng cho rằng các notebook sau đã phản ánh phân tích đang
  hoạt động. Điều này độc lập với cách đánh số `R/01`–`04` bên dưới — các script R đã
  được cài đặt đầy đủ (xem `r-pipeline.md`).
