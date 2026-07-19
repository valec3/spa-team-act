---
name: paper-structure
description: >
  Estructura y planificacion de papers academicos. Guia la organizacion de secciones
  (IMRaD, abstract, intro, metodos, resultados, discusion), adapta la estructura
  segun el tipo de paper (original, replica, revision, meta-analisis, caso), y
  provee plantillas de word count y rubricas de calidad por seccion.
  Trigger: Cuando el usuario pide estructurar un paper, planificar secciones, escribir
  abstract, crear outline, decidir el tipo de paper, o definir la organizacion de un
  articulo academico.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
---

## When to Use

- Crear el outline/esqueleto de un paper academico
- Decidir el tipo de paper y su estructura optima
- Escribir o revisar el abstract estructurado
- Planificar un paper de replica metodologica
- Formular un titulo efectivo con keywords
- Asignar word count por seccion
- Evaluar la calidad de cada seccion con rubrica

## Critical Patterns

### Paper Type Decision Tree

```
                     ┌─────────────────────┐
                     │ ¿Que tipo de paper?  │
                     └──────────┬──────────┘
                                │
          ┌─────────────────────┼──────────────────────┐
          ▼                     ▼                       ▼
  ┌───────────────┐    ┌────────────────┐    ┌──────────────────┐
  │ ¿Datos        │    │ ¿Replica un    │    │ ¿Sintetiza       │
  │ originales?   │    │ estudio previo?│    │ literatura?      │
  └───────┬───────┘    └───────┬────────┘    └───────┬──────────┘
          │                    │                      │
    ┌─────┴─────┐        ┌────┴────┐           ┌─────┴──────┐
    │ EMPIRICO  │        │ REPLICA │           │ REVISION / │
    │ (IMRaD)   │        │ (IMRaD+ │           │ META-ANAL. │
    │           │        │  compar)│           │ (PRISMA)   │
    └───────────┘        └─────────┘           └────────────┘
```

| Tipo | Estructura | Secciones extra | Journals tipicos |
|------|-----------|-----------------|------------------|
| Empirico | IMRaD | - | La mayoria |
| Replica | IMRaD + Original Study + Comparison | Original Study, Comparison Table | Replication-friendly |
| Revision sistematica | PRISMA | Search strategy, PRISMA flowchart | Revision journals |
| Meta-analisis | PRISMA + Forest plot | Effect sizes, heterogeneity | High-impact |
| Caso clinico | CARE | Timeline, Diagnostico diferencial | Clinical journals |
| Metodologico | IMRaD (enfasis en M) | Validation, benchmarks | Methods journals |
| Teorico | Introduction-Body-Conclusion | Conceptual framework | Theory journals |

### IMRaD Structure (Standard)

```
1. Title + Abstract + Keywords
2. Introduction (I) — 15% del texto
3. Methods (M) — 20-25% del texto
4. Results (R) — 25-30% del texto
5. Discussion/Conclusion (D) — 25-30% del texto
6. References
7. Appendices (optional)
```

### Variant: Replication Paper (este proyecto)

```
1. Title + Abstract + Keywords
2. Introduction (15%)
   - Contexto del estudio original
   - Motivacion para la replica
   - Pregunta de investigacion / hipotesis
3. Original Study Summary (10%)
   - Metodos del paper original (resumido)
   - Resultados clave del original
4. Methods — Replication (20%)
   - Datos utilizados (fuente, N, variables)
   - Procedimientos replicados (parametros identicos)
   - Tabla comparativa Original vs Replica
   - Adaptaciones y justificacion
   - Software y versiones
5. Results (25%)
   - Resultados de la replica
   - Comparacion lado a lado con el original
6. Discussion (25%)
   - Interpretacion de similitudes/diferencias
   - Limitaciones de la replica
   - Implicaciones para la generalizabilidad
7. References (5%)
8. Appendix: Codigo, datos suplementarios
```

### Word Count Allocation (Paper de 4000-6000 palabras)

| Seccion | % | 4000w | 5000w | 6000w |
|---------|---|-------|-------|-------|
| Abstract | - | 200-250 | 200-250 | 200-250 |
| Introduction | 15% | 600 | 750 | 900 |
| Methods | 25% | 1000 | 1250 | 1500 |
| Results | 25% | 1000 | 1250 | 1500 |
| Discussion | 25% | 1000 | 1250 | 1500 |
| References | - | ilimitado | ilimitado | ilimitado |
| **Total (sin refs)** | | 3800 | 4700 | 5650 |

### Title Formulation Rules

```
ESTRUCTURA: [Variable dependiente] en/asociada con [Variable independiente] en [poblacion]: [Metodo/Enfoque]

BUEN titulo (informativo, keywords, <15 palabras):
"Segregacion educativa y desigualdad social en el Peru: Un analisis espacial en el nivel secundario"

MAL titulo (generico, sin keywords):
"Un estudio sobre educacion en Peru"
```

### Abstract Structure (Structured)

| Seccion | Contenido | Palabras | Verbo clave |
|---------|-----------|----------|-------------|
| Background | 1-2 frases de contexto | ~40 | presente |
| Objective | Que se investiga | ~20 | infinitivo |
| Methods | Diseno, N, analisis | ~50 | pasado |
| Results | Hallazgos con estadisticos | ~60 | pasado |
| Conclusions | Implicacion principal | ~30 | presente |

