# ============================================================
# 02e_fit_m7.R — Fit M7 (CBD + cong bac hai + cohort) - TUY CHON
# Chay  : Rscript R/02e_fit_m7.R [dataset]
# Input : data/processed/<dataset>/Dxt_total.csv, Ext_total.csv
# Output: models/<dataset>/m7_fit.rds, results/<dataset>/params_m7_*.csv, residuals_m7.csv
# ============================================================
source("R/lib/load_data.R")
source("R/lib/models.R")
source("R/lib/export.R")

cfg <- load_config()
dataset <- get_dataset(cfg)
dat <- load_stmomo_data(dataset, "total")

M7fit <- fit_model("m7", dat, cfg)
save_fit(M7fit, "m7", dataset)
