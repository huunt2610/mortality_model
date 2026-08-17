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
- Vì các mô hình (`R/02_fit_models.R`) dùng giả định Poisson `D_{x,t} ~ Poisson(E^c_{x,t} m_{x,t})`
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
