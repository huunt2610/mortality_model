> **Ghi chú của trợ lý biên tập (xoá trước khi nộp):** Đây là bản nháp dựa trên kết quả thực nghiệm
> trong `notebooks/02_eda_vietnam_mortality.ipynb` và `notebooks/04_lee_carter.ipynb`. Học viên cần
> đọc lại, kiểm chứng từng số liệu với kết quả chạy thực tế, và viết lại bằng giọng văn của mình
> trước khi đưa vào bản thảo chính thức — Lời cam đoan yêu cầu luận văn là công trình do học viên
> thực hiện.
>
> **Đã đối chiếu (2026-08-26):** notebook 04 đã được chạy lại và lưu, số liệu trong mục 3.2 dưới đây
> khớp chính xác với output hiện tại của notebook (kt 1980–2010, cohort residual −0,593→0,527 tại
> cohort 1980/1910, ADF diff(kt) p≈0,09). Cả 3 hình liên quan (`lc_params_total.pdf`,
> `residuals_lc.pdf`, `lc_cohort_mean_residual.pdf`) đã được sinh lại, không còn cảnh báo lỗi thời.
>
> Số hiệu bảng/hình/phương trình dưới đây đánh theo Chương 3, bắt đầu từ 3.1 — cần điều chỉnh lại cho
> khớp với vị trí thực tế trong bản thảo hoàn chỉnh (ví dụ nếu Chương 3 có mục 3.0 nào đó trước).

## 3.1 Đặc điểm dữ liệu tử vong Việt Nam giai đoạn 1955–2023

Ma trận tỷ suất tử vong đặc trưng theo tuổi $m(x,t)$ được dựng từ nguồn UN WPP 2024 cho tuổi
$x \in [0, 100]$ và năm $t \in [1955, 2023]$ (101 tuổi × 69 năm), tách riêng theo nam, nữ và tổng hai
giới. Trước khi ước lượng các mô hình tử vong ngẫu nhiên ở mục 3.2, dữ liệu được khảo sát để xác định
xu hướng chung, khác biệt theo giới tính, và các bất thường cần lưu ý khi diễn giải kết quả mô hình.

### 3.1.1 Xu hướng tử vong theo tuổi và theo thời gian

Đường cong $\log m(x,t)$ theo tuổi giữ nguyên hình dạng đặc trưng "chữ V" (checkmark) qua mọi năm mốc
khảo sát (1960, 1980, 2000, 2020): tử vong cao ở tuổi sơ sinh, giảm mạnh xuống mức thấp nhất ở tuổi
thiếu niên (khoảng 11–12 tuổi), sau đó tăng gần tuyến tính theo tuổi trưởng thành — phù hợp với dạng
Gompertz được ghi nhận rộng rãi trong tài liệu về tử vong người lớn [CẦN BỔ SUNG NGUỒN].

Toàn bộ đường cong dịch chuyển xuống theo thời gian: trung vị $\log m(x,t)$ tính trên toàn dải tuổi
giảm từ $-4,44$ (1960) xuống $-5,34$ (2020), tương ứng tỷ suất tử vong trung vị giảm khoảng 2,4 lần.
Mức cải thiện lớn nhất thuộc về tử vong sơ sinh: $m(0,t)$ giảm từ $0,0707$ (1960) xuống $0,0158$
(2020), giảm $77,6\%$.

Hình 3.1 minh hoạ đường cong $\log m(x,t)$ theo tuổi tại các năm mốc (nguồn hình:
`reports/figures/log_mx_total_by_age.pdf`). Bảng 3.1 trình bày cùng số liệu tại một số tuổi và năm mốc
đại diện.

**Bảng 3.1.** Logarit tỷ suất tử vong $\log m(x,t)$ theo tuổi tại các năm mốc, Việt Nam (nguồn: UN WPP 2024, tính toán của tác giả)

