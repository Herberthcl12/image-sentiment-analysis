"""Fútbol · prueba formatos D1–D5 + 2 de la skill (A2, B5), en 3 paletas.
1 D2 gráfico · 2 A2 tachado · 3 D3 lista 01–04 · 4 D4 paso con íconos · 5 D5 papel arrugado · 6 B5 frase · 7 D1 CTA lead magnet"""
import sys, os, glob, math, random
import numpy as np
sys.path.insert(0, "/root/.claude/skills/synced/a83d7b8b-6484-4f1d-b672-5dde2b410928_0fec2520-89fe-4255-ba8e-9c8f4e367f11/hh-carrusel-instagram/scripts")
from generar_slide import *
from PIL import Image, ImageDraw, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
TOTAL = 7
def cx(d, t, f): return (ANCHO - d.textlength(t, font=f)) / 2

# ---------- superficies ----------
def textura_oscura(img, fuerza=0.09):
    g = Image.effect_noise((ANCHO, ALTO), 70).convert("L").filter(ImageFilter.GaussianBlur(0.6))
    return Image.blend(img, Image.merge("RGB", (g, g, g)), fuerza)

def glow(img, x, y, r, color, alpha=150):
    capa = Image.new("L", img.size, 0)
    ImageDraw.Draw(capa).ellipse((x - r, y - r, x + r, y + r), fill=alpha)
    capa = capa.filter(ImageFilter.GaussianBlur(r * 0.6))
    img.paste(Image.new("RGB", img.size, color), (0, 0), capa)

def papel_arrugado(semilla=5):
    random.seed(semilla)
    base = np.full((ALTO, ANCHO), 232.0)
    luz = Image.new("L", (ANCHO, ALTO), 128)
    d = ImageDraw.Draw(luz)
    for _ in range(26):  # pliegues: línea clara y línea oscura paralelas
        x0, y0 = random.randint(-200, ANCHO + 200), random.randint(-200, ALTO + 200)
        ang = random.uniform(0, math.pi)
        L = random.randint(400, 1400)
        x1, y1 = x0 + math.cos(ang) * L, y0 + math.sin(ang) * L
        nx, ny = -math.sin(ang) * 6, math.cos(ang) * 6
        d.line((x0, y0, x1, y1), fill=175, width=10)
        d.line((x0 + nx, y0 + ny, x1 + nx, y1 + ny), fill=85, width=8)
    for _ in range(40):  # facetas suaves
        pts = [(random.randint(0, ANCHO), random.randint(0, ALTO)) for _ in range(3)]
        d.polygon(pts, fill=random.randint(120, 136))
    luz = np.array(luz.filter(ImageFilter.GaussianBlur(14)), float) - 128
    arr = np.clip(base + luz * 0.7, 0, 255)
    img = Image.fromarray(arr.astype("uint8")).convert("RGB")
    g = Image.effect_noise((ANCHO, ALTO), 40).convert("L")
    return Image.blend(img, Image.merge("RGB", (g, g, g)), 0.05)

VERS = {
    "noche_roja": dict(nombre="Noche + rojo (textura)",
        dev=lambda c=(0.5, 0.4): textura_oscura(fondo_noche(c)), tapa=lambda: textura_oscura(fondo_noche((0.5, 0.35))),
        cta=lambda: textura_oscura(fondo_negro()), acento_tapa=ROJO, txt=BLANCO, txt2="#C9C9CC", meta=GRIS_META, logo="blanco", lineas="#2A2F3A"),
    "foco_clasico": dict(nombre="Foco clásico",
        dev=lambda c=(0.9, 0.9): fondo_hh(posicion=c, intensidad=0.75), tapa=lambda: fondo_hh(posicion=(0.9, 0.1)),
        cta=lambda: textura_oscura(fondo_noche((0.5, 0.5))), acento_tapa=ROJO, txt=BLANCO, txt2=GRIS_TEXTO, meta=GRIS_META, logo="blanco", lineas="#1E3350"),
    "vino_noche": dict(nombre="Vino + noche",
        dev=lambda c=(0.5, 0.4): textura_oscura(fondo_noche(c)), tapa=lambda: textura_oscura(fondo_vino((0.5, 0.4)), 0.06),
        cta=lambda: textura_oscura(fondo_noche((0.5, 0.35))), acento_tapa="#FFB3BE", txt=BLANCO, txt2="#D9CFD2", meta=GRIS_META, logo="blanco", lineas="#2A2F3A"),
}

