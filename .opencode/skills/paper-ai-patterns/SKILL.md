---
name: paper-ai-patterns
description: >
  Catalogo de patrones linguisticos que los detectores de IA (Turnitin, GPTZero,
  Originality.ai) identifican como texto generado artificialmente. Incluye
  listas de palabras, estructuras sintacticas, y patrones de parrafo a evitar.
  Complementa a paper-humanize como referencia rapida.
  Trigger: Cuando el usuario busca patrones de IA, quiere ver que palabras evitar,
  consulta la lista de terminos "red flag", o necesita el catalogo de referencia.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## AI Detection Patterns — Quick Reference

### 🔴 HIGH RISK — Eliminar siempre

**Palabras y frases:**
```
delve, delve into, delves
tapestry (of)
a testament to
moreover
furthermore                
consequently               
it is important to note
it is worth mentioning
it should be noted
it is crucial to
```

**Estructuras sintacticas:**
```
"This [noun] [verb] the [adjective] [noun] of [noun]"
  → "This study investigates the spatial distribution of poverty"

"[Claim]. [Claim]. This [verb] that [explanation]."
  → "... This suggests that spatial clustering is significant."

"Not only [clause A], but also [clause B]."
  → Muy comun en IA, usar con MUCHA moderacion (max 1 por paper)
```

### 🟠 MEDIUM RISK — Reducir drasticamente

**Palabras:**
```
robust (cuando se usa como adjetivo generico)
nuanced, multifaceted, pivotal
landscape (como "the landscape of X")
crucial, critical (cuando no es genuinamente critico)
shed light on
underscores, highlights (como verbo comodin)
garnered attention, has emerged
a comprehensive [noun]
in the context of, in terms of, with respect to
```

**Transiciones sobreusadas (max 1-2 por seccion):**
```
Furthermore, Moreover, Additionally, In addition,
Consequently, Thus, Hence, Therefore,
Nevertheless, Nonetheless, Notwithstanding,
Indeed, Notably, Importantly,
Specifically, Particularly, Especially
```

### 🟡 LOW RISK — Usar con variedad

**Aceptables si se alternan:**
```
also, in addition, beyond this, what is more
however, yet, but, at the same time, in contrast
therefore, as a result, for this reason
for example, for instance, consider, take the case of
in other words, that is, put differently
```

### ✅ HUMAN MARKERS — Agregar para humanizar

```
Rhetorical questions:
  "What explains this pattern?"
  "Why does this matter?"
  "But is this enough?"

Positioning phrases:
  "We argue that..."
  "In our view,..."
  "This raises a deeper question:..."

Contrast/qualification:
  "That said,..."
  "To be clear,..."
  "This is not to say that..."

Personal observation:
  "One striking finding is..."
  "What surprised us was..."
  "We did not expect..."

Specificity (reemplaza generalizaciones):
  NO: "Many districts showed..."
  SI: "Seventeen districts — overwhelmingly in Yauyos and Cajatambo — showed..."
```

### Detector-Specific Patterns

**Turnitin AI Detection:**
- Penaliza: parrafos con estructura identica (topic → evidence → explanation)
- Penaliza: uso de "this" + verbo para empezar oraciones consecutivas
- Penaliza: oraciones de exactamente 20-25 palabras en secuencia
- Ignora: citas textuales (correctamente citadas)
- Ignora: referencias bibliograficas

**GPTZero:**
- Mide: perplexity (que tan predecible es cada palabra)
- Mide: burstiness (variacion en estructura de oraciones)
- Penaliza: baja perplexity + baja burstiness = alta probabilidad IA
- Ignora: texto con alta burstiness aunque tenga baja perplexity

**Originality.ai:**
- Penaliza: "delve", "tapestry", "moreover" como TOP red flags
- Penaliza: estructuras "Not only... but also..."
- Penaliza: "a testament to", "it is worth noting"
- Detecta: patrones de n-gramas repetidos entre parrafos

### Quick Scan Checklist (30 segundos por pagina)

```
□ ¿"delve" o "tapestry"? → ELIMINAR
□ ¿"moreover" o "furthermore"? → REDUCIR a 1 por seccion
□ ¿3+ oraciones seguidas de 20-25 palabras? → ROMPER (agregar corta o larga)
□ ¿Parrafos con identica estructura (topic-evidence-conclusion)? → VARIAR
□ ¿"This [verb] that..." repetido? → REFORMULAR
□ ¿Discussion sin preguntas retoricas ni voz personal? → AGREGAR
□ ¿Citas solo parenteticas (Author, Year)? → CONVERTIR algunas a narrativas
□ ¿"it is important to note" o variantes? → ELIMINAR
```

### Human Writing Characteristics (emular)

```
WHAT AI DOESN'T DO (well):
  - Ask genuine questions mid-paragraph
  - Use short, punchy sentences for impact
  - Write sentences of 3-4 words
  - Use discipline-specific colloquialisms
  - Express uncertainty with personality ("we are not sure why...")
  - Make imperfect but clear arguments
  - Use semicolons naturally; combine related ideas
  - Vary paragraph length dramatically (2 sentences vs 8 sentences)

WHAT HUMANS DO:
  - Mix formal and slightly informal registers
  - Occasionally start sentences with "And" or "But"
  - Use parenthetical asides — like this — in moderation  
  - Write topic sentences that don't summarize the paragraph
  - Leave some questions unanswered
  - Cite authors they disagree with
  - Show enthusiasm or disappointment about findings
```
