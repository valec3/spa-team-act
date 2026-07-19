---
name: reproducibility-audit
description: >
  Auditoria completa de reproducibilidad. Verifica que cualquier persona
  pueda clonar el repositorio, instalar dependencias, ejecutar todo el
  pipeline, y obtener resultados identicos. Cubre: entorno computacional,
  disponibilidad de datos, ejecucion de scripts, y matching de outputs.
  Trigger: Cuando el usuario audita la reproducibilidad, verifica que el
  pipeline es ejecutable desde cero, prepara el repo para publicacion,
  o necesita garantizar que los resultados son completamente reproducibles.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Verificar que el repo es completamente reproducible
- Auditar antes de publicar o compartir el repositorio
- Preparar el repo para revision por pares
- Testear el pipeline en un entorno limpio (fresh clone)
- Verificar que las dependencias estan correctamente declaradas
- Detectar dependencias ocultas (paquetes no declarados, archivos no versionados)

## Critical Patterns

### Reproducibility Dimensions (5 Checks)

```
AUDITORIA DE REPRODUCIBILIDAD — 5 dimensiones:

1. ENTORNO: R, paquetes, versiones exactas. ¿Igual en otra maquina?
2. DATOS: fuentes declaradas, disponibles, documentadas. ¿Se pueden obtener?
3. SCRIPTS: ejecutables de principio a fin. ¿Corren sin intervencion manual?
4. OUTPUTS: identicos a los publicados. ¿Mismos numeros, mismas figuras?
5. DOCUMENTACION: instrucciones claras. ¿Un tercero puede seguirlas?
```

### Fresh Clone Test Protocol

```
PROTOCOLO: Simular que un revisor anonimo clona el repo

1. Clonar en directorio temporal
   git clone <repo> /tmp/spa-team-act-test

2. Seguir el README exactamente
   - Instalar dependencias segun instrucciones
   - Descargar datos (si es posible) o usar datos de prueba
   - Ejecutar scripts en orden

3. Verificar outputs
   - Comparar results/tables/*.csv con originales
   - Comparar results/figures/*.png (visual o hash)
   - Compilar paper y verificar que compila sin errores

4. Reportar
   - ¿Se pudo completar el pipeline? SI/NO
   - ¿Outputs identicos? SI/NO (si NO, ¿que difiere?)
   - ¿Instrucciones suficientes? SI/NO
```

### Reproducibility Checklist

```markdown
# Reproducibility Audit Report
## Fecha: 2024-07-18 | Repo: spa-team-act

---

### 1. ENTORNO COMPUTACIONAL

[x] R version declarada (4.4.1)
[x] Paquetes con versiones exactas (sessionInfo() en docs/)
[x] requirements.txt para Python (pdfplumber, pypdf)
[ ] NO hay paquetes instalados localmente sin declarar
    → ⚠️ El script 02_moran.R usa `tmap` pero no esta en requirements
[ ] Entorno reproducible via renv o Docker
    → Sugerencia: agregar renv.lock para R

---

### 2. DISPONIBILIDAD DE DATOS

[x] Fuentes documentadas en datasets/catalog/catalog.yml
[x] Licencias verificadas y compatibles
[ ] Datos raw incluidos en el repo
    → ❌ cpv_27.dta y enc_27.dta NO versionados (son >1 GB)
    → ⚠️ Instrucciones de descarga en data/raw/README.md ¿siguen vigentes?
[x] Datos procesados son derivables desde raw
[ ] Datos sinteticos disponibles para testing sin datos reales
    → Sugerencia: crear datasets/synthetic/ para CI/testing

---

### 3. EJECUCION DE SCRIPTS

[x] Scripts numerados en orden (01_carga.R, 02_moran.R)
[x] Rutas relativas (sin paths absolutos)
[x] Semillas fijas en cada script
[ ] Scripts ejecutables sin intervencion manual
    → ⚠️ 01_carga.R asume que los .dta ya fueron descargados
    → Sugerencia: agregar check inicial con mensaje claro si faltan
[ ] Tiempo de ejecucion documentado (~2 min carga, ~30s moran)

---

### 4. MATCHING DE OUTPUTS

[x] Numeros en paper.pdf coinciden con results/tables/*.csv
[x] Figuras en paper.pdf identicas a results/figures/*.png
[ ] Outputs versionados en el repo
    → ⚠️ results/figures/ no esta versionado (ver .gitignore)
    → Decision: ¿versionar o regenerar en CI?

---

### 5. DOCUMENTACION

[x] README.md con instrucciones de reproduccion
[x] AGENT.md con reglas y flujo de trabajo
[ ] "Getting started" para nuevo colaborador
    → Sugerencia: agregar CONTRIBUTING.md
[ ] Guia de troubleshooting para errores comunes
    → Sugerencia: agregar docs/troubleshooting.md

---

### Resumen
- Checks pasados: 8/12 (67%)
- Issues bloqueantes: 1 (datos no disponibles sin descarga manual)
- Issues menores: 4
- Recomendacion: Agregar renv.lock + datos sinteticos para CI

### Estado de Reproducibilidad: ⚠️ PARCIAL
El pipeline es reproducible SI se tienen los datos raw.
Sin datos raw, NO es reproducible desde cero.
```

