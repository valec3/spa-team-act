# 01_carga.R — Carga, agrega a distrito y construye NSE para el MVP
# Replica metodológica Alonso-Pastor et al. (2025)
cat("=== 01_carga.R — Inicio ===\n")

library(haven)
library(dplyr)
library(sf)
library(tidyr)

# ── 1. Cargar datos ──────────────────────────────────────────────
cat("Cargando cpv_27.dta (1 GB, puede tardar ~30s)...\n")
d_raw <- read_dta("data/raw/cpv_27.dta")
cat("  Filas:", nrow(d_raw), "| Columnas:", ncol(d_raw), "\n")

# ── 2. Explorar estructura: qué columnas hay realmente ───────────
cat("\n=== Estructura del dataset ===\n")

# Verificar si hay columnas ya agregadas a UBIGEO (prefijo ubi_)
ubi_cols <- names(d_raw)[grep("^ubi_", names(d_raw))]
cat("Columnas con prefijo 'ubi_':", length(ubi_cols), "\n")
if (length(ubi_cols) > 0) print(head(ubi_cols, 20))

# Verificar distribucion de idubigeo
n_distritos <- length(unique(d_raw$idubigeo))
cat("Distritos unicos (idubigeo):", n_distritos, "\n")
cat("Filas por distrito (rango):", min(table(d_raw$idubigeo)), "-", max(table(d_raw$idubigeo)), "\n")

# ── 3. Identificar variables clave para NSE y logro ──────────────
# Paper original: ISE = PCA sobre educacion padres, materiales vivienda,
#                  servicios basicos, activos del hogar
# Nosotros construimos NSE con las variables disponibles

# Variables que queremos explorar:
vars_nse <- c(
  "idubigeo",
  # Educacion
  "pyedujefe", "pyedujefe2", "pyeducony", "preduprim1", "predusec1",
  "pranalfab", "pranalfabh", "pranalfabm",
  # Vivienda (materiales)
  "vpared1", "vpiso1", "vtecho1",
  # Servicios basicos
  "vagua1", "vagua2", "vsshh1", "vserviv1", "valum",
  # Activos / TIC
  "htelefono", "hinternet", "hequipo1",
  # NBI
  "nbi_almenos1", "nbi1", "nbi2", "nbi3", "nbi4", "nbi5",
  # Pobreza
  "pobreza2013",
  # ECE (puntajes estandarizados distritales?)
  "ece_lengua_inicio_MZ", "ece_lengua_satisf_MZ",
  "ece_mate_inicio_MZ", "ece_mate_satisf_MZ"
)

# Verificar cuales existen realmente
vars_existen <- vars_nse[vars_nse %in% names(d_raw)]
vars_faltan  <- vars_nse[!vars_nse %in% names(d_raw)]
cat("\nVariables NSE encontradas:", length(vars_existen), "\n")
cat("Variables faltantes:", paste(vars_faltan, collapse=", "), "\n")

# ── 4. Agregar a nivel distrital ─────────────────────────────────
cat("\n=== Agregando a nivel distrital ===\n")

d_dist <- d_raw %>%
  select(all_of(vars_existen)) %>%
  group_by(idubigeo) %>%
  summarise(
    across(everything(), ~ mean(.x, na.rm = TRUE)),
    n_conglomerados = n(),
    .groups = "drop"
  )

cat("  Distritos resultantes:", nrow(d_dist), "\n")

# Renombrar columnas para claridad
d_dist <- d_dist %>%
  rename(
    UBIGEO    = idubigeo,
    edu_jefe  = pyedujefe,
    nbi_1mas  = nbi_almenos1,
    pobreza   = pobreza2013,
    ece_leng  = ece_lengua_inicio_MZ,
    ece_mate  = ece_mate_inicio_MZ,
    ece_leng_sat = ece_lengua_satisf_MZ,
    ece_mate_sat = ece_mate_satisf_MZ
  )

# ── 5. Construir NSE via PCA simplificado ────────────────────────
cat("\n=== Construyendo indice NSE ===\n")

# Seleccionamos variables para PCA (solo las que existen)
# Invertimos variables de carencia para que valores altos = mejor NSE
d_dist <- d_dist %>%
  mutate(
    # Vivienda: pared noble (vpared1), piso noble (vpiso1), techo noble (vtecho1)
    viv_material = (vpared1 + vpiso1 + vtecho1) / 3,
    # Servicios: agua red (vagua1), desague (vsshh1), electricidad (vserviv1)
    serv_basicos = (vagua1 + vsshh1 + vserviv1) / 3,
    # Invertir NBI (menos NBI = mejor)
    nse_inv_nbi = 1 - nbi_1mas / max(nbi_1mas, na.rm = TRUE),
    # Activos digitales
    tic_acceso = (htelefono + hinternet + hequipo1) / 3
  )

