# Nguồn dữ liệu — ghi lại mỗi lần tải

WPP đặt vào `data/raw/wpp/`, HMD vào `data/raw/hmd/<COUNTRY>/` (Deaths_1x1.txt, Exposures_1x1.txt),
bảng CSO 1980 vào `data/raw/cso/`. Bảng sống GSO số hoá tay nằm ở `data/external/gso/` (commit).

| Nguồn | File | URL | Ngày tải | Ghi chú |
|---|---|---|---|---|
| UN WPP 2024 | WPP2024_MORT_F06_1_SINGLE_AGE_LIFE_TABLE_ESTIMATES_BOTH_SEXES.xlsx | https://population.un.org/wpp/ | | Bảng sống tuổi đơn, đã làm trơn bằng mô hình |
| UN WPP 2024 | WPP2024_MORT_F06_2_SINGLE_AGE_LIFE_TABLE_ESTIMATES_MALE.xlsx | https://population.un.org/wpp/ | | Bảng sống tuổi đơn, đã làm trơn bằng mô hình |
| UN WPP 2024 | WPP2024_MORT_F06_3_SINGLE_AGE_LIFE_TABLE_ESTIMATES_FEMALE.xlsx | https://population.un.org/wpp/ | | Bảng sống tuổi đơn, đã làm trơn bằng mô hình |
| GSO | gso/bang_song_tdt2019.csv | https://www.nso.gov.vn | | Nguồn: Kết quả TĐT dân số và nhà ở 01/4/2019, tr. 96 |
| HMD | <COUNTRY>/Deaths_1x1.txt, Exposures_1x1.txt | https://www.mortality.org | | Nhánh A: JPN, KOR, TWN - cần đăng ký tài khoản |
| Bộ Tài chính | CSO 1980 | | | [CẦN KIỂM TRA số hiệu thông tư hiện hành] |
