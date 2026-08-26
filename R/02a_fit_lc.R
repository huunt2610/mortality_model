# ============================================================
# 02a_fit_lc.R — Fit Lee-Carter tren du lieu Viet Nam
# Input : data/processed/Dxt_total.csv, Ext_total.csv
# Output: models/lc_fit.rds, data/processed/params_lc_*.csv, residuals_lc.csv
# ============================================================
library(StMoMo)
library(yaml)
source("R/01_load_data.R")
source("R/utils.R")

cfg <- yaml::read_yaml("config/params.yaml")
dat <- load_vn_data("total")

ages_lc <- cfg$ages$lc_rh$min:cfg$ages$lc_rh$max
# Loai giai doan chien tranh/bien dong lich su (truoc 1980) khoi uoc luong
# tham so - xem ghi chu trong config/params.yaml (fitting.years)
years_fit <- cfg$fitting$years$start:cfg$fitting$years$end

LCfit <- fit(lc(link = "log"), Dxt = dat$Dxt, Ext = dat$Ext, ages = dat$ages,
             years = dat$years, ages.fit = ages_lc, years.fit = years_fit)

saveRDS(LCfit, "models/lc_fit.rds")
export_params(LCfit, "lc")
export_fit_summary(LCfit, "lc")
