# Cai dat cac package R can thiet cho luan van
pkgs <- c("StMoMo",            # LC, RH, CBD, APC, M7 — cong cu chinh
          "demography",        # doc du lieu demogdata, lifetable
          "forecast",          # ARIMA cho kt, gamma_c
          "mgcv",              # P-splines lam tron (thay MortalitySmooth)
          "fanplot",           # fan chart cho du bao
          "lifecontingencies", # tinh phi bao hiem, annuity tu bang song
          "yaml")
install.packages(setdiff(pkgs, rownames(installed.packages())),
                 repos = "https://cloud.r-project.org")