### Environment Freeze

```r
# Congelar entorno R para reproducibilidad exacta
# Ejecutar en el entorno de desarrollo:
session_info <- sessionInfo()

# Guardar para referencia
writeLines(capture.output(session_info), "docs/session_info.txt")

# Opcional: usar renv para lockfile
# renv::init()
# renv::snapshot()  # genera renv.lock
```

### Output Hashing

```bash
# Verificar que outputs no cambiaron despues de re-ejecutar
md5sum results/tables/cuadro1_moran_lima.csv > results/hashes.md5
md5sum results/figures/*.png >> results/hashes.md5

# En fresh clone, verificar:
md5sum -c results/hashes.md5
# OK: cuadro1_moran_lima.csv
# OK: moran_scatter_nse.png
# FAIL: lisa_map.png  ← algo cambio!
```

### CI Reproducibility Pipeline (Conceptual)

```yaml
# .github/workflows/reproducibility.yml
name: Reproducibility Check

on: [push, pull_request]

jobs:
  test-reproducibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup R
        uses: r-lib/actions/setup-r@v2
        with:
          r-version: '4.4.1'

      - name: Install dependencies
        run: |
          install.packages(c("sf", "spdep", "ggplot2", "dplyr", "haven"))
        shell: Rscript {0}

      - name: Generate synthetic test data
        run: Rscript tests/generate_synthetic_data.R

      - name: Run pipeline with synthetic data
        run: |
          Rscript src/01_carga.R
          Rscript src/02_moran.R

      - name: Verify outputs
        run: Rscript tests/verify_outputs.R
```

## Pipeline Integration

```
reproducibility-audit (verifica TODO el repo)
  │
  ├── Verifica data-catalog (datos documentados)
  ├── Verifica data-preprocessing (scripts ejecutables)
  ├── Verifica method-library (metodos reproducibles)
  ├── Verifica paper-factory (papers regenerables)
  └── Verifica paper-batch (batch reproducible)
```

## Rules for This Project

1. **Auditar antes de publicar.** Todo paper debe pasar la auditoria de reproducibilidad.
2. **Fresh clone test.** Al menos una vez, simular clonar y ejecutar desde cero.
3. **Dependencias explicitas.** Ni un solo `library()` sin su `install.packages()` documentado.
4. **Datos sinteticos para CI.** Permiten testear el pipeline sin acceso a datos reales.
5. **Hashes de outputs.** Versionar hashes para detectar cambios no intencionales.
6. **Entorno congelado.** `sessionInfo()` o `renv.lock` versionado en el repo.
