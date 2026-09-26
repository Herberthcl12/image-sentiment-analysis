"""Vinos v2: más ordenado. Sistema: rojo (portada y CTA) + noche (desarrollo) + 1 papel. Todo alineado a la izquierda.
1 A1 rojo · 2 B4 noche · 3 A2 noche · 4 B3 papel · 5 B5 noche · 6 A8 rojo"""
import sys, os, glob
import numpy as np
sys.path.insert(0, "/root/.claude/skills/synced/a83d7b8b-6484-4f1d-b672-5dde2b410928_0fec2520-89fe-4255-ba8e-9c8f4e367f11/hh-carrusel-instagram/scripts")
from generar_slide import *
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v2") + "/"
TOTAL = 6
W = ANCHO - 2 * M

def bodoni(t):
    return fuente_tematica("Bodoni Moda", 700, italic=True, tamano=t) or serif(800, t)

def _radial(c_centro, c_borde, centro=(0.5, 0.45), curva=1.3, grano=0.05):
    yy, xx = np.mgrid[0:ALTO, 0:ANCHO]
    d = np.sqrt(((xx / ANCHO) - centro[0]) ** 2 + (((yy / ALTO) - centro[1]) * ALTO / ANCHO) ** 2)
    t = np.clip(d / 0.8, 0, 1) ** curva
    a, b = np.array(c_centro, float), np.array(c_borde, float)
    arr = a + (b - a) * t[:, :, None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
    g = Image.effect_noise((ANCHO, ALTO), 45).convert("L")
    return Image.blend(img, Image.merge("RGB", (g, g, g)), grano)

def contador_blanco(img, n):
    d = ImageDraw.Draw(img); t = f"{n}/{TOTAL}"; f = inter(500, 26)
    d.text((ANCHO - M - d.textlength(t, font=f), ALTO - 90), t, font=f, fill=BLANCO)

def fondo_noche(centro=(0.35, 0.4)):
    """Negro al centro que se funde en azul noche hacia los bordes. Nunca negro plano."""
    return _radial((7, 8, 12), (12, 34, 64), centro=centro)

def fondo_rojo():
    """Rojo HH con viñeta leve hacia un rojo más profundo en los bordes."""
    return _radial((254, 0, 0), (196, 0, 0), centro=(0.4, 0.4), curva=1.8, grano=0.04)

# 1 PORTADA roja
img = fondo_rojo()
logo_esquina(img)
d = ImageDraw.Draw(img)
y = lineas(d, M, 340, "Tu cliente\nno sabe de vino.", inter(800, 98), BLANCO, 114)
caja_destacada(img, M, y + 12, "Y no tiene por qué.", bodoni(92), bg=AZUL_NOCHE, fg=BLANCO)
d = ImageDraw.Draw(img)
d.line((M, y + 195, M + 170, y + 195), fill=BLANCO, width=5)
lineas(d, M, y + 255, "Por eso compra el que\nalguien le explicó mejor.", inter(800, 56), BLANCO, 72)
contador_blanco(img, 1)
img.save(OUT + "slide_01.png")

# 2 B4 noche, alineado a la izquierda
img = fondo_noche(centro=(0.3, 0.3))
logo_esquina(img)
d = ImageDraw.Draw(img)
def bloque(y, et, frase, nota):
    d.text((M, y), et, font=inter(800, 40), fill=ROJO)
    yy = lineas(d, M, y + 75, frase, inter(800, 54), BLANCO, 68)
    d.text((M, yy + 18), nota, font=serif_fina(44), fill=GRIS_TEXTO)
bloque(260, "NO DIGAS:", "“Cabernet Sauvignon 2021,\nValle del Maipo.”", "(Eso es una ficha técnica.)")
d.line((M, 690, ANCHO - M, 690), fill=ROJO, width=3)
bloque(790, "MEJOR DI:", "“El que llevas al asado:\nintenso y con fruta madura.”", "Le dices para qué sirve, no qué es.")
contador(img, 2, TOTAL)
img.save(OUT + "slide_02.png")

# 3 A2 noche
img = fondo_noche(centro=(0.6, 0.35))
logo_esquina(img)
d = ImageDraw.Draw(img)
fh = inter(800, 84)
lineas(d, M, 400, "Publica fotos\nde botellas.", fh, CREMA, 100)
for yy, txt in ((458, "Publica fotos"), (558, "de botellas.")):
    trazo_mano(d, M, M + d.textlength(txt, font=fh), yy)
lineas(d, M, 700, "Publica\ndecisiones.", inter(900, 116), ROJO, 130)
lineas(d, M, 990, "Nadie busca un vino.\nBusca saber cuál llevar esta noche.", inter(400, 38), GRIS_TEXTO, 54)
contador(img, 3, TOTAL)
img.save(OUT + "slide_03.png")

# 4 B3 papel
img = fondo_papel()
d = ImageDraw.Draw(img)
linea_mixta(d, 210, [("Ideas ", inter(900, 104), "#111111"), ("de vino", serif_fina(124), ROJO)], centrado=False)
d.line((M, 250, ANCHO - M - 150, 250), fill="#111111", width=3)
ideas = ["Qué vino llevar a un asado, según tu presupuesto.",
         "Tres vinos bajo $10.000 que recomiendas de verdad.",
         "Cómo leer una etiqueta en 30 segundos.",
         "El error más común al servir un vino blanco.",
         "Maridaje chileno: empanadas y pastel de choclo.",
         "Cómo llega una botella hasta tu estante.",
         "Tu recomendación de la semana, en 15 segundos.",
         "El mito de que más caro siempre es mejor.",
         "Varietal, reserva, gran reserva: qué cambia.",
         "Un cliente prueba a ciegas y opina.",
         "Cómo guardar un vino que quedó abierto.",
         "La pregunta que más te hacen en caja."]
y = 350
for i, t in enumerate(ideas):
    d.text((M, y), f"{i+1}.", font=inter(800, 31), fill="#111111")
    d.text((M + 62, y), t, font=inter(500, 31), fill="#1A1A1A")
    y += 66
d.text((M, ALTO - 110), "1–12  |  IDEAS DE VINO", font=inter(700, 24), fill="#333333")
pegar_logo(img, "negro", "inferior_derecha", tamano=64, margen=M - 8)
img.save(OUT + "slide_04.png")

# 5 B5 noche, alineada a la izquierda
img = fondo_noche(centro=(0.4, 0.55))
logo_esquina(img)
d = ImageDraw.Draw(img)
fs, fb = inter(800, 94), bodoni(108)
filas = [[("El vino se", fs, CREMA)],
         [("disfruta", fb, ROJO)],
         [("en la copa,", fb, ROJO)],
         [("pero se ", fs, CREMA), ("elige", fs, CREMA, True)],
         [("en el celular.", fb, ROJO)]]
y = 420
for f in filas:
    linea_mixta(d, y, f, centrado=False); y += 140
contador(img, 5, TOTAL)
img.save(OUT + "slide_05.png")

# 6 CTA rojo (espejo de la portada)
img = fondo_rojo()
logo_esquina(img)
d = ImageDraw.Draw(img)
d.text((M, 400), "Comenta", font=inter(700, 60), fill=BLANCO)
img, yb = etiqueta_cta(img, M, 500, "VINO", bg=AZUL_NOCHE, fg=BLANCO)
d = ImageDraw.Draw(img)
f42 = inter(700, 42)
y = yb + 110
for fila in [[("y te mando las 12 ideas con el", BLANCO)],
             [("guion de cada video, listas", BLANCO)],
             [("para grabar ", BLANCO), ("esta semana.", AZUL_NOCHE)]]:
    x = M
    for t, c in fila:
        d.text((x, y), t, font=f42, fill=c); x += d.textlength(t, font=f42)
    y += 62
contador_blanco(img, 6)
img.save(OUT + "slide_06_cta.png")

print(vista_previa(sorted(glob.glob(OUT + "slide_0*.png")), OUT + "vista_previa.png", columnas=3))
