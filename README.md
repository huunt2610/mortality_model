# Mortality Forecasting Models for Vietnam

Luận văn Thạc sĩ - Lý thuyết Xác suất và Thống kê Toán học, ĐH KHTN, ĐHQG-HCM.

Xây dựng, hiệu chỉnh và so sánh các mô hình tử vong ngẫu nhiên (Lee-Carter,
Renshaw-Haberman, Cairns-Blake-Dowd) trên dữ liệu Việt Nam, và ứng dụng vào
quản trị rủi ro trong doanh nghiệp bảo hiểm nhân thọ.

## Phân công ngôn ngữ

| Việc | Công cụ |
|---|---|
| Thu thập, tiền xử lý dữ liệu, EDA, vẽ hình | Python (pandas, matplotlib) - `src/`, `notebooks/` |
| Fit mô hình LC / RH / CBD, dự báo, mô phỏng | R (**StMoMo**, demography, forecast) - `R/` |
| Đánh giá, backtest, tổng hợp kết quả | Python + R - `src/evaluation/`, `notebooks/07` |

R fit mô hình rồi export kết quả (tham số, dự báo, residuals) ra CSV trong
`data/processed/` và `models/`; Python đọc lại để phân tích và vẽ hình luận văn.

## Cấu trúc thư mục

```
vn-mortality-models/
├── config/
│   └── params.yaml          # Phạm vi tuổi, năm, split train/test - MỘT nơi duy nhất
├── data/
│   ├── raw/                 # Dữ liệu gốc tải về, KHÔNG BAO GIỜ sửa tay (không commit)
│   ├── external/            # Tài liệu tham chiếu: bảng sống GSO, metadata nguồn
│   ├── interim/             # Dữ liệu trung gian đang xử lý
│   └── processed/           # Ma trận Dxt, Ext sạch - input cho mô hình
├── notebooks/               # Đánh số theo thứ tự pipeline, mỗi notebook ≈ 1 mục luận văn
│   ├── 01_data_collection.ipynb
│   ├── 02_eda_vietnam_mortality.ipynb
│   ├── 03_smoothing_graduation.ipynb
│   ├── 04_lee_carter.ipynb
│   ├── 05_renshaw_haberman.ipynb
│   ├── 06_cbd.ipynb
│   ├── 07_model_comparison_backtest.ipynb
│   └── 08_insurance_applications.ipynb
├── R/
│   ├── 00_install_packages.R
│   ├── 01_load_data.R       # Đọc Dxt/Ext từ data/processed thành StMoMoData
│   ├── 02_fit_models.R      # Fit LC, RH, CBD bằng StMoMo
│   ├── 03_forecast.R        # Dự báo kt, gamma_c bằng ARIMA / RWD, mô phỏng
│   ├── 04_backtest.R        # Out-of-sample: refit trên tập train, dự báo tập test
│   └── utils.R
├── src/                     # Python package
│   ├── data/                # download, làm sạch, dựng ma trận Dxt/Ext
│   ├── evaluation/          # RMSE, MAPE, deviance, so sánh mô hình
│   └── visualization/       # Hình chuẩn cho luận văn (log mx, Lexis heatmap,…)
├── models/                  # Object mô hình đã fit (.rds) + tham số export (không commit file lớn)
├── reports/
│   ├── figures/             # Hình cuối cùng chèn vào luận văn (PDF/PNG 300dpi)
│   └── thesis/              # Bản thảo các chương
├── references/              # PDF papers (không commit nếu có bản quyền)
├── tests/                   # pytest cho src/
├── requirements.txt         # Môi trường Python
└── .gitignore
```

## Nguyên tắc làm việc

1. **Dữ liệu thô là bất biến.** Mọi biến đổi đều bằng code, chạy lại được từ đầu:
   `raw → interim → processed`. Không sửa tay file Excel.
2. **Tham số cấu hình tập trung** ở `config/params.yaml`. Đổi phạm vi tuổi hay
   split train/test ở một chỗ, mọi script đọc từ đó.
3. **Notebook để khám phá và trình bày; logic tái sử dụng nằm trong `src/` và `R/`.**
   Notebook chỉ gọi hàm, không chứa hàm dài.
