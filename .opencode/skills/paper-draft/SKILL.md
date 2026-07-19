---
name: paper-draft
description: >
  Ensamblaje del primer borrador de un paper academico. Toma materiales crudos
  (notas de metodologia, outputs de resultados, lista de citas) y los integra en
  un draft coherente en prosa academica, aplicando la estructura definida por
  paper-structure y el estilo de paper-methodology/paper-results.
  Trigger: Cuando el usuario pide generar un primer borrador, ensamblar secciones,
  integrar resultados con metodologia, o escribir el draft inicial del paper.
  NOTA: Esta skill PRODUCE el draft que luego sera revisado por paper-revision.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Generar el primer borrador completo del paper
- Integrar secciones escritas por separado en un documento unico
- Convertir notas y outputs en prosa academica continua
- Escribir transiciones entre secciones
- Asegurar que el draft cubre todos los elementos de la estructura
- Preparar el insumo para el ciclo de revision

## Position in the Agentic Pipeline

```
[INPUTS]                      [PROCESS]           [OUTPUT]
metodologia-original.md  ─┐
results/tables/*.csv    ─┤
results/figures/*.png   ─┤
docs/referencias.md     ─┼──→ paper-draft ──→ paper/draft_v1.md
paper-structure (plan)  ─┤
paper-methodology (guia)─┤
paper-results (guia)    ─┘
```

## Critical Patterns

### Draft Assembly Process

```
FASE 1: INGESTA DE MATERIALES
  1.1 Leer plan estructural (de paper-structure)
  1.2 Leer metodologia documentada (docs/metodologia-original.md)
  1.3 Leer outputs de resultados (results/tables/*.csv)
  1.4 Leer lista de referencias (docs/referencias.md)
  1.5 Identificar figuras disponibles (results/figures/*.png)

FASE 2: REDACCION POR SECCION
  2.1 Title + Abstract + Keywords (200-250 palabras)
  2.2 Introduction (estructura funnel, 5 parrafos)
  2.3 Methods (desde metodologia-original.md)
  2.4 Results (desde outputs, sin interpretar)
  2.5 Discussion (interpreta, compara, limita)
  2.6 References (formato APA 7)

FASE 3: ENSAMBLAJE
  3.1 Unir secciones en orden IMRaD
  3.2 Insertar placeholders para figuras y tablas
  3.3 Agregar citas en formato \cite{key}
  3.4 Verificar cobertura de la estructura
  3.5 Guardar draft_v1.md
```

### Section Writing Prompts (Internal)

Cada seccion se redacta siguiendo un prompt interno:

```
TITLE:
"Genera un titulo de maximo 15 palabras que incluya: [var dependiente],
[var independiente], [poblacion], [metodo]. Sigue el formato APA 7."

ABSTRACT (200-250 palabras):
"Escribe un abstract estructurado con: Antecedentes (2 frases),
Objetivo (1 frase con verbo en infinitivo), Metodo (diseno, N, analisis
con parametros), Resultados (estadisticos clave en APA 7), Conclusiones
(1-2 frases de implicacion)."

INTRODUCTION (~750 palabras):
"Estructura funnel de 5 parrafos. P1: contexto del problema general.
P2: literatura relevante (citar 3-5 fuentes clave). P3: gap especifico.
P4: objetivo + hipotesis. P5: resumen de metodo."
```

### Draft Quality Gate

Antes de pasar a revision, el draft DEBE cumplir:

```
[ ] Abstract entre 200-250 palabras
[ ] Introduction tiene estructura funnel (5 parrafos)
[ ] Methods declara TODOS los parametros de docs/metodologia-original.md
[ ] Results NO contiene interpretacion
[ ] Discussion interpreta, compara con literatura, declara limitaciones
[ ] Cada referencia citada en texto esta en la lista de referencias
[ ] Figuras y tablas referenciadas con placeholders
[ ] Sin placeholder markers sin resolver (TODO, FIXME, ???)
```

### Draft Annotation Conventions

Durante la redaccion, usar anotaciones estandar:

| Marcador | Significado | Accion requerida |
|----------|-------------|-----------------|
| `[CITAR: razon]` | Falta cita para afirmacion | Agregar \cite{key} |
| `[VERIFICAR: fuente]` | Dato inseguro | Verificar contra output |
| `[FIGURA: descripcion]` | Placeholder para figura | Insertar en LaTeX |
| `[TABLA: descripcion]` | Placeholder para tabla | Insertar en LaTeX |
| `[N = ?]` | N pendiente de confirmar | Verificar en datos |
| `[TRANSICION]` | Falta transicion entre secciones | Escribir puente |