| Tuổi | 1960 | 1980 | 2000 | 2020 |
|---|---|---|---|---|
| 0 | −2,649 | −3,007 | −3,786 | −4,145 |
| 1 | −4,294 | −4,741 | −5,865 | −6,420 |
| 10 | −5,902 | −6,588 | −7,302 | −7,385 |
| 30 | −5,274 | −5,764 | −6,228 | −6,418 |
| 60 | −3,940 | −4,249 | −4,607 | −4,766 |
| 90 | −1,271 | −1,394 | −1,628 | −1,848 |

### 3.1.2 Tốc độ cải thiện tử vong theo tuổi và điểm gãy cấu trúc

Mức cải thiện tử vong giai đoạn 1960–2020 không đồng đều theo tuổi: khoảng $78$–$88\%$ ở nhóm tuổi
0–10, giảm còn $58$–$68\%$ ở nhóm 30–60 tuổi, và chỉ còn $43,9\%$ ở tuổi 90, $33,8\%$ ở tuổi 100. Nói
cách khác, dư địa cải thiện tử vong ở nhóm tuổi già còn lớn hơn đáng kể so với nhóm tuổi trẻ — một
điểm cần lưu ý khi đánh giá phạm vi tuổi 55–90 dùng để ước lượng mô hình Cairns–Blake–Dowd (CBD) ở
mục sau. Ngược lại, độ dốc log-tuyến tính của $m(x,t)$ trong khoảng tuổi già 60–90 khá ổn định qua
thời gian (dao động hẹp $9,0$–$10,5\%$ mỗi năm tuổi), cho thấy cải thiện tử vong chủ yếu là một sự
dịch chuyển mức (level shift) hơn là thay đổi hình dạng theo tuổi — phù hợp với giả định hệ số $b_x$
bất biến theo thời gian của mô hình Lee–Carter.

Hình 3.2 minh hoạ mức cải thiện tử vong theo tuổi giai đoạn 1960–2020 (nguồn hình:
`reports/figures/mortality_improvement_by_age.pdf`).

Để kiểm định giả định bước ngẫu nhiên có drift (random walk with drift — RWD) cho thành phần xu hướng
chung theo thời gian trước khi ước lượng mô hình chính thức, chỉ số

$$\bar m_t = \frac{1}{|X|}\sum_{x \in X} \log m(x,t), \qquad X = \{0, 1, \dots, 90\} \tag{3.1}$$

được tính trên toàn bộ giai đoạn 1955–2023 (68 sai phân), khớp phạm vi tuổi dùng để fit LC/RH
(`ages.lc_rh` trong `config/params.yaml`) nhưng không cần fit mô hình. Kiểm định Dickey–Fuller mở
rộng (Augmented Dickey-Fuller — ADF) không bác bỏ giả thuyết có nghiệm đơn vị (unit root) trên chuỗi
gốc ($p \approx 0,78$), trong khi bác bỏ mạnh giả thuyết đó trên chuỗi sai phân bậc một ($p \approx
0,0002$) — phù hợp với cấu trúc RWD.

Hình 3.3 trình bày biến động của $\bar m_t$ qua thời gian (nguồn hình: `reports/figures/mbar_t_trend.pdf`).

Dò điểm gãy cấu trúc (structural break) bằng phương pháp chia đôi chuỗi tại từng năm ứng viên, hồi
quy tuyến tính riêng hai đoạn và chọn điểm gãy có tổng sai số bình phương nhỏ nhất, sau đó kiểm định ý
nghĩa bằng kiểm định Chow, cho kết quả điểm gãy tại năm **1974** ($F \approx 123,1$, $p < 10^{-16}$):
độ dốc đổi dấu hoàn toàn, từ $+0,0103$/năm (1955–1974, tử vong xấu đi) sang $-0,0143$/năm (1975 trở
đi, tử vong cải thiện). Mốc 1974 trùng gần như chính xác với thời điểm kết thúc Chiến tranh Việt Nam
(1975), và là bằng chứng định lượng độc lập — không cần fit mô hình — cho quyết định loại giai đoạn
1955–1979 khỏi cửa sổ ước lượng tham số chính thức (`fitting.years.start = 1980`, xem mục 3.2).