4. **Mỗi hình trong luận văn sinh ra từ một hàm** trong `src/visualization/`,
   lưu vào `reports/figures/` - sửa được và chạy lại được đến phút chót.
5. Commit thường xuyên, message rõ ràng: `feat: fit RH model with beta0=1 constraint`.

## Nguồn dữ liệu

- **UN World Population Prospects (WPP)** - bảng sống tuổi đơn, 1950–nay, nguồn chính
  (lưu ý trong luận văn: dữ liệu đã được UN làm trơn bằng mô hình).
- **GSO Việt Nam** - bảng sống rút gọn từ Tổng điều tra 2009/2019, điều tra giữa kỳ,
  Niên giám Thống kê: dùng để đối chiếu kiểm chứng.
- **WHO Mortality Database** - dữ liệu VN thưa, chỉ tham khảo.
- Việt Nam **không có** trong Human Mortality Database.

## Ký hiệu, thuật ngữ

Dùng để: (1) thống nhất ký hiệu xuyên suốt luận văn, (2) tra cứu thuật ngữ Việt-Anh khi đọc paper tiếng Anh và viết tiếng Việt.
### 1. Ký hiệu cơ bản về tuổi, thời gian, thế hệ

| Ký hiệu | LaTeX | Tiếng Việt | English |
|---|---|---|---|
| $x$ | `x` | Tuổi (tuổi tròn) | Age |
| $t$ | `t` | Năm lịch / thời kỳ | Calendar year / period |
| $c = t - x$ | `c = t-x` | Năm sinh / thế hệ | Cohort / year of birth |
| $\omega$ | `\omega` | Tuổi cao nhất trong bảng sống | Limiting age |
| $n$ | `n` | Độ dài khoảng tuổi (bảng sống rút gọn) | Length of age interval |

### 2. Đại lượng bảng sống (Life table)

| Ký hiệu | LaTeX | Tiếng Việt | English |
|---|---|---|---|
| $m_{x,t}$ | `m_{x,t}` | Tỷ suất tử vong trung tâm | Central death rate |
| $q_{x,t}$ | `q_{x,t}` | Xác suất tử vong (trong 1 năm) | Probability of death / mortality rate |
| $p_{x,t} = 1 - q_{x,t}$ | `p_{x,t}` | Xác suất sống sót | Survival probability |
| $\mu_{x,t}$ | `\mu_{x,t}` | Lực tử vong (cường độ tử vong) | Force of mortality / hazard rate |
| $l_x$ | `l_x` | Số người sống tại tuổi đúng $x$ | Number of survivors |
| $d_x$ | `d_x` | Số người chết giữa tuổi $x$ và $x+1$ | Number of deaths |
| $L_x$ | `L_x` | Số người-năm sống từ $x$ đến $x+1$ | Person-years lived |
| $T_x$ | `T_x` | Số người-năm sống từ tuổi $x$ trở đi | Total person-years remaining |
| $e_x$ | `e_x` | Triển vọng sống / tuổi thọ kỳ vọng tại tuổi $x$ | Life expectancy at age $x$ |
| $\mathring{e}_x$ | `\mathring{e}_x` | Tuổi thọ kỳ vọng đầy đủ (liên tục) | Complete life expectancy |
| $e_0$, $e_{60}$ | | Tuổi thọ kỳ vọng khi sinh / tại tuổi 60 | Life expectancy at birth / at 60 |
| $a_x$ | `a_x` | Số năm trung bình sống thêm của người chết trong năm | Average fraction of year lived |
| ${}_nq_x$ | `{}_nq_x` | Xác suất chết từ $x$ đến $x+n$ | $n$-year death probability |

**Các quan hệ:**

$$q_{x} = \frac{d_x}{l_x}, \qquad l_{x+1} = l_x - d_x, \qquad e_x = \frac{T_x}{l_x}$$

$$m_x = \frac{d_x}{L_x} \qquad\text{(tử vong trên số người-năm phơi nhiễm)}$$

$$q_x \approx 1 - e^{-m_x} \qquad\text{(giả định lực tử vong hằng số trong năm tuổi)}$$