## Code Examples

### Draft Assembly: Integration Example

Input (metodologia-original.md):
```markdown
## Metodo estadistico
- W: Queen contiguity, orden 1
- I de Moran: 999 permutaciones MC, alpha = 0.05
- LISA: descomposicion local, 999 perms, p < 0.05
```

Output (draft Methods section):
```markdown
## Metodo

### Analisis estadistico

Se calculo el indice global de Moran (I) para evaluar autocorrelacion
espacial en las variables de interes. La matriz de pesos espaciales W
se construyo con criterio de contiguidad Queen de orden 1 (w_ij = 1 si
los distritos i y j comparten frontera o vertice) y fue estandarizada
por filas. La significancia se evaluo mediante 999 permutaciones Monte
Carlo con alpha = 0.05 [CITAR: Anselin 1995].

Para el analisis local, se calcularon indicadores LISA (Anselin, 1995)
que descomponen el I global en contribuciones distritales. Los clusters
significativos (p < .05, 999 permutaciones) se clasificaron en Alto-Alto
(AA), Bajo-Bajo (BB), Alto-Bajo (AB) y Bajo-Alto (BA) [CITAR: paper original].
```

### Abstract Draft from Structured Data

```markdown
Datos de entrada:
- Contexto: "Segregacion educativa en Peru, replica de Alonso-Pastor 2025"
- Objetivo: "Replicar analisis espacial en Lima con datos alternativos"
- Metodo: "CPV 2017, N=128 distritos, PCA→NSE, Queen-1, 999 MC, alpha=.05"
- Resultado clave: "NSE I=0.53, Z=9.45, p<.001. Delta vs orig = -0.13"
- Conclusion: "Patrones se replican con menor intensidad a escala subnacional"

Draft generado:
"La segregacion educativa socioeconomica ha sido documentada a nivel nacional
en Peru (Alonso-Pastor et al., 2025), pero se desconoce si estos patrones se
mantienen a escalas subnacionales. El presente estudio busca replicar el
analisis de autocorrelacion espacial en el departamento de Lima utilizando
datos alternativos. Se emplearon datos del Censo de Poblacion y Vivienda 2017
para 128 distritos. Se construyo un indice socioeconomico (NSE) mediante PCA
y se calculo el I de Moran global y local (LISA) con matriz Queen orden 1,
999 permutaciones Monte Carlo y alpha = .05. El NSE mostro autocorrelacion
espacial positiva significativa (I = 0.53, Z = 9.45, p < .001), aunque de
menor magnitud que el estudio original (delta = -0.13). Los resultados sugieren
que los patrones de segregacion educativa se replican a escala departamental
pero con intensidad atenuada, lo que resalta la importancia de considerar la
heterogeneidad subnacional en estudios de segregacion espacial."
```

### Section Transition Bridges

```markdown
# Transiciones estandar entre secciones IMRaD

INTRO → METHODS:
"Para abordar esta pregunta de investigacion, se [diseno/metodo general]..."

METHODS → RESULTS:
"El analisis [principal] revelo los siguientes hallazgos..."

RESULTS → DISCUSSION:
"Estos resultados [confirman/cuestionan/extienden] los hallazgos previos
en varios aspectos. En primer lugar..."

DISCUSSION → CONCLUSION (interna):
"En conjunto, la evidencia presentada sugiere que..."
```

## Pipeline Integration

```
paper-pipeline
  │
  ├── paper-structure (define estructura)
  ├── ★ paper-draft (ensambla primer borrador) ★
  ├── paper-revision (orquesta revision)
  ├── paper-latex-generate (genera LaTeX)
  └── paper-latex (compila PDF)
```

## Rules for This Project

1. **Prosa original, NUNCA copiada.** El draft es 100% redaccion propia.
2. **Placeholders explicitos.** Usar `[VERIFICAR]` y `[CITAR]` para marcar pendientes.
3. **Sin interpretacion en Results.** Si el draft mezcla resultados con interpretacion, corregir antes de entregar.
4. **Abstract ULTIMO.** Escribir el abstract despues del cuerpo, no antes.
5. **Output en `paper/draft_v1.md`.** Versionar el draft para trazabilidad.
6. **Gate check antes de revision.** El draft debe pasar el quality gate interno.
