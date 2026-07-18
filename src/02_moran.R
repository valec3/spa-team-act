# 02_moran.R — Moran I Global, Moran Local / LISA, scatterplots y mapas
# Replica metodologica Alonso-Pastor et al. (2025)
# Aplicado a 128 distritos de Lima (replica regional)
cat("=== 02_moran.R — Inicio ===\n")

library(sf)
library(spdep)
library(ggplot2)
library(dplyr)
library(RColorBrewer)

# ── 1. Cargar datos procesados ───────────────────────────────────
shp <- readRDS("data/processed/shp_distrital.rds")
cat("Shapefile cargado:", nrow(shp), "features\n")
cat("Columnas disponibles:\n")
cols_interes <- c("NSE", "pobreza", "ece_leng_sc", "ece_mate_sc", 
                   "ece_leng_sat_sc", "ece_mate_sat_sc", "nbi_1mas")
cols_presentes <- cols_interes[cols_interes %in% names(shp)]
cat("  ", paste(cols_presentes, collapse=", "), "\n")

# ── 2. Filtrar distritos con datos ────────────────────────────────
# Para Moran necesitamos que los distritos sin datos NO esten en la matriz
vars_analisis <- intersect(cols_presentes, c("NSE", "pobreza", "ece_leng_sc", "ece_mate_sc"))

for (var in vars_analisis) {
  na_count <- sum(is.na(shp[[var]]))
  cat(sprintf("  NA en %s: %d / %d\n", var, na_count, nrow(shp)))
}

# Tomamos solo distritos con NSE (la variable principal)
shp_ok <- shp[!is.na(shp$NSE), ]
cat("\nDistritos con datos completos (NSE):", nrow(shp_ok), "\n")

# ── 3. Matriz de pesos espaciales W ──────────────────────────────
# Paper: Queen contiguity, orden 1 (compartmenten frontera O vertice)
cat("\n=== Matriz de pesos (Queen, order 1) ===\n")

nb <- poly2nb(shp_ok, queen = TRUE)
cat("  Vecinos: min", min(card(nb)), "max", max(card(nb)), 
    "media", round(mean(card(nb)), 1), "mediana", median(card(nb)), "\n")

# Estandarizar por filas (como el paper: S0 = n)
lw <- nb2listw(nb, style = "W", zero.policy = TRUE)
cat("  Pesos estandarizados por filas (style='W')\n")

# ── 4. Moran I Global para NSE y Pobreza ─────────────────────────
cat("\n=== Moran I Global (999 permutaciones, alpha=0.05) ===\n")

resultados_moran <- list()

for (var in vars_analisis) {
  x <- shp_ok[[var]]
  if (all(is.na(x))) next
  
  mt <- moran.test(x, lw, randomisation = TRUE, zero.policy = TRUE, 
                    alternative = "two.sided")
  
  # Permutacion Monte Carlo (999 reps como el paper)
  mc <- moran.mc(x, lw, nsim = 999, zero.policy = TRUE, 
                  alternative = "two.sided")
  
  cat(sprintf("\n  --- %s ---\n", var))
  cat(sprintf("  I observado:  %.4f\n", mt$estimate[1]))
  cat(sprintf("  E[I] teorico: %.4f\n", mt$estimate[2]))
  cat(sprintf("  Z-valor:      %.4f\n", mt$statistic))
  cat(sprintf("  p-valor (MC): %.3f\n", mc$p.value))
  
  resultados_moran[[var]] <- list(
    variable = var,
    I = mt$estimate[1],
    EI = mt$estimate[2],
    Z = mt$statistic,
    p_teorico = mt$p.value,
    p_mc = mc$p.value
  )
}

# ── 5. Tabla resumen (tipo Cuadro 1 del paper) ───────────────────
cat("\n\n=== CUADRO 1: Indice I de Moran Univariante (Lima) ===\n")
cat(sprintf("%-20s %8s %8s %10s %8s\n", "Variable", "I Moran", "E[I]", "Z-Valor", "p (MC)"))
cat(strrep("-", 60), "\n")
for (r in resultados_moran) {
  cat(sprintf("%-20s %8.4f %8.4f %10.4f %8.3f\n", 
              r$variable, r$I, r$EI, r$Z, r$p_mc))
}

# Guardar tabla
tabla_moran <- do.call(rbind, lapply(resultados_moran, as.data.frame))
write.csv(tabla_moran, 
          "results/tables/cuadro1_moran_lima.csv",
          row.names = FALSE)

# ── 6. Scatterplot de Moran ──────────────────────────────────────
cat("\n=== Scatterplot de Moran ===\n")

