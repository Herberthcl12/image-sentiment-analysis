---
name: hh-carrusel-instagram
description: Genera carruseles de Instagram para HH Studio Creativo con una biblioteca de 13 formatos de slide (azul noche con foco, negro con grano, resplandor rojo, papel claro; Inter + serif cursiva; recuadros, tachados, comparaciones, frases fragmentadas) que elige y mezcla según el tema, rubro y nicho, con vista previa en miniatura antes de entregar y CTA obligatorio "Comenta PALABRA". Úsala SIEMPRE que Herberth pida un carrusel, post de varias láminas, o contenido tipo "swipe" para @hh.condireccion o para un cliente de HH, incluso si solo dice "hazme un carrusel sobre X" sin más detalle. También aplícala si pide "el mismo estilo del carrusel de siempre", "un carrusel como los que ya hacemos" o "usa la skill del carrusel". No apliques la paleta de HH a piezas de un cliente salvo que se indique explícitamente que es para HH.
---

# Carrusel HH Studio Creativo — v3 (biblioteca de formatos)

Produce carruseles de Instagram terminados en PNG (1080x1350) para HH Studio Creativo (@hh.condireccion). La skill no es una plantilla: es una **biblioteca de formatos de slide** más un **criterio para elegirlos y mezclarlos** según el tema. Cada carrusel debe verse distinto al anterior sin dejar de ser reconocible como HH.

Herberth va a seguir mandando referencias y feedback. Cuando lo haga, adapta lo nuevo a lo que ya existe (no lo reemplaces), propón el cambio concreto, y al aprobarlo agrégalo a la biblioteca y al "Registro de cambios".

## Flujo obligatorio

1. **Decidir** (sección "Cómo elegir"): lee el tema, rubro, nicho, audiencia y objetivo. Elige familia visual, formatos por slide, tipografía de acento y palabra del CTA. Si Herberth ya indicó algo (un formato, una fuente, un color), eso manda.
2. **Guion**: texto exacto de cada lámina, con el formato elegido y por qué.
3. **Vista previa**: genera todas las láminas y arma la hoja de miniaturas con `vista_previa([...], "vista_previa.png")`. Entrégale a Herberth **solo esa imagen**, junto con el guion resumido (una línea por slide), la decisión de diseño en 3–4 líneas y el entregable que promete el CTA. Luego **detente y espera**.
4. **Ajustar**: si Herberth pide cambios, corrige y vuelve a mostrar la vista previa.
5. **Entregar**: solo cuando Herberth diga "confirmo" (o equivalente: "dale", "ok, mándalos"), entrega todos los PNG en orden y el caption.

Nunca entregues los slides finales antes de la confirmación. La excepción es que Herberth pida explícitamente saltarse la vista previa.

## Identidad fija (lo que nunca cambia)

- **Rojo `#FE0000`** como único color de acento de HH.
- **Inter** como tipografía base de lectura (`inter(peso, tamaño)`, pesos 400/500/700/800/900).
- **Logo HH** en alguna posición de la lámina (portada, explicaciones y cierre como mínimo).
- **CTA final "Comenta PALABRA"** (ver sección CTA).
- **Voz HH**: tuteo, frases cortas, datos concretos, cero lenguaje de anuncio y nada inventado presentado como real.

Todo lo demás (fondo, tipografía de acento, alineación, formato de cada slide) se elige por carrusel.

## Paleta y fondos

| Nombre | Valor | Función |
|---|---|---|
| Azul noche | `#061323` | Base de la familia "Foco" |
| Rojo | `#FE0000` | Acento único |
| Blanco | `#FFFFFF` | Texto principal sobre oscuro |
| Negro con grano | `#050505` | Base de la familia "Negro" |
| Crema | `#F2EFEA` | Texto grande sobre negro (más cálido que el blanco) |
| Papel | `(236, 234, 230)` + textura | Base de la familia "Papel" |
| Grises derivados | `GRIS_TEXTO #C9D0DA`, `GRIS_APAGADO #3B4E66`, `GRIS_META #AEB6C2` | Cuerpo, inactivos y contador |

