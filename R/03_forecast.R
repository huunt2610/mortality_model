# 03_forecast.R — Du bao kt (RWD/ARIMA), gamma_c (ARIMA), mo phong khoang tin cay
library(StMoMo); library(yaml)
cfg <- yaml::read_yaml("config/params.yaml")
h <- cfg$forecast$horizon; nsim <- cfg$forecast$n_simulations

LCfit  <- readRDS("models/lc_fit.rds")
RHfit  <- readRDS("models/rh_fit.rds")
CBDfit <- readRDS("models/cbd_fit.rds")

LCfor  <- forecast(LCfit,  h = h)                          # mac dinh: RWD cho kt
RHfor  <- forecast(RHfit,  h = h, gc.order = c(1, 1, 0))   # ARIMA cho cohort
CBDfor <- forecast(CBDfit, h = h)                          # MRWD cho (kt1, kt2)

# Mo phong de tinh khoang tin cay (dung cho fan chart + pricing)
LCsim <- simulate(LCfit, nsim = nsim, h = h)
saveRDS(list(LCfor = LCfor, RHfor = RHfor, CBDfor = CBDfor, LCsim = LCsim),
        "models/forecasts.rds")

# Export tỷ suất tử vong dự báo (trung vị) cho Python vẽ hình
write.csv(LCfor$rates,  "data/processed/forecast_rates_lc.csv")
write.csv(RHfor$rates,  "data/processed/forecast_rates_rh.csv")
write.csv(CBDfor$rates, "data/processed/forecast_rates_cbd.csv")
