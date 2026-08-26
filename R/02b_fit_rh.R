# ============================================================
# 02b_fit_rh.R — Fit Renshaw-Haberman tren du lieu Viet Nam
# Input : data/processed/Dxt_total.csv, Ext_total.csv, models/lc_fit.rds
#         (dung lam starting values - chay R/02a_fit_lc.R truoc)
# Output: models/rh_fit.rds, data/processed/params_rh_*.csv, residuals_rh.csv
# ============================================================
library(StMoMo)
library(yaml)
source("R/01_load_data.R")
source("R/utils.R")

cfg <- yaml::read_yaml("config/params.yaml")
dat <- load_vn_data("total")

ages_lc <- cfg$ages$lc_rh$min:cfg$ages$lc_rh$max
years_fit <- cfg$fitting$years$start:cfg$fitting$years$end

if (!file.exists("models/lc_fit.rds")) {
  stop("Khong tim thay models/lc_fit.rds - chay R/02a_fit_lc.R truoc ",
       "(RH dung ket qua LC lam starting values de hoi tu on dinh hon)")
}
LCfit <- readRDS("models/lc_fit.rds")

# RH day du: log m_xt = ax + bx1*kt + bx0*g(t-x). Ban don gian hoa
# (cohortAgeFun = "1", tuc beta0 = 1) on dinh hon nhieu — khuyen nghi
# cua Haberman & Renshaw (2011). Dung ban nay lam mac dinh.
RH <- rh(link = "log", cohortAgeFun = "1", approxConst = TRUE)

# RH noi tieng kho hoi tu (Renshaw & Haberman 2006) vi 2 van de rieng biet:
# (1) nhan dang tham so - da xu ly boi rang buoc chuan hoa mac dinh cua rh()
#     (sum(bx)=1, mean(kt)=0, mean(gc)=0) cong them approxConst=TRUE (Hunt &
#     Villegas 2015: sum((c-mean(c))*gc)=0) de tach xu huong tuyen tinh khoi
#     gc, on dinh hoi tu hon; (2) cac cohort o vien Lexis diagram (nam sinh
#     dau/cuoi cua ages_lc x years_fit) co qua it quan sat, uoc luong gc rieng
#     cho chung khong on dinh so hoc - can loai bang trong so wxt (khuyen nghi
#     chuan trong vignette StMoMo, khong lien quan den rang buoc chuan hoa o
#     tren). clip=3 bo 3 cohort dau/cuoi.
wxt_rh <- genWeightMat(ages = ages_lc, years = years_fit, clip = 3)
RHfit <- fit(RH, Dxt = dat$Dxt, Ext = dat$Ext, ages = dat$ages, years = dat$years,
             ages.fit = ages_lc, years.fit = years_fit, wxt = wxt_rh,
             start.ax = LCfit$ax, start.bx = LCfit$bx, start.kt = LCfit$kt,
             iterMax  = 1e5)
if (!RHfit$conv) warning("RH khong hoi tu — thu doi starting values hoac thu hep pham vi tuoi/nam")

saveRDS(RHfit, "models/rh_fit.rds")
export_params(RHfit, "rh")
export_fit_summary(RHfit, "rh")