# PCA sobre variables de NSE
vars_pca <- c("edu_jefe", "viv_material", "serv_basicos", "tic_acceso", "nse_inv_nbi")
# Remover columnas con todo NA
vars_pca <- vars_pca[apply(d_dist[, vars_pca], 2, function(x) sum(!is.na(x)) > 0)]
cat("  Variables para PCA:", paste(vars_pca, collapse=", "), "\n")

pca_result <- prcomp(~ ., data = d_dist[, vars_pca], scale. = TRUE, na.action = na.omit)
d_dist$NSE <- predict(pca_result)[, 1]  # PC1 como indice NSE
# Estandarizar NSE (media=0, sd=1)
d_dist$NSE <- scale(d_dist$NSE)[, 1]

cat("  Varianza explicada PC1:", round(summary(pca_result)$importance[2, 1] * 100, 1), "%\n")

# ── 6. Preparar variables de logro educativo ─────────────────────
# El paper usa promedio distrital de puntajes ECE
# Nosotros ya tenemos ece_leng y ece_mate (probablemente en %)
# Si estan en rango 0-1, reescalamos a 0-100 para visualizacion

if (max(d_dist$ece_leng, na.rm = TRUE) <= 1) {
  d_dist <- d_dist %>%
    mutate(
      ece_leng_sc = ece_leng * 100,
      ece_mate_sc = ece_mate * 100,
      ece_leng_sat_sc = ece_leng_sat * 100,
      ece_mate_sat_sc = ece_mate_sat * 100
    )
} else {
  d_dist <- d_dist %>%
    mutate(
      ece_leng_sc = ece_leng,
      ece_mate_sc = ece_mate,
      ece_leng_sat_sc = ece_leng_sat,
      ece_mate_sat_sc = ece_mate_sat
    )
}

# ── 7. Cargar shapefile distrital ────────────────────────────────
cat("\n=== Cargando shapefile ===\n")
shp_path <- "data/geo/Distrital INEI 2023 geogpsperu SuyoPomalia.shp"
shp <- st_read(shp_path, quiet = TRUE)
cat("  Shapefile: ", nrow(shp), " features, ", ncol(shp), " columns\n")
cat("  Columnas shapefile:\n")
print(names(shp))

# Buscar columna UBIGEO (posibles nombres: UBIGEO, UBIGEO_INE, IDDIST, idubigeo, CODIGO)
col_ubigeo_shp <- grep("UBIGEO|IDDIST|CODIGO|idubigeo", toupper(names(shp)), value = TRUE)
cat("  Posibles columnas UBIGEO en shape:", paste(col_ubigeo_shp, collapse=", "), "\n")

# ── 8. Joinear datos al shapefile ────────────────────────────────
if (length(col_ubigeo_shp) > 0) {
  col_ubigeo <- col_ubigeo_shp[1]
  cat("\nUsando columna de union:", col_ubigeo, "\n")
} else {
  col_ubigeo <- names(shp)[1]
  cat("\nWARNING: No se encontro columna UBIGEO. Usando primera columna:", col_ubigeo, "\n")
}

# Estandarizar UBIGEO a character de 6 digitos
shp$UBIGEO_join <- as.character(shp[[col_ubigeo]])
shp$UBIGEO_join <- sprintf("%06d", as.numeric(shp$UBIGEO_join))

d_dist$UBIGEO <- sprintf("%06d", as.numeric(d_dist$UBIGEO))

cat("  UBIGEOs en comun:", sum(d_dist$UBIGEO %in% shp$UBIGEO_join), "/", nrow(d_dist), "\n")

# Joinear
shp_data <- shp %>%
  left_join(d_dist, by = c("UBIGEO_join" = "UBIGEO"))

cat("  Shape con datos:", nrow(shp_data), "filas\n")
cat("  NA en NSE:", sum(is.na(shp_data$NSE)), "/", nrow(shp_data), "\n")
cat("  NA en ECE Lengua:", sum(is.na(shp_data$ece_leng_sc)), "/", nrow(shp_data), "\n")

# ── 9. Guardar para el paso moran.R ──────────────────────────────
output_path <- "data/processed/shp_distrital.rds"
saveRDS(shp_data, output_path)
cat("\n=== Datos procesados guardados en:", output_path, " ===\n")
cat("Listo para 02_moran.R\n")
