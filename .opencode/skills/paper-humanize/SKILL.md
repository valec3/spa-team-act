---
name: paper-humanize
description: >
  Humanizacion de texto academico para reducir deteccion de IA por herramientas
  como Turnitin, GPTZero y Originality.ai. Identifica y reemplaza patrones
  tipicos de IA, varia estructura de oraciones, agrega voz personal y naturalidad
  sin sacrificar rigor academico. NO busca "engañar" detectores sino producir
  texto genuinamente humano y natural.
  Trigger: Cuando el usuario pide humanizar texto, reducir deteccion de IA,
  evitar patrones de Turnitin, hacer el texto mas natural, o revisar un paper
  para que no parezca generado por IA.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Humanizar un paper antes de enviarlo a una revista o repositorio
- Reducir la probabilidad de deteccion como texto generado por IA
- Revisar un draft buscando patrones tipicos de IA
- Agregar voz personal y variacion estilistica a un texto academico
- Preparar un manuscrito para someter a Turnitin o similar

## Critical Patterns

### How AI Detectors Work

Los detectores de IA (Turnitin, GPTZero, Originality.ai, Copyleaks) analizan:

| Metrica | Que mide | IA tipico | Humano tipico |
|---------|----------|-----------|---------------|
| **Perplexity** | Predictibilidad de palabras | Baja (palabras predecibles) | Alta (palabras sorprendentes) |
| **Burstiness** | Variacion en longitud de oraciones | Uniforme (todas ~20-25 palabras) | Variable (cortas, medias, largas) |
| **Repeticion de n-gramas** | Frases de 3-5 palabras repetidas | Alta (frases formulaicas) | Baja |
| **Entropia de vocabulario** | Diversidad lexica | Media-baja | Alta |
| **Estructura de parrafos** | Formato predecible | Claim-evidence-explanation uniforme | Variado |
| **Uso de transiciones** | Palabras de conexion | "Moreover, Furthermore, Additionally..." | Natural, variado |

### AI-Typical Vocabulary — PALABRAS PROHIBIDAS

Estas palabras y frases son **banderas rojas** para detectores. EVITARLAS:

```
NUNCA USAR (alta deteccion):
  "delve into"          → "examine", "investigate", "study"
  "tapestry"            → "fabric", "network", "structure" (o eliminar)
  "landscape"           → "context", "field", "setting"
  "a testament to"      → "evidence of", "confirmation of"
  "moreover"            → "also", "furthermore" (usar con moderacion)
  "furthermore"         → "in addition", "also", "beyond this"
  "consequently"        → "as a result", "therefore"
  "thus"                → "therefore", "so", "accordingly"
  "hence"               → "for this reason", "as a result"

EVITAR (deteccion media):
  "it is important to note"    → eliminar (redundante)
  "it is worth mentioning"     → eliminar (redundante)
  "it should be noted"         → eliminar (redundante)
  "plays a crucial role"       → "is central to", "is key to"
  "has emerged as"             → "has become", "is now"
  "in the context of"          → "in", "within", "for"
  "a comprehensive analysis"   → "an analysis" (comprehensive es relleno)
  "a nuanced understanding"    → "understanding" (nuanced es relleno)
  "robust" (sobreuso)          → "reliable", "consistent", "solid"
  "multifaceted"               → "complex", "varied", "diverse"
  "shed light on"              → "reveal", "explain", "illuminate"
  "pivotal"                    → "key", "central", "critical"
```

### Burstiness — La Clave

El patron MAS detectable de IA es la uniformidad. Solucion:

```
IA (mal):
  The results show strong spatial autocorrelation. The SELI exhibited an I value
  of 0.53 with a Z-score of 9.45. These findings are consistent with previous
  studies. The implications for policy are significant. (4 oraciones, todas 10-15 palabras)

HUMANO (bien):
  The results are striking. Across all four indicators, spatial autocorrelation was
  positive and statistically significant (p < .001), with the SELI showing the
  strongest clustering (I = 0.53, Z = 9.45). This is not simply a statistical
  artifact. When we examined the LISA maps, a clear centre-periphery gradient
  emerged — one that mirrors the historical development trajectory of Latin
  American metropolises. Poverty, it seems, has a geography.
  (4 oraciones: 4, 28, 7, 31, 7 palabras — alta burstiness)
```