# ---------- íconos simples ----------
def icono_rollo(d, x, y, s, c):
    d.ellipse((x - s, y - s, x + s, y + s), fill=c)
    for i in range(5):
        a = i * 2 * math.pi / 5 - math.pi / 2
        px, py = x + math.cos(a) * s * 0.55, y + math.sin(a) * s * 0.55
        d.ellipse((px - s * 0.2, py - s * 0.2, px + s * 0.2, py + s * 0.2), fill=(10, 10, 14))
    d.ellipse((x - s * 0.12, y - s * 0.12, x + s * 0.12, y + s * 0.12), fill=(10, 10, 14))
def icono_edicion(d, x, y, s, c):
    d.rounded_rectangle((x - s, y - s * 0.6, x + s, y + s * 0.6), radius=8, fill=c)
    for i in range(4):
        xx = x - s * 0.8 + i * s * 0.53
        d.rectangle((xx, y - s * 0.5, xx + s * 0.18, y - s * 0.32), fill=(10, 10, 14))
        d.rectangle((xx, y + s * 0.32, xx + s * 0.18, y + s * 0.5), fill=(10, 10, 14))
    d.rectangle((x - 5, y - s, x + 5, y + s), fill=c)
def icono_mas(d, x, y, s, c):
    d.rounded_rectangle((x - s, y - s, x + s, y + s), radius=14, fill=c)
    d.rectangle((x - s * 0.5, y - 6, x + s * 0.5, y + 6), fill=(10, 10, 14))
    d.rectangle((x - 6, y - s * 0.5, x + 6, y + s * 0.5), fill=(10, 10, 14))
def icono_carpeta(d, x, y, s, c):
    d.polygon([(x - s, y - s * 0.7), (x - s * 0.2, y - s * 0.7), (x, y - s * 0.45), (x + s, y - s * 0.45), (x + s, y + s * 0.75), (x - s, y + s * 0.75)], fill=c)
def check_circulo(d, x, y, r, bg, fg):
    d.ellipse((x - r, y - r, x + r, y + r), fill=bg)
    d.line([(x - r * 0.45, y), (x - r * 0.1, y + r * 0.38), (x + r * 0.5, y - r * 0.35)], fill=fg, width=6, joint="curve")

# ---------- mockup libro ----------
def libro(titulo_rojo, titulo_blanco, sub, w=520, h=700):
    tapa = Image.new("RGB", (w, h), (14, 14, 18))
    glow(tapa, w * 0.5, h * 0.35, w * 0.55, (150, 0, 10), 180)
    tapa = textura_oscura(tapa.resize((ANCHO, ALTO)), 0.05).resize((w, h))
    d = ImageDraw.Draw(tapa)
    f1 = inter(900, 150)
    d.text(((w - d.textlength(titulo_rojo, font=f1)) / 2, 150), titulo_rojo, font=f1, fill=(235, 30, 36))
    fy = 320
    for l in titulo_blanco.split("\n"):
        f2 = inter(900, 50)
        d.text(((w - d.textlength(l, font=f2)) / 2, fy), l, font=f2, fill=BLANCO); fy += 58
    f3 = inter(700, 22)
    d.text(((w - d.textlength(sub, font=f3)) / 2, h - 70), sub, font=f3, fill="#C9C9CC")
    d.line((w * 0.3, h - 88, w * 0.7, h - 88), fill=(235, 30, 36), width=2)
    lg = Image.open(os.path.join(LOGOS, "logo_hh_blanco.png")).convert("RGBA"); lg = lg.resize((60, int(lg.height * 60 / lg.width)))
    tapa.paste(lg, ((w - 60) // 2, 60), lg)
    # brillo de encuadernación
    sombra = Image.new("L", (w, h), 0); ImageDraw.Draw(sombra).rectangle((0, 0, 26, h), fill=120)
    tapa.paste(Image.new("RGB", (w, h), (0, 0, 0)), (0, 0), sombra.filter(ImageFilter.GaussianBlur(8)))
    return tapa

def pegar_libro(img, tapa, x, y, lomo=46):
    w, h = tapa.size
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((x - lomo + 20, y + 30, x + w + 30, y + h + 30), fill=(0, 0, 0, 170))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(28))).convert("RGB"))
    d = ImageDraw.Draw(img)
    d.polygon([(x - lomo, y + 14), (x, y), (x, y + h), (x - lomo, y + h - 14)], fill=(28, 6, 10))
    img.paste(tapa, (x, y))
    lomo_txt = Image.new("RGBA", (h - 60, lomo - 12), (0, 0, 0, 0))
    ImageDraw.Draw(lomo_txt).text((20, 2), "30 IDEAS  ·  HISTORIAS DE CLUB", font=inter(800, 22), fill=(235, 30, 36, 255))
    lomo_txt = lomo_txt.rotate(90, expand=True)
    img.paste(lomo_txt, (x - lomo + 8, y + 30), lomo_txt)

