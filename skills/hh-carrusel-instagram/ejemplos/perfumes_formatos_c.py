"""EJEMPLO v3.2 (aprobado): formatos C1–C5 + A1/A7 en 3 paletas.
Perfumería · prueba de 5 formatos nuevos (C1–C5) + 2 de la skill, en 3 paletas.
1 A1 portada · 2 C3 aburre/vende · 3 C1 mini nota · 4 C2 nota iPhone + flores · 5 C5 notas en cielo · 6 A7 sentencia · 7 C4 CTA guarda
Fotos: Unsplash (Eve Maier, Olena Bohovyk, Sonny Mauricio, Sally)."""
import sys, os, glob, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from generar_slide import *
from PIL import Image, ImageDraw, ImageFilter

BASE = os.getcwd()
USAR_FOTOS = True   # False -> fondo_nubes() procedural en C2/C5
FOTOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fotos")
TOTAL = 7

def cx(d, t, f): return (ANCHO - d.textlength(t, font=f)) / 2

def foto_cover(ruta, w, h, desenfoque=0):
    im = Image.open(ruta).convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((l, t, l + w, t + h))
    return im.filter(ImageFilter.GaussianBlur(desenfoque)) if desenfoque else im

def pegar_redondeado(img, pieza, x, y, radio=36, sombra=True):
    w, h = pieza.size
    if sombra:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((x + 6, y + 16, x + w + 6, y + h + 16), radius=radio, fill=(6, 19, 35, 70))
        img.paste(Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(18))).convert("RGB"))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), radius=radio, fill=255)
    img.paste(pieza, (x, y), m)

def tarjeta(img, box, color=BLANCO, radio=44, sombra=True):
    x0, y0, x1, y1 = box
    if sombra:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((x0 + 4, y0 + 18, x1 + 4, y1 + 18), radius=radio, fill=(6, 19, 35, 60))
        img.paste(Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(22))).convert("RGB"))
    ImageDraw.Draw(img).rounded_rectangle(box, radius=radio, fill=color)

def pastilla(d, x, y, texto, font, bg, fg, pad=(18, 8), centrado=False):
    w = d.textlength(texto, font=font)
    if centrado: x = x - (w + 2 * pad[0]) / 2
    b = d.textbbox((0, 0), texto, font=font)
    d.rectangle((x, y, x + w + 2 * pad[0], y + (b[3] - b[1]) + 2 * pad[1] + 8), fill=bg)
    d.text((x + pad[0], y + pad[1] - b[1] + 4), texto, font=font, fill=fg)

def flor(img, cx_, cy_, r, color, petalos=8, giro=0):
    """Flor 'inflada' tipo 3D: pétalos redondeados con luz arriba-izquierda."""
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    c = np.array(color, float)
    for i in range(petalos):
        a = giro + i * 2 * math.pi / petalos
        px, py = cx_ + math.cos(a) * r * 0.66, cy_ + math.sin(a) * r * 0.66
        d.ellipse((px - r * 0.34, py - r * 0.34, px + r * 0.34, py + r * 0.34), fill=tuple(c.astype(int)) + (255,))
    d.ellipse((cx_ - r * 0.5, cy_ - r * 0.5, cx_ + r * 0.5, cy_ + r * 0.5), fill=tuple(c.astype(int)) + (255,))
    # luz
    luz = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse((cx_ - r * 0.9, cy_ - r * 0.95, cx_ + r * 0.2, cy_ + r * 0.1), fill=(255, 255, 255, 90))
    luz = luz.filter(ImageFilter.GaussianBlur(r * 0.25))
    mask = capa.split()[3]
    luz.putalpha(Image.composite(luz.split()[3], Image.new("L", img.size, 0), mask))
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse((cx_ - r, cy_ - r * 0.7, cx_ + r, cy_ + r * 1.2), fill=(0, 0, 0, 60))
    sombra = sombra.filter(ImageFilter.GaussianBlur(r * 0.3))
    base = Image.alpha_composite(img.convert("RGBA"), sombra)
    base = Image.alpha_composite(base, capa)
    base = Image.alpha_composite(base, luz)
    img.paste(base.convert("RGB"))

def destello(d, x, y, r, color):
    pts = []
    for i in range(16):
        a = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    d.polygon(pts, fill=color)

