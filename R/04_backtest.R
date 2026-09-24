# ============================================================
# 04_backtest.R — Out-of-sample backtest theo cac split trong config/params.yaml
# Chay  : Rscript R/04_backtest.R [dataset]
# Voi moi split va moi mo hinh trong `backtest.models`: refit tren train_start..train_end,
# du bao den test_end, xuat sai so log tung tuoi-nam ra
# results/<dataset>/backtest_<model>_<train_end>_<test_end>.csv de src/evaluation tinh RMSE/MAPE.
# ============================================================
source("R/lib/load_data.R")
source("R/lib/models.R")

cfg <- load_config()
dataset <- get_dataset(cfg)
dat <- load_stmomo_data(dataset, "total")

for (name in cfg$backtest$models) {
  ages_fit <- model_ages(name, cfg)
  for (s in cfg$backtest$splits) {
    yr_tr <- dat$years[dat$years >= s$train_start & dat$years <= s$train_end]
    # RH khoi tao tu LC refit tren cung tap train (chu y RH co the khong hoi tu tren tap ngan)
    start <- if (name == "rh") fit_model("lc", dat, cfg, years_fit = yr_tr) else NULL
    f <- fit_model(name, dat, cfg, years_fit = yr_tr, start = start)
    fc <- forecast_model(f, name, h = s$test_end - s$train_end)

    mx <- (dat$Dxt / dat$Ext)[as.character(ages_fit), as.character((s$train_end + 1):s$test_end)]
    # So sanh cung dai luong: link logit du bao q(x,t) = 1 - exp(-m(x,t))
    actual <- if (cfg$models[[name]]$link == "logit") 1 - exp(-mx) else mx
    err <- log(fc$rates) - log(actual)
    write.csv(err, file.path(results_dir(dataset),
                             sprintf("backtest_%s_%d_%d.csv", name, s$train_end, s$test_end)))
  }
}