Funciones de fondo (`scripts/generar_slide.py`):
- `fondo_hh(posicion, radio, intensidad)`: azul noche con foco de luz azul. Rota la posición del foco en cada slide.
- `fondo_negro()`: negro con grano fotográfico.
- `fondo_resplandor(luz=(190,0,0))`: brillo rojo difuso detrás del centro, con grilla de puntos.
- `fondo_papel()`: papel claro texturizado. Texto en `#111111`, logo negro.
- `fondo_claro_puntos()`: blanco con grilla de puntos, para el checklist.
- `gradar_foto_hh(ruta)`: si Herberth aporta una foto real, úsala como fondo, gradada al tono HH.

Regla de mezcla: en un carrusel se pueden combinar hasta **3 fondos distintos**. Mínimo 2 slides seguidos con el mismo fondo, salvo que el contraste sea intencional (por ejemplo, un slide de papel entre dos negros para marcar un cambio de tema). El texto nunca va sobre el punto más brillante de un foco o resplandor.

## Tipografía

- **Inter**: base de todo el texto de lectura, titulares sans y números.
- **Serif cursiva de acento** para las palabras que quieres que se sientan:
  - `serif(peso, tamaño)`: Playfair Display Italic 500/700/800. Contundente, para frases fragmentadas, números grandes y remates.
  - `serif_fina(tamaño)`: Instrument Serif Italic. Más fina y editorial, para tonos elegantes, lifestyle o premium.
- Regla de combinación: una línea puede mezclar Inter y serif con `linea_mixta()`, alineadas por línea base. La serif va en las **palabras emocionales o clave**, nunca en frases de más de ~6 palabras seguidas.
- **Fuente temática opcional**: si el tema lo pide (bebidas, deporte, música, gastronomía, infantil…), puedes sumar **una** fuente display de Google Fonts con `fuente_tematica("Familia", peso, tamano=…)`, **solo en hook y sentencia**. Si no hay red o devuelve `None`, usa Inter 900 o serif como respaldo. Elige la fuente por lo que evoca, no por moda, y justifícala en la decisión de diseño.
- Titulares en frase normal (mayúscula inicial), salvo etiquetas cortas tipo "NO DIGAS:".
- Montserrat y League Gothic quedan en `assets/fonts/` solo por compatibilidad. No las uses salvo que Herberth las pida.

## Biblioteca de formatos de slide

### Familia A: Foco (azul noche con luz), estilo v2
Ejemplos completos: `ejemplos/carrusel_web_v2.py` y `ejemplos/agenda_ia_v2.py`.

| ID | Formato | Composición | Sirve para |
|---|---|---|---|
| **A1** | Hook con recuadro | Titular Inter 800, frase clave en `caja_destacada` roja, línea corta y contra-frase gris | Abrir con una afirmación que incomoda |
| **A2** | Tachado | ~~creencia común~~ con `trazo_mano`, verdad en rojo Inter 900 y una línea de cuerpo | Romper un mito o reencuadrar |
| **A3** | Espejo "¿Te suena alguna?" | `fondo_claro_puntos` + 4–5 `tarjeta_check`, una marcada | Que el lector se reconozca en el problema |
| **A4** | Secuencia "Tú empezaste acá" | Números grandes apagados, el activo con círculo rojo, `flecha_curva` y anotación | Mostrar que se saltó un orden |
| **A5** | Lista numerada | Número rojo + título + cuerpo gris, separadores | Explicar 3–5 conceptos |
| **A6** | Pasos con círculo | Círculos rojos numerados, el último relleno, con datos concretos | Un proceso o un orden correcto |
| **A7** | Sentencia | 2 líneas blancas + remate rojo Inter 900 + consecuencia gris | Cerrar el argumento antes del CTA |
| **A8** | CTA | "Comenta" + `etiqueta_cta` + `texto_mixto` | Cierre (ver sección CTA) |

### Familia B: Editorial (referencias aprobadas en sept. 2026)
Ejemplo completo: `ejemplos/formatos_mixtos_ideas.py`.

