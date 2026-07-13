# 01_load_data.R — Doc Dxt/Ext tu data/processed va tao StMoMoData
# (duoc source boi cac script khac; giu logic doc du lieu o MOT noi)
library(StMoMo)
load_vn_data <- function(series = "total") {
  Dxt <- as.matrix(read.csv(sprintf("data/processed/Dxt_%s.csv", series),
                            row.names = 1, check.names = FALSE))
  Ext <- as.matrix(read.csv(sprintf("data/processed/Ext_%s.csv", series),
                            row.names = 1, check.names = FALSE))
  structure(list(Dxt = Dxt, Ext = Ext,
                 ages = as.numeric(rownames(Dxt)),
                 years = as.numeric(colnames(Dxt)),
                 type = "central", series = series, label = "Vietnam"),
            class = "StMoMoData")
}
