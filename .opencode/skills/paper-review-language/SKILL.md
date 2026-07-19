---
name: paper-review-language
description: >
  Revision de lenguaje academico: tono, claridad, concision, gramatica y
  ortografia. Evalua voz pasiva/activa, densidad de jerga, estructura de
  oraciones y parrafos, y transiciones. Disenado como Pase 2 del pipeline
  de revision, orquestado por paper-revision.
  Trigger: Cuando el usuario necesita revision de estilo, tono academico,
  claridad de redaccion, o el pipeline agentico ejecuta el pase 2 de revision.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Revisar el tono academico y formalidad del paper
- Evaluar claridad y concision de la redaccion
- Detectar y corregir problemas gramaticales y ortograficos
- Optimizar estructura de oraciones y parrafos
- Mejorar transiciones entre ideas y secciones
- Reducir voz pasiva excesiva y redundancias
- Ejecutar el Pase 2 del pipeline de revision

## Critical Patterns

### Language Review Dimensions

```
REVISION DE LENGUAJE — 5 dimensiones:

1. TONO ACADEMICO: formalidad, precision, objetividad
2. CLARIDAD: ¿se entiende a la primera lectura?
3. CONCISION: sin palabras innecesarias ni redundancias
4. GRAMATICA: concordancia, puntuacion, ortografia
5. FLUIDEZ: transiciones, variacion de longitud, ritmo
```

### Academic Tone Checklist

```
□ NO usar primera persona excesiva ("nosotros creemos", "nuestro estudio")
  → PREFERIR: "Los resultados sugieren...", "Se encontro que..."
  → ACEPTABLE: 1-2 usos de "nosotros" en Discusion para posicionamiento

□ NO usar lenguaje coloquial o informal
  ❌ "un monton de distritos" → ✅ "una proporcion considerable de distritos"
  ❌ "basicamente lo mismo" → ✅ "resultados similares"
  ❌ "obviamente" → ✅ "consistentemente" (o eliminar)

□ NO usar adverbios de certeza sin evidencia
  ❌ "claramente demuestra" → ✅ "sugiere" / "indica"
  ❌ "sin lugar a dudas" → ELIMINAR

□ SI usar lenguaje preciso y tecnico
  ✅ "autocorrelacion espacial positiva" (no "los datos estan agrupados")
  ✅ "estadisticamente significativo (p < .05)" (no "significativo" a secas)

□ SI mantener consistencia de tiempo verbal
  - Introduccion: presente ("la segregacion constituye un problema")
  - Metodo: pasado ("se utilizaron datos del censo")
  - Resultados: pasado ("el NSE mostro I = 0.53")
  - Discusion: presente ("estos hallazgos sugieren") + pasado para estudios previos
```

### Passive/Active Voice Balance

```
VOZ ACTIVA (recomendada para claridad):
"El NSE mostro autocorrelacion espacial positiva (I = 0.53)"
→ Sujeto claro, verbo directo, facil de leer.

VOZ PASIVA (aceptable en Metodo, excesiva en otros):
"La autocorrelacion espacial fue evaluada mediante el I de Moran"
→ Util en Metodo (enfasis en el procedimiento, no en el agente)

REGLA: En Metodo, hasta 40% de pasiva es aceptable.
       En Resultados y Discusion, maximo 20%.
       Meta global: <25% de oraciones en voz pasiva.
```

### Redundancy Detection

Eliminar estas construcciones redundantes:

| Redundancia | Correccion |
|-------------|------------|
| "en el presente estudio se procedio a realizar" | "se realizo" |
| "cabe mencionar que es importante destacar" | "es importante destacar" |
| "los resultados obtenidos muestran que" | "los resultados muestran que" |
| "en base a los resultados obtenidos" | "con base en los resultados" |
| "se puede observar que existe" | "se observa" |
| "en relacion con" | "en relacion a" o "sobre" |
| "un total de N = 128" | "N = 128" |
| "por parte de" | "de" o "por" |
| "en el caso de" | "en" |
| "es por ello que" | "por lo tanto" |
| "debido al hecho de que" | "porque" |

### Sentence Structure Guidelines

