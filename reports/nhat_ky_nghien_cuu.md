# Nhật ký nghiên cứu

## 2026-08-17 — Không xác định được số ca tử vong thực tế (D_{x,t}) trong dữ liệu UN WPP và GSO

**Vấn đề:** Dữ liệu thô thu thập từ UN WPP và GSO đều không chứa số ca tử vong quan sát trực
tiếp; `Dxt` dùng để fit mô hình trong toàn bộ pipeline hiện tại luôn là đại lượng **suy ra**,
không phải số liệu gốc.

**Dẫn chứng cụ thể:**
- File UN WPP ("Single age life table estimates") chỉ có tỷ suất tử vong trung tâm `m(x,n)`
  và số người-năm phơi nhiễm `L(x,n)` — xem `src/data/read_raw.py::read_wpp_single_age_life_table()`
  (`_HEADER_HINTS` chỉ khớp cột `mx`/`exposure`, không có cột số ca tử vong).
- `src/data/make_dataset.py::build_matrices()` phải **tính** `Dxt = mx * Ext`, với `Ext` xấp xỉ
  từ `L(x,n)` — một giả định, đã ghi chú tại `.claude/rules/data-pipeline.md`.
- Dữ liệu GSO (`data/interim/gso_bang_song_tdt2019.csv`, đọc bởi
  `src/data/read_raw.py::read_gso_life_table()`) chỉ có cột `qx` hoặc `mx` (bảng sống rút gọn
  từ Tổng điều tra dân số), suy ra `mx = -log(1-qx)` khi cần thiết — không có cột số ca tử vong
  tuyệt đối nào.

**Tình trạng:** Chưa xử lý — đây là giới hạn cố hữu của nguồn dữ liệu (UN WPP và GSO đều không
công bố số ca tử vong thô), không phải lỗi trong code có thể sửa được.

**Phương hướng:**
- Ghi rõ giới hạn này trong phần Hạn chế dữ liệu (hoặc mục Phương pháp, Chương 2 luận văn):
  `Dxt` trong toàn bộ mô hình LC/RH/CBD là đại lượng suy ra (`Dxt = mx * Ext`), không phải số
  liệu tử vong quan sát trực tiếp.
- Vì các mô hình (`R/02a_fit_lc.R`, `R/02b_fit_rh.R`, `R/02c_fit_cbd.R`) dùng giả định Poisson `D_{x,t} ~ Poisson(E^c_{x,t} m_{x,t})`
  trên chính `Dxt` suy ra này, cần thảo luận thận trọng trong luận văn: sai số xấp xỉ `Ext` từ
  `L(x,n)` có thể ảnh hưởng gián tiếp đến ước lượng deviance/AIC/BIC.
- Cân nhắc tìm nguồn số ca tử vong thô độc lập (nếu có, ví dụ Niên giám Thống kê GSO) để đối
  chiếu — hiện tại `data/external/SOURCES.md` chưa liệt kê nguồn nào có số ca tử vong tuyệt đối.

## 2026-08-17 — Chốt cách suy luận D_{x,t}, dán nhãn rõ là giả định

**Vấn đề:** Nối tiếp mục ghi phía trên — cần chốt công thức suy luận `Dxt` sẽ dùng xuyên suốt
pipeline, và đảm bảo công thức này được dán nhãn rõ ràng là giả định, không phải số liệu đếm
được, ngay tại nơi người đọc luận văn/notebook sẽ gặp trước tiên.

**Dẫn chứng cụ thể:** `notebooks/01_data_collection.ipynb`, cell 5 (markdown) đã ghi:
> Tuy nhiên, trong file không có $E_{x,t}$. Do đó, `Exposure` sẽ lấy xấp xỉ từ L(x,t) —
> person-years lived trong bảng sống — vì file life table của UN không tách deaths/exposure
> dân số thực.
> Do đó $D_{x,t} = m_x * E_{x,t}$ là MỘT GIẢ ĐỊNH, không phải số ca tử vong thực tế đếm được.

Khớp với cài đặt thực tế ở `src/data/make_dataset.py::build_matrices()` (`Dxt = mx * Ext`) và
ghi chú ở `.claude/rules/data-pipeline.md`.

**Tình trạng:** Đã xử lý phần dán nhãn — công thức và cảnh báo "giả định" đã có sẵn trong
notebook 01, khớp với code và rule đã ghi. Phần **chưa xử lý** vẫn là hai việc nêu ở mục phía
trên: (1) thảo luận ảnh hưởng của giả định này lên deviance/AIC/BIC trong Chương 2, (2) tìm
nguồn đối chiếu độc lập cho số ca tử vong.