$$q_x = \frac{m_x}{1 + (1 - a_x)\, m_x} \qquad\text{(công thức chuyển đổi chính xác hơn)}$$

$${}_nq_x = 1 - \prod_{i=0}^{n-1}(1 - q_{x+i}) \qquad\text{(gộp tuổi đơn về nhóm - dùng khi đối chiếu WPP với GSO)}$$

---

### 3. Dữ liệu đầu vào của mô hình

| Ký hiệu | LaTeX | Tiếng Việt | English |
|---|---|---|---|
| $D_{x,t}$ | `D_{x,t}` | Số ca tử vong quan sát (tuổi $x$, năm $t$) | Observed deaths |
| $E_{x,t}$ | `E_{x,t}` | Số người-năm phơi nhiễm (exposure) | Exposure to risk |
| $E^c_{x,t}$ | `E^c_{x,t}` | Phơi nhiễm trung tâm | Central exposure |
| $E^0_{x,t}$ | `E^0_{x,t}` | Phơi nhiễm ban đầu | Initial exposure |
| $\hat{m}_{x,t} = D_{x,t}/E^c_{x,t}$ | | Ước lượng thực nghiệm của $m_{x,t}$ | Crude/empirical death rate |

> **Quy ước quan trọng:** dùng $E^c$ (central exposure) đi với $m_{x,t}$ và link log; dùng $E^0$ (initial exposure) đi với $q_{x,t}$ và link logit. Trong `StMoMo` đây là tham số `type = "central"` hoặc `"initial"`. Nhầm chỗ này là lỗi phổ biến nhất khi fit mô hình.

---

### 4. Tham số các mô hình tử vong ngẫu nhiên

| Ký hiệu | LaTeX | Tiếng Việt | English |
|---|---|---|---|
| $\alpha_x$ (hoặc $a_x$) | `\alpha_x` | Tham số tuổi - mức tử vong trung bình theo tuổi | Age parameter / general age profile |
| $\beta_x^{(i)}$ (hoặc $b_x$) | `\beta_x^{(i)}` | Tham số nhạy cảm tuổi | Age sensitivity / age-modulating parameter |
| $\kappa_t^{(i)}$ (hoặc $k_t$) | `\kappa_t^{(i)}` | Tham số thời kỳ - xu hướng tử vong theo thời gian | Period effect / time index |
| $\gamma_{t-x}$ (hoặc $\gamma_c$, $g_c$) | `\gamma_{t-x}` | Tham số thế hệ | Cohort effect |
| $\bar{x}$ | `\bar{x}` | Tuổi trung bình của phạm vi dữ liệu | Mean age of the fitting range |
| $\varepsilon_{x,t}$ | `\varepsilon_{x,t}` | Sai số ngẫu nhiên | Error term |

### Các mô hình chính (dạng chuẩn để trích dẫn trong luận văn)

**Lee–Carter (LC), 1992** - baseline, đơn giản nhất:
$$\log m_{x,t} = \alpha_x + \beta_x \kappa_t + \varepsilon_{x,t}$$
Ràng buộc định danh: $\sum_t \kappa_t = 0$, $\sum_x \beta_x = 1$.

**Renshaw–Haberman (RH), 2006** - LC + hiệu ứng thế hệ:
$$\log m_{x,t} = \alpha_x + \beta_x^{(1)} \kappa_t + \beta_x^{(0)} \gamma_{t-x}$$
Bản đơn giản hóa (Haberman & Renshaw 2011), ổn định hơn khi fit: đặt $\beta_x^{(0)} = 1$.

**Age–Period–Cohort (APC)** - trường hợp riêng của RH với $\beta_x^{(1)} = \beta_x^{(0)} = 1$:
$$\log m_{x,t} = \alpha_x + \kappa_t + \gamma_{t-x}$$

**Cairns–Blake–Dowd (CBD), 2006** - hai yếu tố, dùng cho tuổi già:
$$\text{logit}\, q_{x,t} = \log\!\left(\frac{q_{x,t}}{1-q_{x,t}}\right) = \kappa_t^{(1)} + \kappa_t^{(2)}(x - \bar{x})$$
$\kappa^{(1)}$: **yếu tố mức** (level factor) - mức tử vong chung.
$\kappa^{(2)}$: **yếu tố độ dốc** (slope factor) - độ dốc theo tuổi.

