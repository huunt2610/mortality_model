# lib/export.R — Luu fit va xuat ket qua ra results/<dataset>/ cho Python doc
# (can source R/lib/load_data.R truoc - results_dir/models_dir dinh nghia o do, nen
# object_usage_linter khong thay duoc va phai nolint)

# StMoMo tra ve bx/kt dang ma tran voi dimname (vd. "1"), khien data.frame()
# ghi de ten cot argument bang dimname do (thanh "X1" sau make.names) - dat
# lai ten cot tuong minh truoc khi ghi CSV.
name_cols <- function(mat, base) {
  colnames(mat) <- if (ncol(mat) == 1) base else paste0(base, seq_len(ncol(mat)))
  mat
}

# Xuat tham so uoc luong (ax, bx, kt, gc) ra CSV
export_params <- function(f, name, dataset) {
  out_dir <- results_dir(dataset) # nolint: object_usage_linter.
  out <- function(suffix) file.path(out_dir, sprintf("params_%s_%s.csv", name, suffix))
  if (!is.null(f$ax)) {
    age_df <- data.frame(age = f$ages, ax = as.vector(f$ax), check.names = FALSE)
    if (!is.null(f$bx)) age_df <- cbind(age_df, name_cols(as.matrix(f$bx), "bx"))
    write.csv(age_df, out("age"), row.names = FALSE)
  } else if (!is.null(f$bx)) {
    bx_mat <- name_cols(as.matrix(f$bx), "bx")
    write.csv(data.frame(age = f$ages, bx_mat, check.names = FALSE), out("age"), row.names = FALSE)
  }
  kt_mat <- name_cols(t(as.matrix(f$kt)), "kt")
  write.csv(data.frame(year = f$years, kt_mat, check.names = FALSE), out("kt"), row.names = FALSE)
  if (!is.null(f$gc)) {
    write.csv(data.frame(cohort = f$cohorts, gc = as.vector(f$gc)), out("gc"), row.names = FALSE)
  }
}

# Xuat residuals ra CSV (hinh chan doan bat buoc trong luan van) va in AIC/BIC
export_fit_summary <- function(f, name, dataset) {
  res <- residuals(f)
  out_dir <- results_dir(dataset) # nolint: object_usage_linter.
  write.csv(res$residuals, file.path(out_dir, sprintf("residuals_%s.csv", name)))
  cat(sprintf("%s [%s] — AIC: %.1f | BIC: %.1f\n", toupper(name), dataset, AIC(f), BIC(f)))
}

# Luu .rds + xuat params/residuals - dung chung cho cac script R/02*_fit_*.R
save_fit <- function(f, name, dataset) {
  model_dir <- models_dir(dataset) # nolint: object_usage_linter.
  saveRDS(f, file.path(model_dir, sprintf("%s_fit.rds", name)))
  export_params(f, name, dataset)
  export_fit_summary(f, name, dataset)
}
