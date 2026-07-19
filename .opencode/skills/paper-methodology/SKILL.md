---
name: paper-methodology
description: >
  Documentacion de metodos estadisticos con rigor y reproducibilidad. v2.0 agrega:
  framework de justificacion de diseno, power analysis y tamano muestral, validacion
  de instrumentos, guias de reporte STROBE/PRISMA/TRIPOD, y checklist de
  reproducibilidad computacional.
  Trigger: Cuando el usuario documenta metodos estadisticos, describe modelos, define
  variables operacionalmente, especifica parametros de analisis, justifica el diseno,
  o redacta la seccion de Metodo de un paper.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
---

## When to Use

- Redactar la seccion de Metodo de un paper
- Justificar el diseno de investigacion
- Realizar power analysis y justificar tamano muestral
- Definir variables operacionalmente con validacion
- Especificar software, paquetes y versiones
- Aplicar guias de reporte (STROBE, PRISMA, TRIPOD)
- Documentar pipeline de reproducibilidad computacional

## Critical Patterns

### Method Section Structure (v2.0)

```
1. DISENO DE INVESTIGACION
   - Tipo de estudio (observacional, experimental, replica)
   - Justificacion del diseno (¿por que este y no otro?)
   - Guia de reporte seguida (STROBE, PRISMA, etc.)
2. PARTICIPANTES / UNIDADES DE ANALISIS
   - Poblacion objetivo
   - Criterios de inclusion/exclusion (diagrama de flujo)
   - Justificacion del tamano muestral (power analysis o censo)
3. INSTRUMENTOS / FUENTES DE DATOS
   - Descripcion de cada fuente
   - Propiedades psicometricas (si aplica)
   - Validacion y confiabilidad
4. VARIABLES
   - Definicion operacional de CADA variable
   - Transformaciones aplicadas
   - Manejo de datos perdidos
5. PROCEDIMIENTO / ANALISIS
   - Pipeline analitico paso a paso
   - Parametros de cada tecnica
   - Supuestos y verificacion
6. SOFTWARE
   - Lenguaje, version, paquetes con versiones exactas
   - Semillas aleatorias
   - Entorno computacional
```

### Design Justification Framework

Para CADA decision metodologica, responder:

| Pregunta | Donde va en el paper |
|----------|---------------------|
| ¿Por que este diseno y no otro? | Metodo > Diseno |
| ¿Por que este N? ¿Es suficiente? | Metodo > Participantes |
| ¿Por que esta matriz W? ¿Por que orden 1? | Metodo > Analisis |
| ¿Por que 999 permutaciones y no 99 o 9999? | Metodo > Analisis |
| ¿Por que alpha = 0.05 y no correccion Bonferroni? | Metodo > Analisis |
| ¿Por que R y no GeoDa/Stata/Python? | Metodo > Software |

### Sample Size Justification

```
TEMPLATE: "El tamano muestral de N = [X] [unidades] se determino por [razon]:
- Censo: Se incluyeron TODOS los [unidades] disponibles en [fuente].
- Power analysis: Para detectar un efecto de [tamano] con alpha = [.XX] y
  potencia = [.XX], se requieren al menos [N] [unidades] (Faul et al., 2009).
- Convencion del campo: Estudios previos en [area] utilizan N ≥ [valor].
- Restriccion practica: [limitacion logistica/presupuestaria]."
```

### Reporting Guideline Selection

| Tipo de estudio | Guia | Items | Checklist URL |
|----------------|------|-------|---------------|
| Observacional (transversal, cohorte, caso-control) | **STROBE** | 22 | strobe-statement.org |
| Experimental (RCT) | **CONSORT** | 25 | consort-statement.org |
| Revision sistematica / Meta-analisis | **PRISMA** | 27 | prisma-statement.org |
| Estudio diagnostico / pronostico | **STARD / TRIPOD** | 30/22 | equator-network.org |
| Estudio cualitativo | **COREQ / SRQR** | 32/21 | equator-network.org |
| Replica computacional | **No hay guia estandar** → Usar checklist propio | - | Este documento |

### Parameter Declaration (NON-NEGOTIABLE)

TODO parametro DEBE declararse en: (a) header del script, (b) seccion Metodo del paper.

| Parametro | Script | Paper (Metodo) |
|-----------|--------|----------------|
| Semilla aleatoria | `set.seed(20240101)` | "Se fijo semilla 20240101" |
| Alpha | Header comment | "alpha = 0.05" |
| Permutaciones | Header comment | "999 permutaciones MC" |
| Matriz W | Header comment | "Queen orden 1, row-standardized" |
| Criterios inclusion | Header comment | "128 distritos con datos completos" |
| Paquetes + versiones | `sessionInfo()` | "R 4.4.1, spdep 1.3-3" |
| Hardware/OS | `sessionInfo()` | "Windows 11, 16 GB RAM" |

### Variable Definition Template (Complete)