### 3.1.3 Khác biệt tử vong theo giới tính

Tử vong nam cao hơn nữ ở hầu hết các độ tuổi trong toàn bộ giai đoạn quan sát. Tỷ số $m(x,t)$
nam/nữ trung bình theo tuổi tăng dần theo thời gian: từ $1,36$ lần (1960) lên $2,51$ lần (2020).
"Vồng tử vong" (accident hump) đặc trưng ở nam thanh niên xuất hiện rõ quanh tuổi 20, đạt tỷ số cao
nhất $3,71$ lần vào năm 2020 — mô thức được ghi nhận phổ biến ở nhiều quốc gia, liên quan đến tử vong
ngoại sinh (tai nạn giao thông, bạo lực) [CẦN BỔ SUNG NGUỒN].

Hình 3.4 minh hoạ đường $\log m(x,t)$ nam/nữ tại các năm mốc (nguồn hình:
`reports/figures/mx_sex_comparison.pdf`).

Định lượng cường độ vồng (phần vượt của đỉnh $\log m(x,t)$ trong khoảng tuổi 10–30 so với đường nền
nối hai điểm neo tuổi 10 và 40) qua từng năm cho thấy hai giai đoạn biến động tách biệt ở nam giới,
không xuất hiện ở nữ:

- **Giai đoạn chiến tranh (1965–1974):** cường độ vồng tăng vọt và duy trì mức cao (từ $0,46$ đến
  đỉnh $0,71$ năm 1972), rồi giảm đột ngột xuống $0,14$ ngay năm 1975.
- **Thời bình (1980–2019):** cường độ vồng tăng chậm và đều, từ $0,08$ (1980) lên $0,19$ (2019), độ
  dốc tuyến tính xấp xỉ $+0,0036$/năm — ngược chiều hoàn toàn với xu hướng tử vong chung đang giảm
  mạnh cùng giai đoạn, phù hợp với xu hướng mô tô hoá giao thông tăng nhanh sau Đổi Mới.
- **Giai đoạn COVID-19 (2020–2021):** cường độ vồng vọt lên $0,50$/$0,47$ rồi quay lại đúng mức nền
  ($0,19$) vào 2022–2023, xác nhận đây là nhiễu tạm thời chứ không phải thay đổi cấu trúc lâu dài —
  củng cố quyết định loại các năm 2020–2022 khỏi phần đánh giá chính (`exclude_covid_years` trong
  `config/params.yaml`).

Hình 3.5 trình bày cường độ vồng theo năm, phân theo giới tính (nguồn hình:
`reports/figures/accident_hump_excess_trend.pdf`).

Cường độ vồng ở nam và xu hướng tử vong chung $\bar m_t$ di chuyển không đồng bộ (tương quan
$\approx 0,41$). Đây là một giới hạn cấu trúc chung của cả ba mô hình dùng trong luận văn: Lee-Carter
với một cặp $(a_x, b_x, k_t)$ duy nhất không thể đồng thời khớp cả xu hướng tử vong chung lẫn chuyển
động riêng của dải tuổi vồng; Renshaw–Haberman chỉ bổ sung hiệu ứng thế hệ $\gamma_c$ chứ không thêm
một cặp $(b_x, k_t)$ thứ hai nên cũng không khắc phục vấn đề này; còn CBD không fit dải tuổi 15–30 nên
không liên quan. Giới hạn này cần được nêu rõ khi so sánh ba mô hình ở Chương 3 (mục so sánh/backtest),
không phải một câu hỏi được kỳ vọng RH hay CBD sẽ giải quyết.

### 3.1.4 Bất thường tại nhóm tuổi nhỏ: nghi vấn artifact ước lượng