**M7 (CBD mở rộng)** - thêm cong bậc hai và thế hệ, đáng thử làm mô hình đối chứng:
$$\text{logit}\, q_{x,t} = \kappa_t^{(1)} + \kappa_t^{(2)}(x-\bar{x}) + \kappa_t^{(3)}\left[(x-\bar{x})^2 - \hat{\sigma}_x^2\right] + \gamma_{t-x}$$

### Mô hình tham số cổ điển (chương lý thuyết)

| Mô hình | Công thức | Ghi chú |
|---|---|---|
| **Gompertz** (1825) | $\mu_x = B c^x$ | Tử vong tăng theo hàm mũ ở tuổi trưởng thành |
| **Makeham** (1860) | $\mu_x = A + B c^x$ | Thêm hằng số $A$ cho tử vong ngoại sinh (tai nạn) |
| **Heligman–Pollard** (1980) | 8 tham số, 3 thành phần | Mô tả cả tử vong trẻ em, "bướu" tuổi trẻ và tuổi già |

---

### 5. Ước lượng và làm trơn

| Thuật ngữ | Tiếng Việt | Ghi chú |
|---|---|---|
| SVD (Singular Value Decomposition) | Phân rã giá trị kỳ dị | Phương pháp gốc của Lee–Carter |
| MLE (Maximum Likelihood Estimation) | Ước lượng hợp lý cực đại | Chuẩn hiện nay, giả định Poisson |
| GLM / GNM | Mô hình tuyến tính/phi tuyến tổng quát | RH ước lượng bằng GNM (`gnm` trong R) |
| Poisson assumption | Giả định Poisson: $D_{x,t} \sim \text{Poisson}(E^c_{x,t}\, m_{x,t})$ | Nền tảng của deviance |
| Binomial assumption | $D_{x,t} \sim \text{Binomial}(E^0_{x,t}, q_{x,t})$ | Dùng với link logit (CBD) |
| Graduation | Làm trơn / nội suy bảng sống | Chuyển nhóm 5 tuổi → tuổi đơn |
| P-splines | Spline có phạt | Làm trơn 2 chiều tuổi–năm |
| Whittaker–Henderson | Phương pháp làm trơn cổ điển | Cân bằng độ khớp và độ trơn |
| Identification constraints | Ràng buộc định danh | Bắt buộc nêu rõ trong luận văn |
| Convergence | Sự hội tụ (của thuật toán lặp) | RH nổi tiếng khó hội tụ |

---

### 6. Dự báo

| Thuật ngữ | Tiếng Việt | Ghi chú |
|---|---|---|
| ARIMA($p,d,q$) | Mô hình tự hồi quy tích hợp trung bình trượt | Dự báo $\kappa_t$, $\gamma_c$ |
| RWD (Random Walk with Drift) | Bước ngẫu nhiên có bụi/xu thế | Mặc định cho $\kappa_t$ của LC; tương đương ARIMA(0,1,0) với drift |
| MRWD (Multivariate RWD) | Bước ngẫu nhiên đa biến | Dùng cho $(\kappa^{(1)}_t, \kappa^{(2)}_t)$ của CBD |
| Forecast horizon | Tầm dự báo | Số năm dự báo về tương lai |
| Prediction interval | Khoảng dự báo | Thể hiện bất định |
| Parameter uncertainty | Bất định tham số | Tên bài báo gốc CBD nhấn mạnh điều này |
| Bootstrap / simulation | Tự khởi động / mô phỏng | Sinh khoảng tin cậy cho $e_0$, phí bảo hiểm |
| Fan chart | Biểu đồ quạt | Hình chuẩn để trình bày dự báo tử vong |
| Jump-off bias | Sai lệch điểm xuất phát | Chênh giữa giá trị fit và giá trị quan sát năm cuối |

---

### 7. Đánh giá và so sánh mô hình

