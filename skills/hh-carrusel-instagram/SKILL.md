---
name: hh-carrusel-instagram
description: Genera carruseles de Instagram con la identidad visual y estructura narrativa de HH Studio Creativo (estilo v2 con tipografía Inter, fondos azul noche con foco de luz, acento rojo, recuadros destacados, tachado a mano y CTA obligatorio "Comenta PALABRA"). Úsala SIEMPRE que Herberth pida un carrusel, post de varias láminas, o contenido tipo "swipe" para @hh.condireccion o para un cliente de HH, incluso si solo dice "hazme un carrusel sobre X" sin más detalle. También aplícala si pide "el mismo estilo del carrusel de siempre", "un carrusel como los que ya hacemos" o "usa la skill del carrusel". No apliques la paleta/tipografía de esta skill a piezas de un cliente salvo que se indique explícitamente que es para HH.
---

# Carrusel HH Studio Creativo — estilo v2

Skill de identidad visual y estructura para carruseles de Instagram de HH Studio Creativo (@hh.condireccion). Al activarse, produce el **carrusel terminado en PNG** (1080x1350) más guion y caption, no una lista de títulos.

**Estado:** estilo v2 aprobado por Herberth en septiembre 2026, a partir de un carrusel de referencia que le gustó ("Tu web puede desaparecer en un solo día"). El script completo de ese carrusel está en `ejemplos/carrusel_web_v2.py`: léelo antes de armar uno nuevo, es la mejor referencia de tamaños, interlineados y uso de cada recurso.

Herberth va a seguir ajustando este estilo. Cuando dé feedback sobre un carrusel, propón el cambio concreto a esta skill y regístralo en "Registro de cambios" (al final) una vez que lo apruebe.

## Cuándo NO aplica esta identidad

Esta skill define la identidad de **HH como marca**. Si el carrusel es para un cliente de HH (Bar de Blas, Fonda Desna, un streamer, etc.), no uses esta paleta ni tipografía: construye desde la identidad de ese cliente. Sí puedes reutilizar la **estructura narrativa y los recursos** (recuadro destacado, tachado, checklist, CTA "Comenta") con los colores y fuentes del cliente. Confirma con Herberth si no queda claro para quién es la pieza.

## Paleta (hex exactos, no aproximar)

| Color | Hex | Uso |
|---|---|---|
| Azul noche | `#061323` | Fondo principal (siempre con foco de luz, ver Fondos) |
| Rojo | `#FE0000` | Acento: recuadro destacado, tachado, flecha, número activo, frase-remate, palabra del CTA |
| Blanco | `#FFFFFF` | Titulares; fondo del slide claro de contraste |
| Negro | `#000000` | Solo sombras. No como fondo en el estilo v2 |

Tonos derivados permitidos (constantes en el script, no inventes otros):
- `GRIS_TEXTO #C9D0DA`: texto secundario y cuerpo sobre fondo oscuro.
- `GRIS_APAGADO #3B4E66`: elementos inactivos (los números no destacados de una secuencia).
- `GRIS_META #AEB6C2`: contador `n/total`.
- `LUZ_AZUL #2C5C8F`: color del foco de luz del fondo.

El rojo se usa en **un solo elemento protagonista por slide**, más detalles menores (números de lista, checks). Si hay dos cosas rojas grandes en un slide, una sobra.

## Tipografía: Inter (obligatoria)

Todo el carrusel va en **Inter** (`assets/fonts/Inter-400/500/700/800/900.ttf`), con `inter(peso, tamaño)`:

| Rol | Peso | Tamaño guía (px en 1080x1350) |
|---|---|---|
| Titular / hook | 800 | 84–104, interlineado ≈ 1.17x |
| Frase-remate en rojo | 900 | 104–116 |
| Contra-frase gris del hook | 800 | 60–64 |
| Subtítulo de ítem | 700–800 | 38–46 |
| Cuerpo | 400 | 30–38, interlineado ≈ 1.4x |
| Intro de slide ("Una web tiene…") | 500 | 44 |
| Palabra del CTA | 900 | 128 |
| Contador | 500 | 26 |

- Titulares en **frase normal (mayúscula inicial)**, no en TODO MAYÚSCULAS. Terminan en punto cuando son una afirmación: el punto da peso.
- Montserrat y League Gothic quedan en `assets/fonts/` solo por compatibilidad con piezas antiguas. No se usan en carruseles nuevos salvo que Herberth lo pida.

## Fondos

