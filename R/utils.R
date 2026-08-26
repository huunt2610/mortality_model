# utils.R — ham dung chung
# Ve heatmap residuals nhanh de chan doan hieu ung tuoi/nam/the he
plot_residual_heatmap <- function(fit, main = "") {
  res <- residuals(fit)
  image(x = res$years, y = res$ages, z = t(res$residuals),
        xlab = "Nam", ylab = "Tuoi", main = main,
        col = hcl.colors(21, "RdBu", rev = TRUE))
}

# StMoMo tra ve bx/kt dang ma tran voi dimname (vd. "1"), khien data.frame()
# ghi de ten cot argument bang dimname do (thanh "X1" sau make.names) - dat
# lai ten cot tuong minh truoc khi ghi CSV.
name_cols <- function(mat, base) {
  colnames(mat) <- if (ncol(mat) == 1) base else paste0(base, seq_len(ncol(mat)))
  mat
}

# Xuat tham so uoc luong (ax, bx, kt, gc) ra CSV - dung chung cho ca 3 script
# fit rieng le R/02a_fit_lc.R, R/02b_fit_rh.R, R/02c_fit_cbd.R.
export_params <- function(f, name) {
  if (!is.null(f$ax)) {
    bx_mat <- name_cols(as.matrix(f$bx), "bx")
    write.csv(data.frame(age = f$ages, ax = as.vector(f$ax), bx_mat, check.names = FALSE),
              sprintf("data/processed/params_%s_age.csv", name), row.names = FALSE)
  } else if (!is.null(f$bx)) {
    bx_mat <- name_cols(as.matrix(f$bx), "bx")
    write.csv(data.frame(age = f$ages, bx_mat, check.names = FALSE),
              sprintf("data/processed/params_%s_age.csv", name), row.names = FALSE)
  }
  kt_mat <- name_cols(t(as.matrix(f$kt)), "kt")
  write.csv(data.frame(year = f$years, kt_mat, check.names = FALSE),
            sprintf("data/processed/params_%s_kt.csv", name), row.names = FALSE)
  if (!is.null(f$gc)) write.csv(data.frame(cohort = f$cohorts, gc = as.vector(f$gc)),
                                sprintf("data/processed/params_%s_gc.csv", name), row.names = FALSE)
}

# Xuat residuals ra CSV (hinh chan doan bat buoc trong luan van) va in AIC/BIC
# - dung chung cho ca 3 script fit rieng le.
export_fit_summary <- function(f, name) {
  res <- residuals(f)
  write.csv(res$residuals, sprintf("data/processed/residuals_%s.csv", name))
  cat(sprintf("%s — AIC: %.1f | BIC: %.1f\n", toupper(name), AIC(f), BIC(f)))
}
