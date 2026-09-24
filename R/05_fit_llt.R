# ============================================================
# 05_fit_llt.R — Nhanh C: Lee-Carter kieu Li-Lee-Tuljapurkar (2004) tren bang song TCTK
# (docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md, Muc 12.3)
# Chay  : Rscript R/05_fit_llt.R
# Input : data/external/gso/bang_song_*.csv (bang song rut gon, cac nam khong cach deu)
# Output: models/gso_vnm/llt_fit.rds, results/gso_vnm/llt_*.csv
#
# TRANG THAI: KHUNG - chua cai dat. Cac buoc:
#   1. Doc cac bang song TCTK (1989?, 1999, 2009, 2014, 2019, 2024) -> ma tran log nmx
#      theo nhom tuoi x nam quan sat t1 < t2 < ... < tn.
#   2. Uoc luong ax, bx, roi kt tai cac nam quan sat.
#      [CAN KIEM TRA chi tiet uoc luong ax, bx voi bai goc LLT 2004]
#   3. RWD voi phuong sai ty le khoang cach: buoc nhay cua kt giua hai lan quan sat
#      lien tiep co phan phoi chuan, ky vong mu va phuong sai s2 deu nhan voi do dai
#      khoang cach (nam); mu, s2 uoc luong hop ly cuc dai.
#   4. Backtest: khop tren 1989/1999/2009, du bao 2014/2019/2024; so voi nhanh B tren
#      cung diem kiem chung (Python: src/evaluation/decomposition.py, notebook 09).
# ============================================================
source("R/lib/load_data.R")

stop("R/05_fit_llt.R chua duoc cai dat - xem cac buoc trong header")
