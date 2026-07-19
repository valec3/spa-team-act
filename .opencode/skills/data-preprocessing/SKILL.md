---
name: data-preprocessing
description: >
  Pipeline estandarizado de preprocesamiento de datos. Define el flujo:
  load → clean → transform → validate → output. Estandariza la preparacion
  de datos para todos los papers del repositorio. Trabaja con data-validation
  para controles de calidad.
  Trigger: Cuando el usuario necesita limpiar datos, preparar un dataset para
  analisis, estandarizar variables, imputar missing values, o ejecutar el
  pipeline de preprocesamiento.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Preparar un dataset raw para analisis
- Estandarizar nombres de variables y codigos
- Manejar valores perdidos (missing data)
- Detectar y tratar outliers
- Unir datasets (merge por UBIGEO u otra key)
- Agregar datos a nivel geografico (ej: individual → distrital)
- Validar que el output del preprocesamiento es correcto

## Critical Patterns

### Preprocessing Pipeline (5 Stages)

```
[raw] → [cleaned] → [transformed] → [validated] → [ready]

STAGE 1: LOAD
  - Leer archivos fuente (CSV, DTA, SHP)
  - Verificar encoding (UTF-8)
  - Registrar dimensiones iniciales (filas x columnas)

STAGE 2: CLEAN
  - Renombrar variables (snake_case estandar)
  - Filtrar filas invalidas (missing ID, duplicados)
  - Convertir tipos (factor → character, string → numeric)
  - Manejar codigos especiales (999 = missing, -99 = no aplica)

STAGE 3: TRANSFORM
  - Crear variables derivadas (densidad, tasas, indices)
  - Estandarizar (Z-score, min-max, log)
  - Agregar (individual → distrital: mean, sum, count)
  - Merge con shapefile (join por UBIGEO)
  - PCA (si aplica)

STAGE 4: VALIDATE (→ data-validation)
  - Missing data: % por variable, patrones
  - Rangos esperados: min/max plausibles
  - Consistencia: N despues de merge = N esperado
  - Outliers: IQR, Z-score > 3

STAGE 5: OUTPUT
  - Guardar en datasets/<id>/processed/
  - Guardar log de preprocesamiento
  - Actualizar N final en el catalogo
```

### Script Naming Convention

```
datasets/<id>/src/01_load.R       # STAGE 1
datasets/<id>/src/02_clean.R      # STAGE 2
datasets/<id>/src/03_transform.R  # STAGE 3
datasets/<id>/src/04_validate.R   # STAGE 4
```

### Variable Naming Standard

```
TODAS las variables en processed/ deben seguir:

- snake_case (lowercase con underscore)
- Sin acentos ni caracteres especiales
- Prefijos estandar:
  p_  = proporcion    (p_pobreza)
  n_  = conteo        (n_estudiantes)
  avg_ = promedio     (avg_ingreso)
  sd_ = desviacion    (sd_ingreso)
  idx_ = indice       (idx_nse)
  d_  = dummy/binaria (d_rural)
  cat_ = categorica   (cat_region)
  log_ = logaritmo    (log_ingreso)
  z_  = Z-score       (z_nse)

Ejemplos:
  avg_ingreso_laboral  (promedio de ingreso laboral por distrito)
  p_pobreza_extrema    (proporcion de pobreza extrema)
  idx_nse             (indice socioeconomico via PCA)
  z_idx_nse           (NSE estandarizado)
```

### Missing Data Decision Tree

```
¿Missing < 1%? → Listwise deletion (eliminar fila)
¿Missing 1-5%? → Segun patron:
  - MCAR (completamente aleatorio) → Listwise deletion o imputacion simple
  - MAR (aleatorio condicional) → Imputacion multiple (mice)
  - MNAR (no aleatorio) → Documentar sesgo, analisis de sensibilidad
¿Missing > 5%? → Evaluar exclusion de la variable
```

### Preprocessing Log Template

```yaml
# datasets/cpv2017/processed/preprocessing_log.yml
dataset: cpv2017
timestamp: "2024-07-18T10:30:00"
seed: 20240101

stages:
  load:
    files_read: ["cpv_27.dta", "enc_27.dta"]
    initial_rows: 23456789
    initial_cols: 145

  clean:
    rows_removed_duplicates: 0
    rows_removed_missing_id: 1234
    rows_after_clean: 23455555
    variables_renamed: 45
    missing_values_replaced: {ingreso: 0.3, educacion: 0.1}

  transform:
    level: "distrital"
    aggregation: "mean"
    n_after_aggregation: 1874
    variables_derived: ["idx_nse", "p_pobreza"]
    merge_shapefile: true
    n_after_merge: 1874

  validate:
    missing_pct: {idx_nse: 0.0, p_pobreza: 0.5}
    outliers_detected: 12
    passed: true

output:
  file: "datasets/cpv2017/processed/cpv2017_distrital.rds"
  final_rows: 1874
  final_cols: 23
```

## Code Examples

### Standard Preprocessing Script (R)

```r
# =============================================================================
# datasets/cpv2017/src/03_transform.R
# Transformacion: individual → distrital + PCA para NSE
# =============================================================================

# --- STAGE 3: TRANSFORM ---
library(dplyr)
library(sf)

# Cargar datos limpios
df <- readRDS("datasets/cpv2017/processed/cpv2017_clean.rds")

# Agregar a nivel distrital
distrital <- df %>%
  group_by(ubigeo) %>%
  summarise(
    n_poblacion = n(),
    p_rural = mean(d_rural, na.rm = TRUE),
    avg_educacion = mean(anios_estudio, na.rm = TRUE),
    avg_ingreso = mean(ingreso_total, na.rm = TRUE),
    p_pobreza = mean(d_pobreza, na.rm = TRUE),
    .groups = "drop"
  )

# Merge con shapefile
shp <- st_read("datasets/shapefiles/distrital/DISTRITOS.shp")
shp_distrital <- shp %>%
  left_join(distrital, by = c("UBIGEO" = "ubigeo"))

# Guardar
saveRDS(shp_distrital, "datasets/cpv2017/processed/cpv2017_distrital.rds")
```

## Pipeline Integration

```
data-catalog (elige dataset)
  │
  ▼
data-preprocessing (prepara datos)
  │
  ├──→ data-validation (valida calidad)
  │
  ▼
method-library (aplica metodos sobre datos limpios)
  │
  ▼
paper-factory (genera paper)
```

## Rules for This Project

1. **Reproducible siempre.** Scripts ejecutables de principio a fin, sin pasos manuales.
2. **Semilla fija.** `set.seed()` en cada script que involucre aleatoriedad.
3. **Raw inmutable.** `raw/` nunca se modifica; todo output va a `processed/`.
4. **Log obligatorio.** Cada ejecucion genera un log YAML con lo que paso.
5. **Validacion integrada.** El Stage 4 llama a data-validation automaticamente.
6. **Un script por stage.** No mezclar load + clean + transform en un solo archivo.
