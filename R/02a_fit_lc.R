# ============================================================
# 02a_fit_lc.R — Fit Lee-Carter (M1)
# Chay  : Rscript R/02a_fit_lc.R [dataset]   (mac dinh: default_dataset trong config)
# Input : data/processed/<dataset>/Dxt_total.csv, Ext_total.csv
# Output: models/<dataset>/lc_fit.rds, results/<dataset>/params_lc_*.csv, residuals_lc.csv
# ============================================================
source("R/lib/load_data.R")
source("R/lib/models.R")
source("R/lib/export.R")

cfg <- load_config()
dataset <- get_dataset(cfg)
dat <- load_stmomo_data(dataset, "total")

# Loai giai doan chien tranh/bien dong lich su (truoc 1980) khoi uoc luong
# tham so - xem ghi chu trong config/params.yaml (fitting.years)
LCfit <- fit_model("lc", dat, cfg)
save_fit(LCfit, "lc", dataset)