| ID | Formato | Composición | Sirve para |
|---|---|---|---|
| **B1** | Resplandor | `fondo_resplandor`, texto centrado: línea Inter 800 + 1–2 líneas serif cursiva grandes + línea Inter, `boton_flecha` abajo, logo centrado arriba | Portada que se siente "tendencia", "lo nuevo", "esta semana" |
| **B2** | Suma | `fondo_negro`, 2–4 líneas Inter 700 color crema, una línea roja vertical corta y el total en serif 800 rojo gigante, con una línea gris opcional debajo | Abrir o revelar una cifra: "X + Y + Z = total" |
| **B3** | Lista en papel | `fondo_papel`, "Palabra Inter 900 + *Palabra serif roja*", regla negra, 10–15 ítems numerados Inter 500 31px, pie "1–15 \| TEMA" y logo negro | Entregar valor denso: ideas, plantillas, recursos |
| **B4** | Comparación "No digas / Mejor di" | `fondo_negro`, etiqueta roja Inter 800, frase entre comillas Inter 800 blanca, nota en serif cursiva gris; línea roja horizontal al medio y el mismo esquema abajo | Contrastar lo que no funciona con lo que sí (copy, precios, atención, mensajes) |
| **B5** | Frase fragmentada | `fondo_negro`, frase de 5–7 líneas centrada que alterna Inter 800 crema con serif 800 roja, una palabra subrayada | Una idea fuerte, citable y compartible |

Estos formatos son un punto de partida, no moldes cerrados: puedes crear variantes con la misma lógica (por ejemplo, B4 con "Antes / Ahora", o B2 con precios en vez de cantidades). Si una variante funciona y Herberth la aprueba, agrégala a la biblioteca con un ID nuevo.

## Cómo elegir (criterio propio)

Antes de decidir, responde internamente estas preguntas:

1. **¿Qué tipo de contenido es?**
   - Educativo o paso a paso → A5, A6, A4 (Foco) o B3.
   - Opinión, mito o polémica → A2, B5, B4.
   - Valor descargable (ideas, recursos, plantillas) → B2 + B3.
   - Diagnóstico del lector ("¿te pasa esto?") → A3, A4.
   - Tendencia o novedad → B1.
   - Venta de un servicio de HH → A1, A3, A6 y cierre A7 + A8.
2. **¿Qué tono pide el rubro o nicho?**
   - Tecnología, servicios, B2B, legal o finanzas → Familia Foco, Inter dominante y serif mínima.
   - Gastronomía, bares, alcohol, eventos o nocturno → Familia Negro + resplandor rojo, serif 800 protagonista y, si suma, una fuente temática display (condensada, de cartel o de etiqueta).
   - Moda, belleza, lifestyle o premium → Papel y Negro, `serif_fina`, más espacio negativo.
   - Creadores, streaming o marketing en redes → mezcla B1 + B5 + B3, serif 800 y frases fragmentadas.
   - Salud o bienestar → Foco y Papel, tono sereno, sin rojo agresivo en grandes superficies.
3. **¿Cuánto texto tiene cada slide?** Mucho texto → fondo plano (Negro o Papel, o Foco con intensidad 0.7). Una frase → fondo con vida (Resplandor o Foco intenso).
4. **¿Qué se usó en los carruseles anteriores?** Revisa la conversación y la carpeta de trabajo. Evita repetir la misma familia dominante, el mismo formato de portada y la misma secuencia de formatos del último carrusel.

Reglas de mezcla:
- **Carrusel puro**: una sola familia. Conviene cuando el tema es muy homogéneo o el nicho pide una estética clara.
- **Carrusel mixto** (el más común): 2 familias, por ejemplo portada B1 → desarrollo Foco → frase B5 → CTA.
- **Carrusel editorial**: un formato distinto por slide (como la prueba de ideas). Úsalo para contenido de alto valor o cuando el carrusel anterior fue muy homogéneo.
- Nunca repitas el mismo ID de formato más de 2 veces en un carrusel, salvo listas que continúan (B3 de 1–15 y luego 16–30).
- La portada define el tono. Elígela primero y construye el resto para que haga sentido con ella.

En la vista previa, indica siempre qué ID usa cada slide (por ejemplo: "1 B1 · 2 B2 · 3 A3 · …"), así Herberth puede pedir cambios por ID.

## CTA obligatorio: "Comenta PALABRA"

- Siempre es el último slide.
- "Comenta" + la PALABRA en `etiqueta_cta` (recuadro rojo inclinado) + la promesa en `texto_mixto`: **"y te mando [entregable concreto] [para qué] [en X tiempo / listo para X]"**, con el tiempo o beneficio en rojo.
- Puede ir sobre cualquier familia de fondo (Foco, Negro o Resplandor) y alineado a la izquierda o centrado, según el resto del carrusel.
- Una sola palabra, en mayúsculas, ligada al tema.
- Revisa los saltos de línea a mano: sin palabras solas en la última línea y sin espacio antes de ":".
- En la respuesta final, avísale a Herberth qué entregable prometió el CTA, para que lo tenga listo antes de publicar, y ofrécete a crearlo.

