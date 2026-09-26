"""Prueba de 5 formatos nuevos (referencias de Herberth) + 2 slides del estilo v2."""
import sys, os
import numpy as np
sys.path.insert(0, "/root/.claude/skills/synced/a83d7b8b-6484-4f1d-b672-5dde2b410928_0fec2520-89fe-4255-ba8e-9c8f4e367f11/hh-carrusel-instagram/scripts")
from generar_slide import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.dirname(os.path.abspath(__file__)) + "/"
FD = "/tmp/claude-0/-home-user-image-sentiment-analysis/8b9e8f78-b4d2-59c0-9315-bd1bd6715d80/scratchpad/fonts/"
def serif(peso, t): return ImageFont.truetype(FD + f"PlayfairDisplay-Italic-{peso}.ttf", t)
TOTAL = 7
W = ANCHO - 2 * M

def grano(img, fuerza=0.05, sigma=40):
    g = Image.effect_noise((ANCHO, ALTO), sigma).convert("L")
    return Image.blend(img, Image.merge("RGB", (g, g, g)), fuerza)

def fondo_resplandor(base="#050A12", luz=(190, 0, 0), centro=(0.5, 0.45), radio=0.62):
    """Formato 1: resplandor rojo difuso detrás del texto central + grilla de puntos."""
    b = np.array(tuple(int(base.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)), float)
    yy, xx = np.mgrid[0:ALTO, 0:ANCHO]
    d = np.sqrt(((xx / ANCHO) - centro[0]) ** 2 + (((yy / ALTO) - centro[1]) * ALTO / ANCHO) ** 2)
    f = np.clip(1 - d / radio, 0, 1) ** 1.8
    arr = b + (np.array(luz, float) - b) * f[:, :, None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
    dr = ImageDraw.Draw(img)
    for y in range(24, ALTO, 38):
        for x in range(24, ANCHO, 38):
            dr.ellipse((x - 1.4, y - 1.4, x + 1.4, y + 1.4), fill=(70, 78, 92))
    return grano(img, 0.04)

def fondo_negro():
    return grano(Image.new("RGB", (ANCHO, ALTO), "#050505"), 0.06, 50)

def fondo_papel():
    """Formato 3: papel claro con textura (derivado del blanco)."""
    img = Image.new("RGB", (ANCHO, ALTO), (236, 234, 230))
    img = grano(img, 0.10, 60)
    manchas = Image.effect_noise((ANCHO // 8, ALTO // 8), 90).convert("L").resize((ANCHO, ALTO), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
    return Image.composite(img, Image.new("RGB", (ANCHO, ALTO), (222, 219, 214)), manchas.point(lambda v: 150 + v // 3))

def linea_mixta(d, y_base, partes, centrado=True, x=M):
    """partes = [(texto, font, color, subrayado?)] alineadas por línea base."""
    ancho = sum(d.textlength(t, font=f) for t, f, *_ in partes)
    xx = (ANCHO - ancho) / 2 if centrado else x
    for p in partes:
        t, f, c = p[:3]
        d.text((xx, y_base), t, font=f, fill=c, anchor="ls")
        w = d.textlength(t, font=f)
        if len(p) > 3 and p[3]:
            d.line((xx + 4, y_base + 14, xx + w - 4, y_base + 14), fill=c, width=6)
        xx += w

# ---------- 1: RESPLANDOR (ref. REBRND) ----------
img = fondo_resplandor()
d = ImageDraw.Draw(img)
fs, fi = inter(800, 78), serif(700, 150)
linea_mixta(d, 470, [("Lo que puedes", fs, BLANCO)])
linea_mixta(d, 630, [("publicar", fi, BLANCO)])
linea_mixta(d, 790, [("todo el mes", fi, BLANCO)])
linea_mixta(d, 900, [("sin quedarte en blanco", fs, BLANCO)])
d.rounded_rectangle((ANCHO / 2 - 58, 990, ANCHO / 2 + 58, 1050), radius=30, outline=BLANCO, width=3)
d.line((ANCHO / 2 - 28, 1020, ANCHO / 2 + 26, 1020), fill=BLANCO, width=3)
d.line([(ANCHO / 2 + 10, 1006), (ANCHO / 2 + 26, 1020), (ANCHO / 2 + 10, 1034)], fill=BLANCO, width=3)
pegar_logo(img, "blanco", "superior_derecha", tamano=0 or 70, margen=0) if False else None
lg = Image.open(os.path.join(LOGOS, "logo_hh_blanco.png")).convert("RGBA")
lg = lg.resize((96, int(lg.height * 96 / lg.width)))
img.paste(lg, ((ANCHO - 96) // 2, 90), lg)
contador(img, 1, TOTAL)
img.save(OUT + "slide_01.png")

# ---------- 2: SUMA (ref. 120 ideas) ----------
img = fondo_negro()
d = ImageDraw.Draw(img)
fl = inter(700, 70)
for i, t in enumerate(["15 ideas de Reels", "15 ideas de Stories", "15 ideas de Carruseles"]):
    linea_mixta(d, 470 + i * 88, [(t, fl, "#F2EFEA")])
d.line((ANCHO / 2, 700, ANCHO / 2, 820), fill=ROJO, width=4)
linea_mixta(d, 990, [("45 ideas", serif(800, 190), ROJO)])
linea_mixta(d, 1090, [("para todo un trimestre.", inter(500, 36), GRIS_TEXTO)])
contador(img, 2, TOTAL)
img.save(OUT + "slide_02.png")

# ---------- 3: LISTA EN PAPEL (ref. Ideas Reels) ----------
img = fondo_papel()
d = ImageDraw.Draw(img)
linea_mixta(d, 210, [("Ideas ", inter(900, 104), "#111111"), ("Reels", serif(800, 116), ROJO)], centrado=False)
d.line((M, 250, ANCHO - M - 190, 250), fill="#111111", width=3)
ideas = ["Un día normal en tu negocio, en 15 segundos.",
         "El error más común de tus clientes y cómo evitarlo.",
         "Un antes y después de un trabajo real.",
         "La pregunta que más te hacen, respondida en cámara.",
         "Cómo se prepara tu producto o servicio.",
         "Tu opinión sobre una tendencia de tu rubro.",
         "Lo que nadie ve antes de abrir.",
         "Un cliente contando por qué vuelve (con su permiso).",
         "Tres cosas que nunca harías en tu rubro.",
         "Un mito de tu rubro y lo que es verdad.",
         "Tu precio explicado: qué incluye y por qué cuesta eso.",
         "El producto que más se vende y por qué.",
         "Cómo reservar o comprar, paso a paso.",
         "Tu equipo presentándose en una frase.",
         "Lo que aprendiste en tu primer año."]
fn, ft = inter(800, 31), inter(500, 31)
y = 330
for i, t in enumerate(ideas):
    d.text((M, y), f"{i+1}.", font=fn, fill="#111111")
    d.text((M + 62, y), t, font=ft, fill="#1A1A1A")
    y += 58
d.text((M, ALTO - 110), "1–15  |  IDEAS REELS", font=inter(700, 24), fill="#333333")
pegar_logo(img, "negro", "inferior_derecha", tamano=64, margen=M - 8)
img.save(OUT + "slide_03.png")

# ---------- 4: NO DIGAS / MEJOR DI (ref. comparación) ----------
img = fondo_negro()
d = ImageDraw.Draw(img)
def bloque(y, etiqueta, frase, nota, italica_nota=True):
    linea_mixta(d, y, [(etiqueta, inter(800, 42), ROJO)])
    yy = y + 100
    for l in frase.split("\n"):
        linea_mixta(d, yy, [(l, inter(800, 58), BLANCO)]); yy += 72
    linea_mixta(d, yy + 30, [(nota, serif(500, 36), GRIS_TEXTO)])
bloque(250, "NO DIGAS:", "“Tenemos los mejores\nprecios de la zona.”", "(Lo dice todo tu rubro.)")
d.line((0, 675, ANCHO, 675), fill=ROJO, width=3)
bloque(830, "MEJOR DI:", "“Todo lo que incluye\ntu plan de $29.990.”", "Un dato concreto convence más que un adjetivo.")
contador(img, 4, TOTAL)
img.save(OUT + "slide_04.png")

# ---------- 5: FRASE FRAGMENTADA (ref. mix) ----------
img = fondo_negro()
d = ImageDraw.Draw(img)
fs, fi = inter(800, 96), serif(800, 104)
filas = [[("Puedes tener el", fs, "#F2EFEA")],
         [("mejor producto", fi, ROJO)],
         [("de tu ciudad,", fi, ROJO)],
         [("pero si no te ", fs, "#F2EFEA")],
         [("ven ", fs, "#F2EFEA"), ("seguido", fs, "#F2EFEA", True), (",", fs, "#F2EFEA")],
         [("no existes.", fi, ROJO)]]
y = 330
for f in filas:
    linea_mixta(d, y, f); y += 128
lg = Image.open(os.path.join(LOGOS, "logo_hh_blanco.png")).convert("RGBA")
lg = lg.resize((70, int(lg.height * 70 / lg.width)))
img.paste(lg, ((ANCHO - 70) // 2, ALTO - 150), lg)
contador(img, 5, TOTAL)
img.save(OUT + "slide_05.png")

# ---------- 6: TACHADO (estilo v2) ----------
img = fondo_hh(posicion=(0.85, 0.12), radio=1.2, intensidad=1.0)
logo_esquina(img)
d = ImageDraw.Draw(img)
fh = inter(800, 92)
d.text((M, 380), "No te faltan ideas.", font=fh, fill=BLANCO)
trazo_mano(d, M, M + d.textlength("No te faltan ideas.", font=fh), 438)
lineas(d, M, 560, "Te falta un\ncalendario.", inter(900, 110), ROJO, 124)
lineas(d, M, 870, wrap(d, "Con 45 ideas y 3 publicaciones por semana, tienes contenido para 15 semanas.", inter(400, 38), W), inter(400, 38), GRIS_TEXTO, 54)
contador(img, 6, TOTAL)
img.save(OUT + "slide_06.png")

# ---------- 7: CTA (estilo v2) ----------
img = fondo_hh(posicion=(0.12, 0.92), radio=0.95, intensidad=0.85)
logo_esquina(img)
d = ImageDraw.Draw(img)
d.text((M, 400), "Comenta", font=inter(700, 60), fill=BLANCO)
img, yb = etiqueta_cta(img, M, 500, "IDEAS")
d = ImageDraw.Draw(img)
texto_mixto(d, M, yb + 110, [("y te mando las 45 ideas ordenadas", BLANCO)], inter(700, 42), W)
texto_mixto(d, M, yb + 170, [("en un calendario de", BLANCO), ("15 semanas,", ROJO)], inter(700, 42), W)
texto_mixto(d, M, yb + 230, [("listo para usar mañana.", BLANCO)], inter(700, 42), W)
contador(img, 7, TOTAL)
img.save(OUT + "slide_07_cta.png")
print("ok")
