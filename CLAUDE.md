# CLAUDE.md

File này cung cấp hướng dẫn cho Claude Code (claude.ai/code) khi làm việc với code trong repo này.

## Dự án

Luận văn Thạc sĩ (ĐH KHTN – ĐHQG-HCM) dự báo tử vong Việt Nam bằng các mô hình tử vong ngẫu
nhiên (Lee-Carter, Renshaw-Haberman, Cairns-Blake-Dowd), kèm ứng dụng quản trị rủi ro trong
bảo hiểm. Đây là một pipeline nghiên cứu, không phải thư viện — không có CLI, không đóng gói
để cài đặt. **Đọc `README.md` trước** — đó là tài liệu gốc của dự án, gồm bảng chú giải ký
hiệu Việt/Anh/LaTeX đầy đủ; không lặp lại ở đây.

## Các rule chi tiết

Hướng dẫn theo từng chủ đề nằm trong `.claude/rules/` (tự động được tải, một số chỉ tải khi
đang chỉnh sửa đường dẫn tương ứng):

- `language-split.md` — phân công Python vs R và cách chúng tương tác với nhau
- `r-pipeline.md` — thứ tự chạy `R/` fit → forecast → backtest và output của từng bước
- `config.md` — `config/params.yaml` là nguồn cấu hình duy nhất
- `data-pipeline.md` — luồng dữ liệu raw → interim → processed và quy ước
- `python-modules.md` — bản đồ các module trong `src/` và hàm của chúng
- `figures.md` — cách sinh và lưu hình cho luận văn
- `code-style.md` — quy ước comment tiếng Việt, đặt tên
- `commands-testing.md` — lệnh dev, lint, các test đang lỗi sẵn (known failures)
- `commits.md` — văn phong commit message