### Paragraph Structure Variation

```
IA (formulaico):
  [Topic sentence]. [Evidence 1]. [Evidence 2]. [Explanation]. [Transition].

HUMANO (variado):
  [Pregunta retorica]. [Evidencia concreta con numeros]. [Oracion corta de impacto].
  [Contraste con literatura]. [Implicacion especifica, no generica].
```

### Voice and Personality

```
AGREGAR (marcadores humanos):
  - "We found that..." (en Discussion, no en Results)
  - "Surprisingly,..." (cuando algo realmente sorprende)
  - "This raises the question:..." (pregunta retorica)
  - "What explains this pattern?" (involucra al lector)
  - "In our view,..." (posicionamiento claro)
  - "It is worth asking whether..." (reflexion genuina)

NO AGREGAR (falsa humanizacion):
  - "Interestingly,..." (si no es realmente interesante)
  - Exceso de "we" (maximo 3-4 veces en Discussion)
  - "Obviously,..." (nada es obvio en academia)
  - "As we all know,..." (condescendiente)
```

### Citations: Natural Integration

```
IA (formulaico):
  "Previous studies have demonstrated spatial clustering of poverty
  (Author A, 2020; Author B, 2021; Author C, 2022)."

HUMANO (natural):
  "The spatial clustering of deprivation is by now well documented. In Colombia,
  González Bula et al. (2025) found comparable Moran's I values across
  municipalities using census-based multidimensional poverty indicators.
  Tatli and colleagues (2025) extended this line of inquiry to subjective
  poverty in Turkey, revealing that perceived deprivation clusters spatially
  just as strongly as income-based measures. What is less clear — and what
  motivates the present study — is whether these patterns hold at the
  intra-metropolitan scale in Latin American cities."
```

### The "Humanization Pass" Protocol

```
Para CADA parrafo del paper:

1. MEDIR burstiness: contar palabras por oracion. ¿Hay variacion?
   Maxima oracion: _______ palabras
   Minima oracion: _______ palabras
   ¿(max - min) > 15? → ✅ PASA
   ¿(max - min) < 10? → ❌ REESCRIBIR

2. ESCANEAR vocabulario: buscar palabras de la lista PROHIBIDA
   ¿Aparece alguna? → reemplazar o eliminar

3. VERIFICAR transiciones: ¿empiezan 2+ oraciones con la misma palabra?
   → variar (However → But → Yet → At the same time → In contrast)

4. AGREGAR marcador humano: ¿hay al menos 1 pregunta retorica
   o posicionamiento personal en Discussion?

5. ROMPER patron formulaico: si 3 parrafos seguidos tienen la misma
   estructura (topic-evidence-conclusion), reestructurar uno
```

## Code Examples

### Before/After: Abstract Humanization

```
BEFORE (IA, detectable):
  This study investigates the spatial distribution and clustering patterns of
  multidimensional socioeconomic deprivation across 128 districts of Metropolitan
  Lima, Peru, using the 2017 National Population and Housing Census. A composite
  Socioeconomic Level Index (SELI) was constructed via Principal Component
  Analysis incorporating education, housing quality, and access to basic services.
  Spatial autocorrelation was assessed using Global Moran's I with Queen contiguity
  weights (order 1), while Local Indicators of Spatial Association (LISA) identified
  statistically significant clusters. (3 oraciones: 28, 26, 28 palabras — uniforme)

AFTER (humanizado):
  How does socioeconomic deprivation cluster across one of Latin America's largest
  metropolises? This study examines 128 districts of Metropolitan Lima using Peru's
  2017 census. We constructed a composite Socioeconomic Level Index via Principal
  Component Analysis and assessed spatial autocorrelation through Global Moran's I
  (Queen contiguity, order 1) and LISA statistics. The patterns we found are
  striking. (4 oraciones: 15, 14, 35, 6 palabras — alta burstiness)
```