**Phương hướng:** Khi viết Chương 2 (Phương pháp), trích dẫn nguyên văn ghi chú "MỘT GIẢ ĐỊNH"
từ notebook 01 làm căn cứ, không diễn giải lại `Dxt` như số liệu quan sát ở bất kỳ đâu trong
luận văn (bảng, hình, hay phần Kết quả).

## 2026-08-17 — Kết quả EDA: tử vong cải thiện theo thời gian, Nam luôn cao hơn Nữ

**Vấn đề/phát hiện:** EDA trên `notebooks/02_eda_vietnam_mortality.ipynb` xác nhận hai xu
hướng chính của tử vong Việt Nam 1955-2023: (1) tỷ lệ tử vong giảm dần qua thời gian ở mọi độ
tuổi, (2) tỷ lệ tử vong nam luôn cao hơn nữ ở hầu hết các tuổi.

**Dẫn chứng cụ thể (trích từ notebook 02, đã có số liệu tính toán):**
- **Xu hướng giảm theo thời gian:** median $\log m_{x,t}$ toàn dải tuổi giảm từ **−4.44
  (1960) xuống −5.34 (2020)**, tức $m_x$ trung vị giảm khoảng **2.4 lần** (cell 9). Toàn bộ
  đường cong $\log m_{x,t}$ dịch chuyển xuống dưới theo thời gian, năm sau luôn nằm dưới năm
  trước.
- **Cải thiện KHÔNG đồng đều theo tuổi** (cell 14, `plot_mortality_improvement_by_age`, hình
  `reports/figures/mortality_improvement_by_age.pdf`): % giảm $m_x$ 1960→2020 là **~78-88% ở
  tuổi 0-10**, chỉ còn **~58-68% ở tuổi 30-60**, và giảm tiếp xuống **43.9% ở tuổi 90**,
  **33.8% ở tuổi 100** — trẻ em cải thiện nhanh hơn hẳn người già, dư địa cải thiện tuổi già
  còn lớn (liên quan trực tiếp đến phạm vi fit CBD chỉ 55-90 tuổi, xem `config/params.yaml`).
- **Nam luôn cao hơn Nữ:** năm 2020, tỷ số $m_x$ nam/nữ trung bình **≈ 2.5 lần** trên toàn
  dải tuổi (cell 27, `plot_mx_sex_comparison`, hình `reports/figures/mx_sex_comparison.pdf`).
- **"Hõm tai nạn" (accident hump) chỉ ở nam, tuổi 15-30:** khoảng cách nam/nữ đạt đỉnh quanh
  tuổi 20, $m_x$ nam gấp **~3.71 lần** nữ năm 2020 (cell 27); đào sâu thêm ở cell 29-34 cho
  thấy vồng này tồn tại rõ rệt ở nam trong cả giai đoạn chiến tranh (1965-1974, đỉnh 1972) lẫn
  thời bình (tăng chậm 0.08→0.19 giai đoạn 1980-2019), nhưng **không quan sát được ở nữ ở bất
  kỳ năm mốc nào**.

**Tình trạng:** Đã xác nhận qua EDA định lượng (không phải quan sát định tính), có hình và số
liệu cụ thể đi kèm. Chưa đưa các con số này vào bản thảo luận văn.

**Phương hướng:**
- Đưa hai nhận xét này vào Chương 1 (Tổng quan/bối cảnh) hoặc phần EDA của Chương 3, kèm số
  liệu cụ thể ở trên thay vì mô tả định tính chung chung.
- Vì accident hump là đặc trưng riêng của nam (không có ở nữ) và độ dốc cải thiện khác nhau
  theo tuổi, cân nhắc nêu rõ trong Chương 2 lý do fit `series = "total"` làm mặc định (theo
  `.claude/rules/r-pipeline.md`) có thể che khuất khác biệt giới tính này — nếu thời gian cho
  phép, nên thử fit riêng theo `male`/`female` để đối chiếu, hoặc ít nhất nêu đây là hạn chế
  của phạm vi luận văn.
- Khác biệt nam/nữ mạnh nhất đúng ở dải tuổi 15-30 (thanh niên), nằm ngoài phạm vi fit của
  CBD (55-90) nhưng nằm trong phạm vi LC/RH (0-90) — cần lưu ý khi diễn giải residual theo
  tuổi của LC/RH ở dải tuổi này.