```
[NOMBRE]: [Definicion conceptual breve]
  - Operacionalizacion: [Formula o procedimiento de calculo]
  - Fuente: [Dataset, pregunta, instrumento]
  - Tipo: [Continua | Categorica (k niveles) | Ordinal | Binaria]
  - Rango teorico: [min - max]
  - Rango observado: [min - max] (reportar en Descriptivos)
  - Transformacion: [Ninguna | Z-score | log | PCA | Otra: especificar]
  - Valores perdidos: [% missing | Imputacion por media/mediana/MICE | Listwise deletion]
  - Validacion: [Alpha de Cronbach | KMO | Juicio de expertos | NA]
  - Justificacion: [Por que esta variable y no otra alternativa]
```

### Replication-Specific: Method Comparison Table

| Aspecto | Original | Esta replica | Justificacion |
|---------|----------|-------------|---------------|
| Datos | [fuente original] | [nuestra fuente] | [por que] |
| N | [N original] | [nuestro N] | [por que difiere] |
| Periodo | [ano original] | [nuestro ano] | [por que] |
| Metodo A | [parametros] | [parametros] | Identico / Adaptado: [razon] |
| Metodo B | [parametros] | [parametros] | Identico / Adaptado: [razon] |
| Software | [original] | R (spdep) | Reproducibilidad |
| Variables | [vars originales] | [nuestras vars] | [mapeo o limitacion] |

### Reproducibility Pipeline Documentation

```r
# =============================================================================
# REPRODUCIBILITY HEADER — Obligatorio en cada script
# =============================================================================
# Script:    01_carga.R
# Proposito: Carga de CPV 2017 y construccion de NSE via PCA
# Pipeline:  01_carga.R → 02_moran.R → 03_figuras.R
# Autor:     [nombre]
# Fecha:     2024-07-15
#
# --- PARAMETROS ---
# Semilla:   20240715
# Alpha:     0.05
# PCA:       Rotacion varimax, retencion eigenvalue > 1
# N:         128 distritos de Lima con datos completos
#
# --- DEPENDENCIAS ---
# R:         4.4.1
# Paquetes:  sf (1.0-16), dplyr (1.1.4), haven (2.5.4),
#            tidyr (1.3.1), psych (2.4.3)
# OS:        Windows 11 x64, 16 GB RAM
#
# --- INPUTS ---
# data/raw/cpv_27.dta    — Censo de poblacion (INEI, 2017)
# data/raw/enc_27.dta    — Encuesta de hogares (INEI, 2017)
# data/geo/DISTRITOS.shp — Shapefile distrital (IGN, 2023)
#
# --- OUTPUTS ---
# data/processed/shp_distrital.rds — Shapefile con variables agregadas
# =============================================================================
```

## Code Examples

### Statistical Method Description with Justification

```latex
\subsection{Analisis de autocorrelacion espacial}

Se calculo el indice global de Moran (I; Moran, 1950) para evaluar
autocorrelacion espacial. Se eligio la matriz de pesos Queen de orden 1
porque: (a) es el estandar en estudios de segregacion educativa
(Alonso-Pastor et al., 2025; Bonal & Zancajo, 2020) y (b) captura tanto
fronteras compartidas como vertices, lo cual es apropiado para la
geometria irregular de los distritos peruanos (Bivand et al., 2013).

La matriz fue estandarizada por filas ($S_0 = n$), lo que facilita la
interpretacion del I de Moran como coeficiente de regresion en el
scatterplot de Moran (Anselin, 1996). Se utilizaron 999 permutaciones
Monte Carlo para la inferencia, siguiendo la recomendacion de que el
numero de permutaciones sea al menos $19 + 10/\alpha$ para $\alpha = 0.05$
(Edgington & Onghena, 2007). Con 999 permutaciones, el p-valor minimo
alcanzable es $1/1000 = .001$, suficiente para controlar el error Tipo I
al nivel deseado.
```

### Sample Size Justification (Spanish)

```latex
\subsection{Participantes}

La unidad de analisis fue el distrito ($N = 128$), correspondiente a la
totalidad de distritos del departamento de Lima con datos disponibles en
el Censo de Poblacion y Vivienda 2017 (INEI, 2018). Se trata de un censo
de las unidades administrativas del departamento, por lo que no aplico
calculo de tamano muestral.

Se excluyeron [X] distritos por [razon especifica: falta de datos
censales, islas sin vecinos espaciales que impiden el calculo de W,
etc.]. La Figura~\ref{fig:flowchart} presenta el diagrama de flujo de
inclusion/exclusion.
```

## Pipeline Integration

`paper-methodology` alimenta a `paper-draft` con la seccion de Metodo.
Durante `paper-review-consistency`, se verifica que cada parametro declarado
aqui aparezca en los scripts y en los resultados.

## Rules for This Project

1. **Parametros en tres lugares.** Script header + seccion Metodo + docs/metodologia-original.md.
2. **Justificar, no solo declarar.** "Queen orden 1" no alcanza; decir POR QUE Queen y POR QUE orden 1.
3. **Power analysis o justificacion de N.** Aunque sea censo, explicitar que lo es.
4. **Guia de reporte.** Declarar que guia se sigue (STROBE, etc.) o justificar por que no.
5. **Software versionado.** `sessionInfo()` en appendix o repositorio.
6. **Comparacion metodologica.** Para replicas, tabla Original vs Replica.