for (var in vars_analisis[1:2]) {  # NSE + pobreza (los 2 principales)
  x <- shp_ok[[var]]
  x_scaled <- as.vector(scale(x))
  
  # Calcular lag espacial (Wz)
  lag <- lag.listw(lw, x_scaled, zero.policy = TRUE)
  
  # Dataframe para ggplot
  df_plot <- data.frame(
    z = x_scaled,
    Wz = lag,
    distrito = shp_ok$DISTRITO
  )
  
  # Identificar cuadrantes
  df_plot$cuadrante <- with(df_plot, 
    ifelse(z > 0 & Wz > 0, "AA",
    ifelse(z < 0 & Wz < 0, "BB",  
    ifelse(z > 0 & Wz < 0, "AB",
    ifelse(z < 0 & Wz > 0, "BA", "Centro"))))
  )
  
  # Moran I real
  I_val <- resultados_moran[[var]]$I
  
  p <- ggplot(df_plot, aes(x = z, y = Wz)) +
    geom_point(aes(color = cuadrante), alpha = 0.7, size = 2.5) +
    geom_smooth(method = "lm", se = TRUE, color = "darkred", linewidth = 0.8) +
    geom_hline(yintercept = 0, linetype = "dashed", alpha = 0.4) +
    geom_vline(xintercept = 0, linetype = "dashed", alpha = 0.4) +
    scale_color_manual(
      values = c("AA" = "#E74C3C", "BB" = "#2980B9", 
                 "AB" = "#F39C12", "BA" = "#27AE60", "Centro" = "grey70"),
      name = "Cuadrante"
    ) +
    labs(
      title = sprintf("Scatterplot de Moran — %s (Lima)", var),
      subtitle = sprintf("I de Moran = %.4f  |  999 permutaciones  |  alpha = 0.05", I_val),
      x = "Variable (z-score)",
      y = "Retraso espacial (Wz)"
    ) +
    theme_minimal(base_size = 13) +
    theme(
      plot.title = element_text(face = "bold"),
      legend.position = "bottom"
    )
  
  ggsave(
    sprintf("results/figures/moran_scatter_%s.png", var),
    p, width = 8, height = 7, dpi = 150, bg = "white"
  )
  cat(sprintf("  Guardado: moran_scatter_%s.png\n", var))
}

# ── 7. LISA — Local Moran ────────────────────────────────────────
cat("\n=== LISA — Local Moran (999 perms, alpha=0.05) ===\n")

for (var in vars_analisis[1:2]) {
  x <- shp_ok[[var]]
  
  # Local Moran
  locm <- localmoran(x, lw, zero.policy = TRUE, 
                      alternative = "two.sided")
  
  # Agregar al shapefile
  shp_ok$loc_I     <- locm[, "Ii"]
  shp_ok$loc_pval  <- locm[, "Pr(z != E(Ii))"]
  
  # Clasificar LISA (AA, BB, AB, BA, No sig)
  x_scaled <- as.vector(scale(x))
  lag_x <- lag.listw(lw, x_scaled, zero.policy = TRUE)
  
  shp_ok$lisa_cluster <- ifelse(shp_ok$loc_pval > 0.05, "No significativo",
    ifelse(x_scaled > 0 & lag_x > 0, "Alto-Alto (AA)",
    ifelse(x_scaled < 0 & lag_x < 0, "Bajo-Bajo (BB)",
    ifelse(x_scaled > 0 & lag_x < 0, "Alto-Bajo (AB)",
    ifelse(x_scaled < 0 & lag_x > 0, "Bajo-Alto (BA)", "No sig")))))
  
  # Contar por categoria
  cat(sprintf("\n  %s — Clusters LISA:\n", var))
  print(table(shp_ok$lisa_cluster))
  
  # ── Mapa LISA con ggplot2 ───────────────────────────────────
  pal_lisa <- c(
    "Alto-Alto (AA)"     = "#E74C3C",
    "Bajo-Bajo (BB)"     = "#2980B9",
    "Alto-Bajo (AB)"     = "#F39C12",
    "Bajo-Alto (BA)"     = "#27AE60",
    "No significativo"   = "#D5DBDB"
  )
  
  m <- ggplot(shp_ok) +
    geom_sf(aes(fill = lisa_cluster), color = "grey40", linewidth = 0.3) +
    scale_fill_manual(
      values = pal_lisa,
      name = NULL
    ) +
    labs(
      title = sprintf("Clústeres LISA — %s", var),
      subtitle = "Lima Metropolitana + Provincias  |  999 permutaciones  |  alpha = 0.05",
      caption = "Fuente: Mapa de Pobreza INEI 2018 — Replica metodologica Alonso-Pastor et al. (2025)"
    ) +
    theme_minimal(base_size = 12) +
    theme(
      plot.title = element_text(face = "bold"),
      legend.position = "bottom",
      axis.text = element_blank(),
      axis.ticks = element_blank(),
      panel.grid = element_blank()
    )
  
  ggsave(
    sprintf("results/figures/lisa_mapa_%s.png", var),
    m, width = 11, height = 9, dpi = 150, bg = "white"
  )
  cat(sprintf("  Mapa guardado: lisa_mapa_%s.png\n", var))
}

# ── 8. Resumen ──────────────────────────────────────────────────
cat("\n=== MVP COMPLETO ===\n")
cat("Resultados en:\n")
cat("  results/tables/cuadro1_moran_lima.csv\n")
cat("  results/figures/moran_scatter_NSE.png\n")
cat("  results/figures/moran_scatter_pobreza.png\n")
cat("  results/figures/lisa_mapa_NSE.png\n")
cat("  results/figures/lisa_mapa_pobreza.png\n")