## 2026-08-26 — notebook 04 hiển thị kết quả Lee-Carter lỗi thời, không khớp dữ liệu hiện tại

**Vấn đề/phát hiện:** Khi viết bản nháp Chương 3 (mục Lee-Carter) từ nội dung
`notebooks/04_lee_carter.ipynb`, phát hiện các cell markdown "Nhận xét" trong notebook đang mô
tả một lần fit **cũ** — không khớp với `data/processed/params_lc_*.csv`/`residuals_lc.csv` hiện
tại (cửa sổ fit 1980-2010, 31 năm, theo `fitting.years` trong `config/params.yaml`). Nguyên
nhân: notebook chưa được chạy lại kể từ sau khi `R/02_fit_models.R` được tách thành
`R/02a_fit_lc.R`/`02b_fit_rh.R`/`02c_fit_cbd.R` (xem mục ghi liên quan tới `R/02b_fit_rh.R` —
chưa có entry riêng, xem lịch sử commit R/).

**Dẫn chứng cụ thể (số liệu cũ vs. số liệu đúng sau khi chạy lại):**

| Đại lượng | Notebook 04 (cũ) | Dữ liệu hiện tại |
|---|---|---|
| Phạm vi năm của kt | 1955-2023 (69 năm) | 1980-2010 (31 năm) |
| kt: đầu → cuối | 57,0 → −47,3 | 24,22 → −18,09 |
| Độ dốc kt | −1,87/năm | −1,57/năm |
| ax thấp nhất | tuổi 12 | tuổi 11 |
| bx cao nhất (tuổi 1) | 0,0196 | 0,0361 |
| ADF diff(kt), p-value | 0,00005 | 0,09 (không còn ý nghĩa ở mức 5%) |
| Đỉnh cohort residual | 1980-1984 (+0,67), min_obs=40 | rải rác ở biên: 1910 (+0,53) / 1980 (−0,59), min_obs=40 cho ra rỗng vì cửa sổ chỉ còn 31 năm |

**Tình trạng:** Đã xử lý. Sửa `cohort_mean_residual(..., min_obs=40)` → `min_obs=20` (40 không
khả thi với cửa sổ 31 năm) và viết lại 3 cell markdown liên quan (tham số ax/bx/kt, kiểm định
ADF, phân tích cohort residual) khớp số liệu hiện tại trong `notebooks/04_lee_carter.ipynb`.
Người dùng đã chạy lại và lưu notebook, đối chiếu xác nhận khớp chính xác (cohort residual
−0,593 → 0,527 tại cohort 1980/1910).

**Phương hướng:**
- **Bài học quy trình cho các phiên sau**: sau bất kỳ thay đổi nào ở `R/02a_fit_lc.R` (hoặc
  `config/params.yaml::fitting.years`), phải chạy lại và lưu `notebooks/04_lee_carter.ipynb`
  trước khi trích số liệu từ đó vào luận văn — cell output không tự đồng bộ.
  `notebooks/05_renshaw_haberman.ipynb`/`06_cbd.ipynb` khi được viết đầy đủ cũng sẽ có cùng rủi
  ro này với `R/02b_fit_rh.R`/`02c_fit_cbd.R`.
- ADF trên kt cửa sổ 30 năm chỉ có ý nghĩa biên (p≈0,09) — cần nêu rõ trong phần Hạn chế của
  luận văn: bằng chứng chính cho RWD nên dựa vào kiểm định $\bar m_t$ trên toàn bộ 1955-2023 ở
  notebook 02 (p≈0,0002, xem entry EDA phía trên), không phải ADF trực tiếp trên kt của cửa sổ
  fit ngắn hơn.
- Mô thức cohort residual của LC giờ bị chi phối bởi hiệu ứng biên cửa sổ (age-period-cohort
  identification problem) chứ không còn đỉnh gọn như trước — kết luận về hình dạng thật của
  hiệu ứng thế hệ cần đợi γc chính thức từ Renshaw-Haberman (`R/02b_fit_rh.R` đã fit sẵn, chưa
  viết notebook 05).

## 2026-08-26 — Bổ sung tuổi thọ kỳ vọng (e0, e60) làm bằng chứng già hoá dân số cho Chương 3

