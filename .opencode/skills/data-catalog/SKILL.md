---
name: data-catalog
description: >
  Registro y descubrimiento de datasets. Mantiene el catalogo maestro en
  datasets/catalog/catalog.yml con metadata completa de cada fuente de datos.
  Permite buscar datasets por variables, geografia, periodo, y calidad.
  Trigger: Cuando el usuario registra un nuevo dataset, busca datos disponibles,
  consulta metadata de datasets, o necesita saber que variables estan disponibles
  para analisis.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Registrar un nuevo dataset en el catalogo
- Buscar datasets por criterios (variable X, geografia Y, año Z)
- Consultar metadata: fuente, licencia, N, variables, calidad
- Verificar que datasets estan disponibles antes de planificar papers
- Documentar la procedencia de datos (obligatorio por regla del repo)
- Auditar cobertura de datos (que variables tenemos, cuales faltan)

## Critical Patterns

### Dataset Registration Protocol

TODO dataset nuevo en el repo DEBE registrarse en `datasets/catalog/catalog.yml` ANTES de usarse:

```
1. Identificar: fuente, licencia, formato
2. Descargar: colocar en datasets/<id>/raw/
3. Documentar: metadata completa en catalog.yml
4. Validar: calidad (missing, outliers, consistencia)
5. Publicar: commit con conventional commit
```

### Dataset Discovery Query Patterns

```
"¿Que datasets tienen variable de pobreza a nivel distrital?"
→ Buscar en catalog.yml: variables.category = "pobreza" AND geography.level = "distrital"

"¿Que datasets cubren el departamento de Lima?"
→ Buscar en catalog.yml: geography.coverage contiene "Lima"

"¿Que datasets son posteriores a 2015?"
→ Buscar en catalog.yml: temporal.year >= 2015

"¿Que datasets no se han usado en ningun paper?"
→ Buscar en catalog.yml: used_in = [] (vacio)
```

### Dataset Metadata Template

```yaml
- id: [short_id]                  # Unico, snake_case
  name: "[Nombre completo]"       # Titulo descriptivo
  source: "[Institucion]"         # Quien produjo los datos
  url: "[URL]"                    # Donde se descargan
  license: "[Tipo de licencia]"   # Restricciones de uso
  format: "[CSV | Stata | Shapefile | Excel]"
  files:                          # Archivos que componen el dataset
    - archivo1.dta
    - archivo2.dta
  geography:                      # Cobertura geografica
    level: "[distrital | provincial | departamental | nacional]"
    coverage: "[Peru | Lima | Nacional]"
    n_units: 1874
    shapefile: "[path si aplica]"
  temporal:                       # Cobertura temporal
    year: 2017
    type: "[cross-sectional | panel | time-series]"
  variables:                      # Variables disponibles
    - category: "[categoria]"
      names: ["var1", "var2"]
  used_in:                        # Papers que usan este dataset
    - "papers/replica_lima"
  notes: "[Notas adicionales]"
  quality:                        # Evaluacion de calidad
    completeness: "[Alta | Media | Baja]"
    missing_data: "[Descripcion]"
    known_issues: "[Problemas conocidos]"
```

### Dataset Quality Matrix

| Dimension | Excelente | Aceptable | Problematico |
|-----------|-----------|-----------|--------------|
| Completitud | <1% missing | 1-5% missing | >5% missing |
| Documentacion | README + codebook | Solo README | Sin documentacion |
| Procedencia | Fuente oficial + URL | Fuente conocida | Origen dudoso |
| Actualidad | <5 años | 5-10 años | >10 años |
| Formato | Estandar (CSV, DTA) | Convertible | Binario propietario |
| Matching geografico | UBIGEO exacto | Aproximado | Sin key geografica |

### Catalog Integrity Checks

```
[ ] Todo dataset en datasets/*/raw/ tiene entrada en catalog.yml
[ ] Toda entrada en catalog.yml tiene archivos en datasets/<id>/raw/
[ ] No hay datasets sin usar que sean redundantes
[ ] Licencias verificadas y compatibles con el uso
[ ] URLs de descarga funcionales
```

## Code Examples

### Registering a New Dataset

```yaml
# Agregar en datasets/catalog/catalog.yml bajo "datasets:"

  - id: enaho2022
    name: "Encuesta Nacional de Hogares 2022"
    source: "INEI"
    url: "https://proyectos.inei.gob.pe/microdatos/"
    license: "Uso público con atribución (INEI)"
    format: "Stata (.dta)"
    files:
      - enaho01-2022-100.dta
      - enaho01-2022-200.dta
      - enaho01-2022-300.dta
    geography:
      level: "distrital"
      coverage: "Nacional (Perú)"
      n_units: 1874
    temporal:
      year: 2022
      type: "cross-sectional"
    variables:
      - category: "ingresos"
        names: ["ingreso_total", "ingreso_laboral", "ingreso_no_laboral"]
      - category: "educación"
        names: ["nivel_educativo", "anios_estudio", "asistencia"]
      - category: "salud"
        names: ["seguro_salud", "enfermedad_cronica"]
    used_in: []
    notes: "ENAHO anual. Módulos 100 (características), 200 (ingresos), 300 (salud)."
    quality:
      completeness: "Alta (encuesta nacional representativa)"
      missing_data: "<2%, principalmente en módulo de ingresos"
      known_issues: "Factor de expansión requerido para inferencia poblacional"
```

### Dataset Discovery (conceptual)

```python
# Buscar datasets con variable "pobreza" a nivel distrital después de 2015
def find_datasets(catalog, variable=None, level=None, year_min=None):
    results = []
    for ds in catalog["datasets"]:
        if year_min and ds["temporal"]["year"] < year_min:
            continue
        if level and ds["geography"]["level"] != level:
            continue
        if variable:
            var_names = [v for cat in ds["variables"] for v in cat["names"]]
            if not any(variable in v.lower() for v in var_names):
                continue
        results.append(ds)
    return results
```

## Pipeline Integration

```
data-catalog
  │
  ├──→ data-preprocessing (elige dataset a procesar)
  ├──→ data-validation (verifica calidad)
  ├──→ paper-planning (determina papers posibles)
  └──→ paper-factory (selecciona dataset para paper)
```

## Rules for This Project

1. **Registrar ANTES de usar.** Ningún dataset se toca sin entrada en catalog.yml.
2. **Licencia verificada.** Todo dataset debe tener licencia compatible.
3. **README en raw/.** Cada dataset/raw/ debe tener README con instrucciones de descarga.
4. **Id estable.** El id del dataset no cambia una vez creado (rompería referencias).
5. **Catalog como fuente de verdad.** Cualquier pregunta sobre datos se responde desde el catálogo.
6. **Actualizar used_in.** Cuando un paper usa un dataset, actualizar el campo used_in.
