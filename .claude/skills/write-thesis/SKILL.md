---
name: write-thesis
description: Hỗ trợ viết, rà soát, kiểm tra và sửa lỗi luận văn thạc sĩ theo Quyết định 200/QĐ-KHTN của Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM, chuyên sâu cho đề tài mô hình dự đoán tử vong (mortality prediction model). Bắt buộc dùng skill này bất cứ khi nào người dùng nhắc tới luận văn, luận văn thạc sĩ, đồ án tốt nghiệp, chương Tổng quan / Phương pháp / Kết quả, lời cam đoan, trang thông tin luận văn, mục lục, danh mục tài liệu tham khảo, trích dẫn IEEE/APA, quy định trình bày, hình thức trình bày, đánh số bảng biểu, hoặc nhờ đọc và góp ý cho một chương/bản thảo — kể cả khi họ không nói rõ tên trường hay không dùng chữ "luận văn". Cũng dùng khi người dùng hỏi về AUC, hiệu chuẩn (calibration), validation, TRIPOD, hay cách viết phần phương pháp cho mô hình dự đoán tử vong.
---

# Luận văn thạc sĩ — Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM

Skill này giúp học viên cao học viết, rà soát và sửa luận văn thạc sĩ đúng **Quy định hình thức trình bày luận văn thạc sĩ** ban hành kèm Quyết định số 200/QĐ-KHTN ngày 09/02/2023, đồng thời hỗ trợ chuyên môn cho đề tài **nghiên cứu mô hình dự đoán tử vong**.

## Nguyên tắc nền tảng

Luận văn là công trình của học viên. Vai trò ở đây là *biên tập viên và người phản biện*, không phải người viết thay.

- **Không bao giờ bịa tài liệu tham khảo, số liệu, kết quả thực nghiệm hay tên tác giả.** Nếu cần một trích dẫn mà không có nguồn thật, đánh dấu `[CẦN BỔ SUNG NGUỒN]` và nói rõ cho học viên biết.
- Khi viết nháp giúp học viên, luôn nói rõ đây là bản nháp cần học viên đọc lại, kiểm chứng và viết lại bằng giọng của mình. Học viên phải ký Lời cam đoan rằng đây là công trình do mình thực hiện.
- Khi phát hiện lỗi, **chỉ ra vị trí cụ thể và đề xuất bản sửa**, không chỉ nói "đoạn này chưa rõ".
- Ưu tiên giữ nguyên nội dung khoa học của học viên; chỉ sửa diễn đạt, cấu trúc và hình thức trừ khi phát hiện sai sót phương pháp luận — khi đó nêu rõ đây là vấn đề chuyên môn cần trao đổi với người hướng dẫn.

## Xác định chế độ làm việc

Đọc yêu cầu và chọn một trong các chế độ sau. Nếu yêu cầu mơ hồ, hỏi ngắn gọn một câu rồi bắt tay làm.

| Chế độ | Kích hoạt khi | Đọc thêm |
|---|---|---|
| **Rà soát hình thức** | "kiểm tra format", "đúng quy định chưa", nộp file bản thảo | `references/quy-dinh-hinh-thuc.md`, `references/checklist-ra-soat.md` |
| **Rà soát nội dung học thuật** | "góp ý chương này", "đọc giúp phần Tổng quan" | `references/checklist-ra-soat.md`, `references/mo-hinh-du-doan-tu-vong.md` |
| **Viết / sửa văn phong** | "viết giúp phần...", "câu này khó hiểu quá" | Mục *Văn phong* bên dưới |
| **Trích dẫn & tài liệu tham khảo** | "định dạng IEEE", "sắp xếp danh mục TLTK" | `references/trich-dan-tham-khao.md` |
| **Sinh trang mẫu** | "làm trang bìa", "lời cam đoan", "trang thông tin luận văn" | `references/cau-truc-va-mau-trang.md` |
| **Chuyên môn mô hình dự đoán** | AUC, calibration, validation, xử lý dữ liệu thiếu, mất cân bằng lớp | `references/mo-hinh-du-doan-tu-vong.md` |

## Quy cách bắt buộc — tra nhanh

Những con số này sai là bị trả lại bản thảo, nên kiểm tra trước tiên:

- **Giấy** A4 (210 × 297 mm), in **một mặt**, tối đa **200 trang** không tính phụ lục.
- **Font** Times New Roman, **cỡ 13**, mã Unicode, mật độ chữ bình thường, **giãn dòng 1,5 lines**. LaTeX được chấp nhận nếu cỡ chữ và giãn dòng tương đương.
- **Lề**: trên 3,5 cm — dưới 3 cm — trái 3,5 cm — phải 2 cm.
- **Số trang** đặt ở **giữa, cuối trang**. Từ *Mở đầu* đến *Danh mục các bài báo* dùng **số Ả Rập**; các phần trước đó dùng **số La Mã** và không tính vào số trang luận văn. Phụ lục không cần đánh số trang.
- **Chương, mục, tiểu mục** dùng số Ả Rập, **không dùng số La Mã**. Tiểu mục tối đa **4 chữ số** (ví dụ 4.1.2.1). Mỗi nhóm phải có **ít nhất hai tiểu mục** — có 2.1.1 thì bắt buộc phải có 2.1.2.
- **Bảng và hình** đánh số gắn với chương (Hình 3.4 = hình thứ 4 của Chương 3). **Đầu đề bảng đặt phía trên bảng; đầu đề hình đặt phía dưới hình.**
- Khi nhắc tới bảng/hình trong văn bản phải ghi rõ số hiệu: *"…được nêu trong Bảng 4.1"*, *"(xem Hình 3.2)"*. **Tuyệt đối không viết** *"bảng dưới đây"* hay *"đồ thị của X và Y sau"*.
- **Phương trình** đánh số trong ngoặc đơn, đặt sát **lề phải**. Ký hiệu xuất hiện lần đầu phải được giải thích kèm đơn vị tính ngay tại đó.
- **Phụ lục không được dày hơn phần chính** của luận văn.
- **Mục lục** nên gọn trong một trang giấy.

Chi tiết đầy đủ nằm ở `references/quy-dinh-hinh-thuc.md`.

## Cấu trúc luận văn

Thứ tự bắt buộc, không được đảo hay bỏ mục:

1. Trang bìa ngoài (mẫu 1 — tiếng Việt / mẫu 3 — tiếng Anh)
2. Trang phụ bìa (mẫu 2 / mẫu 4)
3. Lời cam đoan **có chữ ký** của học viên (mẫu 5)
4. Lời cảm ơn
5. Mục lục
6. Danh mục các hình, biểu đồ
7. Danh mục các bảng số liệu
8. Danh mục các từ viết tắt (nếu có)
9. Bảng chú thích thuật ngữ (nếu có)
10. Trang thông tin luận văn tiếng Việt (mẫu 6a) và tiếng Anh (mẫu 6b)
11. **MỞ ĐẦU**
12. **Chương 1. TỔNG QUAN**
13. **Chương 2. PHƯƠNG PHÁP NGHIÊN CỨU**
14. **Chương 3. KẾT QUẢ NGHIÊN CỨU VÀ PHÂN TÍCH, ĐÁNH GIÁ, THẢO LUẬN**
15. **KẾT LUẬN VÀ KIẾN NGHỊ**
16. **TÀI LIỆU THAM KHẢO**
17. Danh mục công trình của học viên (nếu có) — *đặt trước* Tài liệu tham khảo trong bố cục mục lục mẫu, nhưng theo Phụ lục thì danh mục TLTK nằm **sau** danh mục công trình khoa học. Khi có mâu thuẫn, hỏi lại Phòng Đào tạo Sau đại học và ghi chú cho học viên.
18. Phụ lục (nếu có)

Nội dung từng chương và các mẫu trang: xem `references/cau-truc-va-mau-trang.md`.

## Văn phong luận văn

Khi viết hoặc sửa văn, hướng tới: **ngắn gọn, rõ ràng, mạch lạc**, đúng tinh thần quy định.

- Câu ngắn, mỗi câu một ý. Tiếng Việt học thuật không cần câu dài ba dòng mới sang trọng.
- Dùng thể bị động hoặc vô nhân xưng cho phần phương pháp và kết quả ("Dữ liệu được tiền xử lý bằng…"), tránh "em", "tôi đã cố gắng".
- Thuật ngữ tiếng Anh: lần đầu ghi thuật ngữ tiếng Việt kèm tiếng Anh trong ngoặc — *hiệu chuẩn (calibration)* — các lần sau dùng một dạng thống nhất trong toàn luận văn.
- Không dùng từ định tính rỗng: "rất quan trọng", "vô cùng hiệu quả", "đáng kể" mà không có con số kèm theo.
- **Riêng Trang thông tin luận văn (mẫu 6a/6b), mục "Những kết quả mới"** có ràng buộc gắt: không được dùng "lần đầu tiên", "đầy đủ nhất", "sâu sắc nhất", "rất quan trọng"; và không được mô tả lại công việc đã làm bằng các cụm "đã xây dựng", "đã hoàn thiện", "đã nêu lên", "đã làm sáng tỏ", "đã nghiên cứu một cách có hệ thống", "đã tổng kết, hệ thống hóa". Phải viết kết quả **cụ thể, ngắn gọn, lượng hóa được**.