def meta(img, n, color):
    contador_color(img, n, TOTAL, color)

def construir(clave):
    P = PALETAS[clave]
    D = P["dev_estilo"]
    out = os.path.join(BASE, "versiones", clave) + "/"
    os.makedirs(out, exist_ok=True)
    caja_bg, caja_fg = P["caja"]
    claro_dev = D["txt"] == AZUL_NOCHE

    # 1 PORTADA (A1 centrado)
    img = P["tapa"](); logo_centrado(img, 100, P["tapa_logo"], 90)
    d = ImageDraw.Draw(img)
    fh = inter(800, 92)
    y = lineas(d, 0, 380, "Tu perfume\nhuele increíble.", fh, P["tapa_txt"], 108, centrado=True)
    fb = serif(700, 88)
    t = "En Instagram no huele."
    tapa_clara = P["tapa_txt"] == AZUL_NOCHE
    cb = (AZUL_NOCHE, BLANCO) if tapa_clara else (caja_bg, caja_fg)
    caja_destacada(img, cx(d, t, fb), y + 20, t, fb, bg=cb[0], fg=cb[1])
    d = ImageDraw.Draw(img)
    d.line((ANCHO / 2 - 85, y + 200, ANCHO / 2 + 85, y + 200), fill=P["tapa_txt"], width=5)
    lineas(d, 0, y + 250, "Lo que vende son las palabras\nde los primeros segundos.", inter(700, 48), P["tapa_txt2"], 64, centrado=True)
    meta(img, 1, P["tapa_meta"]); img.save(out + "slide_01.png")

    # 2 C3 aburre / vende
    img = P["dev"]((0.5, 0.2)); d = ImageDraw.Draw(img)
    fl = inter(900, 64)
    colw, gap, y0 = 430, 40, 410
    xs = [(ANCHO - 2 * colw - gap) // 2, (ANCHO - 2 * colw - gap) // 2 + colw + gap]
    for x, et in zip(xs, ["aburre", "vende"]):
        pastilla(d, x + colw / 2, 280, et, fl, "#E9B8D3" if claro_dev else CREMA, AZUL_NOCHE, pad=(22, 6), centrado=True)
    foto = foto_cover(os.path.join(FOTOS, "perfume_rosa.jpg"), colw, 640)
    oscura = foto.copy()
    grad = Image.new("L", (1, 640))
    for yy in range(640):
        grad.putpixel((0, yy), int(max(0, (yy - 280) / 360) ** 1.2 * 200))
    oscura.paste(Image.new("RGB", foto.size, (10, 10, 18)), (0, 0), grad.resize(foto.size))
    pegar_redondeado(img, foto, xs[0], y0, radio=30)
    pegar_redondeado(img, oscura, xs[1], y0, radio=30)
    d = ImageDraw.Draw(img)
    pastilla(d, xs[0] + 24, y0 + 640 - 90, "Nuevo stock disponible", inter(600 if False else 500, 26), "#E36A9A", BLANCO, pad=(14, 6))
    fr = serif(700, 50)
    for i, l in enumerate(["El perfume que", "te preguntan"]):
        d.text((xs[1] + colw / 2 - d.textlength(l, font=fr) / 2, y0 + 400 + i * 58), l, font=fr, fill=BLANCO)
    pastilla(d, xs[1] + colw / 2, y0 + 530, "EN EL ASCENSOR", inter(800, 30), ROJO, BLANCO, pad=(18, 8), centrado=True)
    fg = inter(700, 32)
    t = "Guárdalo y compártelo"
    d.text((cx(d, t, fg), y0 + 700), t, font=fg, fill=D["txt"])
    meta(img, 2, D["meta"]); img.save(out + "slide_02.png")

    # 3 C1 mini nota con tarjeta desplazada
    img = P["dev"]((0.3, 0.5)); d = ImageDraw.Draw(img)
    logo_esquina(img, D["logo"])
    x0, y0, x1, y1 = 150, 250, 960, 1110
    sombra_card = AZUL_NOCHE if claro_dev else "#1E3350"
    d.rounded_rectangle((x0 + 40, y0 + 40, x1 + 40, y1 + 40), radius=40, fill=sombra_card)
    tarjeta(img, (x0, y0, x1, y1), color=CREMA, radio=40, sombra=False)
    d = ImageDraw.Draw(img)
    d.text((x0 + 60, y0 + 70), "Hooks", font=inter(900, 96), fill="#111111")
    d.text((x0 + 60, y0 + 175), "de deseo", font=serif(800, 92), fill=ROJO)
    d.line((x0 + 60, y0 + 300, x0 + 400, y0 + 300), fill="#111111", width=3)
    items = ["Este es el perfume que te van a preguntar todo el día.",
             "Si solo pudieras tener un perfume, que sea este.",
             "Huele a lujo. Y no cuesta como uno.",
             "El perfume que usas cuando quieres que te recuerden."]
    fi, fn = inter(500, 34), inter(800, 34)
    y = y0 + 350
    for i, t in enumerate(items):
        d.text((x0 + 60, y), f"{i+1}.", font=fn, fill="#111111")
        y = lineas(d, x0 + 115, y, wrap(d, t, fi, x1 - x0 - 175), fi, "#1A1A1A", 46) + 26
    d.text((M, ALTO - 110), "1–4  |  HOOKS DE DESEO", font=inter(700, 24), fill=D["txt2"])
    meta(img, 3, D["meta"]); img.save(out + "slide_03.png")

    # 4 C2 nota iPhone sobre cielo + flores
    img = foto_cover(os.path.join(FOTOS, "cielo.jpg"), ANCHO, ALTO, desenfoque=2) if USAR_FOTOS else fondo_nubes(semilla=7)
    x0, y0, x1, y1 = 140, 200, 940, 1080
    tarjeta(img, (x0, y0, x1, y1), color=BLANCO, radio=50)
    d = ImageDraw.Draw(img)
    d.text((x0 + 45, y0 + 40), "‹ Notas", font=inter(500, 30), fill=ROJO)
    for i in range(4):
        cxx = x1 - 60 - i * 62
        d.ellipse((cxx - 18, y0 + 45, cxx + 18, y0 + 81), outline=ROJO, width=3)
    ft = serif(700, 64)
    for i, l in enumerate(["Hooks de", "curiosidad"]):
        d.text((cx(d, l, ft), y0 + 130 + i * 72), l, font=ft, fill=ROJO)
    bloques = [("1. “Nadie te dice esto de los perfumes dulces.”", "Promete un secreto y obliga a quedarse hasta el final."),
               ("2. “El error que hace que tu perfume dure 2 horas.”", "Nombra un problema que tu cliente ya vivió.")]
    y = y0 + 340
    fq, fp = inter(800, 38), inter(400, 32)
    for q, porq in bloques:
        y = lineas(d, 0, y, wrap(d, q, fq, x1 - x0 - 120), fq, AZUL_NOCHE, 50, centrado=True) + 20
        txt = wrap(d, "Por qué funciona: " + porq, fp, x1 - x0 - 140)
        for j, l in enumerate(txt.split("\n")):
            if j == 0:
                a = "Por qué funciona: "
                w = d.textlength(l, font=fp) + d.textlength(a, font=inter(800, 32)) - d.textlength(a, font=fp)
                xx = (ANCHO - w) / 2
                d.text((xx, y), a, font=inter(800, 32), fill=AZUL_NOCHE)
                d.text((xx + d.textlength(a, font=inter(800, 32)), y), l[len(a):], font=fp, fill="#3B4E66")
            else:
                d.text((cx(d, l, fp), y), l, font=fp, fill="#3B4E66")
            y += 44
        y += 50
    flor(img, 925, 1150, 125, (224, 36, 44), petalos=7, giro=0.3)
    flor(img, 1010, 985, 82, (244, 170, 196), petalos=7, giro=0.1)
    meta(img, 4, BLANCO); img.save(out + "slide_04.png")

    # 5 C5 notas en cielo (lista)
    img = foto_cover(os.path.join(FOTOS, "cielo2.jpg"), ANCHO, ALTO) if USAR_FOTOS else fondo_nubes(semilla=21)
    logo_centrado(img, 90, "blanco", 90)
    x0, y0, x1, y1 = 150, 290, 930, 1110
    tarjeta(img, (x0, y0, x1, y1), color=BLANCO, radio=56)
    d = ImageDraw.Draw(img)
    d.text((x0 + 45, y0 + 30), "‹", font=inter(500, 56), fill=AZUL_NOCHE)
    for i in range(3):
        cxx = x1 - 60 - i * 78
        d.ellipse((cxx - 26, y0 + 36, cxx + 26, y0 + 88), fill="#EEF1F5")
    d.text((x0 + 60, y0 + 120), "Hooks para cerrar la venta", font=inter(800, 36), fill=ROJO)
    hooks = ["“POV: encontraste tu perfume firma.”",
             "“Para quienes no quieren oler igual que todos.”",
             "“Pruébalo en tienda y decide en 10 segundos.”",
             "“Este es el regalo que no falla.”",
             "“Lo vas a querer en tu wishlist.”"]
    y = y0 + 200
    fh5 = inter(500, 36)
    for i, h in enumerate(hooks):
        txt = wrap(d, f"{i+1}  {h}", fh5, x1 - x0 - 120)
        y = lineas(d, x0 + 60, y, txt, fh5, "#111111", 48) + 30
    for i in range(5):
        cxx = x0 + 70 + i * 90
        d.ellipse((cxx - 22, y1 - 90, cxx + 22, y1 - 46), outline="#9AA4B2", width=3)
    meta(img, 5, BLANCO); img.save(out + "slide_05.png")

    # 6 A7 sentencia (skill), centrada
    img = P["dev"]((0.5, 0.6)); d = ImageDraw.Draw(img)
    logo_centrado(img, 100, D["logo"], 90)
    y = lineas(d, 0, 400, "Un perfume\nno se describe.", inter(800, 96), D["txt"], 112, centrado=True)
    y = lineas(d, 0, y + 40, "Se provoca.", serif(800, 130), D["acento"], 140, centrado=True)
    lineas(d, 0, y + 70, "Cuenta dónde se usa, quién lo usa\ny qué pasa cuando lo usa.", inter(400, 38), D["txt2"], 54, centrado=True)
    meta(img, 6, D["meta"]); img.save(out + "slide_06.png")

    # 7 C4 CTA "Guarda este post"
    # CTA: superficie distinta a la portada
    cta = {"rosa_celeste": (fondo_manchas(), AZUL_NOCHE, "#E9B8D3", AZUL_NOCHE, ROJO, "#5B6B80"),
           "crema_azul": (fondo_noche((0.5, 0.6)), BLANCO, CREMA, AZUL_NOCHE, BLANCO, GRIS_META),
           "vino_noche": (fondo_crema((0.5, 0.6)), AZUL_NOCHE, (120, 14, 30), BLANCO, (120, 14, 30), "#5B6B80")}[clave]
    img, ctxt, cbox, cboxtxt, cdest, cmeta = cta
    d = ImageDraw.Draw(img)
    fg1 = inter(800, 64)
    d.text((cx(d, "Guarda este", fg1), 150), "Guarda este", font=fg1, fill=ctxt)
    fp_ = inter(900, 150)
    w = d.textlength("post", font=fp_)
    d.rectangle((ANCHO / 2 - w / 2 - 70, 250, ANCHO / 2 + w / 2 + 70, 410), fill=cbox)
    d.text((cx(d, "post", fp_), 235), "post", font=fp_, fill=cboxtxt)
    destello(d, ANCHO / 2 - w / 2 - 70, 400, 60, cdest)
    fs_ = inter(700, 36)
    lineas(d, 0, 450, "y comenta tu perfume favorito\npara incluirlo en la parte II.", fs_, ctxt, 50, centrado=True)
    foto = foto_cover(os.path.join(FOTOS, "mano_perfume2.jpg"), 560, 620)
    pegar_redondeado(img, foto, (ANCHO - 560) // 2, 600, radio=36)
    meta(img, 7, cmeta); img.save(out + "slide_07_cta.png")

    return vista_previa(sorted(glob.glob(out + "slide_0*.png")), out + "vista_previa.png", columnas=7, ancho_mini=260)

claves = ["rosa_celeste", "crema_azul", "vino_noche"]
hojas = [construir(k) for k in claves]
print(comparar_versiones(hojas, [f"VERSIÓN {c} · {PALETAS[k]['nombre']}" for c, k in zip("ABC", claves)],
                         os.path.join(BASE, "versiones", "comparacion_versiones.png")))