Tuổi 1 là tuổi **duy nhất** trong toàn bộ 101 tuổi từng ghi nhận tỷ số $m(x,t)$ nam/nữ nhỏ hơn 1
(47/69 năm, liên tục từ khoảng 1980 trở đi) — một mô thức cô lập tại đúng một điểm tuổi, không phải
nhiễu rải rác. Kiểm tra độ mượt của $\log m(x,t)$ quanh tuổi 0–1–2 (sai phân bậc một) cho thấy từ
khoảng 1990–2010, đường của nam giới bị "phẳng" bất thường tại tuổi 1–3 trong khi đường của nữ vẫn
giảm mượt — một dấu hiệu điển hình của việc ghép nối (splicing) hai mô hình ước lượng riêng biệt
không mượt tại ranh giới tuổi 0/1, thường gặp khi cơ quan thống kê quốc tế ước lượng tử vong trẻ em
qua hai cấu phần tách biệt ($_1q_0$ và $_4q_1$) từ khảo sát hộ gia đình thay vì số liệu đăng ký hộ
tịch đầy đủ.

Hình 3.6 minh hoạ tỷ số $m(x,t)$ nam/nữ tuổi 0–15 giữa ba quốc gia (nguồn hình:
`reports/figures/ratio_vn_jpn_kor_comparison.pdf`).

Đối chiếu với Nhật Bản và Hàn Quốc — cùng nguồn UN WPP, cùng phương pháp luận — không cho thấy mô
thức cô lập tương tự: Nhật Bản có 17 tuổi khác nhau từng có tỷ số dưới 1 (rải rác, tuổi 1 chỉ chiếm
4/69 năm), Hàn Quốc có 26 tuổi (tuổi 1 chiếm 29/69 năm nhưng không cô lập). Bảng 3.2 tóm tắt kết quả
đối chiếu.

**Bảng 3.2.** Đối chiếu mô thức tỷ số $m(x,t)$ nam/nữ nhỏ hơn 1 giữa ba quốc gia (nguồn: UN WPP 2024, tính toán của tác giả)

| Quốc gia | Số tuổi (trên 101) từng có tỷ số < 1 | Tuổi 1: số năm có tỷ số < 1 | Tuổi 1 có cô lập? |
|---|---|---|---|
| Việt Nam | 1 | 47/69 | Có |
| Nhật Bản | 17 | 4/69 | Không |
| Hàn Quốc | 26 | 29/69 | Không |

Hai hệ thống đăng ký hộ tịch của Nhật Bản và Hàn Quốc đã đầy đủ từ nhiều thập kỷ nên số liệu UN WPP
cho hai nước gần như là số đếm thực tế, ít cần mô hình hoá; điều kiện thuận lợi cho artifact ghép nối
xuất hiện — thiếu số liệu đăng ký đầy đủ, phải ước lượng gián tiếp từ khảo sát — đúng với bối cảnh
Việt Nam trong phần lớn giai đoạn quan sát. Kết quả này, cùng với hai kiểm định độc lập bổ sung bằng
phương pháp graduation và gộp nhóm tuổi khi đối chiếu với bảng sống Tổng điều tra dân số 2019 của
Tổng cục Thống kê [CẦN BỔ SUNG NGUỒN — báo cáo TĐT Dân số 2019], cùng cho một kết luận nhất quán: bất
thường tại nhóm tuổi 1–4 trong UN WPP nhiều khả năng là sản phẩm phụ của phương pháp ước lượng, không
phải một đặc điểm dịch tễ có thật của Việt Nam. Đây là một hạn chế dữ liệu cần nêu rõ khi diễn giải
tham số mô hình liên quan đến nhóm tuổi này ở mục 3.2.

### 3.1.5 Già hoá dân số nhìn từ góc độ tuổi thọ kỳ vọng