### Before/After: Discussion Paragraph

```
BEFORE (IA, detectable):
  The results provide robust evidence of spatial clustering of socioeconomic
  conditions within Metropolitan Lima. This pattern has important implications
  for both academic understanding and policy design. The strong positive spatial
  autocorrelation of the SELI confirms that socioeconomic conditions are far
  from randomly distributed. Instead, they exhibit a clear centre-periphery
  gradient where districts in the historic urban core form contiguous clusters
  of high socioeconomic status, while peripheral districts form clusters of
  concentrated deprivation. (4 oraciones: 17, 14, 20, 29 palabras)

AFTER (humanizado):
  What emerges from these maps is a city divided. The Global Moran's I of 0.53
  is not merely a statistic — it quantifies a geography of exclusion that has
  deep historical roots. Central Lima's affluent districts cluster together as
  tightly as the peripheral settlements that ring the city's northern and
  southern edges. This is the spatial footprint of decades of uneven investment,
  housing market sorting, and infrastructure planning that has favoured the
  historic core over the expanding periphery. The LISA analysis makes this
  visible in ways that aggregate statistics cannot. (5 oraciones: 9, 20, 21,
  28, 11 palabras — variado, voz personal, sin palabras AI)
```

### Automation: Burstiness Check

```python
import re

def check_burstiness(text: str) -> dict:
    """Analiza la variacion de longitud de oraciones."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    lengths = [len(s.split()) for s in sentences]

    if not lengths:
        return {"error": "no sentences found"}

    return {
        "total_sentences": len(lengths),
        "min_words": min(lengths),
        "max_words": max(lengths),
        "range": max(lengths) - min(lengths),
        "mean": sum(lengths) / len(lengths),
        "burstiness_ok": (max(lengths) - min(lengths)) > 15,
        "uniform_sequences": count_uniform_sequences(lengths),
    }

def check_ai_vocabulary(text: str) -> dict:
    """Busca palabras tipicas de IA."""
    ai_words = {
        "delve": 3, "tapestry": 3, "landscape": 2, "moreover": 2,
        "furthermore": 2, "consequently": 1, "thus": 1, "hence": 1,
        "crucial": 2, "robust": 2, "multifaceted": 2, "pivotal": 2,
        "a testament to": 3, "it is important to note": 2,
        "it is worth mentioning": 2, "shed light on": 2,
        "comprehensive analysis": 2, "nuanced understanding": 2,
    }
    found = {}
    for word, severity in ai_words.items():
        count = text.lower().count(word.lower())
        if count > 0:
            found[word] = {"count": count, "severity": severity}
    return found
```

## Pipeline Integration

```
paper-review-language (PASE 2 del pipeline)
  │
  └── paper-humanize (sub-skill especializada)
       ├── Burstiness check
       ├── AI vocabulary scan
       ├── Voice injection
       └── Citation naturalization
```

Esta skill se integra en `paper-review-language` como un chequeo adicional.
O puede ejecutarse de forma independiente.

## Rules for This Project

1. **Humanizar, no "trucar".** El objetivo es escribir mejor, no engañar detectores.
2. **Burstiness > 15.** Diferencia minima de 15 palabras entre la oracion mas corta y mas larga por seccion.
3. **Zero AI vocabulary.** Eliminar TODAS las palabras de la lista PROHIBIDA.
4. **Voice en Discussion.** Al menos 2 marcadores de voz personal en Discussion.
5. **Citations narrativas.** No mas de 1 cita parentetica por parrafo; preferir narrativas.
6. **Verificar antes de compilar.** Correr el humanization pass ANTES de generar LaTeX final.
