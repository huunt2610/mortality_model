# ============================================================
# 06_simulate_scenarios.R — Ung dung: mo phong kich ban tu vong co bat dinh tham so
# (docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md, Muc 14.2 buoc 1)
# Chay  : Rscript R/06_simulate_scenarios.R [dataset]
# Input : models/<dataset>/<model>_fit.rds (mo hinh duoc chon theo ket qua nhanh A, B)
# Output: models/<dataset>/scenarios_<model>.rds - mang q(x,t,kich ban) cho Python dinh gia
#         (src/risk/pricing.py, src/risk/measures.py, notebook 10)
#
# TRANG THAI: KHUNG - chua cai dat. Cac buoc:
#   1. Refit tren WPP den 2019 (hoac 2023 kem xu ly COVID - backtest.exclude_covid_years).
#   2. Bootstrap bat dinh tham so (Brouhns, Denuit & Van Keilegom 2005): ham bootstrap()
#      cua StMoMo, type "semiparametric".
#   3. Mo phong application.n_scenarios duong trong application.horizon nam: simulate()
#      tren ket qua bootstrap.
#   4. Chuyen ve q(x,t) (LC/RH/APC: q = 1 - exp(-m)), luu ra .rds / CSV.
# ============================================================
source("R/lib/load_data.R")
source("R/lib/models.R")

stop("R/06_simulate_scenarios.R chua duoc cai dat - xem cac buoc trong header")
