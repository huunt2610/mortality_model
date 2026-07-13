# 04_backtest.R — Out-of-sample backtest theo cac split trong config/params.yaml
# Voi moi split: refit tren nam <= train_end, du bao den test_end,
# xuat sai so tung tuoi-nam ra CSV de src/evaluation tinh RMSE/MAPE.
library(StMoMo); library(yaml)
source("R/01_load_data.R")
cfg  <- yaml::read_yaml("config/params.yaml")
dat  <- load_vn_data("total")

run_split <- function(train_end, test_end) {
  yr_tr <- dat$years[dat$years <= train_end]
  h     <- test_end - train_end
  amin  <- cfg$ages$lc_rh$min; amax <- cfg$ages$lc_rh$max
  fitLC <- fit(lc(), Dxt = dat$Dxt, Ext = dat$Ext, ages = dat$ages,
               years = dat$years, ages.fit = amin:amax, years.fit = yr_tr)
  forLC <- forecast(fitLC, h = h)
  actual <- (dat$Dxt / dat$Ext)[as.character(amin:amax),
                                as.character((train_end + 1):test_end)]
  err <- log(forLC$rates) - log(actual)
  write.csv(err, sprintf("data/processed/backtest_lc_%d_%d.csv", train_end, test_end))
  # TODO: lap lai cho RH va CBD (chu y RH co the khong hoi tu tren tap ngan hon)
}
for (s in cfg$backtest$splits) run_split(s$train_end, s$test_end)
