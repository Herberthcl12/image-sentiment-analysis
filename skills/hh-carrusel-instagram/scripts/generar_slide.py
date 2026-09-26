#!/usr/bin/env python3
"""
Generador de slides para carruseles de HH Studio Creativo.

Uso típico (estilo v2, ver ejemplos/carrusel_web_v2.py):

    from generar_slide import *

    img = fondo_hh(posicion=(0.92, 0.08))
    logo_esquina(img)
    d = ImageDraw.Draw(img)
    y = lineas(d, M, 300, "Tu web puede\ndesaparecer", inter(800, 92), BLANCO, 108)
    caja_destacada(img, M, y + 4, "en un solo día.", inter(800, 92))
    contador(img, 1, total=8)
    img.save("slide_01.png")

No pretende ser una librería genérica: es deliberadamente simple para que
Claude arme cada slide a medida según el guion aprobado, ajustando
posiciones caso a caso en vez de forzar un layout rígido.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import math
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(BASE, "assets", "fonts")
LOGOS = os.path.join(BASE, "assets")

# Paleta exacta de marca
AZUL_NOCHE = "#061323"
NEGRO = "#000000"
ROJO = "#FE0000"
BLANCO = "#FFFFFF"
GRIS_CLARO = "#D9D9D9"

# Dimensiones estándar de carrusel de Instagram (4:5, la más usada para carruseles)
ANCHO, ALTO = 1080, 1350

def fuente(nombre, tamano):
    rutas = {
        "inter": "Inter-400.ttf",
        "inter_medium": "Inter-500.ttf",
        "inter_bold": "Inter-700.ttf",
        "inter_extrabold": "Inter-800.ttf",
        "inter_black": "Inter-900.ttf",
        "league_gothic": "LeagueGothic-Regular.ttf",
        "league_gothic_ancha": "LeagueGothic-Wide-Regular.ttf",
        "montserrat": "Montserrat-Regular.ttf",
        "montserrat_semibold": "Montserrat-SemiBold.ttf",
        "montserrat_bold": "Montserrat-Bold.ttf",
        "montserrat_black": "Montserrat-Black.ttf",
        "montserrat_italic": "Montserrat-Italic.ttf",
    }
    return ImageFont.truetype(os.path.join(FONTS, rutas[nombre]), tamano)

def nuevo_slide(fondo=AZUL_NOCHE):
    return Image.new("RGB", (ANCHO, ALTO), fondo)

def _hex_a_rgb(hexcolor):
    h = hexcolor.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _mezclar(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def fondo_con_vida(color_base=AZUL_NOCHE, estilo="degradado_diagonal", intensidad_grano=10):
    """
    Genera un fondo con algo de profundidad en vez de un color plano:
    - degradado_diagonal: transición sutil del color base a una versión
      más clara/oscura de sí mismo, en diagonal.
    - viñeta: el centro queda levemente más claro que los bordes,
      dando foco visual al contenido.
    - plano: color sólido, sin efecto (para cuando el slide ya tiene
      mucho contenido y no conviene competir con más textura).
    Siempre se le suma un grano fotográfico sutil encima, consistente
    con la identidad de HH (nunca fondo perfectamente limpio).

    No inventa colores nuevos: solo varía la luminosidad del color de marca
    que le pases (AZUL_NOCHE o NEGRO), manteniéndose dentro de la paleta.
    """
    base = _hex_a_rgb(color_base) if isinstance(color_base, str) else color_base
    img = Image.new("RGB", (ANCHO, ALTO))
    px = img.load()

    if estilo == "degradado_diagonal":
        claro = tuple(min(255, c + 28) for c in base)
        for y in range(ALTO):
            for x in range(0, ANCHO, 4):  # paso de 4px: suficiente para un degradado suave, más rápido
                t = ((x / ANCHO) + (y / ALTO)) / 2
                color = _mezclar(base, claro, t)
                for dx in range(4):
                    if x + dx < ANCHO:
                        px[x + dx, y] = color
    elif estilo == "vineta":
        claro = tuple(min(255, c + 22) for c in base)
        cx, cy = ANCHO / 2, ALTO / 2
        max_d = math.hypot(cx, cy)
        for y in range(0, ALTO, 2):
            for x in range(0, ANCHO, 4):
                d = math.hypot(x - cx, y - cy) / max_d
                color = _mezclar(claro, base, min(1, d * 1.15))
                for dy in range(2):
                    for dx in range(4):
                        if x + dx < ANCHO and y + dy < ALTO:
                            px[x + dx, y + dy] = color
    else:  # plano
        img = Image.new("RGB", (ANCHO, ALTO), base)

    # grano fotográfico sutil
    if intensidad_grano > 0:
        grano = Image.effect_noise((ANCHO, ALTO), intensidad_grano * 4).convert("L")
        grano_rgb = Image.merge("RGB", (grano, grano, grano))
        img = Image.blend(img, grano_rgb, 0.035)

    return img

def gradar_foto_hh(ruta_entrada, ruta_salida=None, oscurecer=0.55, empuje_azul=18):
    """
    Toma una foto real (BTS de grabación, set, equipo) y la gradúa hacia
    el tono cinematográfico de referencia de HH: oscura, azulada en sombras,
    con viñeta. Uso: cuando Herberth aporta una foto real para la portada,
    en vez de usarla tal cual, pasarla por acá para unificar el tono con
    el resto del carrusel.
    No inventa contenido ni recorta al sujeto — solo ajusta color y luz.
    """
    import numpy as _np
    img = Image.open(ruta_entrada).convert("RGB")
    # reencuadre a proporción 4:5 (recorte centrado) para consistencia con el carrusel
    w, h = img.size
    target_ratio = ANCHO / ALTO
    if w / h > target_ratio:
        nuevo_w = int(h * target_ratio)
        offset = (w - nuevo_w) // 2
        img = img.crop((offset, 0, offset + nuevo_w, h))
    else:
        nuevo_h = int(w / target_ratio)
        offset = (h - nuevo_h) // 2
        img = img.crop((0, offset, w, offset + nuevo_h))
    img = img.resize((ANCHO, ALTO))

    arr = _np.array(img).astype("float32")
    arr *= oscurecer  # oscurece general
    arr[:, :, 2] = _np.clip(arr[:, :, 2] + empuje_azul, 0, 255)  # empuja azul en sombras
    arr[:, :, 0] = _np.clip(arr[:, :, 0] - empuje_azul * 0.4, 0, 255)  # resta un poco de rojo

    # viñeta
    cy, cx = ALTO / 2, ANCHO / 2
    yy, xx = _np.mgrid[0:ALTO, 0:ANCHO]
    d = _np.hypot(xx - cx, yy - cy) / math.hypot(cx, cy)
    vin = _np.clip(1 - (d - 0.3) * 0.6, 0.55, 1)
    arr *= vin[:, :, None]

    arr = _np.clip(arr, 0, 255).astype("uint8")
    resultado = Image.fromarray(arr, "RGB")
    if ruta_salida:
        resultado.save(ruta_salida)
    return resultado

def fondo_foco(color_base=AZUL_NOCHE, posicion=(0.82, 0.85), radio=0.55, intensidad=1.0, color_luz=None):
    """
    Fondo cinematográfico con un foco de luz en un punto (no una foto real,
    es una interpretación gráfica del mood: set oscuro, un solo punto de luz,
    mucho espacio negativo alrededor). Inspirado en referencias de set de
    grabación / escritorio de edición que Herberth aportó.

    posicion: (x, y) relativo al lienzo, 0-1. Ej: (0.82, 0.85) = esquina
    inferior derecha, como en las referencias (el sujeto/objeto va ahí,
    el texto va en la zona oscura opuesta).
    radio: qué tan grande es el área iluminada (0-1, relativo al ancho).
    color_luz: por defecto un azul frío más claro que el de marca — mantiene
    la familia de color, no introduce un tono nuevo.
    """
    base = np.array(_hex_a_rgb(color_base) if isinstance(color_base, str) else color_base, dtype=float)
    luz = np.array([70, 130, 190], dtype=float) if color_luz is None else np.array(_hex_a_rgb(color_luz), dtype=float)

    yy, xx = np.mgrid[0:ALTO, 0:ANCHO]
    xx = xx / ANCHO
    yy = yy / ALTO
    px, py = posicion
    dist = np.sqrt((xx - px) ** 2 + ((yy - py) * (ANCHO / ALTO)) ** 2)
    falloff = np.clip(1 - dist / radio, 0, 1) ** 2.2 * intensidad

    arr = base[None, None, :] + (luz - base)[None, None, :] * falloff[:, :, None]
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, "RGB")

    grano = Image.effect_noise((ANCHO, ALTO), 32).convert("L")
    grano_rgb = Image.merge("RGB", (grano, grano, grano))
    return Image.blend(img, grano_rgb, 0.03)

def fondo_haz_luz(color_base=AZUL_NOCHE, origen=(0.75, 0.0), destino=(0.75, 0.75), ancho_haz=0.22, color_luz=None):
    """
    Variante con un haz de luz tipo foco de set/teatro cayendo desde arriba,
    como en las referencias con el rig de luces. 'origen' y 'destino' son
    puntos relativos (0-1); el haz se dibuja como un cono difuminado entre
    ambos, sobre un fondo oscuro con viñeta.
    """
    base = np.array(_hex_a_rgb(color_base) if isinstance(color_base, str) else color_base, dtype=float)
    luz = np.array([120, 170, 210], dtype=float) if color_luz is None else np.array(_hex_a_rgb(color_luz), dtype=float)

    capa = Image.new("L", (ANCHO, ALTO), 0)
    draw = ImageDraw.Draw(capa)
    ox, oy = origen[0] * ANCHO, origen[1] * ALTO
    dx, dy = destino[0] * ANCHO, destino[1] * ALTO
    mitad = ancho_haz * ANCHO
    draw.polygon([(ox - mitad * 0.15, oy), (ox + mitad * 0.15, oy),
                  (dx + mitad, dy), (dx - mitad, dy)], fill=255)
    capa = capa.filter(ImageFilter.GaussianBlur(ANCHO * 0.05))

    arr_base = np.array(Image.new("RGB", (ANCHO, ALTO), tuple(base.astype(int))), dtype=float)
    mask = np.array(capa, dtype=float)[:, :, None] / 255.0
    arr = arr_base + (luz - base)[None, None, :] * mask
    # punto de luz más intenso donde el haz toca el suelo
    yy, xx = np.mgrid[0:ALTO, 0:ANCHO]
    xx_n, yy_n = xx / ANCHO, yy / ALTO
    dist = np.sqrt((xx_n - destino[0]) ** 2 + ((yy_n - destino[1]) * (ANCHO / ALTO)) ** 2)
    brillo_suelo = np.clip(1 - dist / 0.35, 0, 1) ** 2
    arr += (luz - base)[None, None, :] * brillo_suelo[:, :, None] * 0.6
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, "RGB")

    grano = Image.effect_noise((ANCHO, ALTO), 32).convert("L")
    grano_rgb = Image.merge("RGB", (grano, grano, grano))
    return Image.blend(img, grano_rgb, 0.035)

def pegar_logo(img, variante="blanco", esquina="inferior_derecha", tamano=70, margen=50):
    archivo = {"azul": "logo_hh_azul.png", "negro": "logo_hh_negro.png", "blanco": "logo_hh_blanco.png"}[variante]
    logo = Image.open(os.path.join(LOGOS, archivo)).convert("RGBA")
    ratio = tamano / logo.width
    logo = logo.resize((tamano, int(logo.height * ratio)))
    posiciones = {
        "superior_izquierda": (margen, margen),
        "superior_derecha": (img.width - logo.width - margen, margen),
        "inferior_izquierda": (margen, img.height - logo.height - margen),
        "inferior_derecha": (img.width - logo.width - margen, img.height - logo.height - margen),
        "centro": ((img.width - logo.width) // 2, (img.height - logo.height) // 2),
    }
    img.paste(logo, posiciones[esquina], logo)

def texto_multilinea(draw, texto, xy, font, fill, max_width=None, line_spacing=1.15, align="left"):
    """Dibuja texto respetando saltos de línea explícitos (\n)."""
    x, y = xy
    lineas = texto.split("\n")
    for linea in lineas:
        bbox = draw.textbbox((0, 0), linea, font=font)
        alto_linea = (bbox[3] - bbox[1]) * line_spacing
        draw.text((x, y), linea, font=font, fill=fill)
        y += alto_linea
    return y  # devuelve la posición y final, útil para encadenar elementos debajo

def texto_con_sombra(img, xy, texto, font, fill=ROJO, sombra_opacidad=110, offset=(0, 6), blur=8):
    """
    Dibuja texto con una sombra suave detrás — pensado sobre todo para el
    rojo de marca, que sin sombra queda plano sobre el fondo oscuro.
    Se aplica sobre 'img' directamente (no sobre un ImageDraw), porque
    necesita compositar una capa aparte para difuminar la sombra.
    Devuelve la imagen resultante (con la capa de texto ya fusionada).
    """
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    x, y = xy
    d.text((x + offset[0], y + offset[1]), texto, font=font, fill=(0, 0, 0, sombra_opacidad))
    capa = capa.filter(ImageFilter.GaussianBlur(blur))
    d2 = ImageDraw.Draw(capa)
    d2.text((x, y), texto, font=font, fill=fill)
    base = img.convert("RGBA")
    compuesta = Image.alpha_composite(base, capa)
    img.paste(compuesta.convert("RGB"))
    return img

# =====================================================================
#  ESTILO V2 (tipografía Inter + fondos con foco + recursos gráficos)
#  Aprobado por Herberth en sept. 2026 como estilo base de HH.
# =====================================================================

M = 90                    # margen lateral estándar
GRIS_TEXTO = "#C9D0DA"    # texto secundario sobre fondo oscuro
GRIS_APAGADO = "#3B4E66"  # elementos inactivos (números no destacados)
GRIS_META = "#AEB6C2"     # contador y metadatos
LUZ_AZUL = "#2C5C8F"      # color del foco de luz (familia del azul noche)

def inter(peso, tamano):
    """peso: 400, 500, 700, 800 o 900."""
    return ImageFont.truetype(os.path.join(FONTS, f"Inter-{peso}.ttf"), tamano)

def fondo_hh(posicion=(0.92, 0.08), radio=0.95, intensidad=0.9):
    """Fondo base v2: azul noche con un foco de luz azul difuso.
    Cambia 'posicion' en cada slide para dar ritmo al deslizar
    (arriba-derecha, abajo-izquierda, centro-alto, etc.)."""
    return fondo_foco(AZUL_NOCHE, posicion=posicion, radio=radio,
                      intensidad=intensidad, color_luz=LUZ_AZUL)

def fondo_claro_puntos(paso=34, color_punto="#D6DAE0"):
    """Slide claro de contraste (máx. 1 por carrusel): blanco con grilla de puntos."""
    img = Image.new("RGB", (ANCHO, ALTO), BLANCO)
    d = ImageDraw.Draw(img)
    for y in range(20, ALTO, paso):
        for x in range(20, ANCHO, paso):
            d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=color_punto)
    return img

def logo_esquina(img, variante="blanco", esquina="superior_izquierda", tamano=78):
    pegar_logo(img, variante, esquina, tamano=tamano, margen=M - 8)

def contador(img, n, total, oscuro=True):
    """'n/total' abajo a la derecha, discreto."""
    d = ImageDraw.Draw(img)
    t = f"{n}/{total}"
    f = inter(500, 26)
    w = d.textlength(t, font=f)
    d.text((ANCHO - M - w, ALTO - 90), t, font=f, fill=GRIS_META if oscuro else "#7A828E")

def wrap(d, texto, font, ancho):
    """Parte un texto en líneas que caben en 'ancho' px."""
    out, linea = [], ""
    for p in texto.split():
        prueba = (linea + " " + p).strip()
        if d.textlength(prueba, font=font) <= ancho:
            linea = prueba
        else:
            out.append(linea); linea = p
    out.append(linea)
    return "\n".join(out)

def lineas(d, x, y, texto, font, fill, alto_linea, centrado=False):
    """Dibuja líneas separadas por \n. Devuelve la y siguiente.
    centrado=True centra cada línea en el lienzo (ignora x)."""
    for l in texto.split("\n"):
        xx = (ANCHO - d.textlength(l, font=font)) / 2 if centrado else x
        d.text((xx, y), l, font=font, fill=fill)
        y += alto_linea
    return y

def caja_destacada(img, x, y, texto, font, bg=ROJO, fg=BLANCO, pad=(22, 10)):
    """Frase clave sobre un recuadro sólido (rojo por defecto). Devuelve el bbox del texto."""
    d = ImageDraw.Draw(img)
    b = d.textbbox((x, y), texto, font=font)
    d.rectangle((b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1] + 6), fill=bg)
    d.text((x, y), texto, font=font, fill=fg)
    return b

def trazo_mano(d, x0, x1, y, color=ROJO, grosor=12):
    """Tachado irregular 'hecho a mano' sobre una frase (x0..x1 a la altura y)."""
    pts = []
    for i in range(41):
        t = i / 40
        pts.append((x0 - 10 + (x1 - x0 + 40) * t, y + 6 * math.sin(t * math.pi * 1.3) - 8 * t))
    d.line(pts, fill=color, width=grosor, joint="curve")
    for px, py in (pts[0], pts[-1]):
        d.ellipse((px - grosor / 2, py - grosor / 2, px + grosor / 2, py + grosor / 2), fill=color)

def flecha_curva(d, p0, p1, p2, color=ROJO, grosor=6):
    """Flecha curva (Bézier cuadrática p0 -> p2 con control p1) con punta en p2."""
    pts = []
    for i in range(31):
        t = i / 30
        pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]))
    d.line(pts, fill=color, width=grosor, joint="curve")
    (ax, ay), (bx, by) = pts[-4], pts[-1]
    ang = math.atan2(by - ay, bx - ax)
    for s_ in (2.6, -2.6):
        d.line([(bx, by), (bx + 34 * math.cos(ang + s_), by + 34 * math.sin(ang + s_))], fill=color, width=grosor)

def tarjeta_check(img, x0, y, x1, texto, font, marcada=False):
    """Tarjeta de checklist para el slide claro. Devuelve la y inferior."""
    d = ImageDraw.Draw(img)
    txt = wrap(d, texto, font, x1 - x0 - 150)
    n = txt.count("\n") + 1
    h = 58 + n * 46
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((x0 + 4, y + 10, x1 + 4, y + h + 10), radius=18, fill=(6, 19, 35, 45))
    sombra = sombra.filter(ImageFilter.GaussianBlur(12))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sombra).convert("RGB"))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y, x1, y + h), radius=18, fill=AZUL_NOCHE if marcada else BLANCO,
                        outline=None if marcada else "#E3E6EA", width=2)
    cb = (x0 + 36, y + h / 2 - 24, x0 + 84, y + h / 2 + 24)
    d.rounded_rectangle(cb, radius=8, outline=ROJO if marcada else AZUL_NOCHE, width=5)
    if marcada:
        d.line([(cb[0] + 11, cb[1] + 25), (cb[0] + 21, cb[1] + 35), (cb[0] + 38, cb[1] + 13)],
               fill=ROJO, width=6, joint="curve")
    lineas(d, x0 + 120, y + 29, txt, font, BLANCO if marcada else AZUL_NOCHE, 46)
    return y + h

def etiqueta_cta(img, x, y, palabra, font=None, angulo=2, bg=ROJO, fg=BLANCO):
    """La PALABRA del CTA 'Comenta ___' en recuadro rojo levemente inclinado con sombra.
    Devuelve (imagen, y_inferior): reasignar con img, y = etiqueta_cta(...)."""
    font = font or inter(900, 128)
    d = ImageDraw.Draw(img)
    b = d.textbbox((0, 0), palabra, font=font)
    bw, bh = b[2] - b[0] + 70, b[3] - b[1] + 60
    capa = Image.new("RGBA", (bw + 80, bh + 80), (0, 0, 0, 0))
    cd = ImageDraw.Draw(capa)
    cd.rounded_rectangle((40, 40, 40 + bw, 40 + bh), radius=10, fill=bg)
    cd.text((40 + 35 - b[0], 40 + 30 - b[1]), palabra, font=font, fill=fg)
    capa = capa.rotate(angulo, resample=Image.BICUBIC, expand=False)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x + 10, y + 20, x + bw + 10, y + 20 + bh), radius=10, fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    base = Image.alpha_composite(img.convert("RGBA"), sh)
    base.paste(capa, (x - 40, y - 40), capa)
    return base.convert("RGB"), y + bh

def texto_mixto(d, x, y, partes, font, ancho_max, alto_linea=60):
    """Párrafo con tramos de distinto color: partes = [("texto", color), ...].
    Útil para destacar en rojo 'en 10 minutos' dentro del CTA. Devuelve la y final."""
    xx = x
    for texto, color in partes:
        for palabra in texto.split(" "):
            if not palabra:
                continue
            if xx + d.textlength(palabra, font=font) > x + ancho_max:
                xx, y = x, y + alto_linea
            d.text((xx, y), palabra, font=font, fill=color)
            xx += d.textlength(palabra + " ", font=font)
    return y + alto_linea

# =====================================================================
#  ESTILO V3: formatos B (referencias aprobadas sept. 2026)
# =====================================================================

NEGRO_GRANO = "#050505"
CREMA = "#F2EFEA"         # blanco cálido para texto grande sobre negro
PAPEL = (236, 234, 230)    # base del fondo papel (derivado del blanco)

def serif(peso, tamano):
    """Playfair Display Italic (500, 700, 800). Para palabras destacadas en cursiva."""
    return ImageFont.truetype(os.path.join(FONTS, f"PlayfairDisplay-Italic-{peso}.ttf"), tamano)

def serif_fina(tamano):
    """Instrument Serif Italic: cursiva más fina y editorial (alternativa a Playfair)."""
    return ImageFont.truetype(os.path.join(FONTS, "InstrumentSerif-Italic.ttf"), tamano)

def fuente_tematica(familia, peso=700, italic=False, tamano=100, carpeta="/tmp/fuentes_hh"):
    """Descarga una fuente de Google Fonts (TTF) para un carrusel temático.
    Devuelve ImageFont o None si no hay red (usar entonces Inter/serif como respaldo).
    Ej: fuente_tematica("Bebas Neue", 400, tamano=180)."""
    import subprocess, re
    os.makedirs(carpeta, exist_ok=True)
    nombre = f"{familia.replace(' ', '')}-{peso}{'i' if italic else ''}.ttf"
    ruta = os.path.join(carpeta, nombre)
    if not os.path.exists(ruta):
        eje = f"ital,wght@1,{peso}" if italic else f"wght@{peso}"
        url = f"https://fonts.googleapis.com/css2?family={familia.replace(' ', '+')}:{eje}"
        try:
            css = subprocess.run(["curl", "-sS", "-m", "20", "-A", "Mozilla/4.0", url], capture_output=True, text=True).stdout
            ttf = re.search(r"https://[^)]+\.ttf", css)
            if not ttf:
                return None
            subprocess.run(["curl", "-sS", "-m", "30", "-o", ruta, ttf.group(0)], check=True)
        except Exception:
            return None
    try:
        return ImageFont.truetype(ruta, tamano)
    except Exception:
        return None

def _grano(img, fuerza=0.05, sigma=40):
    g = Image.effect_noise((ANCHO, ALTO), sigma).convert("L")
    return Image.blend(img, Image.merge("RGB", (g, g, g)), fuerza)

def fondo_negro():
    """B2/B4/B5: negro con grano fotográfico."""
    return _grano(Image.new("RGB", (ANCHO, ALTO), NEGRO_GRANO), 0.06, 50)

def fondo_resplandor(base="#050A12", luz=(190, 0, 0), centro=(0.5, 0.45), radio=0.62, puntos=True):
    """B1: resplandor difuso (rojo por defecto) detrás del texto central + grilla de puntos."""
    b = np.array(_hex_a_rgb(base), float)
    yy, xx = np.mgrid[0:ALTO, 0:ANCHO]
    d = np.sqrt(((xx / ANCHO) - centro[0]) ** 2 + (((yy / ALTO) - centro[1]) * ALTO / ANCHO) ** 2)
    f = np.clip(1 - d / radio, 0, 1) ** 1.8
    arr = b + (np.array(luz, float) - b) * f[:, :, None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
    if puntos:
        dr = ImageDraw.Draw(img)
        for y in range(24, ALTO, 38):
            for x in range(24, ANCHO, 38):
                dr.ellipse((x - 1.4, y - 1.4, x + 1.4, y + 1.4), fill=(70, 78, 92))
    return _grano(img, 0.04)

def fondo_papel():
    """B3: papel claro con textura y leves manchas."""
    img = _grano(Image.new("RGB", (ANCHO, ALTO), PAPEL), 0.10, 60)
    manchas = Image.effect_noise((ANCHO // 8, ALTO // 8), 90).convert("L").resize((ANCHO, ALTO), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
    return Image.composite(img, Image.new("RGB", (ANCHO, ALTO), (222, 219, 214)), manchas.point(lambda v: 150 + v // 3))

def linea_mixta(d, y_base, partes, centrado=True, x=M):
    """Una línea que mezcla fuentes/colores alineados por línea base.
    partes = [(texto, font, color), (texto, font, color, True)]  -> True = subrayado."""
    ancho = sum(d.textlength(p[0], font=p[1]) for p in partes)
    xx = (ANCHO - ancho) / 2 if centrado else x
    for p in partes:
        t, f, c = p[:3]
        d.text((xx, y_base), t, font=f, fill=c, anchor="ls")
        w = d.textlength(t, font=f)
        if len(p) > 3 and p[3]:
            d.line((xx + 4, y_base + 14, xx + w - 4, y_base + 14), fill=c, width=6)
        xx += w
    return xx

def boton_flecha(d, cy=1020, color=BLANCO):
    """B1: botón ovalado con flecha →, centrado, invita a deslizar."""
    d.rounded_rectangle((ANCHO / 2 - 58, cy - 30, ANCHO / 2 + 58, cy + 30), radius=30, outline=color, width=3)
    d.line((ANCHO / 2 - 28, cy, ANCHO / 2 + 26, cy), fill=color, width=3)
    d.line([(ANCHO / 2 + 10, cy - 14), (ANCHO / 2 + 26, cy), (ANCHO / 2 + 10, cy + 14)], fill=color, width=3)

def logo_centrado(img, y, variante="blanco", tamano=90):
    lg = Image.open(os.path.join(LOGOS, f"logo_hh_{variante}.png")).convert("RGBA")
    lg = lg.resize((tamano, int(lg.height * tamano / lg.width)))
    img.paste(lg, ((ANCHO - tamano) // 2, int(y)), lg)

def vista_previa(rutas_png, salida, columnas=4, ancho_mini=360):
    """Hoja de contactos con todas las láminas en miniatura y su número.
    OBLIGATORIA antes de entregar: se muestra a Herberth y se espera 'confirmo'."""
    minis = [Image.open(r).convert("RGB").resize((ancho_mini, int(ancho_mini * ALTO / ANCHO))) for r in rutas_png]
    h = minis[0].height
    filas = (len(minis) + columnas - 1) // columnas
    gap = 16
    hoja = Image.new("RGB", (columnas * ancho_mini + (columnas + 1) * gap, filas * (h + 44) + gap), (24, 24, 28))
    d = ImageDraw.Draw(hoja)
    for i, m in enumerate(minis):
        x = gap + (i % columnas) * (ancho_mini + gap)
        y = gap + (i // columnas) * (h + 44)
        hoja.paste(m, (x, y))
        d.text((x, y + h + 8), f"{i + 1}", font=inter(700, 24), fill=BLANCO)
    hoja.save(salida)
    return salida

# =====================================================================
#  V3.1: SISTEMA DE PALETAS (aprobado por Herberth, sept. 2026)
#  Cada paleta define 3 roles de fondo + colores de texto por rol.
#  Los formatos (A1…B5) se dibujan leyendo estos roles, así cualquier
#  estructura nueva se puede "vestir" con cualquier paleta.
# =====================================================================

def fondo_radial(c_centro, c_borde, centro=(0.4, 0.4), curva=1.4, grano=0.045, alcance=0.85):
    """Degradado radial suave (centro -> bordes) con grano. Base de todas las paletas v3.1."""
    yy, xx = np.mgrid[0:ALTO, 0:ANCHO]
    d = np.sqrt(((xx / ANCHO) - centro[0]) ** 2 + (((yy / ALTO) - centro[1]) * ALTO / ANCHO) ** 2)
    t = np.clip(d / alcance, 0, 1) ** curva
    a, b = np.array(c_centro, float), np.array(c_borde, float)
    img = Image.fromarray(np.clip(a + (b - a) * t[:, :, None], 0, 255).astype("uint8"))
    g = Image.effect_noise((ANCHO, ALTO), 45).convert("L")
    return Image.blend(img, Image.merge("RGB", (g, g, g)), grano)

# Superficies (fondos completos). Mueve 'centro' en cada slide para dar ritmo.
def fondo_noche(centro=(0.35, 0.4)):
    """Oscuro por defecto: casi negro al centro, azul noche en los bordes.
    (El negro plano, fondo_negro(), se reserva para slides de impacto o legibilidad.)"""
    return fondo_radial((7, 8, 12), (12, 34, 64), centro=centro, curva=1.3, grano=0.05)

def fondo_vino(centro=(0.3, 0.35)):
    """Rojo vino profundo con sombra hacia los bordes (NO el rojo chillón)."""
    return fondo_radial((150, 16, 34), (66, 6, 18), centro=centro, curva=1.2)

def fondo_crema(centro=(0.3, 0.3)):
    """Blanco cálido que se enfría hacia un azul muy suave en los bordes."""
    return fondo_radial((248, 245, 240), (214, 224, 238), centro=centro, curva=1.3, grano=0.06)

def fondo_rosa_celeste(centro=(0.35, 0.3)):
    """Rosado suave al centro que pasa a celeste en los bordes."""
    return fondo_radial((252, 214, 222), (206, 226, 246), centro=centro, curva=1.1, grano=0.05)

def fondo_celeste(centro=(0.35, 0.4)):
    """Celeste muy claro, para desarrollos luminosos."""
    return fondo_radial((244, 248, 253), (200, 222, 244), centro=centro, curva=1.3, grano=0.05)

def fondo_rojo_profundo(centro=(0.4, 0.4)):
    """Rojo de marca oscurecido en los bordes, para portadas/CTA potentes sin gritar."""
    return fondo_radial((214, 10, 18), (120, 4, 12), centro=centro, curva=1.3)

# Estilos de texto por tipo de superficie
_OSCURO = dict(txt=BLANCO, txt2=GRIS_TEXTO, crema=CREMA, acento=ROJO, logo="blanco", meta=GRIS_META)
_CLARO = dict(txt=AZUL_NOCHE, txt2="#4A5A70", crema=AZUL_NOCHE, acento=ROJO, logo="azul", meta="#5B6B80")

PALETAS = {
    # tapa = superficie de portada (el CTA puede usarla o elegir otra: dev, negro plano, etc.)
    # dev  = slides de desarrollo
    # caja = (fondo, texto) del recuadro destacado y la etiqueta del CTA
    # acento_tapa = color de la palabra destacada dentro del CTA
    "vino_noche": dict(
        nombre="Vino + noche", uso="bebidas, gastronomía, nocturno, eventos, cualquier tema cálido o intenso",
        tapa=fondo_vino, tapa_txt=BLANCO, tapa_txt2="#F3D9DD", tapa_logo="blanco", tapa_meta="#F3D9DD",
        caja=(AZUL_NOCHE, BLANCO), acento_tapa="#FFB3BE",
        dev=fondo_noche, dev_estilo=_OSCURO),
    "crema_azul": dict(
        nombre="Crema + azul", uso="premium, corporativo, servicios, tecnología, legal, finanzas",
        tapa=fondo_crema, tapa_txt=AZUL_NOCHE, tapa_txt2="#3B4E66", tapa_logo="azul", tapa_meta="#5B6B80",
        caja=(AZUL_NOCHE, BLANCO), acento_tapa=ROJO,
        dev=fondo_noche, dev_estilo=_OSCURO),
    "rosa_celeste": dict(
        nombre="Rosa + celeste", uso="belleza, lifestyle, bienestar, educación amable, feed más claro",
        tapa=fondo_rosa_celeste, tapa_txt=AZUL_NOCHE, tapa_txt2="#3B4E66", tapa_logo="azul", tapa_meta="#5B6B80",
        caja=(ROJO, BLANCO), acento_tapa=ROJO,
        dev=fondo_celeste, dev_estilo=_CLARO),
    "foco_clasico": dict(
        nombre="Foco clásico (v2)", uso="marketing, web, IA, negocios: la estética original de HH",
        tapa=lambda centro=(0.92, 0.08): fondo_hh(posicion=centro), tapa_txt=BLANCO, tapa_txt2=GRIS_TEXTO,
        tapa_logo="blanco", tapa_meta=GRIS_META, caja=(ROJO, BLANCO), acento_tapa=ROJO,
        dev=lambda centro=(0.9, 0.9): fondo_hh(posicion=centro, intensidad=0.75), dev_estilo=_OSCURO),
}
# Superficie de contraste común a todas: fondo_papel() (1 slide por carrusel, listas densas).

def contador_color(img, n, total, color):
    """Contador n/total con color explícito (para superficies de color o claras)."""
    d = ImageDraw.Draw(img); t = f"{n}/{total}"; f = inter(500, 26)
    d.text((ANCHO - M - d.textlength(t, font=f), ALTO - 90), t, font=f, fill=color)

def comparar_versiones(hojas, nombres, salida):
    """Apila varias vistas previas (una por paleta) con su rótulo, para elegir en una sola imagen."""
    ims = [Image.open(h).convert("RGB") for h in hojas]
    etq = 70
    ancho = max(i.width for i in ims)
    comp = Image.new("RGB", (ancho, sum(i.height + etq for i in ims)), (24, 24, 28))
    d = ImageDraw.Draw(comp); y = 0
    for n, im in zip(nombres, ims):
        d.text((20, y + 18), n, font=inter(800, 34), fill=BLANCO)
        comp.paste(im, (0, y + etq)); y += im.height + etq
    comp.save(salida)
    return salida

# =====================================================================
#  V3.2: FORMATOS C (notas, tarjetas, comparación con foto, CTA guarda)
#        + fondos sin fotos (nubes y manchas difuminadas)
# =====================================================================

def fondo_nubes(cielo_arriba=(110, 162, 220), cielo_abajo=(200, 225, 248), densidad=9, semilla=7):
    """Cielo con nubes difuminadas, 100 % procedural (no necesita descargar fotos).
    Úsalo cuando no haya foto disponible o no se pueda descargar."""
    import random as _r
    _r.seed(semilla)
    yy = np.linspace(0, 1, ALTO)[:, None, None]
    a, b = np.array(cielo_arriba, float), np.array(cielo_abajo, float)
    cielo = np.repeat(a + (b - a) * yy, ANCHO, axis=1)
    nubes = np.zeros((ALTO, ANCHO), float)     # máscara de densidad de nube (0-1)
    sombra = np.zeros((ALTO, ANCHO), float)
    for _ in range(densidad):
        m = Image.new("L", (ANCHO, ALTO), 0)
        sm = Image.new("L", (ANCHO, ALTO), 0)
        d, ds = ImageDraw.Draw(m), ImageDraw.Draw(sm)
        cx_, cy_ = _r.randint(-150, ANCHO + 150), _r.randint(-80, ALTO + 80)
        for _ in range(_r.randint(6, 10)):
            rx, ry = _r.randint(120, 280), _r.randint(70, 150)
            ox, oy = _r.randint(-240, 240), _r.randint(-70, 50)
            d.ellipse((cx_ + ox - rx, cy_ + oy - ry, cx_ + ox + rx, cy_ + oy + ry), fill=_r.randint(150, 230))
        ds.ellipse((cx_ - 300, cy_ + 30, cx_ + 300, cy_ + 150), fill=120)
        nubes = np.maximum(nubes, np.array(m.filter(ImageFilter.GaussianBlur(_r.randint(38, 60))), float) / 255)
        sombra = np.maximum(sombra, np.array(sm.filter(ImageFilter.GaussianBlur(60)), float) / 255)
    sombra = sombra * (1 - nubes)
    blanco = np.array([255, 255, 255], float)
    tono_sombra = np.array([150, 176, 208], float)
    arr = cielo + (tono_sombra - cielo) * (sombra[:, :, None] * 0.35)
    arr = arr + (blanco - arr) * (nubes[:, :, None] ** 0.8)
    return _grano(Image.fromarray(np.clip(arr, 0, 255).astype("uint8")), 0.03)

def fondo_manchas(base=(246, 240, 242), colores=((250, 200, 214), (196, 220, 246), (255, 255, 255)), n=6, semilla=3):
    """Fondo difuminado con manchas suaves de color (tipo luz de estudio / bruma).
    Alternativa sin fotos para portadas y CTA claros."""
    import random as _r
    _r.seed(semilla)
    arr = np.ones((ALTO, ANCHO, 3), float) * np.array(base, float)
    for i in range(n):
        c = np.array(colores[i % len(colores)], float)
        m = Image.new("L", (ANCHO, ALTO), 0)
        r = _r.randint(260, 480)
        x, y = _r.randint(0, ANCHO), _r.randint(0, ALTO)
        ImageDraw.Draw(m).ellipse((x - r, y - r, x + r, y + r), fill=210)
        k = np.array(m.filter(ImageFilter.GaussianBlur(130)), float)[:, :, None] / 255
        arr = arr + (c - arr) * k
    return _grano(Image.fromarray(np.clip(arr, 0, 255).astype("uint8")), 0.04)

def foto_cover(ruta, w, h, desenfoque=0):
    """Recorta una foto para llenar w x h (como 'cover' en CSS)."""
    im = Image.open(ruta).convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((l, t, l + w, t + h))
    return im.filter(ImageFilter.GaussianBlur(desenfoque)) if desenfoque else im

def pegar_redondeado(img, pieza, x, y, radio=36, sombra=True):
    """Pega una imagen con esquinas redondeadas y sombra suave."""
    w, h = pieza.size
    if sombra:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((x + 6, y + 16, x + w + 6, y + h + 16), radius=radio, fill=(6, 19, 35, 70))
        img.paste(Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(18))).convert("RGB"))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), radius=radio, fill=255)
    img.paste(pieza, (x, y), m)

def oscurecer_abajo(foto, desde=0.45, fuerza=200):
    """Degradado oscuro en la parte baja de una foto, para que el texto encima se lea."""
    w, h = foto.size
    g = Image.new("L", (1, h))
    for yy in range(h):
        g.putpixel((0, yy), int(max(0, (yy / h - desde) / (1 - desde)) ** 1.2 * fuerza))
    out = foto.copy()
    out.paste(Image.new("RGB", foto.size, (10, 10, 18)), (0, 0), g.resize(foto.size))
    return out

def tarjeta(img, box, color=BLANCO, radio=44, sombra=True):
    """Tarjeta redondeada con sombra difusa (base de C1, C2 y C5)."""
    x0, y0, x1, y1 = box
    if sombra:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((x0 + 4, y0 + 18, x1 + 4, y1 + 18), radius=radio, fill=(6, 19, 35, 60))
        img.paste(Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(22))).convert("RGB"))
    ImageDraw.Draw(img).rounded_rectangle(box, radius=radio, fill=color)

def tarjeta_desplazada(img, box, color=CREMA, color_sombra=AZUL_NOCHE, offset=40, radio=40):
    """C1: tarjeta clara con una tarjeta sólida desplazada detrás (efecto nota apilada)."""
    x0, y0, x1, y1 = box
    ImageDraw.Draw(img).rounded_rectangle((x0 + offset, y0 + offset, x1 + offset, y1 + offset), radius=radio, fill=color_sombra)
    tarjeta(img, box, color=color, radio=radio, sombra=False)

def barra_notas(d, box, estilo="notas", color=ROJO):
    """Barra superior tipo app de notas del iPhone dentro de una tarjeta.
    estilo='notas' -> '‹ Notas' + 4 íconos circulares (C2); estilo='iconos' -> '‹' + 3 botones grises (C5)."""
    x0, y0, x1, _ = box
    if estilo == "notas":
        d.text((x0 + 45, y0 + 40), "‹ Notas", font=inter(500, 30), fill=color)
        for i in range(4):
            c = x1 - 60 - i * 62
            d.ellipse((c - 18, y0 + 45, c + 18, y0 + 81), outline=color, width=3)
    else:
        d.text((x0 + 45, y0 + 30), "‹", font=inter(500, 56), fill=AZUL_NOCHE)
        for i in range(3):
            c = x1 - 60 - i * 78
            d.ellipse((c - 26, y0 + 36, c + 26, y0 + 88), fill="#EEF1F5")

def pastilla(d, x, y, texto, font, bg, fg, pad=(18, 8), centrado=False):
    """Etiqueta de texto sobre un rectángulo de color (aburre/vende, 'EN EL ASCENSOR', etc.)."""
    w = d.textlength(texto, font=font)
    if centrado:
        x = x - (w + 2 * pad[0]) / 2
    b = d.textbbox((0, 0), texto, font=font)
    d.rectangle((x, y, x + w + 2 * pad[0], y + (b[3] - b[1]) + 2 * pad[1] + 8), fill=bg)
    d.text((x + pad[0], y + pad[1] - b[1] + 4), texto, font=font, fill=fg)

def flor(img, cx_, cy_, r, color, petalos=7, giro=0):
    """Flor decorativa 'inflada' tipo 3D con luz y sombra (decoración de C2)."""
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    col = tuple(int(v) for v in color) + (255,)
    for i in range(petalos):
        a = giro + i * 2 * math.pi / petalos
        px, py = cx_ + math.cos(a) * r * 0.66, cy_ + math.sin(a) * r * 0.66
        d.ellipse((px - r * 0.34, py - r * 0.34, px + r * 0.34, py + r * 0.34), fill=col)
    d.ellipse((cx_ - r * 0.5, cy_ - r * 0.5, cx_ + r * 0.5, cy_ + r * 0.5), fill=col)
    luz = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse((cx_ - r * 0.9, cy_ - r * 0.95, cx_ + r * 0.2, cy_ + r * 0.1), fill=(255, 255, 255, 90))
    luz = luz.filter(ImageFilter.GaussianBlur(r * 0.25))
    luz.putalpha(Image.composite(luz.split()[3], Image.new("L", img.size, 0), capa.split()[3]))
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse((cx_ - r, cy_ - r * 0.7, cx_ + r, cy_ + r * 1.2), fill=(0, 0, 0, 60))
    base = Image.alpha_composite(img.convert("RGBA"), sombra.filter(ImageFilter.GaussianBlur(r * 0.3)))
    base = Image.alpha_composite(Image.alpha_composite(base, capa), luz)
    img.paste(base.convert("RGB"))

def destello(d, x, y, r, color):
    """Estrella de 8 puntas (acento del CTA 'Guarda este post')."""
    pts = []
    for i in range(16):
        a = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    d.polygon(pts, fill=color)

if __name__ == "__main__":
    print("Módulo de utilidades — importar, no ejecutar directo.")
