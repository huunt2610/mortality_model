# ============================================================
# 03_forecast.R — Du bao kt (RWD/ARIMA), gamma_c (ARIMA), mo phong khoang tin cay
# Chay  : Rscript R/03_forecast.R [dataset]
# Input : models/<dataset>/<model>_fit.rds (moi mo hinh trong `models:` da duoc fit)
# Output: models/<dataset>/forecasts.rds, results/<dataset>/forecast_rates_<model>.csv
# ============================================================
source("R/lib/load_data.R")
source("R/lib/models.R")

cfg <- load_config()
dataset <- get_dataset(cfg)
h <- cfg$forecast$horizon
nsim <- cfg$forecast$n_simulations

fit_paths <- file.path(models_dir(dataset), sprintf("%s_fit.rds", names(cfg$models)))
names(fit_paths) <- names(cfg$models)
fit_paths <- fit_paths[file.exists(fit_paths)]
if (length(fit_paths) == 0) {
  stop("Chua co fit nao trong ", models_dir(dataset), " - chay R/02*_fit_*.R truoc")
}

forecasts <- list()
for (name in names(fit_paths)) {
  f <- readRDS(fit_paths[[name]])
  forecasts[[name]] <- forecast_model(f, name, h)
  # Export ty suat tu vong du bao (trung vi) cho Python ve hinh.
  # Luu y: LC/RH/APC tra ve m(x,t); CBD/M7 (link logit) tra ve q(x,t)
  write.csv(forecasts[[name]]$rates,
            file.path(results_dir(dataset), sprintf("forecast_rates_%s.csv", name)))
}

# Mo phong de tinh khoang tin cay (dung cho fan chart + pricing)
sims <- list()
if ("lc" %in% names(fit_paths)) sims$lc <- simulate(readRDS(fit_paths[["lc"]]), nsim = nsim, h = h)
saveRDS(list(forecasts = forecasts, sims = sims), file.path(models_dir(dataset), "forecasts.rds"))