## Recursos disponibles (`scripts/generar_slide.py`)

- **Texto**: `inter`, `serif`, `serif_fina`, `fuente_tematica`, `lineas` (con `centrado=True`), `linea_mixta` (fuentes y colores mezclados, subrayado), `wrap`, `texto_mixto`, `texto_con_sombra`.
- **Gráficos**: `caja_destacada`, `trazo_mano`, `flecha_curva`, `tarjeta_check`, `etiqueta_cta`, `boton_flecha`.
- **Fondos**: `fondo_hh`, `fondo_negro`, `fondo_resplandor`, `fondo_papel`, `fondo_claro_puntos`, `gradar_foto_hh`.
- **Marca**: `logo_esquina`, `logo_centrado`, `pegar_logo` (variantes blanco, azul y negro).
- **Meta**: `contador(img, n, total)` y `vista_previa(rutas, salida)`.

Medidas: 1080x1350, margen lateral `M = 90`. Tamaños de referencia en los tres ejemplos.

## Logo

`assets/logo_hh_blanco.png` para fondos oscuros, y `logo_hh_negro.png` o `logo_hh_azul.png` para papel o blanco. Los archivos tienen transparencia real. Si Herberth sube un logo nuevo, verifica el canal alfa antes de usarlo. Si el logo está en la lámina, no repitas "HH" ni el @ como texto.

## Cuándo NO aplica la identidad HH

Si el carrusel es para un cliente (Bar de Blas, Fonda Desna, un streamer, etc.), usa su paleta, sus fuentes y su logo, pero puedes usar la **biblioteca de formatos y el criterio de elección** de esta skill. Si no está claro para quién es la pieza, pregunta.

## Referencias nuevas de Herberth

Cuando lleguen screenshots de referencia:
1. Analiza cada una: fondo, tipografías, jerarquía, recursos gráficos y manejo del espacio.
2. Tradúcela a un formato con la identidad fija de HH (rojo, Inter, logo, voz), sin copiar colores, fuentes ni textos ajenos.
3. Haz una prueba que la combine con los formatos existentes.
4. Si Herberth la aprueba, agrégala a la biblioteca con un ID nuevo (C1, C2… o la familia que corresponda), súmale su función en `generar_slide.py` si hace falta y actualiza el registro de cambios.

## Control de calidad (antes de la vista previa)

Revisa la hoja de miniaturas y cualquier slide dudoso a tamaño completo:
- Texto cortado, superpuesto o fuera del margen, y choques con el pie o el logo.
- Palabras solas en la última línea de un párrafo.
- Espacio mal repartido (bloque apretado arriba y la mitad inferior vacía sin intención).
- Un solo protagonista rojo por slide.
- Contraste legible en cada fondo, contador presente (salvo B3, que lleva su propio pie) y logo sin tapar texto.

## Entregables

- **Vista previa**: `vista_previa.png` + guion resumido con IDs + decisión de diseño + entregable del CTA.
- **Tras "confirmo"**: `slide_01.png` … `slide_NN_cta.png` en orden, y el caption (máx. ~120 palabras, repite el CTA, 5–6 hashtags).
- No prometas publicar en Instagram: Herberth sube los archivos.

## Registro de cambios

- **v3 (sept. 2026)**: la skill pasa a ser una biblioteca de formatos (familia A Foco y familia B Editorial) con criterio propio para elegir y mezclar según el tema, rubro y nicho. Se suman Playfair Display Italic e Instrument Serif Italic como tipografías de acento, la descarga opcional de una fuente temática, los fondos negro con grano, resplandor rojo y papel, las funciones `linea_mixta`, `boton_flecha`, `logo_centrado` y `vista_previa`, y el flujo obligatorio de vista previa → "confirmo" → entrega. Ejemplos en `ejemplos/`.
- **v2 (sept. 2026)**: Inter reemplaza a League Gothic y Montserrat. Fondo azul noche con foco rotativo, recuadro destacado, tachado a mano, secuencia con flecha, checklist claro, contador y CTA "Comenta PALABRA".
- **v1**: League Gothic + Montserrat, estructura portada/cuerpo (A/B/C/D)/cierre.
