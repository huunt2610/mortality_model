# ============================================================
# 02c_fit_cbd.R — Fit Cairns-Blake-Dowd (M5)
# Chay  : Rscript R/02c_fit_cbd.R [dataset]
# Input : data/processed/<dataset>/Dxt_total.csv, Ext_total.csv
# Output: models/<dataset>/cbd_fit.rds, results/<dataset>/params_cbd_*.csv, residuals_cbd.csv
# ============================================================
source("R/lib/load_data.R")
source("R/lib/models.R")
source("R/lib/export.R")

cfg <- load_config()
dataset <- get_dataset(cfg)
dat <- load_stmomo_data(dataset, "total")

# CBD dung xac suat tu vong qxt (link logit) tren nhom tuoi gia (ages.cbd)
CBDfit <- fit_model("cbd", dat, cfg)
save_fit(CBDfit, "cbd", dataset)