Việt Nam đang trải qua quá trình già hoá dân số (population ageing) nhanh — hệ quả của cả tỷ suất
sinh giảm lẫn tỷ suất tử vong giảm liên tục qua các thập kỷ [CẦN BỔ SUNG NGUỒN — số liệu tỷ suất sinh,
tỷ trọng dân số cao tuổi và dự báo dân số của Tổng cục Thống kê/UN Population Division]. Bộ dữ liệu
$m(x,t)$ dùng trong luận văn chỉ ghi nhận phía tử vong của quá trình này — không có thông tin về tỷ
suất sinh hay cấu trúc tuổi thực tế của dân số — nên phần này chỉ trình bày bằng chứng về **tuổi thọ
kỳ vọng tăng**, thành phần trực tiếp liên quan đến tử vong và có ý nghĩa nhất về mặt actuarial (rủi ro
trường thọ — longevity risk) cho phần ứng dụng bảo hiểm ở chương sau.

Tuổi thọ kỳ vọng khi sinh $e_0$ và tuổi thọ kỳ vọng ở tuổi 60 $e_{60}$ được dựng từ bảng sống suy ra
theo $m(x,t)$ (xem `src/data/life_table.py`, giả định lực chết không đổi trong mỗi khoảng tuổi). Bảng
3.3 trình bày kết quả tại các năm mốc. Hình 3.7 và Hình 3.8 minh hoạ xu hướng theo thời gian, phân theo
giới tính (nguồn hình: `reports/figures/e0_trend_by_sex.pdf`, `reports/figures/e60_trend_by_sex.pdf`).

**Bảng 3.3.** Tuổi thọ kỳ vọng khi sinh ($e_0$) và ở tuổi 60 ($e_{60}$) theo giới tính, Việt Nam (nguồn: UN WPP 2024, tính toán của tác giả)

| Năm | $e_0$ Nam | $e_0$ Nữ | $e_0$ Chung | $e_{60}$ Nam | $e_{60}$ Nữ | $e_{60}$ Chung |
|---|---|---|---|---|---|---|
| 1960 | 55,00 | 61,15 | 57,99 | 15,48 | 17,29 | 16,44 |
| 1980 | 60,88 | 69,91 | 65,31 | 16,58 | 19,62 | 18,19 |
| 2000 | 68,20 | 77,28 | 72,74 | 18,05 | 22,65 | 20,53 |
| 2020 | 70,37 | 80,32 | 75,39 | 18,93 | 24,57 | 22,07 |
| 2023 | 69,88 | 79,27 | 74,59 | 18,34 | 23,65 | 21,27 |

Tuổi thọ kỳ vọng khi sinh (chung hai giới) tăng $17,4$ năm trong 60 năm, từ $57,99$ (1960) lên $75,39$
(2020) — phần lớn mức tăng này đến từ cải thiện tử vong ở tuổi nhỏ đã trình bày ở mục 3.1.1–3.1.2.
Điều đáng chú ý hơn cho quá trình già hoá dân số là tuổi thọ kỳ vọng **ở tuổi 60** cũng tăng đáng kể
và liên tục, từ $16,44$ (1960) lên $22,07$ năm (2020, tăng $5,6$ năm) — nghĩa là người đã sống đến 60
tuổi ngày nay được kỳ vọng sống thêm nhiều năm hơn hẳn so với thế hệ trước, chứ không phải toàn bộ mức
tăng tuổi thọ chỉ đến từ giảm tử vong sơ sinh/trẻ em. Đây chính là cấu phần tử vong của già hoá dân số:
dân số không chỉ sống lâu hơn nhờ ít trẻ em tử vong sớm, mà người cao tuổi cũng tử vong muộn hơn — làm
tăng tỷ trọng và thời gian sống của nhóm dân số cao tuổi, và trực tiếp làm tăng rủi ro trường thọ mà
các sản phẩm hưu trí/niên kim (annuity) phải định phí dựa trên dự báo tỷ suất tử vong tương lai (xem
notebook 08, phần ứng dụng bảo hiểm).

Khoảng cách tuổi thọ nam/nữ cũng doãng ra: chênh lệch $e_0$ tăng từ $6,15$ năm (1960) lên $9,95$ năm
(2020); chênh lệch $e_{60}$ đạt $5,64$ năm (2020) — nhất quán với tỷ số $m(x,t)$ nam/nữ ngày càng cao ở
mục 3.1.3. Cả $e_0$ và $e_{60}$ đều **giảm nhẹ giai đoạn 2020–2023** (lần lượt từ $75,39$ xuống $74,59$
và từ $22,07$ xuống $21,27$) — nhất quán với đột biến tử vong do COVID-19 đã ghi nhận ở mục 3.1.3, và
là một lý do bổ sung cho quyết định loại các năm 2020–2022 khỏi cửa sổ ước lượng tham số chính thức.

