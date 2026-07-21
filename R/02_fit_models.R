# ============================================================
# 02_fit_models.R — Fit LC, RH, CBD trên du lieu Viet Nam
# Input : data/processed/Dxt.csv, Ext.csv (hang = tuoi, cot = nam)
# Output: models/*.rds, data/processed/params_*.csv, residuals_*.csv
# ============================================================
library(StMoMo)
library(yaml)

cfg <- yaml::read_yaml("config/params.yaml")

# ---- 1. Doc du lieu ----------------------------------------
# Dung series "total" (ca hai gioi) lam mac dinh cho LC/RH/CBD chinh;
# doi ten file (vd. Dxt_male.csv) neu fit rieng theo gioi tinh.
Dxt <- as.matrix(read.csv("data/processed/Dxt_total.csv", row.names = 1, check.names = FALSE))
Ext <- as.matrix(read.csv("data/processed/Ext_total.csv", row.names = 1, check.names = FALSE))
ages  <- as.numeric(rownames(Dxt))
years <- as.numeric(colnames(Dxt))

# ---- 2. Dinh nghia mo hinh ---------------------------------
LC  <- lc(link = "log")
# RH day du: log m_xt = ax + bx1*kt + bx0*g(t-x). Ban don gian hoa
# (cohortAgeFun = "1", tuc beta0 = 1) on dinh hon nhieu — khuyen nghi
# cua Haberman & Renshaw (2011). Dung ban nay lam mac dinh.
RH  <- rh(link = "log", cohortAgeFun = "1", approxConst = TRUE)
CBD <- cbd(link = "logit")

# ---- 3. Fit ------------------------------------------------
ages_lc  <- cfg$ages$lc_rh$min:cfg$ages$lc_rh$max
ages_cbd <- cfg$ages$cbd$min:cfg$ages$cbd$max

LCfit <- fit(LC, Dxt = Dxt, Ext = Ext, ages = ages, years = years,
             ages.fit = ages_lc)

# RH noi tieng kho hoi tu: khoi tao tu ket qua LC, tang so vong lap.
RHfit <- fit(RH, Dxt = Dxt, Ext = Ext, ages = ages, years = years,
             ages.fit = ages_lc,
             start.ax = LCfit$ax, start.bx = LCfit$bx, start.kt = LCfit$kt,
             iterMax  = 1e5)
if (!RHfit$conv) warning("RH khong hoi tu — thu doi starting values hoac thu hep pham vi tuoi/nam")

# CBD dung xac suat tu vong qxt (link logit) tren nhom tuoi gia
CBDfit <- fit(CBD, Dxt = Dxt, Ext = Ext, ages = ages, years = years,
              ages.fit = ages_cbd)

# ---- 4. Luu ket qua ----------------------------------------
saveRDS(LCfit,  "models/lc_fit.rds")
saveRDS(RHfit,  "models/rh_fit.rds")
saveRDS(CBDfit, "models/cbd_fit.rds")

export_params <- function(f, name) {
  if (!is.null(f$ax)) write.csv(data.frame(age = f$ages, ax = f$ax, bx = f$bx),
                                sprintf("data/processed/params_%s_age.csv", name), row.names = FALSE)
  write.csv(data.frame(year = f$years, t(f$kt)),
            sprintf("data/processed/params_%s_kt.csv", name), row.names = FALSE)
  if (!is.null(f$gc)) write.csv(data.frame(cohort = f$cohorts, gc = f$gc),
                                sprintf("data/processed/params_%s_gc.csv", name), row.names = FALSE)
}
export_params(LCfit, "lc"); export_params(RHfit, "rh"); export_params(CBDfit, "cbd")

# Residuals de ve heatmap chan doan (hinh bat buoc trong luan van)
for (m in list(lc = LCfit, rh = RHfit, cbd = CBDfit)) {}
res_lc  <- residuals(LCfit);  write.csv(res_lc$residuals,  "data/processed/residuals_lc.csv")
res_rh  <- residuals(RHfit);  write.csv(res_rh$residuals,  "data/processed/residuals_rh.csv")
res_cbd <- residuals(CBDfit); write.csv(res_cbd$residuals, "data/processed/residuals_cbd.csv")

# In-sample information criteria
cat(sprintf("AIC  — LC: %.1f | RH: %.1f | CBD: %.1f\n", AIC(LCfit), AIC(RHfit), AIC(CBDfit)))
cat(sprintf("BIC  — LC: %.1f | RH: %.1f | CBD: %.1f\n", BIC(LCfit), BIC(RHfit), BIC(CBDfit)))
