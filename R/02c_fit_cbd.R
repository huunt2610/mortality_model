# ============================================================
# 02c_fit_cbd.R — Fit Cairns-Blake-Dowd tren du lieu Viet Nam
# Input : data/processed/Dxt_total.csv, Ext_total.csv
# Output: models/cbd_fit.rds, data/processed/params_cbd_*.csv, residuals_cbd.csv
# ============================================================
library(StMoMo)
library(yaml)
source("R/01_load_data.R")
source("R/utils.R")

cfg <- yaml::read_yaml("config/params.yaml")
dat <- load_vn_data("total")

ages_cbd <- cfg$ages$cbd$min:cfg$ages$cbd$max
years_fit <- cfg$fitting$years$start:cfg$fitting$years$end

# CBD dung xac suat tu vong qxt (link logit) tren nhom tuoi gia
CBDfit <- fit(cbd(link = "logit"), Dxt = dat$Dxt, Ext = dat$Ext, ages = dat$ages,
              years = dat$years, ages.fit = ages_cbd, years.fit = years_fit)

saveRDS(CBDfit, "models/cbd_fit.rds")
export_params(CBDfit, "cbd")
export_fit_summary(CBDfit, "cbd")
