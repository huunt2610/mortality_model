# lib/models.R — Dinh nghia cac mo hinh ho GAPC va ham fit dung chung
# (docs/ban-do-tri-thuc-luan-van-du-bao-tu-vong.md, Muc 9)
#
#   lc  (M1): log m = ax + bx*kt
#   rh  (M2): log m = ax + bx1*kt + g(t-x)          (beta0 = 1)
#   apc (M3): log m = ax + kt + g(t-x)
#   cbd (M5): logit q = kt1 + kt2*(x - xbar)
#   m7      : logit q = kt1 + kt2*(x - xbar) + kt3*((x - xbar)^2 - s2) + g(t-x)
library(StMoMo)
library(forecast) # generic forecast() (StMoMo da Depends, khai bao tuong minh)

COHORT_MODELS <- c("rh", "apc", "m7")

model_spec <- function(name) {
  switch(name,
    lc  = lc(link = "log"),
    # RH day du: log m_xt = ax + bx1*kt + bx0*g(t-x). Ban don gian hoa
    # (cohortAgeFun = "1", tuc beta0 = 1) on dinh hon nhieu — khuyen nghi
    # cua Haberman & Renshaw (2011). Dung ban nay lam mac dinh.
    # approxConst = TRUE (Hunt & Villegas 2015: sum((c-mean(c))*gc)=0) tach xu
    # huong tuyen tinh khoi gc, on dinh hoi tu hon.
    rh  = rh(link = "log", cohortAgeFun = "1", approxConst = TRUE),
    apc = apc(link = "log"),
    cbd = cbd(link = "logit"),
    m7  = m7(link = "logit"),
    stop("Mo hinh '", name, "' chua duoc dinh nghia trong R/lib/models.R")
  )
}

model_ages <- function(name, cfg) {
  rng <- cfg$ages[[cfg$models[[name]]$ages]]
  rng$min:rng$max
}

fit_years <- function(cfg) cfg$fitting$years$start:cfg$fitting$years$end

# Fit mot mo hinh. `start`: fit LC dung lam starting values cho RH (RH noi tieng
# kho hoi tu - Renshaw & Haberman 2006).
fit_model <- function(name, dat, cfg, years_fit = fit_years(cfg), start = NULL) {
  ages_fit <- model_ages(name, cfg)
  args <- list(model_spec(name), Dxt = dat$Dxt, Ext = dat$Ext, ages = dat$ages,
               years = dat$years, ages.fit = ages_fit, years.fit = years_fit)
  if (name %in% COHORT_MODELS) {
    # Cac cohort o vien Lexis diagram co qua it quan sat, uoc luong gc rieng cho
    # chung khong on dinh so hoc - loai bang trong so wxt (khuyen nghi chuan
    # trong vignette StMoMo, khong lien quan den rang buoc chuan hoa cua mo hinh).
    args$wxt <- genWeightMat(ages = ages_fit, years = years_fit, clip = cfg$fitting$cohort_clip)
  }
  if (name == "rh") {
    args$iterMax <- 1e5
    if (!is.null(start)) {
      args$start.ax <- start$ax
      args$start.bx <- start$bx
      args$start.kt <- start$kt
    }
  }
  f <- do.call(fit, args)
  if (!f$conv) {
    warning(toupper(name), " khong hoi tu — thu doi starting values hoac thu hep pham vi tuoi/nam")
  }
  f
}

# Du bao: kt bang RWD (LC/RH/APC) / MRWD (CBD, M7); cohort bang ARIMA(1,1,0)
forecast_model <- function(f, name, h) {
  if (name %in% COHORT_MODELS) forecast(f, h = h, gc.order = c(1, 1, 0)) else forecast(f, h = h)
}
