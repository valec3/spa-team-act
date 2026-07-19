---
name: paper-latex
description: >
  Formateo y compilacion de papers academicos en LaTeX. Cubre compilacion con
  XeLaTeX, inclusion de figuras y tablas con formato profesional, ecuaciones
  matematicas, y configuracion de paquetes esenciales para papers en espanol.
  Trigger: Cuando el usuario trabaja con LaTeX, compila documentos, inserta figuras
  o tablas, escribe ecuaciones, o necesita formatear el paper final.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Compilar un paper con XeLaTeX (2-pass para referencias)
- Insertar figuras con el tamano y formato correcto
- Crear tablas profesionales con `booktabs`
- Escribir ecuaciones matematicas y estadisticas
- Configurar paquetes para papers en espanol
- Solucionar errores de compilacion LaTeX
- Generar PDF final para entrega

## Critical Patterns

### Compilation Pipeline (XeLaTeX)

```bash
# Compilacion completa (2-pass para referencias + indice)
cd paper
xelatex replica_lima.tex    # Pass 1: genera .aux
xelatex replica_lima.tex    # Pass 2: resuelve referencias cruzadas
```

### Essential Packages for Spanish Papers

```latex
\documentclass[12pt,a4paper]{article}

% Encoding y fuentes
\usepackage{fontspec}                  % Fuentes del sistema
\usepackage[spanish,es-tabla]{babel}   % Idioma espanol
\usepackage{csquotes}                  % Comillas tipograficas

% Matematicas y estadistica
\usepackage{amsmath,amssymb}           % Simbolos matematicos
\usepackage{siunitx}                   % Unidades y numeros con formato

% Figuras y tablas
\usepackage{graphicx}                  % Inclusion de figuras
\usepackage{booktabs}                  % Tablas profesionales
\usepackage{caption}                   % Captions personalizados
\usepackage{subcaption}                % Subfiguras

% Bibliografia
\usepackage[backend=biber,style=apa]{biblatex}  % APA 7
\addbibresource{referencias.bib}

% Hipervinculos
\usepackage[colorlinks=true,urlcolor=blue,citecolor=blue]{hyperref}

% Geometria de pagina
\usepackage[margin=2.5cm]{geometry}
```

### Figure Inclusion

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{../results/figures/moran_scatter_nse.png}
  \caption{Scatterplot de Moran para el Nivel Socioeconomico (NSE).
           Eje X: NSE en desviaciones de la media ($z_i$).
           Eje Y: retraso espacial ($Wz_i$).
           La pendiente de la recta de regresion es el I de Moran global ($I = 0.53$).}
  \label{fig:moran-nse}
\end{figure}
```

### Professional Tables with booktabs

```latex
\begin{table}[htbp]
  \centering
  \caption{Indice de Moran Global para variables socioeconomicas y educativas}
  \label{tab:moran}
  \begin{tabular}{lrrrr}
    \toprule
    Variable & $I$ de Moran & $Z$ & $p$ (MC) \\
    \midrule
    NSE (via PCA)   & 0.5296 & 9.45 & .000 \\
    Pobreza 2013     & 0.5300 & 9.44 & .000 \\
    ECE Lengua       & 0.1063 & 2.01 & .042 \\
    ECE Matematicas  & 0.1774 & 3.26 & .004 \\
    \bottomrule
    \multicolumn{4}{l}{\footnotesize \textit{Nota.} MC = Monte Carlo con 999 permutaciones.
    $N = 128$ distritos de Lima. Matriz de pesos Queen orden 1.} \\
  \end{tabular}
\end{table}
```

### Mathematical Equations

```latex
% Indice de Moran (inline)
El indice de Moran se define como $I = \frac{\sum_i \sum_j w_{ij} z_i z_j / S_0}{\sum_i z_i^2 / n}$.

% Indice de Moran (display)
\begin{equation}
  I = \frac{\sum_{i=1}^{n} \sum_{j=1}^{n} w_{ij} z_i z_j / S_0}
           {\sum_{i=1}^{n} z_i^2 / n}
  \label{eq:moran}
\end{equation}

% Matriz de pesos
\begin{equation}
  w_{ij} =
  \begin{cases}
    1 & \text{si } i \text{ y } j \text{ comparten frontera o vertice} \\
    0 & \text{en caso contrario}
  \end{cases}
  \label{eq:weights}
\end{equation}
```

### Figure/Table Placement Rules

| Specifier | Meaning | Use case |
|-----------|---------|----------|
| `h` | Here (approximately) | Preferido: LaTeX decide |
| `t` | Top of page | Tablas anchas |
| `b` | Bottom of page | Figuras secundarias |
| `p` | Page of floats | Figuras grandes que necesitan pagina completa |
| `!` | Override restrictions | Cuando LaTeX se niega a colocar |
| `H` | FORCE here (needs `float` package) | Solo si es absolutamente necesario |

## Commands

```bash
# Compilacion completa con limpieza
cd paper && xelatex replica_lima.tex && xelatex replica_lima.tex && rm -f *.aux *.log *.out *.bbl *.blg

# Verificar warnings de compilacion
cd paper && xelatex replica_lima.tex 2>&1 | rg -i "warning|error|underfull|overfull"

# Contar palabras del PDF compilado
pdftotext paper/replica_lima.pdf - | wc -w

# Verificar que todas las figuras referenciadas existen
rg "includegraphics" paper/replica_lima.tex
```

## Rules for This Project

1. **XeLaTeX, no pdfLaTeX.** Para soporte nativo de UTF-8 y fuentes del sistema.
2. **2-pass obligatorio.** Primera pasada genera `.aux` con referencias, segunda las resuelve.
3. **booktabs para tablas.** Nada de lineas verticales. Solo `\toprule`, `\midrule`, `\bottomrule`.
4. **Rutas relativas desde `paper/`.** Figuras en `../results/figures/`, no rutas absolutas.
5. **Compilacion limpia.** Antes de commitear, verificar que compila sin errores ni warnings graves.

## Common Errors and Solutions

| Error | Causa | Solucion |
|-------|-------|----------|
| `Undefined control sequence` | Paquete no cargado | Agregar `\usepackage{...}` |
| `Citation undefined` | Falta segunda pasada | Ejecutar xelatex de nuevo |
| `File not found` | Ruta de figura incorrecta | Verificar ruta relativa desde `paper/` |
| `Overfull \hbox` | Tabla/figura muy ancha | Reducir `width=` o usar `resizebox` |
| `Too many unprocessed floats` | Demasiadas figuras pendientes | Usar `\clearpage` o `!` specifier |