---

## 3.2 Kết quả ước lượng mô hình Lee-Carter

Mô hình Lee-Carter (Lee & Carter, 1992 [CẦN BỔ SUNG NGUỒN]) được ước lượng trên chuỗi tổng hai giới
(`series = "total"`), với cấu trúc

$$\log m(x,t) = a_x + b_x k_t, \qquad \sum_x b_x = 1, \quad \sum_t k_t = 0 \tag{3.2}$$

bằng gói `StMoMo` trong R, giả định số ca tử vong tuân theo phân phối Poisson và liên kết log. Tham số
được ước lượng trên phạm vi tuổi 0–90 và giai đoạn 1980–2010 (`fitting.years` trong
`config/params.yaml`), sau khi loại giai đoạn 1955–1979 dựa trên bằng chứng điểm gãy cấu trúc tại 1974
đã trình bày ở mục 3.1.2.

### 3.2.1 Tham số $a_x$ và $b_x$

Hệ số $a_x$ (log tỷ suất tử vong trung bình theo thời gian tại từng tuổi) tái hiện đúng hình dạng chữ
V đã quan sát ở mục 3.1.1: thấp nhất tại tuổi 11 ($a_x \approx -7,13$), cao nhất tại tuổi 90
($a_x \approx -1,55$). Hình 3.9 trình bày cả ba tham số $a_x$, $b_x$, $k_t$ (nguồn hình:
`reports/figures/lc_params_total.pdf`).

Hệ số $b_x$ đo mức độ mỗi tuổi phản ứng với xu hướng chung $k_t$, đạt giá trị cao nhất tại **tuổi 1**
($b_x \approx 0,0361$) — cao gấp khoảng 3,3 lần mức trung bình ($1/91 \approx 0,011$) — và thấp nhất
tại tuổi 90 ($b_x \approx 0,007$). Tuổi 1 nhạy nhất với $k_t$ đồng nghĩa $m(1,t)$ biến động (cải
thiện) nhanh nhất theo thời gian trong toàn bộ dải tuổi ước lượng. Đáng chú ý, đây đúng là tuổi đã
được xác định nghi vấn có artifact ước lượng của UN ở mục 3.1.4; hệ số $b_x$ bất thường cao tại đây
cần được diễn giải thận trọng — nhiều khả năng phản ánh một phần nguồn artifact ước lượng tử vong trẻ
em, không hoàn toàn là tín hiệu cải thiện y tế thuần tuý.

### 3.2.2 Xu hướng $k_t$ và kiểm định giả định random-walk-with-drift

Chỉ số xu hướng chung $k_t$ giảm gần như tuyến tính trong giai đoạn ước lượng, từ $24,22$ (1980)
xuống $-18,09$ (2010), độ dốc trung bình $\approx -1,57$/năm — cùng chiều với xu hướng cải thiện tử
vong chung ($b_x > 0$ tại mọi tuổi nên $k_t$ giảm đồng nghĩa $m(x,t)$ giảm ở mọi tuổi).

