# CLAUDE.md

File này cung cấp hướng dẫn cho Claude Code (claude.ai/code) khi làm việc với code trong repo này.

## Dự án

Luận văn Thạc sĩ (ĐH KHTN – ĐHQG-HCM) dự báo tử vong Việt Nam bằng các mô hình tử vong ngẫu
nhiên (Lee-Carter, Renshaw-Haberman, Cairns-Blake-Dowd), kèm ứng dụng quản trị rủi ro trong
bảo hiểm. Đây là một pipeline nghiên cứu, không phải thư viện — không có CLI, không đóng gói
để cài đặt. **Đọc `README.md` trước** — đó là tài liệu gốc của dự án, gồm bảng chú giải ký
hiệu Việt/Anh/LaTeX đầy đủ; không lặp lại ở đây.

Thiết kế nghiên cứu (ba nhánh A/B/C, tiêu chí đánh giá, phần ứng dụng, các điểm
**[CẦN KIỂM TRA]**) nằm trong `docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md` (file HTML dù
có đuôi `.md`) — cấu trúc code được tổ chức theo tài liệu này. Nhật ký nghiên cứu:
`reports/nhat_ky_nghien_cuu.md`.

## Các rule chi tiết

Hướng dẫn theo từng chủ đề nằm trong `.claude/rules/` (tự động được tải, một số chỉ tải khi
đang chỉnh sửa đường dẫn tương ứng):

- `language-split.md` — phân công Python vs R và cách chúng tương tác với nhau
- `r-pipeline.md` — thứ tự chạy `R/` fit → forecast → backtest, `R/lib/`, output theo dataset
- `config.md` — `config/params.yaml` là nguồn cấu hình duy nhất (dataset, mô hình, split)
- `data-pipeline.md` — luồng dữ liệu raw → interim → processed và quy ước
- `python-modules.md` — bản đồ các module trong `src/` và hàm của chúng
- `figures.md` — cách sinh và lưu hình cho luận văn
- `code-style.md` — quy ước comment tiếng Việt, đặt tên
- `commands-testing.md` — lệnh dev, test, lint
- `commits.md` — văn phong commit message