def construir(clave):
    V = VERS[clave]
    out = os.path.join(BASE, "versiones", clave) + "/"; os.makedirs(out, exist_ok=True)

    # 1 D2 titular + gráfico
    img = V["tapa"](); d = ImageDraw.Draw(img)
    fT = inter(900, 64)
    linea_mixta(d, 170, [("LAS HISTORIAS DE TU CLUB", fT, V["txt"])])
    linea_mixta(d, 262, [("venden más ", serif(800, 84), V["acento_tapa"]), ("QUE UN 3-0.", fT, V["txt"])])
    ox, oy, W_, H_ = 260, 900, 560, 460
    d.line((ox, oy - H_, ox, oy), fill="#6B6F7A", width=3); d.line((ox, oy, ox + W_, oy), fill="#6B6F7A", width=3)
    pts = [(ox + W_ * t, oy - 20 - H_ * 0.82 * (t ** 2.2)) for t in [i / 60 for i in range(61)]]
    d.line(pts, fill=(230, 230, 235), width=6, joint="curve")
    ex, ey = pts[-1]
    glow(img, ex, ey, 60, (200, 0, 0), 160); d = ImageDraw.Draw(img)
    d.ellipse((ex - 16, ey - 16, ex + 16, ey + 16), fill=ROJO, outline=BLANCO, width=3)
    fl = serif_fina(40)
    for i, l in enumerate(["Historias", "del club"]):
        d.text((ex - d.textlength(l, font=fl) / 2, ey - 120 + i * 42), l, font=fl, fill=V["txt"])
    d.text((ox + W_ - d.textlength("Solo resultados", font=inter(500, 26)), oy - 60), "Solo resultados", font=inter(500, 26), fill="#6B6F7A")
    d.line((ox + 10, oy - 30, ox + W_, oy - 45), fill="#6B6F7A", width=3)
    linea_mixta(d, 1110, [("Aquí tienes cómo contarlas en", inter(500, 40), V["txt"])])
    linea_mixta(d, 1170, [("4 formatos ", serif(700, 50), V["acento_tapa"]), ("que funcionan  →", inter(500, 40), V["txt"])])
    contador_color(img, 1, TOTAL, V["meta"]); img.save(out + "slide_01.png")

    # 2 A2 tachado (skill)
    img = V["dev"]((0.3, 0.3)); logo_esquina(img, V["logo"]); d = ImageDraw.Draw(img)
    fh = inter(800, 80)
    lineas(d, M, 360, "Publica el resultado\ndel partido.", fh, CREMA, 96)
    for yy, t in ((412, "Publica el resultado"), (508, "del partido.")):
        trazo_mano(d, M, M + d.textlength(t, font=fh), yy)
    lineas(d, M, 650, "Publica lo que\npasó antes.", inter(900, 108), ROJO, 122)
    lineas(d, M, 930, "El 3-0 dura un día. La historia del\narquero de 12 años que atajó su\nprimer penal dura toda la temporada.", inter(400, 36), V["txt2"], 52)
    contador_color(img, 2, TOTAL, V["meta"]); img.save(out + "slide_02.png")

    # 3 D3 lista 01–04 con líneas diagonales
    img = V["dev"]((0.7, 0.2)); d = ImageDraw.Draw(img)
    for y0 in (400, 690, 980):
        d.line([(0, y0 + 40), (560, y0 + 40), (660, y0 - 40), (ANCHO, y0 - 40)], fill=V["lineas"], width=3, joint="curve")
    items = [("El camino del jugador", "cómo un niño pasó de la banca a titular."),
             ("Detrás del entrenamiento", "lo que nadie ve a las 7 de la mañana."),
             ("Sobre el club", "cómo nació y quién lo sostiene."),
             ("Antes y después", "el primer día vs. el último partido.")]
    y = 170
    for i, (t, desc) in enumerate(items):
        d.text((M, y), f"0{i+1}", font=inter(900, 110), fill=ROJO)
        d.text((M + 190, y + 4), t, font=serif(700, 56), fill=V["txt"])
        lineas(d, M + 190, y + 80, wrap(d, desc, inter(400, 34), ANCHO - M - 190 - M), inter(400, 34), V["txt2"], 46)
        y += 290
    contador_color(img, 3, TOTAL, V["meta"]); img.save(out + "slide_03.png")

    # 4 D4 paso con íconos
    img = V["dev"]((0.5, 0.45)); d = ImageDraw.Draw(img)
    linea_mixta(d, 240, [("PASO FINAL:", inter(900, 72), V["txt"])])
    linea_mixta(d, 340, [("Graba ", serif(500, 84), V["txt"]), ("donde pasa", serif(700, 84), ROJO)])
    icono_rollo(d, 330, 600, 62, ROJO); icono_edicion(d, 540, 600, 66, ROJO); icono_mas(d, 750, 600, 58, ROJO)
    icono_carpeta(d, 540, 800, 110, BLANCO)
    linea_mixta(d, 1060, [("Cuando tengas la ", inter(500, 38), V["txt"]), ("historia,", serif(700, 44), ROJO), (" grábala", inter(500, 38), V["txt"])])
    linea_mixta(d, 1115, [("en el entrenamiento, edita en el celular y publica.", inter(500, 34), V["txt"])])
    contador_color(img, 4, TOTAL, V["meta"]); img.save(out + "slide_04.png")

    # 5 D5 papel arrugado con checks
    img = papel_arrugado(); d = ImageDraw.Draw(img)
    logo_centrado(img, 230, "negro", 80)
    d.text((cx(d, "HH STUDIO CREATIVO", inter(500, 22)), 250), "HH STUDIO CREATIVO", font=inter(500, 22), fill="#555555") if False else None
    fb = inter(800, 46)
    t = "CUENTA LA HISTORIA DE TU CLUB"
    wb = d.textlength(t, font=fb)
    d.rectangle(((ANCHO - wb) / 2 - 30, 460, (ANCHO + wb) / 2 + 30, 540), fill="#7A7A7E")
    d.text((cx(d, t, fb), 472), t, font=fb, fill=BLANCO)
    checks = ["¿Cómo nació?", "¿Quién está detrás?", "3 cosas que nadie sabe\ndel club."]
    y = 660
    for c in checks:
        check_circulo(d, 230, y + 28, 30, "#58585C", BLANCO)
        y = lineas(d, 290, y, c, inter(500, 50), "#2E2E32", 62) + 40
    contador_color(img, 5, TOTAL, "#6B6B70"); img.save(out + "slide_05.png")

    # 6 B5 frase fragmentada (skill), sobre noche
    img = V["dev"]((0.5, 0.6)); d = ImageDraw.Draw(img)
    fs, fb2 = inter(800, 92), serif(800, 104)
    filas = [[("Nadie se enamora", fs, CREMA)], [("de un marcador.", fb2, ROJO)], [("Se enamoran de la", fs, CREMA)],
             [("historia", fs, CREMA, True)], [("detrás del escudo.", fb2, ROJO)]]
    y = 380
    for f in filas:
        linea_mixta(d, y, f); y += 136
    logo_centrado(img, ALTO - 160, V["logo"], 70)
    contador_color(img, 6, TOTAL, V["meta"]); img.save(out + "slide_06.png")

    # 7 D1 CTA lead magnet
    img = V["cta"](); glow(img, ANCHO / 2, 470, 380, (120, 0, 8), 150); img = textura_oscura(img, 0.04)
    tapa = libro("30", "IDEAS DE\nHISTORIAS\nPARA TU CLUB", "PARA INSTAGRAM", 440, 600)
    pegar_libro(img, tapa, (ANCHO - 440) // 2 + 20, 130)
    d = ImageDraw.Draw(img)
    fc = inter(900, 52)
    linea_mixta(d, 850, [("COMENTA ", fc, BLANCO), ("CLUB", fc, ROJO), (" y te mando el PDF", fc, BLANCO)])
    d.polygon([(ANCHO / 2 - 60, 920), (ANCHO / 2 + 60, 920), (ANCHO / 2 + 60, 1040), (ANCHO / 2 + 130, 1040),
               (ANCHO / 2, 1190), (ANCHO / 2 - 130, 1040), (ANCHO / 2 - 60, 1040)], fill=ROJO)
    contador_color(img, 7, TOTAL, V["meta"]); img.save(out + "slide_07_cta.png")
    return vista_previa(sorted(glob.glob(out + "slide_0*.png")), out + "vista_previa.png", columnas=7, ancho_mini=260)

claves = ["noche_roja", "foco_clasico", "vino_noche"]
hojas = [construir(k) for k in claves]
print(comparar_versiones(hojas, [f"VERSIÓN {c} · {VERS[k]['nombre']}" for c, k in zip("ABC", claves)],
                         os.path.join(BASE, "versiones", "comparacion_versiones.png")))