```
LONGITUD DE ORACION:
- Promedio ideal: 15-22 palabras (espanol academico)
- Maximo recomendado: 30 palabras
- Si una oracion tiene >35 palabras, DIVIDIR

ESTRUCTURA DE PARRAFO:
- 3-7 oraciones por parrafo
- Primera oracion = idea principal (topic sentence)
- Ultima oracion = transicion o conclusion del parrafo
- Evitar parrafos de 1 sola oracion
- Evitar parrafos de >10 oraciones

VARIACION:
- Alternar oraciones cortas, medias y largas para ritmo
- No empezar 3 parrafos seguidos con la misma palabra
```

### Transition Phrases (Spanish Academic)

```
PARA AGREGAR:
"Asimismo,...", "Ademas,...", "De igual manera,..."

PARA CONTRASTAR:
"Sin embargo,...", "No obstante,...", "En contraste,...",
"A diferencia de..."

PARA CONCLUIR:
"En conclusion,...", "En conjunto,...",
"Estos hallazgos sugieren que..."

PARA EJEMPLIFICAR:
"Por ejemplo,...", "En particular,...",
"Especificamente,..."

PARA CAUSA-EFECTO:
"En consecuencia,...", "Por lo tanto,...",
"Como resultado,..."
```

### Language Issues Classification

| Nivel | Ejemplo | Correccion |
|-------|---------|------------|
| 🔴 BLOQUEANTE | Error gramatical que cambia el significado | Reescribir |
| 🟠 MAYOR | Parrafo ininteligible | Reestructurar |
| 🟡 MENOR | Redundancia ("se procedio a realizar") | Eliminar palabras |
| 🔵 SUGERENCIA | Voz pasiva evitable | Reformular en activa |

## Code Examples

### Language Review Report Template

```markdown
# Language Review Report
## Draft: paper/draft_v1.1.md
## Fecha: [YYYY-MM-DD]

### Metricas
- Total oraciones: [N]
- Promedio palabras/oracion: [X]
- Oraciones >30 palabras: [N]
- % voz pasiva: [X]%
- Redundancias detectadas: [N]

---

### Issues

🔴 BLOQUEANTE:
1. [Seccion, parrafo] "Los resultado muestran que..."
   → Error de concordancia: "Los resultados muestran que..."
   Linea: [N]

🟠 MAYOR:
1. [Seccion, parrafo 3] Parrafo de 2 oraciones sin transicion
   → Agregar oracion puente entre idea A y B

🟡 MENOR:
1. [Results, para 2] "se procedio a calcular" → "se calculo"
2. [Methods, para 1] "un total de 128 distritos" → "128 distritos"

🔵 SUGERENCIA:
1. [Discusion, para 4] 65% voz pasiva → reformular 3 oraciones en activa
2. [Intro, para 1] "en las ultimas decadas" → especificar periodo
```

### Before/After: Redundancy

```
ANTES (42 palabras, redundante):
"En el presente estudio de investigacion, se procedio a realizar un
analisis de los datos obtenidos con la finalidad de evaluar la presencia
de autocorrelacion espacial en las variables de interes consideradas."

DESPUES (20 palabras, conciso):
"Se evaluo la autocorrelacion espacial de las variables de interes
mediante el indice de Moran."

→ Reduccion: 52% menos palabras, mismo significado.
```

### Before/After: Academic Tone

```
ANTES (coloquial, primera persona):
"Nosotros creemos que estos resultados son bastante interesantes porque
muestran que hay un monton de diferencias entre los distritos ricos y
los distritos pobres de Lima."

DESPUES (academico, impersonal):
"Estos resultados revelan heterogeneidad espacial sustantiva entre los
distritos de Lima, con concentracion de indicadores socioeconomicos
favorables en el area metropolitana y desfavorables en la periferia
departamental."
```

## Pipeline Integration

```
paper-draft (v1.0)
  │
  ▼
paper-review-consistency (PASE 1) → v1.1
  │
  ▼
★ paper-review-language (PASE 2) → v1.2 ★
  │
  ▼
paper-polish (PASE 3) → v2.0
```

## Rules for This Project

1. **Corregir solo lenguaje, no contenido.** Si el contenido es incorrecto, marcarlo pero no cambiarlo (eso es consistency).
2. **Tono impersonal.** Preferir "se encontro" sobre "encontramos".
3. **Eliminar redundancias sin piedad.** Cada palabra debe ganarse su lugar.
4. **Oraciones <30 palabras.** Si es mas larga, dividir.
5. **Transiciones explicitas.** Cada parrafo debe conectar con el anterior y el siguiente.