**Vấn đề/phát hiện:** Bản nháp Chương 3 (EDA) chưa đề cập hiện tượng già hoá dân số ở Việt Nam.
Dữ liệu $m(x,t)$ của luận văn chỉ ghi nhận phía tử vong của quá trình này (không có tỷ suất sinh
hay cấu trúc tuổi dân số thật), nên chỉ tính được cấu phần tuổi thọ kỳ vọng — nhưng cấu phần này
chưa từng được tính ở notebook 02 hay 04 (mục "Tuổi thọ kỳ vọng $e_0$, $e_{60}$..." của notebook
02 có sinh hình `e0_trend_by_sex.pdf`/`e60_trend_by_sex.pdf` nhưng không in số liệu ra text).

**Dẫn chứng cụ thể (tính trực tiếp từ `src/data/life_table.py::life_expectancy_series`):**
- $e_0$ (chung 2 giới): $57,99$ (1960) → $75,39$ (2020), tăng $17,4$ năm.
- $e_{60}$ (chung 2 giới): $16,44$ (1960) → $22,07$ (2020), tăng $5,6$ năm — xác nhận cải thiện
  không chỉ đến từ giảm tử vong sơ sinh/trẻ em mà cả người đã sống đến 60 tuổi cũng tử vong muộn
  hơn hẳn.
- Khoảng cách $e_0$ nam/nữ doãng ra: $6,15$ năm (1960) → $9,95$ năm (2020); $e_{60}$: $5,64$ năm
  (2020).
- Cả $e_0$ và $e_{60}$ giảm nhẹ 2020→2023 ($75,39$→$74,59$ và $22,07$→$21,27$), nhất quán với đột
  biến tử vong COVID-19 đã ghi nhận trong entry EDA 2026-08-17.

**Tình trạng:** Đã viết thành mục 3.1.5 trong `reports/thesis/chuong3_eda_lc.md`, liên hệ trực
tiếp đến rủi ro trường thọ (longevity risk) cho phần ứng dụng bảo hiểm (notebook 08).

**Phương hướng:**
- Khi viết notebook 08 (ứng dụng bảo hiểm), dùng lại $e_{60}$ tăng liên tục làm động lực chính
  cho rủi ro trường thọ trong định phí sản phẩm hưu trí/niên kim.
- Phần bối cảnh già hoá dân số rộng hơn (tỷ suất sinh, tỷ trọng dân số cao tuổi, dự báo dân số)
  cần nguồn ngoài dự án (GSO, UN Population Division) — đã đánh dấu `[CẦN BỔ SUNG NGUỒN]` trong
  bản nháp, chưa có số liệu.

## 2026-08-26 — Bổ sung trực quan hoá điểm gãy cấu trúc 1974 vào notebook 02

**Vấn đề/phát hiện:** Mục "Điểm gãy cấu trúc" ở notebook 02 (entry EDA 2026-08-17) chỉ có bảng số
liệu bằng lời (Chow F, p-value, độ dốc trước/sau), chưa có hình minh hoạ trực quan cho kết luận
điểm gãy 1974 — khó thuyết phục khi trình bày trong luận văn nếu không có hình.

**Dẫn chứng cụ thể:** Thêm 2 hàm vào `src/visualization/plots.py`: `plot_breakpoint_search` (SSE
theo từng năm ứng viên, đánh dấu cực tiểu) và `plot_structural_break` (chuỗi $\bar m_t$ kèm 2
đường hồi quy trước/sau điểm gãy). Thêm 4 cell vào `notebooks/02_eda_vietnam_mortality.ipynb`
(sau cell tính Chow test, id `ee190d3e`) gọi 2 hàm trên và in bảng so sánh SSE: fit 1 đường thẳng
SSE=$1,550$ (2 tham số) vs. fit 2 đoạn tại 1974 SSE=$0,324$ (4 tham số, giảm ~79%), Chow F=$123,1$,
p≈$1,11\times10^{-16}$. Đã chạy thử độc lập (ngoài notebook) xác nhận không lỗi, 2 file hình
`breakpoint_search_mbar_t.pdf`/`structural_break_mbar_t.pdf` sinh ra thành công.

**Tình trạng:** Đã sửa source code trong notebook (qua script Python đọc/ghi JSON trực tiếp, xem
phương hướng bên dưới), nhưng **chưa chạy qua kernel Jupyter thật** nên 4 cell mới chưa có output
hiển thị trong notebook — cần người dùng mở và Run All + lưu lại.

