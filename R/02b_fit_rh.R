# ============================================================
# 02b_fit_rh.R — Fit Renshaw-Haberman (M2, beta0 = 1)
# Chay  : Rscript R/02b_fit_rh.R [dataset]
# Input : data/processed/<dataset>/Dxt_total.csv, Ext_total.csv, models/<dataset>/lc_fit.rds
#         (dung lam starting values - chay R/02a_fit_lc.R truoc)
# Output: models/<dataset>/rh_fit.rds, results/<dataset>/params_rh_*.csv, residuals_rh.csv
# ============================================================
source("R/lib/load_data.R")
source("R/lib/models.R")
source("R/lib/export.R")

cfg <- load_config()
dataset <- get_dataset(cfg)
dat <- load_stmomo_data(dataset, "total")

lc_path <- file.path(models_dir(dataset), "lc_fit.rds")
if (!file.exists(lc_path)) {
  stop("Khong tim thay ", lc_path, " - chay R/02a_fit_lc.R ", dataset, " truoc ",
       "(RH dung ket qua LC lam starting values de hoi tu on dinh hon)")
}

# Chi tiet mo hinh, rang buoc va trong so wxt (clip cohort o vien): R/lib/models.R
RHfit <- fit_model("rh", dat, cfg, start = readRDS(lc_path))
save_fit(RHfit, "rh", dataset)
