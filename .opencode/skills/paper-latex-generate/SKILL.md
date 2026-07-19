---
name: paper-latex-generate
description: >
  Generacion del documento LaTeX completo a partir del draft pulido. Convierte
  el contenido en un archivo .tex compilable con paqueteria completa, figuras,
  tablas, ecuaciones, referencias cruzadas, y bibliografia APA 7. Es el paso
  previo a paper-latex (compilacion).
  Trigger: Cuando el usuario pide generar el archivo LaTeX, convertir el draft a
  .tex, preparar el documento para compilacion, o el pipeline agentico llega al
  paso de generacion LaTeX.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Convertir el draft pulido (v2.0) en un archivo .tex compilable
- Generar el preambulo LaTeX completo con paqueteria
- Insertar figuras y tablas desde results/ al documento
- Convertir ecuaciones en formato LaTeX
- Configurar biblatex para APA 7 con referencias.bib
- Preparar el documento para compilacion con XeLaTeX
- Ejecutar el paso 5 del pipeline agentico

## Position in the Agentic Pipeline

```
paper-polish (v2.0 final draft)
  │
  ▼
★ paper-latex-generate ★
  │
  ├── paper/replica_lima.tex  (documento LaTeX completo)
  │
  ▼
paper-latex (compila → PDF)
```

## Critical Patterns

### LaTeX Document Structure

```latex
% ===========================================================================
% [TITULO DEL PAPER]
% Generado por paper-latex-generate
% Fecha: [YYYY-MM-DD]
% ===========================================================================

% --- PREAMBULO ---
\documentclass[12pt,a4paper]{article}

% Encoding y fuentes (XeLaTeX)
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}
\usepackage[spanish,es-tabla]{babel}
\usepackage{csquotes}

% Matematicas y estadistica
\usepackage{amsmath,amssymb}
\usepackage{siunitx}
\sisetup{output-decimal-marker={.}}

% Figuras y tablas
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{float}

% Bibliografia APA 7
\usepackage[backend=biber,style=apa,sorting=nyt]{biblatex}
\addbibresource{referencias.bib}

% Hipervinculos
\usepackage[colorlinks=true,urlcolor=blue,citecolor=blue,linkcolor=black]{hyperref}

% Geometria
\usepackage[margin=2.5cm]{geometry}
\usepackage{setspace}
\onehalfspacing

% --- METADATOS ---
\title{[TITULO DEL PAPER]}
\author{[AUTORES]}
\date{\today}

% --- DOCUMENTO ---
\begin{document}

\maketitle

% Abstract + Keywords
\begin{abstract}
[ABSTRACT]
\end{abstract}

\noindent\textbf{Palabras clave:} [KEYWORDS]

% --- CUERPO ---
\section{Introduccion}
[CONTENIDO]

\section{[Estudio original]}  % solo para replicas
[CONTENIDO]

\section{Metodo}
\subsection{Diseno}
\subsection{Datos}
\subsection{Variables}
\subsection{Analisis estadistico}
[CONTENIDO]

\section{Resultados}
\subsection{Descriptivos}
\subsection{[Analisis principal]}
\subsection{[Analisis complementario]}
[CONTENIDO]

\section{Discusion}
\subsection{Principales hallazgos}
\subsection{Limitaciones}
\subsection{Implicaciones}
[CONTENIDO]

% --- REFERENCIAS ---
\printbibliography

% --- APENDICES ---
\appendix
\section{[Apéndice A: Titulo]}
[CONTENIDO]

\end{document}
```

### Figure Generation from results/

```latex
% Template para cada figura
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{../results/figures/[ARCHIVO].png}
  \caption{[CAPTION COMPLETO CON DESCRIPCION Y ESTADISTICOS CLAVE]}
  \label{fig:[LABEL]}
\end{figure}
```

### Table Generation from .csv

```latex
% Opcion A: Tabla inline (pocas filas)
\begin{table}[htbp]
  \centering
  \caption{[TITULO DE LA TABLA]}
  \label{tab:[LABEL]}
  \begin{tabular}{lrrrr}
    \toprule
    Variable & $I$ de Moran & $Z$ & $p$ (MC) \\
    \midrule
    NSE (via PCA)   & 0.5296 & 9.45 & .000 \\
    Pobreza 2013    & 0.5300 & 9.44 & .000 \\
    ECE Lengua      & 0.1063 & 2.01 & .042 \\
    ECE Matematicas & 0.1774 & 3.26 & .004 \\
    \bottomrule
    \multicolumn{4}{l}{\footnotesize \textit{Nota.} MC = Monte Carlo con 999
    permutaciones. $N = 128$ distritos. Matriz Queen orden 1.} \\
  \end{tabular}
\end{table}

% Opcion B: Tabla desde CSV externo (muchas filas)
% Usar input de un .tex generado por R (ej: xtable, kableExtra)
```

### Equation Formatting

