# lib/load_data.R — Doc cau hinh, quy uoc duong dan theo dataset, doc Dxt/Ext thanh StMoMoData
# (duoc source boi cac script khac; giu logic doc du lieu o MOT noi)
#
# Moi dataset (khai bao o `datasets:` trong config/params.yaml) co thu muc rieng:
#   data/processed/<dataset>/  input (Dxt, Ext, mx)
#   models/<dataset>/          object da fit (.rds)
#   results/<dataset>/         params, residuals, forecast, backtest (CSV cho Python doc)
library(StMoMo)
library(yaml)

load_config <- function() yaml::read_yaml("config/params.yaml")

# Dataset lay tu tham so dong lenh (Rscript R/02a_fit_lc.R hmd_jpn), mac dinh
# `default_dataset` trong config
get_dataset <- function(cfg) {
  args <- commandArgs(trailingOnly = TRUE)
  dataset <- if (length(args) >= 1) args[1] else cfg$default_dataset
  if (is.null(cfg$datasets[[dataset]])) {
    stop("Dataset '", dataset, "' khong co trong config/params.yaml (datasets:)")
  }
  dataset
}

processed_dir <- function(dataset) file.path("data", "processed", dataset)

models_dir <- function(dataset) {
  d <- file.path("models", dataset)
  dir.create(d, recursive = TRUE, showWarnings = FALSE)
  d
}

results_dir <- function(dataset) {
  d <- file.path("results", dataset)
  dir.create(d, recursive = TRUE, showWarnings = FALSE)
  d
}

load_stmomo_data <- function(dataset, series = "total") {
  read_mat <- function(kind) {
    as.matrix(read.csv(file.path(processed_dir(dataset), sprintf("%s_%s.csv", kind, series)),
                       row.names = 1, check.names = FALSE))
  }
  Dxt <- read_mat("Dxt")
  Ext <- read_mat("Ext")
  structure(list(Dxt = Dxt, Ext = Ext,
                 ages = as.numeric(rownames(Dxt)),
                 years = as.numeric(colnames(Dxt)),
                 type = "central", series = series, label = dataset),
            class = "StMoMoData")
}