| Ký hiệu / thuật ngữ | Tiếng Việt | Công thức / ghi chú |
|---|---|---|
| Deviance | Độ lệch | $2\sum \left[D \log\frac{D}{\hat{D}} - (D - \hat{D})\right]$ |
| Deviance residual | Phần dư độ lệch | Vẽ heatmap theo tuổi–năm–thế hệ để chẩn đoán |
| AIC | Tiêu chuẩn thông tin Akaike | $-2\log L + 2k$ |
| BIC | Tiêu chuẩn thông tin Bayes | $-2\log L + k\log n$; phạt nặng hơn AIC |
| RMSE | Sai số bình phương trung bình gốc | Nên tính trên thang **log** vì $m_x$ trải nhiều bậc độ lớn |
| MAPE | Sai số phần trăm tuyệt đối trung bình | |
| In-sample fit | Độ khớp trong mẫu | AIC/BIC/deviance |
| Out-of-sample / backtest | Kiểm định ngoài mẫu | RMSE/MAPE trên tập test |
| Goodness of fit | Mức độ phù hợp | |
| Robustness | Tính ổn định (của mô hình/kết quả) | Đổi phạm vi tuổi/năm xem kết quả có đổi không |
| Biological reasonableness | Tính hợp lý sinh học | Dự báo có phi lý không (VD: tử vong âm, đảo chiều bất thường) |
| Model risk | Rủi ro mô hình | Chênh lệch kết quả giữa các mô hình - mục ứng dụng |

---

### 8. Toán bảo hiểm - ứng dụng quản trị rủi ro

#### Ký hiệu chuẩn quốc tế (International Actuarial Notation)

| Ký hiệu | LaTeX | Tiếng Việt | English |
|---|---|---|---|
| $i$ | `i` | Lãi suất kỹ thuật hằng năm | Interest rate |
| $v = (1+i)^{-1}$ | `v = (1+i)^{-1}` | Hệ số chiết khấu | Discount factor |
| $\delta = \ln(1+i)$ | `\delta` | Lãi suất tức thời | Force of interest |
| ${}_tp_x$ | `{}_tp_x` | Xác suất người tuổi $x$ sống thêm $t$ năm | $t$-year survival probability |
| $A_x$ | `A_x` | Giá trị hiện tại kỳ vọng bảo hiểm trọn đời | Whole life insurance EPV |
| $A^1_{x:\overline{n}\rvert}$ | `A^1_{x:\overline{n}\rvert}` | BH tử kỳ $n$ năm | Term insurance |
| $\ddot{a}_x$ | `\ddot{a}_x` | Niên kim trọn đời trả đầu kỳ | Whole life annuity-due |
| $a_x$ | `a_x` | Niên kim trả cuối kỳ | Annuity-immediate |
| $\ddot{a}_{x:\overline{n}\rvert}$ | | Niên kim tạm thời $n$ năm | Temporary annuity |
| $P$ | `P` | Phí thuần | Net premium |
| ${}_tV$ | `{}_tV` | Dự phòng toán học tại thời điểm $t$ | Reserve |
| EPV | | Giá trị hiện tại kỳ vọng | Expected Present Value |

**Công thức nền tảng:**

$$\ddot{a}_x = \sum_{k=0}^{\infty} v^k\, {}_kp_x \qquad\qquad A_x = \sum_{k=0}^{\infty} v^{k+1}\, {}_kp_x \, q_{x+k}$$

$$A_x = 1 - d\,\ddot{a}_x \quad (d = iv) \qquad\qquad P = \frac{A_x}{\ddot{a}_x} \quad\text{(nguyên tắc tương đương)}$$

> Đây là cầu nối giữa phần thống kê và phần bảo hiểm: dự báo $q_{x,t}$ từ LC/RH/CBD → tính ${}_kp_x$ → tính $\ddot{a}_x$, $A_x$ → so sánh phí/dự phòng giữa các mô hình. Chênh lệch chính là **định lượng model risk**.



## Khởi động nhanh

```bash
# Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# R
Rscript R/00_install_packages.R

# Chạy pipeline dữ liệu
python -m src.data.make_dataset

# Fit mô hình
Rscript R/02_fit_models.R
```