**Phương hướng:**
- **Giới hạn công cụ phát hiện được, cần lưu ý cho phiên sau**: tool Read không mở được
  `notebooks/02_eda_vietnam_mortality.ipynb` nữa (882KB+, 14 ảnh PNG nhúng base64 — vượt giới hạn
  token của tool kể cả khi dùng `offset`/`limit`). Từ giờ, sửa notebook này (và có thể các
  notebook khác có nhiều output ảnh) cần thao tác trực tiếp qua `json.load`/`json.dump` bằng
  script Python (giữ nguyên `indent=1`, `ensure_ascii=False` khớp định dạng gốc) thay vì tool
  NotebookEdit — nhớ `nbformat.validate()` sau khi sửa để đảm bảo không hỏng cấu trúc.
- Cần cập nhật `.claude/rules/language-split.md`: ghi chú "chỉ notebook 01, 02 có nội dung thật"
  đã lỗi thời — notebook 03 (làm trơn/graduation) và 04 (Lee-Carter) hiện đã có nội dung đầy đủ,
  chỉ còn 05-08 là placeholder/stub thật sự (xem cập nhật cùng ngày trong CLAUDE.md/rules).

## 2026-09-24 — Đổi cửa sổ ước lượng từ 1980-2010 sang 1990-2008 theo thiết kế nhánh B

**Vấn đề/quyết định:** Tái cấu trúc repo theo `docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md`
(ba nhánh A/B/C). Nhánh B (Mục 12.2) yêu cầu khớp trên WPP **1990-2008**, dự báo 2009-2024 rồi
kiểm chứng với bảng sống TCTK 2009, 2014, 2019, 2024 (tầm 1, 6, 11, 16 năm). Theo quyết định
của học viên, `config/params.yaml::fitting.years` đổi từ 1980-2010 thành 1990-2008;
`backtest.splits` đổi thành {1990, 2008, 2023} (split chính) và {1990, 2003, 2013} (ổn định).

**Dẫn chứng cụ thể (LC, series total, tuổi 0-90):**

| Đại lượng | 1980-2010 (cũ) | 1990-2008 (mới) |
|---|---|---|
| kt: đầu → cuối | 24,22 → −18,09 | 13,61 → −8,67 |
| Độ dốc kt | −1,57/năm | −1,38/năm |
| ax thấp nhất / cao nhất | tuổi 11 (−7,13) / tuổi 90 (−1,55) | tuổi 11 (−7,25) / tuổi 90 (−1,59) |
| bx cao nhất (tuổi 1) | 0,0361 | 0,0442 |
| bx thấp nhất | tuổi 90 (0,007) | tuổi 19 (0,0083) |
| ADF diff(kt), p-value | 0,09 | 0,43 |
| Cohort residual (min_obs) | 1980 −0,59 / 1910 +0,53 (20) | 1992 −0,57 / 1997 +1,33 (12) |
| AIC / BIC | 24057,9 / 25312,2 | 14515,4 / 15601,0 |

AIC/BIC các mô hình khác trên cửa sổ mới: RH 14456,9 / 16091,4; APC 14547,6 / 15691,8;
CBD 7764,8 / 7936,9; M7 6535,9 / 6996,0 (RH hội tụ). AIC/BIC chỉ so được giữa các mô hình cùng
dải tuổi (LC/RH/APC: 0-90; CBD/M7: 55-90).

**Tình trạng:** Đã xử lý. Refit toàn bộ `R/02a`-`02e`, `03_forecast`, `04_backtest`; chạy lại và
lưu `notebooks/04_lee_carter.ipynb` (min_obs cohort đổi thành ~2/3 số năm fit, tính động, vì 20
không khả thi với 19 năm); cập nhật markdown liên quan ở notebook 01, 02, 03, 04 và mục 3.2 của
`reports/thesis/chuong3_eda_lc.md`; sinh lại 3 hình LC.

**Phương hướng:**
- ADF trên kt với 18 sai phân không còn cho bằng chứng gì — bằng chứng cho RWD dựa hoàn toàn vào
  kiểm định $\bar m_t$ 1955-2023 ở notebook 02; nêu rõ trong phần Hạn chế.
- Cohort residual cực trị giờ nằm ở cohort trẻ sát biên (chỉ quan sát tuổi 0-16), gắn với vùng
  tuổi nhỏ nghi artifact UN — không diễn giải như hiệu ứng thế hệ; chờ γc của RH (notebook 05)
  và nhớ Mục 4.2/8.2: γc trên WPP không diễn giải như dấu vết lịch sử.
- Cửa sổ 19 năm: RH có γc cho các cohort rìa kém định danh — bản đồ tri thức xếp RH là "thận trọng"
  ở nhánh B; APC là đối chứng ổn định hơn.