- **`fondo_hh(posicion, radio, intensidad)`**: el fondo estándar. Azul noche con un foco de luz azul difuso y grano sutil.
- **Rota la posición del foco en cada slide** para que el carrusel tenga ritmo al deslizar: arriba-derecha `(0.92, 0.08)`, centro-alto `(0.8, 0.15)` con `radio=1.2`, izquierda-media `(0.1, 0.45)`, abajo-derecha `(0.95, 0.95)`, abajo-izquierda `(0.15, 0.95)`. Nunca el mismo foco en dos slides seguidos.
- Los slides de frase (hook, tachado, sentencia) aguantan más luz (`radio` 1.0–1.2, `intensidad` 1.0). Los slides con lista o pasos van con menos luz (`intensidad` 0.7–0.8) para no competir con el texto.
- **`fondo_claro_puntos()`**: slide claro de contraste, blanco con grilla de puntos. **Máximo uno por carrusel**, ideal para el checklist "¿Te suena alguna?". Lleva el logo azul (`variante="azul"`) y el texto en azul noche.
- El texto nunca va sobre el punto más brillante del foco: el foco es atmósfera, el texto va en la zona oscura.
- Si Herberth aporta una foto real (BTS, set, equipo), pásala por `gradar_foto_hh()` y úsala como fondo de portada en vez del foco procedural. No inventes ni simules fotografías.

## Recursos gráficos del estilo v2

Todos están en `scripts/generar_slide.py`:

| Recurso | Función | Cuándo |
|---|---|---|
| Recuadro destacado | `caja_destacada(img, x, y, texto, font)` | La frase clave del hook o del titular ("en un solo día.", "correcto."). Uno por slide como máximo |
| Tachado a mano | `trazo_mano(d, x0, x1, y)` | Reencuadre: tachar la creencia equivocada y responder abajo en rojo |
| Línea divisoria corta | `d.line((M, y, M+170, y), fill=BLANCO, width=5)` | Separar el hook de la contra-frase |
| Secuencia con número activo | Números Inter 800 150px en `GRIS_APAGADO`, el activo en blanco con círculo rojo | "Hay N pasos y tú empezaste en el X" |
| Flecha curva + anotación | `flecha_curva(d, p0, p1, p2)` + `texto_con_sombra` en rojo | Señalar el elemento activo ("Tú empezaste acá.") |
| Tarjeta de checklist | `tarjeta_check(img, x0, y, x1, texto, font, marcada)` | En el slide claro. Una sola tarjeta marcada (azul noche + check rojo): la más dolorosa |
| Lista numerada | Número rojo Inter 800 + título Inter 800 + cuerpo gris, separadores `#1E3350` | Explicar piezas o conceptos |
| Pasos con círculo | Círculo rojo con número; el último relleno | Un orden o proceso |
| Etiqueta CTA | `etiqueta_cta(img, x, y, "PALABRA")` | Solo en el cierre |
| Texto mixto | `texto_mixto(d, x, y, [(texto, color), ...], font, ancho)` | Destacar en rojo el tiempo o beneficio dentro del CTA |
| Contador | `contador(img, n, total)` | En todos los slides |
| Logo | `logo_esquina(img)`: arriba a la izquierda, 78px | Portada, slides de explicación y cierre. En los slides de frase pura se puede omitir para dejar respirar |

## Estructura narrativa

Todo carrusel tiene **entre 6 y 10 slides**: un hook, desarrollo y cierre con CTA. Los tipos de slide del estilo v2 son estos:

1. **Hook**: afirmación que incomoda o sorprende, con la frase clave en recuadro rojo. Debajo, una línea corta y una contra-frase gris que explica el giro ("Y no por un hackeo. Por un correo de renovación que nadie leyó.").
2. **Reencuadre con tachado**: ~~la creencia común~~ tachada en rojo, y abajo la verdad en rojo Inter 900 ("Es un tema de dueño."). Una línea de cuerpo que la explica.
3. **Espejo "¿Te suena alguna?"**: slide claro con 4–5 tarjetas de síntomas reales del lector; una marcada.
4. **Secuencia "Tú empezaste acá"**: intro corta ("Una web tiene cuatro piezas, y van en un orden."), números con el activo en círculo rojo, flecha y anotación. Cierra con dos líneas en blanco del tipo "Por eso X. Y por eso Y."
5. **Explicación**: lista numerada de 3–5 ítems.
6. **Proceso / orden correcto**: pasos con círculo, con datos concretos (precios, plazos, nombres de herramientas).
7. **Sentencia**: frase de 2 líneas en blanco + remate en rojo 900, y una línea de consecuencia.
8. **CTA** (obligatorio, siempre el último): ver abajo.

No todos los carruseles usan los 8 tipos ni en ese orden. Elige los que el tema necesita, repite un tipo si hace falta (por ejemplo, dos de explicación) y evita slides de relleno o que prometan algo que el desarrollo no entrega.

## CTA obligatorio: "Comenta PALABRA"

Todo carrusel cierra con este formato:

- "Comenta" (Inter 700, 60px, blanco).
- La **PALABRA** en `etiqueta_cta` (recuadro rojo, Inter 900, levemente inclinado, con sombra). Una sola palabra, en mayúsculas, ligada al tema (DOMINIO, WEB, REELS, PRECIO…).
- La promesa en `texto_mixto` (Inter 700, 42px): **"y te mando [entregable concreto] para [resultado] [en X minutos / en X pasos]"**, con el tiempo o beneficio en rojo.
- El entregable debe existir o ser fácil de preparar (checklist, guion, plantilla, PDF). En la respuesta final, avísale a Herberth qué entregable prometió el CTA, para que lo tenga listo antes de publicar, y ofrécete a crearlo.
- Sin lenguaje de anuncio: nada de "no te lo pierdas", "¡aprovecha!" ni "link en la bio" como CTA principal.

