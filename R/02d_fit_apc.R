# ============================================================
# 02d_fit_apc.R — Fit Age-Period-Cohort (M3)
# Chay  : Rscript R/02d_fit_apc.R [dataset]
# Input : data/processed/<dataset>/Dxt_total.csv, Ext_total.csv
# Output: models/<dataset>/apc_fit.rds, results/<dataset>/params_apc_*.csv, residuals_apc.csv
# ============================================================
source("R/lib/load_data.R")
source("R/lib/models.R")
source("R/lib/export.R")

cfg <- load_config()
dataset <- get_dataset(cfg)
dat <- load_stmomo_data(dataset, "total")

# APC on dinh hon RH (it tham so hon) - doi chung cho RH khi chuoi ngan
APCfit <- fit_model("apc", dat, cfg)
save_fit(APCfit, "apc", dataset)