Kiểm định ADF trực tiếp trên $k_t$ (chỉ 30 sai phân do cửa sổ ước lượng 1980–2010) cho kết quả yếu
hơn phép kiểm tra sơ bộ ở mục 3.1.2: chuỗi gốc không bác bỏ giả thuyết nghiệm đơn vị ($p \approx
0,57$, đúng kỳ vọng của bước ngẫu nhiên), nhưng chuỗi sai phân chỉ bác bỏ giả thuyết đó ở mức ý nghĩa
biên ($p \approx 0,09$, không đạt ngưỡng $5\%$ thông thường). Điều này phù hợp với nhận định đã nêu ở
mục 3.1.2: cửa sổ ước lượng càng hẹp, số sai phân càng ít, kiểm định càng mất power thống kê. Do đó,
bằng chứng chính cho việc chọn random-walk-with-drift làm mô hình dự báo $k_t$ (`forecast.kt_model:
"rwd"`) nên dựa vào kết quả kiểm định trên chỉ số $\bar m_t$ tính trên toàn bộ 1955–2023 (68 sai phân,
mục 3.1.2, $p \approx 0,0002$) — vốn có power cao hơn hẳn — hơn là kiểm định trực tiếp trên $k_t$ của
cửa sổ ước lượng ngắn hơn. Đây cũng là một hạn chế cần nêu trong phần thảo luận: cỡ mẫu thời gian
30 năm là tương đối ngắn để kiểm định vững chắc tính chất chuỗi thời gian của $k_t$.

### 3.2.3 Phân tích phần dư và giới hạn của cửa sổ ước lượng đối với hiệu ứng thế hệ

Hình 3.10 (heatmap phần dư, nguồn hình: `reports/figures/residuals_lc.pdf`) và Hình 3.11 (phần dư trung
bình theo cohort, nguồn hình: `reports/figures/lc_cohort_mean_residual.pdf`) minh hoạ phân tích dưới đây.

Deviance residual của mô hình LC đã fit cho phép kiểm tra hiệu ứng thế hệ (cohort effect) còn sót lại
mà mô hình — không có cấu phần cohort $\gamma_c$ — không nắm bắt được. Với cửa sổ ước lượng 1980–2010
(31 năm), số quan sát tối đa cho một cohort (năm sinh $c = t - x$) chỉ có thể đạt 31 — thấp hơn nhiều
so với cửa sổ đầy đủ 1955–2023 dùng ở phân tích EDA sơ bộ (mục 3.1). Áp dụng ngưỡng tối thiểu 20 quan
sát mỗi cohort để loại các cohort ở rìa dữ liệu, phần dư trung bình theo cohort dao động từ $-0,59$
(cohort 1980, nằm ngay biên đầu cửa sổ ước lượng) đến $+0,53$ (cohort 1910, chỉ quan sát được ở các
tuổi rất già 70–90 trong cửa sổ này).

**Nhận định:** với cửa sổ ước lượng chỉ 31 năm, phần lớn các cohort có phần dư cực trị nằm ngay tại
hoặc gần biên của cửa sổ quan sát (năm 1980 hoặc các cohort chỉ quan sát được một phần hẹp của vòng
đời) — đây là biểu hiện điển hình của vấn đề nhận dạng tuổi–năm–thế hệ (age-period-cohort
identification problem) khi cửa sổ thời gian ngắn so với dải tuổi ước lượng, không phải bằng chứng
đủ mạnh cho một hiệu ứng thế hệ có cấu trúc rõ ràng như mô thức "gò" (đỉnh dương quanh cohort
1950–1954) đã quan sát được ở phân tích EDA sơ bộ trên toàn bộ 1955–2023 (mục 3.1, sử dụng phép tách
tuổi+năm đơn giản, giả định ngầm $b_x = 1$). Kết luận về sự tồn tại và hình dạng thật của hiệu ứng
thế hệ tại Việt Nam, do đó, cần dựa vào kết quả ước lượng $\gamma_c$ chính thức của mô hình
Renshaw–Haberman (Chương 3, mục kế tiếp) hơn là phần dư LC trên cửa sổ ước lượng hẹp này — và cần
thảo luận thẳng thắn trong phần Hạn chế rằng cửa sổ 30 năm là tương đối ngắn để tách bạch tin cậy ba
hiệu ứng tuổi/năm/thế hệ.

Chỉ số thông tin AIC $= 24057,9$ và BIC $= 25312,2$ của mô hình LC được dùng làm mốc so sánh với các
mô hình Renshaw-Haberman và CBD ở phần so sánh mô hình (Chương 3, mục so sánh/backtest).
