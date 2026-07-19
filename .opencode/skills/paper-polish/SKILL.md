---
name: paper-polish
description: >
  Pulido final del paper: optimizacion de fluidez global, alineacion
  Abstract-Conclusiones, refinamiento de keywords y titulo, verificacion de
  readability, y preparacion del draft para conversion a LaTeX. Es el ULTIMO
  pase antes de la generacion LaTeX.
  Trigger: Cuando el usuario pide el pulido final, optimizar el titulo,
  verificar alineacion Abstract-Conclusiones, o el pipeline agentico ejecuta
  el pase 3 de revision.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Pulido final del draft antes de conversion a LaTeX
- Optimizar titulo para discoverability e impacto
- Verificar alineacion entre Abstract y Conclusiones
- Refinar keywords para SEO academico
- Verificar readability general
- Cerrar el ciclo de revision antes de paper-latex-generate
- Ejecutar el Pase 3 del pipeline de revision

## Critical Patterns

### Polish Dimensions

```
PULIDO FINAL — 4 dimensiones:

1. ALINEACION: Abstract ↔ Introduction ↔ Conclusiones
2. TITULO + KEYWORDS: optimizacion para discoverability
3. FLUIDEZ GLOBAL: transiciones entre secciones, narrativa
4. READABILITY: legibilidad, escaneabilidad, densidad
```

### Abstract ↔ Conclusions Alignment Check

```
El Abstract promete → Las Conclusiones entregan

VERIFICAR:
□ Objetivo del Abstract = lo que efectivamente se investigo
□ Metodo del Abstract = lo descrito en Metodo (consistente)
□ Resultado principal del Abstract = mencionado en Conclusiones
□ Conclusion del Abstract = alineada con Conclusion del paper
□ NO hay informacion en Conclusiones que no este en Abstract (o viceversa,
  salvo detalles que no caben en 250 palabras)
```

### Title Optimization

```
CRITERIOS DE TITULO EFECTIVO:

1. INFORMATIVO (no enigmatico):
   ❌ "Mirando mas alla de Lima"
   ✅ "Segregacion educativa en Lima Metropolitana: Un analisis espacial"

2. KEYWORDS incluida:
   - Variable dependiente presente
   - Variable independiente presente
   - Poblacion/muestra presente
   - Metodo (si es distintivo)

3. LONGITUD: 10-15 palabras

4. FORMULA:
   [Fenomeno] en [poblacion]: [Metodo/Enfoque]
   [Variable dep] asociada a [Variable indep] en [contexto]
   [Concepto clave]: [hallazgo principal o metodo]

5. EVITAR:
   - Titulos interrogativos (a menos que la revista lo requiera)
   - "Un estudio sobre..." (redundante)
   - Abreviaturas no universales
   - Jerga excesivamente tecnica en el titulo
```

### Keyword Optimization

```
ESTRATEGIA DE KEYWORDS:

1. CANTIDAD: 4-6 keywords

2. TIPOS:
   - 2 keywords del titulo (refuerzan discoverability)
   - 2 keywords del campo/area (ej: "analisis espacial")
   - 1-2 keywords del metodo (ej: "I de Moran", "LISA")
   - 0-1 keyword geografica si es relevante

3. FORMATO:
   - Usar terminos MeSH/DeCS si existen equivalentes
   - Preferir terminos en ingles ademas de espanol (revistas indexadas)
   - Evitar keywords demasiado amplias ("educacion") o demasiado especificas

4. EJEMPLO (este proyecto):
   Keywords: segregacion educativa; analisis espacial; I de Moran;
             LISA; Lima; replica metodologica
```

### Global Flow Audit

```
Leer el paper COMPLETO de corrido, anotando:

□ ¿La Introduction termina donde la pregunta de investigacion esta clara?
□ ¿El Methods fluye naturalmente desde la Introduction?
□ ¿El primer parrafo de Results conecta con el ultimo de Methods?
□ ¿La Discussion arranca resumiendo hallazgos SIN repetir Results textualmente?
□ ¿Cada seccion tiene un parrafo de apertura que la contextualiza?
□ ¿Cada seccion tiene un parrafo de cierre que transiciona?
□ ¿No hay "saltos" abruptos entre temas dentro de una seccion?

PROBLEMAS COMUNES:
- Results empieza directo con numeros sin parrafo introductorio
- Discussion repite los resultados en lugar de interpretarlos
- La seccion "Estudio original" (replicas) no conecta con el Methods
- Las limitaciones estan escondidas en un parrafo, no en subseccion propia
```

### Readability Checklist