## Variación: cómo mantenerlo vivo sin romper el estilo

Lo fijo es la tipografía, la paleta, los recursos, el fondo con foco, el contador y el CTA. Rota en cada carrusel nuevo al menos 2 de estas variables:

- **Alineación**: bloque a la izquierda (estándar), centrado (bueno para slides de frase y el CTA) o alineado abajo, dejando la luz arriba.
- **Orden de los tipos de slide** (por ejemplo: hook → espejo → reencuadre → explicación → sentencia → CTA).
- **Posición del foco de luz** por slide.
- **Dónde cae el recuadro destacado**: primera línea, última línea o una palabra suelta.
- **Qué slide es el claro**: el checklist u otro, como una comparación antes/después.
- **La palabra del CTA** y el entregable.

Nunca repitas el mismo hook, la misma secuencia de slides y la misma alineación de un carrusel anterior de HH.

## Voz y copy

- Tuteo, frases cortas, en el idioma del dueño de negocio, sin tecnicismos. Si un término técnico es inevitable, explícalo con una analogía cotidiana (por ejemplo, dominio = dirección del local).
- Datos concretos antes que adjetivos: precios reales en CLP, plazos, nombres de herramientas. Verifica los datos que no sean de conocimiento general.
- Nada de historias o cifras inventadas presentadas como reales. Si el hook usa un caso, es hipotético ("Tu web puede…") o real y verificado.
- Cero lenguaje de anuncio.

## Marca de agua / logo

En `assets/` hay tres variantes del isotipo HH (las dos H enfrentadas con punto rojo central), con fondo transparente real:
- `logo_hh_blanco.png`: para el fondo azul noche (estándar).
- `logo_hh_azul.png`: para el slide claro.
- `logo_hh_negro.png`: alternativa sobre fondos claros.

Nota técnica: los archivos originales no tenían canal alfa (PNG de fondo blanco opaco). Estas versiones ya están corregidas. Si Herberth sube un logo nuevo, verifica el canal alfa antes de usarlo.

Si el logo está presente, no repitas "HH" ni el @ como texto suelto en la misma gráfica.

## Referencias visuales que Herberth adjunte

Si llegan imágenes de referencia, analízalas antes de generar nada: dónde ubican el texto, cuánto espacio negativo dejan, qué recursos usan (recuadros, tachados, flechas, tarjetas) y cómo es el fondo. Replica la composición y los recursos dentro de la paleta y la tipografía de HH. No copies colores, fuentes ni textos ajenos.

## Qué entregar

### Paso 1: Guion
Antes de generar imágenes, define:
- Tipo de slide y función de cada lámina, en qué orden y por qué.
- Texto exacto de cada lámina.
- Qué variables rotaste respecto al estilo base (alineación, orden, focos, etc.).
- La palabra del CTA y el entregable prometido.
- Caption del post (máx. ~120 palabras, sin lenguaje de anuncio, repite el CTA al final) y 5–6 hashtags.

### Paso 2: PNG
- Arma un script propio importando `scripts/generar_slide.py`. Si Pillow no está instalado, instálalo (`pip install pillow numpy`).
- 1080x1350 (4:5). Margen lateral `M = 90`.
- Exporta `slide_01.png` … `slide_NN_cta.png` y entrégalos juntos, en orden.

### Control de calidad antes de entregar
Arma una hoja de contactos (todas las láminas reducidas en una imagen) y revísala, y luego revisa por separado cualquier slide dudoso:
- Texto cortado, superpuesto o saliéndose del margen.
- Palabras sueltas en la última línea de un párrafo (corrígelas con saltos manuales).
- Espacio mal repartido: bloque apretado arriba y la mitad inferior vacía sin intención.
- Contraste legible, logo sin tapar texto, contador presente, un solo protagonista rojo por slide.
- Puntuación del CTA (sin espacio antes de ":").

Corrige y regenera. No entregues un slide que no revisaste visualmente.

No prometas publicar en Instagram: el entregable son los PNG para que Herberth los suba, salvo que exista una herramienta de publicación conectada y autorizada.

## Antes de escribir el contenido

Pregunta solo si no está claro por el contexto:
1. Tema y objetivo (qué debe entender, sentir o hacer la audiencia).
2. Si es para HH o para un cliente.

No preguntes por paleta, tipografía ni estructura: eso ya está definido arriba.

## Registro de cambios

- **v2 (sept. 2026)**: Inter reemplaza a League Gothic/Montserrat. Fondo azul noche con foco de luz rotativo. Nuevos recursos: recuadro destacado, tachado a mano, secuencia "Tú empezaste acá" con flecha, slide claro con checklist, contador n/total. CTA obligatorio "Comenta PALABRA + entregable + tiempo". Reglas de variación para que cada carrusel sea distinto. Ejemplo de referencia en `ejemplos/carrusel_web_v2.py`.
- **v1**: League Gothic + Montserrat, estructura portada/cuerpo (A/B/C/D)/cierre.
