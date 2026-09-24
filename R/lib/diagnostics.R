# lib/diagnostics.R — Chan doan ad-hoc trong R (hinh luan van ve bang Python, xem
# src/visualization/plots.py)

# Ve heatmap residuals nhanh de chan doan hieu ung tuoi/nam/the he
plot_residual_heatmap <- function(fit, main = "") {
  res <- residuals(fit)
  image(x = res$years, y = res$ages, z = t(res$residuals),
        xlab = "Nam", ylab = "Tuoi", main = main,
        col = hcl.colors(21, "RdBu", rev = TRUE))
}