```latex
% Ecuacion en display (numerada)
\begin{equation}
  I = \frac{\sum_{i=1}^{n} \sum_{j=1}^{n} w_{ij} z_i z_j / S_0}
           {\sum_{i=1}^{n} z_i^2 / n}
  \label{eq:moran}
\end{equation}

% Ecuacion inline
El indice de Moran se define como $I = \frac{\sum_i \sum_j w_{ij} z_i z_j / S_0}{\sum_i z_i^2 / n}$.

% Matriz (cases)
\begin{equation}
  w_{ij} =
  \begin{cases}
    1 & \text{si } i \text{ y } j \text{ comparten frontera o vertice} \\
    0 & \text{en caso contrario}
  \end{cases}
  \label{eq:weights}
\end{equation}
```

### APA 7 Citation Commands

```latex
% Cita parentetica
La segregacion educativa ha sido documentada a nivel nacional \parencite{alonso2025segregacion}.

% Cita narrativa
\textcite{anselin1995local} desarrollo los indicadores LISA.

% Multiples citas
Estudios previos han utilizado este enfoque \parencite{anselin1995local, moran1950notes}.

% Cita con pagina (cita textual)
"la autocorrelacion espacial es la correlacion de una variable consigo misma
en el espacio" \parencite[93]{anselin1995local}.
```

### Generation Checklist

```
ANTES de generar:
[ ] Draft v2.0 pulido y aprobado (paper-polish paso)
[ ] Todas las figuras existen en results/figures/
[ ] Todas las tablas tienen datos en results/tables/
[ ] referencias.bib tiene todas las entradas citadas
[ ] Titulo, autores, abstract y keywords definidos

DURANTE la generacion:
[ ] Preambulo completo con todos los paquetes necesarios
[ ] Cada seccion del draft → seccion LaTeX correspondiente
[ ] Figuras insertadas con ruta relativa y caption completo
[ ] Tablas formateadas con booktabs (sin lineas verticales)
[ ] Ecuaciones en formato LaTeX correcto
[ ] Citas en formato \parencite{} o \textcite{}
[ ] Labels consistentes: fig:X, tab:X, eq:X, sec:X

DESPUES de generar:
[ ] El .tex compila con xelatex sin errores
[ ] 2-pass compilacion resuelve todas las referencias
[ ] PDF generado correctamente
```

### Variable Substitution Map

Al generar LaTeX, mapear variables del draft a comandos LaTeX:

| Draft (markdown) | LaTeX |
|-----------------|-------|
| `**Abstract:** texto` | `\begin{abstract} texto \end{abstract}` |
| `## Introduccion` | `\section{Introduccion}` |
| `### Diseno` | `\subsection{Diseno}` |
| `I = 0.53, Z = 9.45` | `$I = 0.53$, $Z = 9.45$` |
| `p < .001` | `$p < .001$` |
| `\cite{anselin1995local}` | `\parencite{anselin1995local}` |
| `[FIGURA: moran_scatter_nse]` | `\includegraphics{../results/figures/moran_scatter_nse.png}` |
| `[TABLA: cuadro1]` | (generar entorno table completo) |

## Code Examples

### Complete Preambulo for Replication Paper

```latex
% ===========================================================================
% replica_lima.tex
% Generado por paper-latex-generate
% ===========================================================================

\documentclass[12pt,a4paper]{article}

% --- Encoding y fuentes ---
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{Latin Modern Mono}
\usepackage[spanish,es-tabla]{babel}
\usepackage{csquotes}

% --- Matematicas ---
\usepackage{amsmath,amssymb}
\usepackage{siunitx}
\sisetup{
  output-decimal-marker={.},
  group-separator={,},
  group-minimum-digits=4
}

% --- Figuras ---
\usepackage{graphicx}
\graphicspath{{../results/figures/}}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{float}

% --- Tablas ---
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{array}

% --- Bibliografia ---
\usepackage[backend=biber,style=apa,sorting=nyt,maxcitenames=2]{biblatex}
\addbibresource{referencias.bib}
\DeclareLanguageMapping{spanish}{spanish-apa}

% --- Hipervinculos ---
\usepackage[colorlinks=true,urlcolor=blue,citecolor=blue,linkcolor=black]{hyperref}

% --- Diseno ---
\usepackage[margin=2.5cm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage{fancyhdr}
\pagestyle{plain}

% --- Metadata ---
\title{\textbf{Segregacion educativa y desigualdad espacial en Lima Metropolitana:\\
Una replica metodologica con datos censales}}
\author{[Autores]\\
\small Universidad Nacional Altiplano de Puno}
\date{\today}

\begin{document}
\maketitle
% ... resto del documento
```

## Pipeline Integration

```
paper-polish (draft v2.0)
  │
  ▼
★ paper-latex-generate → paper/replica_lima.tex ★
  │
  ▼
paper-latex → xelatex → paper/replica_lima.pdf
```

## Rules for This Project

1. **XeLaTeX como compilador target.** El .tex generado debe compilar con xelatex.
2. **Rutas relativas.** Figuras desde `../results/figures/`, .bib desde `paper/referencias.bib`.
3. **booktabs SIEMPRE.** Nunca generar tablas con lineas verticales.
4. **biblatex + biber.** No usar bibtex tradicional.
5. **Labels semanticos.** `fig:moran-nse`, `tab:descriptivos`, `eq:moran`, `sec:metodo`.
6. **Generacion idempotente.** Poder regenerar el .tex sin perder personalizaciones manuales.