```
□ Oraciones de longitud variada (cortas, medias, largas)
□ Parrafos de 3-7 oraciones (no monolito de 15 lineas)
□ Sin bloques de texto sin subtitulos por >1 pagina
□ Figuras y tablas intercaladas (no todas al final)
□ Ecuaciones en display (no inline) para formulas complejas
□ Abreviaturas definidas en primera aparicion
□ Notas al pie minimas (si se puede integrar al texto, mejor)
```

## Code Examples

### Polish Report Template

```markdown
# Polish Report
## Draft: paper/draft_v1.2.md → v2.0
## Fecha: [YYYY-MM-DD]

---

### 1. Alineacion Abstract-Conclusiones

Abstract promete: "replicar analisis espacial en Lima para evaluar
generalizabilidad de hallazgos de Alonso-Pastor et al. (2025)"

Conclusiones entrega: ✅ SI — Discusion aborda generalizabilidad,
limitaciones de escala subnacional, y comparacion con original.

Abstract promete: "N = 128 distritos, Queen orden 1, 999 MC"
Metodo contiene: ✅ SI — Coinciden todos los parametros.

---

### 2. Titulo Actual vs Propuesto

ACTUAL: "Replica metodologica del analisis espacial de segregacion
educativa en el Peru: Caso del departamento de Lima"

PROPUESTO: "Segregacion educativa y desigualdad espacial en Lima
Metropolitana: Una replica metodologica con datos censales"

Cambios:
- "Caso del departamento" → implicito en "Lima Metropolitana" (+3 palabras liberadas)
- Agregado "desigualdad espacial" (keyword adicional)
- Agregado "datos censales" (diferencia el metodo)

---

### 3. Keywords Actuales vs Optimizadas

ACTUALES: segregacion, educacion, analisis espacial, Lima
OPTIMIZADAS: segregacion educativa; autocorrelacion espacial; I de Moran;
             LISA; Lima Metropolitana; replica metodologica

Cambios:
- "segregacion, educacion" → "segregacion educativa" (termino compuesto MeSH-like)
- Agregado "autocorrelacion espacial" (second keyword principal)
- Agregado "I de Moran; LISA" (terminos metodologicos buscables)
- "Lima" → "Lima Metropolitana" (mas preciso)
- Agregado "replica metodologica" (diferencia el estudio)

---

### 4. Global Flow Issues

🔴 BLOQUEANTE: Results empieza sin parrafo introductorio
   → Agregar: "A continuacion se presentan los resultados del analisis
   de autocorrelacion espacial, organizados en tres secciones:
   descriptivos, I global, y LISA."

🟡 MENOR: Discussion repite textualmente el primer resultado
   → Reemplazar con: "Consistentemente con el estudio original
   (Alonso-Pastor et al., 2025), el NSE mostro la autocorrelacion
   espacial mas alta..."

🔵 SUGERENCIA: Limitaciones estan en un solo parrafo largo
   → Separar en: Limitaciones de datos, Limitaciones metodologicas,
   Limitaciones de generalizabilidad

---

### Checklist Pre-LaTeX
[x] Abstract alineado con Conclusiones
[x] Titulo optimizado (<15 palabras, keywords incluida)
[x] Keywords 4-6, especificas y buscables
[x] No hay repeticion textual de Results en Discussion
[x] Transiciones entre todas las secciones
[x] Readability: sin parrafos >10 oraciones ni bloques sin subtitulos
[x] Listo para paper-latex-generate
```

### Abstract-Conclusions Cross-Check

```
ABSTRACT dice:
"[...] El NSE mostro autocorrelacion positiva (I = 0.53, p < .001).
Los clusters Alto-Alto se concentraron en Lima Metropolitana. Las
magnitudes fueron menores que el original (delta = -0.13). [...]"

CONCLUSIONES debe contener:
✅ "autocorrelacion positiva" → SI: "Los resultados confirman..."
✅ "I = 0.53" → SI: mencionado en primer parrafo de Discusion
✅ "clusters Alto-Alto en Lima Metropolitana" → SI: Discussion lo interpreta
✅ "delta = -0.13" → SI: Discussion compara explicitamente
```

## Pipeline Integration

```
paper-review-language (PASE 2) → v1.2
  │
  ▼
★ paper-polish (PASE 3) → v2.0 (FINAL) ★
  │
  ▼
paper-latex-generate → paper.tex
```

## Rules for This Project

1. **Ultimo pase antes de LaTeX.** Despues de polish, NO se agrega contenido nuevo.
2. **Abstract es lo ultimo que se toca.** Asegurar que refleja el paper final.
3. **Titulo con keywords.** Optimizar para que search engines academicos lo encuentren.
4. **No new issues.** Polish no debe introducir nuevos errores de consistency.
5. **Gate final.** Solo si todo el checklist esta en verde, avanzar a LaTeX.
