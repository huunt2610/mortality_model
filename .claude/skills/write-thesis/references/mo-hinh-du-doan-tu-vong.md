# Chuyên môn: mô hình dự đoán tử vong

Tài liệu này hỗ trợ viết và rà soát Chương 2 (Phương pháp) và Chương 3 (Kết quả) cho đề tài xây dựng mô hình dự đoán tử vong.

## Mục lục tài liệu này

- [1. Khung báo cáo TRIPOD+AI](#1-khung-báo-cáo-tripodai)
- [2. Định nghĩa bài toán](#2-định-nghĩa-bài-toán)
- [3. Dữ liệu và tiền xử lý](#3-dữ-liệu-và-tiền-xử-lý)
- [4. Thiết kế thẩm định](#4-thiết-kế-thẩm-định)
- [5. Chỉ số đánh giá bắt buộc báo cáo](#5-chỉ-số-đánh-giá-bắt-buộc-báo-cáo)
- [6. Bảy lỗi khiến luận văn bị vặn](#6-bảy-lỗi-khiến-luận-văn-bị-vặn)
- [7. Câu hỏi hội đồng thường đặt](#7-câu-hỏi-hội-đồng-thường-đặt)
- [8. Khung viết Chương 2 và Chương 3](#8-khung-viết-chương-2-và-chương-3)
- [9. Thuật ngữ Việt–Anh](#9-thuật-ngữ-việt-anh)

---

## 1. Khung báo cáo TRIPOD+AI

**TRIPOD** (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis) là chuẩn báo cáo quốc tế cho mô hình dự đoán lâm sàng; bản mở rộng **TRIPOD+AI (2024)** dành riêng cho mô hình học máy. **PROBAST** là công cụ đánh giá nguy cơ sai lệch của các mô hình dự đoán.

Vì sao quan trọng với luận văn: đây là bộ khung sẵn có để trả lời câu "phương pháp của em có đủ chặt không". Nếu Chương 2 được viết bám theo các hạng mục của TRIPOD, phản biện rất khó bắt lỗi thiếu sót, và học viên có sẵn lập luận bảo vệ.

Các hạng mục cần có mặt trong luận văn, dù đặt ở mục nào:

| Hạng mục | Nội dung phải nêu rõ |
|---|---|
| Nguồn dữ liệu | Cơ sở dữ liệu nào, thu thập ở đâu, khoảng thời gian, thiết kế hồi cứu hay tiến cứu |
| Quần thể | Tiêu chí nhận vào, tiêu chí loại trừ, và số bệnh nhân bị loại ở từng bước (nên có sơ đồ dòng chảy) |
| Kết cục | Định nghĩa tử vong dùng trong nghiên cứu: tử vong nội viện? 28 ngày? 30 ngày? 1 năm? Cách xác định |
| Thời điểm dự đoán | Mô hình dự đoán tại thời điểm nào — lúc nhập viện, sau 24 giờ, hay liên tục |
| Biến dự báo | Danh sách biến, đơn vị, thời điểm đo, cách xử lý biến đo nhiều lần |
| Cỡ mẫu | Căn cứ nào, số biến so với số biến cố |
| Dữ liệu thiếu | Cơ chế, tỷ lệ theo từng biến, phương pháp xử lý |
| Xây dựng mô hình | Thuật toán, siêu tham số, quy trình tinh chỉnh, hạt giống ngẫu nhiên |
| Thẩm định | Nội bộ, thời gian, hay ngoại bộ; cách chia dữ liệu |
| Hiệu năng | Cả phân biệt lẫn hiệu chuẩn |
| Diễn giải | Vì sao mô hình cho kết quả như vậy |
| Hạn chế | Trung thực, cụ thể |

## 2. Định nghĩa bài toán

Trước khi viết bất kỳ dòng nào về thuật toán, hai câu hỏi này phải được trả lời dứt khoát trong luận văn:

**Kết cục là gì, đo trong cửa sổ thời gian nào?** "Dự đoán tử vong" là chưa đủ. Tử vong nội viện, tử vong 28 ngày kể từ nhập ICU, tử vong 30 ngày sau xuất viện, và tử vong 1 năm là bốn bài toán khác nhau với tỷ lệ biến cố và ứng dụng lâm sàng khác nhau.

**Bài toán phân loại nhị phân hay phân tích sống còn?** Nếu có bệnh nhân mất theo dõi hoặc thời gian theo dõi khác nhau giữa các bệnh nhân, dùng phân loại nhị phân sẽ tạo sai lệch do dữ liệu bị kiểm duyệt (censoring). Khi đó cần mô hình sống còn: Cox proportional hazards, random survival forest, DeepSurv, hoặc phân loại có tính tới censoring. Nếu tất cả bệnh nhân đều được theo dõi đủ cửa sổ thời gian thì phân loại nhị phân là hợp lý — nhưng phải nói rõ điều đó trong luận văn.

**Tử vong do nguyên nhân cạnh tranh**: nếu kết cục quan tâm là tử vong do một nguyên nhân cụ thể, cần mô hình rủi ro cạnh tranh (Fine–Gray) thay vì Kaplan–Meier thông thường.

## 3. Dữ liệu và tiền xử lý

### Bộ dữ liệu thường dùng

MIMIC-III và MIMIC-IV, eICU Collaborative Research Database là các bộ dữ liệu ICU công khai được dùng nhiều nhất. Nếu dùng, luận văn phải nêu: phiên bản chính xác, việc đã hoàn thành khóa huấn luyện bảo vệ đối tượng nghiên cứu và được cấp quyền truy cập, và truy vấn trích xuất dữ liệu (nên đưa vào phụ lục).

Nếu dùng dữ liệu bệnh viện trong nước: phải nêu rõ đã được **Hội đồng đạo đức trong nghiên cứu y sinh học** của cơ sở chấp thuận, số quyết định, và cách bảo vệ thông tin định danh bệnh nhân. Thiếu phần này là vấn đề nghiêm trọng, không phải chi tiết hình thức.

### Dữ liệu thiếu

Trong dữ liệu lâm sàng, việc một xét nghiệm **không được chỉ định** tự nó đã mang thông tin về tình trạng bệnh nhân — nghĩa là dữ liệu thường không thiếu ngẫu nhiên. Luận văn cần:

- Báo cáo tỷ lệ thiếu theo **từng biến**, không phải một con số tổng
- Thảo luận cơ chế thiếu (MCAR / MAR / MNAR) và căn cứ để giả định
- Nêu phương pháp xử lý và **lý do chọn**: đa gán (multiple imputation, ví dụ MICE) thường tốt hơn thay bằng trung vị; với biến MNAR, thêm biến chỉ báo thiếu (missingness indicator) có thể cải thiện hiệu năng
- **Quan trọng**: quy trình gán phải được học **chỉ trên tập huấn luyện** rồi áp lên tập kiểm tra. Gán trước khi chia dữ liệu là rò rỉ dữ liệu.
- Loại bỏ bệnh nhân có dữ liệu thiếu (complete case analysis) thường tạo sai lệch chọn mẫu — nếu dùng, phải biện luận.

### Mất cân bằng lớp

Tỷ lệ tử vong thường 5–20%, nên dữ liệu mất cân bằng là đương nhiên. Ba điểm cần lưu ý:

1. **Mất cân bằng không tự động là vấn đề cần "sửa".** Nếu mục tiêu là ước lượng xác suất rủi ro đã hiệu chuẩn, việc lấy mẫu lại (SMOTE, oversampling) sẽ **phá hỏng hiệu chuẩn** — mô hình sẽ dự đoán xác suất tử vong cao hơn thực tế.
2. Nếu vẫn dùng lấy mẫu lại, chỉ áp dụng trên tập huấn luyện, và phải **hiệu chỉnh lại xác suất** (recalibration) trước khi báo cáo.
3. Thay thế tốt hơn: dùng trọng số lớp, hoặc giữ nguyên phân bố và đánh giá bằng AUPRC cùng với các chỉ số hiệu chuẩn.

### Rò rỉ dữ liệu

Đây là lỗi giết chết nhiều luận văn ở vòng phản biện. Kiểm tra:

- Biến được ghi nhận **sau** thời điểm dự đoán, hoặc sau khi bệnh nhân đã xấu đi (ví dụ liều vận mạch cao, chỉ định lọc máu cấp cứu, mã lệnh không hồi sức)
- Chuẩn hóa, chọn biến, hoặc gán dữ liệu thiếu thực hiện trên toàn bộ dữ liệu trước khi chia
- Cùng một bệnh nhân xuất hiện ở cả tập huấn luyện và tập kiểm tra (nhiều lần nhập viện) — phải chia theo **bệnh nhân**, không theo lượt nhập viện
- Biến thời gian nằm viện dùng làm biến dự báo cho tử vong nội viện

## 4. Thiết kế thẩm định

Xếp theo mức độ thuyết phục tăng dần:

| Kiểu | Mô tả | Đủ cho luận văn thạc sĩ? |
|---|---|---|
| Chia ngẫu nhiên đơn | Tách ngẫu nhiên 70/30 | Yếu — chỉ nên là bước đầu |
| Kiểm định chéo k-fold | Lặp lại nhiều lần, báo cáo trung bình ± độ lệch chuẩn | Chấp nhận được, là mức tối thiểu |
| Bootstrap có hiệu chỉnh lạc quan | Ước lượng mức độ mô hình quá khớp | Tốt, chuẩn của TRIPOD cho thẩm định nội bộ |
| Thẩm định thời gian | Huấn luyện trên dữ liệu giai đoạn trước, kiểm tra giai đoạn sau | Tốt, cho thấy mô hình chịu được thay đổi theo thời gian |
| Thẩm định ngoại bộ | Kiểm tra trên bệnh viện/quần thể khác | Mạnh nhất, là điểm cộng lớn khi bảo vệ |

Nếu chỉ làm được chia ngẫu nhiên, hãy nói thẳng đó là hạn chế trong phần Hạn chế thay vì để phản biện phát hiện.

**Tinh chỉnh siêu tham số phải nằm trong vòng lặp thẩm định** (nested cross-validation), nếu không hiệu năng báo cáo sẽ bị thổi phồng.

## 5. Chỉ số đánh giá bắt buộc báo cáo

Nhiều luận văn chỉ báo cáo AUC rồi dừng. Điều này không đủ và là điểm bị hỏi nhiều nhất.

### Khả năng phân biệt (discrimination)

- **AUROC** (C-statistic): xác suất mô hình xếp một bệnh nhân tử vong có điểm cao hơn một bệnh nhân sống. Với dữ liệu sống còn, dùng **Harrell's C-index** hoặc **time-dependent AUC**.
- **AUPRC**: quan trọng khi lớp dương hiếm, phản ánh hiệu năng thực tế tốt hơn AUROC.
- Luôn kèm **khoảng tin cậy 95%** (bootstrap).

### Hiệu chuẩn (calibration) — không được bỏ qua

Hiệu chuẩn trả lời: khi mô hình nói "nguy cơ tử vong 30%", có đúng khoảng 30% nhóm bệnh nhân đó tử vong không? Một mô hình có AUROC 0,90 vẫn có thể cho xác suất sai lệch hoàn toàn, và khi đó không dùng được để ra quyết định lâm sàng.

Báo cáo:
- **Biểu đồ hiệu chuẩn** (calibration plot / calibration belt) — nên là một hình trong Chương 3
- **Độ dốc hiệu chuẩn** (calibration slope): lý tưởng = 1. Nhỏ hơn 1 nghĩa là mô hình quá tự tin ở hai đầu.
- **Chặn hiệu chuẩn** (calibration-in-the-large): lý tưởng = 0
- **Điểm Brier**: kết hợp cả phân biệt và hiệu chuẩn
- Kiểm định Hosmer–Lemeshow đã lỗi thời và phụ thuộc cỡ mẫu — có thể nêu nhưng đừng dùng làm bằng chứng chính

### Giá trị lâm sàng

- **Phân tích đường cong quyết định** (decision curve analysis): cho thấy mô hình mang lợi ích ròng ở ngưỡng nào so với "điều trị tất cả" và "không điều trị ai"
- **Độ nhạy, độ đặc hiệu, PPV, NPV tại ngưỡng cụ thể** — ngưỡng phải được chọn theo lý do lâm sàng (ví dụ: chấp nhận bỏ sót tối đa 10%), **chọn trước** khi nhìn kết quả tập kiểm tra, và nêu rõ căn cứ

### So sánh với thang điểm sẵn có

Đây là điều làm nên giá trị của luận văn. Mô hình mới phải được so với chuẩn hiện hành trong bối cảnh tương ứng: **SOFA, APACHE II/IV, SAPS II, OASIS** cho ICU; **NEWS/MEWS** cho cảnh báo sớm nội trú; **GRACE** cho hội chứng vành cấp; **EuroSCORE II, STS** cho phẫu thuật tim; **CURB-65, PSI** cho viêm phổi; **MELD** cho bệnh gan.

So sánh phải trên **cùng tập dữ liệu, cùng bệnh nhân**, và báo cáo cả AUROC lẫn hiệu chuẩn của thang điểm chuẩn. Nếu mô hình học máy chỉ hơn 0,01 AUROC nhưng phức tạp gấp trăm lần thì đó là một phát hiện thành thật, và viết thẳng ra sẽ được đánh giá cao hơn là che giấu.

### Diễn giải mô hình

Với mô hình cây tăng cường hoặc mạng nơ-ron, cần một mục về diễn giải: **SHAP** cho đóng góp từng biến, độ quan trọng theo hoán vị, biểu đồ phụ thuộc riêng phần. Nêu rõ đây là **giải thích tương quan, không phải quan hệ nhân quả** — một mô hình có thể học rằng "được chỉ định lọc máu" dự báo tử vong mà không có nghĩa lọc máu gây tử vong.

### Công bằng và tính khái quát

Báo cáo hiệu năng phân theo nhóm tuổi, giới tính, và các phân nhóm lâm sàng quan trọng. Nếu mô hình hoạt động tốt ở nhóm này và kém ở nhóm khác, đó là phát hiện đáng viết chứ không phải điều cần giấu.

## 6. Bảy lỗi khiến luận văn bị vặn

1. **Chỉ báo cáo AUROC**, không có hiệu chuẩn.
2. **Rò rỉ dữ liệu** qua biến ghi nhận sau thời điểm dự đoán hoặc qua tiền xử lý trước khi chia dữ liệu.
3. **Chọn ngưỡng sau khi nhìn kết quả** tập kiểm tra, rồi báo cáo độ nhạy/độ đặc hiệu tại ngưỡng đó như thể nó được định trước.
4. **Không so sánh với thang điểm lâm sàng sẵn có**, khiến không trả lời được câu "mô hình này hơn cái đang dùng ở chỗ nào".
5. **Dùng SMOTE rồi báo cáo xác suất dự đoán** mà không hiệu chỉnh lại — xác suất bị thổi phồng có hệ thống.
6. **Số biến cố quá ít so với số biến dự báo**, dẫn tới quá khớp. Với hồi quy logistic, quy tắc kinh nghiệm cũ là ≥10 biến cố cho mỗi biến; các tiêu chí cỡ mẫu của Riley và cộng sự chặt chẽ hơn và nên được trích dẫn.
7. **Kết luận vượt quá bằng chứng**: viết "mô hình có thể ứng dụng trong lâm sàng" khi mới chỉ thẩm định nội bộ hồi cứu trên một trung tâm. Cách viết đúng là nêu rõ cần thẩm định ngoại bộ tiến cứu trước khi triển khai.

## 7. Câu hỏi hội đồng thường đặt

Chuẩn bị sẵn câu trả lời cho những câu này — chúng gần như chắc chắn xuất hiện:

- Định nghĩa tử vong trong nghiên cứu là gì, vì sao chọn cửa sổ thời gian đó?
- Mô hình dự đoán tại thời điểm nào, và tại thời điểm đó bác sĩ đã có sẵn thông tin gì?
- Mô hình của em hơn SOFA/APACHE ở điểm nào, và hơn có ý nghĩa lâm sàng không hay chỉ có ý nghĩa thống kê?
- Hiệu chuẩn của mô hình thế nào?
- Xử lý dữ liệu thiếu ra sao, và tại sao chọn cách đó?
- Làm sao chắc chắn không có rò rỉ dữ liệu?
- Biến nào quan trọng nhất, và điều đó có hợp lý về mặt y học không?
- Nếu triển khai ở một bệnh viện khác thì mô hình còn hoạt động không?
- Bác sĩ sẽ dùng kết quả này như thế nào trong thực tế?
- Nếu mô hình dự đoán sai, hậu quả với bệnh nhân là gì, và em đã cân nhắc rủi ro đó chưa?

## 8. Khung viết Chương 2 và Chương 3

### Chương 2. PHƯƠNG PHÁP NGHIÊN CỨU

```
2.1  Thiết kế nghiên cứu
     2.1.1  Loại hình nghiên cứu và bối cảnh
     2.1.2  Định nghĩa kết cục và thời điểm dự đoán
2.2  Dữ liệu
     2.2.1  Nguồn dữ liệu và khía cạnh đạo đức
     2.2.2  Tiêu chí nhận vào và loại trừ (kèm sơ đồ dòng chảy)
     2.2.3  Biến dự báo
     2.2.4  Xử lý dữ liệu thiếu
     2.2.5  Tiền xử lý và kỹ thuật đặc trưng
2.3  Cơ sở lý thuyết các mô hình sử dụng
     2.3.1  Mô hình cơ sở (hồi quy logistic / Cox)
     2.3.2  Các mô hình học máy
2.4  Quy trình huấn luyện và tinh chỉnh siêu tham số
2.5  Chiến lược thẩm định
2.6  Chỉ số đánh giá
     2.6.1  Khả năng phân biệt
     2.6.2  Hiệu chuẩn
     2.6.3  Giá trị lâm sàng
2.7  Phương pháp diễn giải mô hình
2.8  Công cụ và môi trường thực nghiệm
```

Nhớ quy định: mỗi nhóm tiểu mục phải có ít nhất hai thành viên. Nếu 2.1 chỉ có 2.1.1 thì phải gộp lại thành văn xuôi.

### Chương 3. KẾT QUẢ NGHIÊN CỨU VÀ PHÂN TÍCH, ĐÁNH GIÁ, THẢO LUẬN

```
3.1  Đặc điểm quần thể nghiên cứu
     (Bảng 3.1: đặc điểm nền, so sánh nhóm sống và nhóm tử vong)
3.2  Kết quả huấn luyện và lựa chọn siêu tham số
3.3  Khả năng phân biệt
     (Bảng: AUROC, AUPRC kèm KTC 95% cho từng mô hình)
     (Hình: đường cong ROC và đường cong precision-recall)
3.4  Hiệu chuẩn
     (Hình: biểu đồ hiệu chuẩn; Bảng: độ dốc, chặn, điểm Brier)
3.5  So sánh với thang điểm lâm sàng hiện hành
3.6  Phân tích đường cong quyết định
3.7  Diễn giải mô hình
     (Hình: biểu đồ SHAP)
3.8  Phân tích theo phân nhóm
3.9  Phân tích độ nhạy
3.10 Thảo luận
     3.10.1  Đối chiếu với các nghiên cứu trước
     3.10.2  Ý nghĩa lâm sàng
     3.10.3  Hạn chế của nghiên cứu
```

## 9. Thuật ngữ Việt–Anh

Dùng nhất quán trong toàn luận văn. Lần đầu xuất hiện ghi kèm tiếng Anh trong ngoặc, sau đó dùng một dạng duy nhất.

| Tiếng Việt | Tiếng Anh |
|---|---|
| khả năng phân biệt | discrimination |
| hiệu chuẩn | calibration |
| độ dốc hiệu chuẩn | calibration slope |
| thẩm định nội bộ / ngoại bộ | internal / external validation |
| thẩm định thời gian | temporal validation |
| kiểm định chéo | cross-validation |
| rò rỉ dữ liệu | data leakage |
| quá khớp | overfitting |
| mất cân bằng lớp | class imbalance |
| dữ liệu bị kiểm duyệt | censored data |
| rủi ro cạnh tranh | competing risk |
| đa gán dữ liệu thiếu | multiple imputation |
| biến dự báo | predictor |
| kết cục | outcome |
| tỷ số nguy cơ | hazard ratio |
| khoảng tin cậy | confidence interval |
| phân tích đường cong quyết định | decision curve analysis |
| lợi ích ròng | net benefit |
| giá trị tiên đoán dương / âm | positive / negative predictive value |
| điểm Brier | Brier score |
| sơ đồ dòng chảy bệnh nhân | patient flow diagram |