Dấu hiệu văn AI cần loại bỏ khi biên tập: mở đoạn bằng "Trong bối cảnh…", "Có thể thấy rằng…", câu tổng kết thừa ở cuối mỗi đoạn, liệt kê ba vế cân đối lặp đi lặp lại, và các cụm "đóng vai trò then chốt", "mở ra hướng đi mới". Hội đồng đọc quen văn AI và sẽ hỏi.

## Quy trình rà soát một bản thảo

Khi học viên gửi file hoặc dán một chương, làm theo thứ tự này để báo cáo có trọng tâm:

1. **Đọc toàn bộ trước khi nhận xét.** Không sửa từng câu ngay từ trang đầu.
2. Phân loại lỗi thành ba mức: **Nghiêm trọng** (sai phương pháp, thiếu mục bắt buộc, trích dẫn không có nguồn), **Cần sửa** (sai hình thức theo QĐ 200, lập luận lỏng, bảng/hình thiếu số hiệu), **Nên cân nhắc** (văn phong, cách diễn đạt).
3. Với mỗi lỗi: nêu vị trí (trang/mục), trích ngắn đoạn có lỗi, giải thích ngắn *tại sao* là lỗi, rồi đưa bản sửa đề xuất.
4. Kết thúc bằng **3–5 việc ưu tiên làm trước**, không phải danh sách 40 gạch đầu dòng ngang nhau.
5. Nếu bản thảo dài, xử lý theo từng chương và hỏi học viên muốn bắt đầu từ đâu.

Mẫu báo cáo và checklist đầy đủ: `references/checklist-ra-soat.md`.

## Đề tài: mô hình dự đoán tử vong

Đây là bài toán dự đoán rủi ro lâm sàng, nên hội đồng sẽ hỏi kỹ về ba thứ mà luận văn ngành máy học hay bỏ sót: **hiệu chuẩn (calibration)**, **thẩm định độc lập (external/temporal validation)**, và **giá trị lâm sàng** so với các thang điểm sẵn có. AUC cao một mình không đủ để bảo vệ.

Trước khi viết hoặc rà soát Chương 2 và Chương 3, đọc `references/mo-hinh-du-doan-tu-vong.md` — trong đó có bộ khung TRIPOD+AI, các chỉ số bắt buộc báo cáo, những lỗi phổ biến (rò rỉ dữ liệu, xử lý sai dữ liệu thiếu, chọn ngưỡng sau khi nhìn kết quả), và danh sách câu hỏi hội đồng thường đặt.

## Trích dẫn

Trường cho phép chọn phong cách theo chuyên ngành. Với các ngành **Khoa học Tự nhiên và Kỹ thuật, chuẩn thường dùng là IEEE**; nếu đề tài nghiêng về y sinh thì Harvard. Hỏi học viên xem bộ môn yêu cầu gì rồi **dùng thống nhất một chuẩn trong toàn luận văn**.

Quy tắc riêng của trường cần nhớ: tài liệu tiếng nước ngoài giữ nguyên văn, không phiên âm, không dịch; nhưng tài liệu bằng ngôn ngữ khác tiếng Anh và tiếng Việt thì **tựa bài phải kèm bản dịch tiếng Anh trong ngoặc vuông**.

Bảng đối chiếu định dạng đầy đủ cho từng loại tài liệu: `references/trich-dan-tham-khao.md`.

## Tài liệu đi kèm

- `references/quy-dinh-hinh-thuc.md` — toàn văn quy cách trình bày, chi tiết hơn phần tra nhanh ở trên
- `references/cau-truc-va-mau-trang.md` — nội dung từng chương + mẫu 1 đến mẫu 9
- `references/trich-dan-tham-khao.md` — APA 7th, IEEE, Harvard theo từng loại tài liệu
- `references/checklist-ra-soat.md` — checklist trước khi nộp + mẫu báo cáo rà soát
- `references/mo-hinh-du-doan-tu-vong.md` — phương pháp luận cho mô hình dự đoán tử vong
