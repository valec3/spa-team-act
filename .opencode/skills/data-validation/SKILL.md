---
name: data-validation
description: >
  Validacion de calidad de datos. Ejecuta controles automaticos sobre datasets
  procesados: valores faltantes, outliers, rangos esperados, consistencia
  interna, y matching geografico. Genera reportes de validacion y alertas.
  Trigger: Cuando el usuario valida datos, verifica calidad, detecta anomalias,
  ejecuta controles pre-analisis, o necesita un reporte de calidad de datos.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Validar un dataset despues del preprocesamiento
- Detectar valores anomalos (outliers, missing patterns)
- Verificar consistencia entre variables relacionadas
- Validar matching geografico (UBIGEO, shapefile)
- Generar reporte de calidad de datos
- Decidir si un dataset esta listo para analisis
- Comparar calidad entre multiples datasets

## Critical Patterns

### Validation Dimensions (6 Checks)

```
VALIDACION DE DATOS — 6 dimensiones:

1. COMPLETITUD: % missing por variable, patrones de missing
2. RANGO: valores dentro de limites plausibles (min/max)
3. CONSISTENCIA: variables relacionadas no se contradicen
4. UNICIDAD: IDs duplicados, UBIGEOS repetidos
5. MATCHING: correspondencia con shapefile u otras fuentes
6. DISTRIBUCION: outliers, asimetria extrema, distribuciones anomalas
```

### Validation Rules Table

| Check | Variable type | Rule | Severity if failed |
|-------|--------------|------|-------------------|
| Missing % | Todas | missing < 5% | 🟠 MAYOR |
| Missing % | Key variables | missing < 1% | 🔴 BLOQUEANTE |
| Range | Proporcion | 0 ≤ x ≤ 1 | 🔴 BLOQUEANTE |
| Range | Conteo | x ≥ 0, integer | 🔴 BLOQUEANTE |
| Range | Z-score | -4 ≤ x ≤ 4 (99.99%) | 🟡 MENOR |
| Consistency | p_pobreza vs avg_ingreso | correlacion negativa esperada | 🟠 MAYOR |
| Consistency | N poblacion ≥ N estudiantes | por definicion | 🔴 BLOQUEANTE |
| Uniqueness | UBIGEO | sin duplicados | 🔴 BLOQUEANTE |
| Matching | UBIGEO vs shapefile | ≥ 95% match | 🟠 MAYOR |
| Distribution | Cualquiera | IQR outlier detection | 🟡 MENOR |

### Validation Report Template

```markdown
# Data Validation Report
## Dataset: cpv2017_distrital
## Fecha: 2024-07-18 | Stage: Preprocessing → Validacion

---

### Resumen
- Dimensiones: 1,874 filas × 23 columnas
- Checks ejecutados: 18
- Passed: 15 | Warnings: 2 | Failed: 1
- Estado: ⚠️ REQUIERE ATENCION (1 bloqueante)

---

### 1. Completitud

| Variable | Missing (N) | Missing (%) | Estado |
|----------|------------|-------------|--------|
| idx_nse | 0 | 0.0% | ✅ |
| p_pobreza | 9 | 0.5% | ✅ |
| avg_ingreso | 0 | 0.0% | ✅ |
| ece_matematica | 92 | 4.9% | ⚠️ Cerca del umbral |

---

### 2. Rangos

| Variable | Min | Max | Esperado | Estado |
|----------|-----|-----|----------|--------|
| p_pobreza | 0.00 | 0.89 | [0, 1] | ✅ |
| z_idx_nse | -2.34 | 3.12 | [-4, 4] | ✅ |
| avg_ingreso | 0 | 999999 | ≥ 0 | ❌ Max sospechoso (outlier?) |

🔴 BLOQUEANTE: avg_ingreso = 999,999 en UBIGEO 150101
   → Posible error de codificacion o outlier extremo.

---

### 3. Consistencia

| Check | Resultado | Estado |
|-------|-----------|--------|
| p_pobreza correlacion con avg_ingreso | r = -0.78 | ✅ (negativa esperada) |
| N_poblacion ≥ 0 en todos los distritos | OK | ✅ |

---

### 4. Matching Geografico

| Check | Resultado | Estado |
|-------|-----------|--------|
| UBIGEOs en datos vs shapefile | 128/128 (100%) | ✅ |
| Distritos sin vecinos espaciales | 1 (isla) | ⚠️ Documentado |

---

### Acciones Requeridas
1. 🔴 Revisar avg_ingreso = 999,999 en UBIGEO 150101
2. ⚠️ Documentar 92 missing en variables ECE (distritos sin datos)
```

### Automated Validation Script (Conceptual)

```r
# validate_dataset.R — Ejecuta todos los checks sobre un dataset procesado
validate_dataset <- function(data, dataset_id) {
  report <- list(
    dataset = dataset_id,
    timestamp = Sys.time(),
    checks = list()
  )

  # 1. Completitud
  report$checks$completeness <- data %>%
    summarise(across(everything(), ~ sum(is.na(.)) / n() * 100))

  # 2. Rangos
  report$checks$ranges <- check_ranges(data, get_expected_ranges(dataset_id))

  # 3. Consistencia
  report$checks$consistency <- check_consistency(data)

  # 4. Unicidad
  report$checks$uniqueness <- check_duplicates(data, "ubigeo")

  # 5. Matching
  report$checks$matching <- check_geographic_match(data)

  # 6. Distribucion
  report$checks$distribution <- check_outliers(data)

  report$status <- if (any_blocking_issues(report)) "FAIL" else "PASS"
  return(report)
}
```

### Outlier Detection Methods

```
METODO 1: IQR (Interquartile Range)
  outlier si: x < Q1 - 1.5*IQR  OR  x > Q3 + 1.5*IQR
  Uso: distribuciones no necesariamente normales
  Severidad: 🟡 MENOR (marcar, no eliminar automaticamente)

METODO 2: Z-score
  outlier si: |z| > 3
  Uso: distribuciones aproximadamente normales
  Severidad: 🟡 MENOR

METODO 3: Rango esperado (domain knowledge)
  outlier si: x fuera de [min_plausible, max_plausible]
  Uso: variables con limites naturales (proporciones, edades)
  Severidad: 🔴 BLOQUEANTE (posible error de datos)
```

## Pipeline Integration

```
data-preprocessing (Stage 3: transform)
  │
  ▼
data-validation (Stage 4: validate)
  │
  ├── PASS → dataset listo para method-library
  └── FAIL → volver a data-preprocessing para correccion
```

## Rules for This Project

1. **Validar antes de analizar.** Ningun paper usa datos no validados.
2. **Reporte versionado.** Guardar en `datasets/<id>/processed/validation_report.md`.
3. **Outliers: marcar, no eliminar.** La decision de excluir outliers es metodologica, no automatica.
4. **Matching geografico ≥ 95%.** Si es menor, documentar distritos faltantes.
5. **Bloqueante = no avanza.** Un solo check bloqueante detiene el pipeline.