### Introduction Funnel (5 parrafos)

```
PARRAFO 1: Contexto amplio — "En las ultimas decadas, [fenomeno] ha sido..."
PARRAFO 2: Literatura relevante — "Estudios previos han demostrado que..."
PARRAFO 3: Gap/brecha — "Sin embargo, persiste la falta de evidencia sobre..."
PARRAFO 4: Objetivo + hipotesis — "El presente estudio busca [verbo]..."
PARRAFO 5: Adelanto de metodo/resultados — "Para ello, se [metodo]..."
```

### Section Quality Rubric

| Seccion | Excelente (3) | Aceptable (2) | Deficiente (1) |
|---------|--------------|---------------|----------------|
| **Intro** | Gap claro, hipotesis explicita, literatura actualizada | Gap mencionado, hipotesis implicita | No hay gap, no hay hipotesis |
| **Metodo** | Replicable completamente, parametros explicitos | Replicable con ambiguedades | No replicable |
| **Resultados** | Estadisticos APA 7, sin interpretacion | Estadisticos presentes pero mal formateados | Interpretacion en Resultados |
| **Discusion** | Compara con literatura, declara limitaciones, implicaciones | Compara parcialmente | Solo repite resultados |

## Code Examples

### Abstract Template (Spanish)

```latex
\begin{abstract}
\textbf{Antecedentes:} La segregacion educativa socioeconomica constituye
un problema estructural que limita la equidad en el acceso a aprendizaje
de calidad. Estudios previos han documentado patrones de autocorrelacion
espacial en indicadores educativos a nivel nacional en Peru.

\textbf{Objetivo:} Replicar el analisis de autocorrelacion espacial de
Alonso-Pastor et al. (2025) sobre datos del departamento de Lima para
evaluar la generalizabilidad de sus hallazgos.

\textbf{Metodo:} Se utilizaron datos del Censo de Poblacion y Vivienda
2017 (N = 128 distritos de Lima). Se construyo un indice socioeconomico
(NSE) via PCA y se calculo el I de Moran global y local (LISA) con
matriz Queen orden 1, 999 permutaciones Monte Carlo, alpha = 0.05.

\textbf{Resultados:} El NSE mostro autocorrelacion espacial positiva
significativa (I = 0.53, Z = 9.45, p < .001). Los clusters Alto-Alto se
concentraron en Lima Metropolitana; los Bajo-Bajo en la periferia
departamental. Las magnitudes fueron menores que las del estudio original
(delta = -0.13 para NSE).

\textbf{Conclusiones:} Los patrones de segregacion espacial se replican
a escala departamental aunque con menor intensidad, sugiriendo que la
heterogeneidad subnacional modera la autocorrelacion.
\end{abstract}
```

### Section Skeleton for Replication

```latex
\section{Introduccion}           % ~750 palabras (15%)
\section{Estudio original}       % ~500 palabras (10%)
\section{Metodo}                 % ~1250 palabras (25%)
  \subsection{Diseno}
  \subsection{Datos}
  \subsection{Variables}
  \subsection{Analisis estadistico}
  \subsection{Comparacion metodologica con el original}
\section{Resultados}             % ~1250 palabras (25%)
  \subsection{Descriptivos}
  \subsection{Autocorrelacion global}
  \subsection{Analisis local (LISA)}
  \subsection{Comparacion con el original}
\section{Discusion}              % ~1250 palabras (25%)
  \subsection{Principales hallazgos}
  \subsection{Comparacion con la literatura}
  \subsection{Limitaciones}
  \subsection{Implicaciones}
\section{Referencias}
```

## Pipeline Integration

Esta skill es el **PUNTO DE ENTRADA** del pipeline agentico. Cuando `paper-pipeline` inicia, delega en `paper-structure` para definir la estructura antes de pasar a `paper-draft`.

```
paper-pipeline → paper-structure (define estructura)
              → paper-draft (ensambla borrador)
              → paper-review-consistency (audita)
              → paper-review-language (revisa)
              → paper-polish (pule)
              → paper-latex-generate (genera LaTeX)
              → paper-latex (compila)
```

## Rules for This Project

1. **Tipo de paper primero.** Determinar si es empirico, replica, o revision ANTES de estructurar.
2. **Metodos si, texto no.** Replicar metodos, NUNCA copiar redaccion del original.
3. **Word count por seccion.** Asignar y respetar el word count antes de escribir.
4. **Abstract en espanol + ingles.** Para revistas hispanas. Verificar requisitos.
5. **Keywords estrategicas.** 4-6 terminos, idealmente MeSH/DeCS, que maximicen discoverability.
6. **Quality gate.** Cada seccion debe pasar la rubrica (≥2) antes de avanzar en el pipeline.

## Commands

```bash
# Contar palabras por seccion
rg -o '\\\\section\{[^}]+\}' paper/replica_lima.tex

# Verificar que existen todas las secciones requeridas
rg "\\\\section\{" paper/replica_lima.tex --only-matching | sort

# Contar keywords
rg -o 'keyword' paper/replica_lima.tex | wc -l
```
