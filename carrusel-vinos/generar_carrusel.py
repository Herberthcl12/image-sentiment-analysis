"""Carrusel HH v3: vender vino con contenido. 1 A1(resplandor) · 2 B4 · 3 A2(negro) · 4 B3 · 5 B2 · 6 B5 · 7 A8(resplandor)"""
import sys, os
sys.path.insert(0, "/root/.claude/skills/synced/a83d7b8b-6484-4f1d-b672-5dde2b410928_0fec2520-89fe-4255-ba8e-9c8f4e367f11/hh-carrusel-instagram/scripts")
from generar_slide import *
from PIL import ImageDraw

OUT = os.path.dirname(os.path.abspath(__file__)) + "/"
TOTAL = 7
W = ANCHO - 2 * M
BURDEO = (120, 0, 22)   # luz del resplandor: familia del rojo, tono vino

def bodoni(t, italic=True):
    f = fuente_tematica("Bodoni Moda", 700, italic=italic, tamano=t)
    return f or serif(800, t)

# 1 HOOK: resplandor burdeo abajo (como una copa iluminada), Bodoni + recuadro
img = fondo_resplandor(luz=BURDEO, centro=(0.72, 0.82), radio=0.7)
logo_esquina(img)
d = ImageDraw.Draw(img)
y = lineas(d, M, 330, "Tu cliente", inter(800, 96), BLANCO, 112)
y = lineas(d, M, y, "no sabe de vino.", inter(800, 96), BLANCO, 112)
caja_destacada(img, M, y + 10, "Y no tiene por qué.", bodoni(92))
d = ImageDraw.Draw(img)
d.line((M, y + 190, M + 170, y + 190), fill=BLANCO, width=5)
lineas(d, M, y + 250, "Por eso compra el que\nalguien le explicó mejor.", inter(800, 56), CREMA, 72)
contador(img, 1, TOTAL)
img.save(OUT + "slide_01.png")

# 2 B4: No digas / Mejor di
img = fondo_negro()
d = ImageDraw.Draw(img)
def bloque(y, et, frase, nota):
    linea_mixta(d, y, [(et, inter(800, 42), ROJO)])
    yy = y + 100
    for l in frase.split("\n"):
        linea_mixta(d, yy, [(l, inter(800, 54), BLANCO)]); yy += 68
    linea_mixta(d, yy + 30, [(nota, serif_fina(44), GRIS_TEXTO)])
bloque(230, "NO DIGAS:", "“Cabernet Sauvignon 2021,\nValle del Maipo.”", "(Eso es una ficha técnica.)")
d.line((0, 660, ANCHO, 660), fill=ROJO, width=3)
bloque(800, "MEJOR DI:", "“El que llevas al asado:\nintenso y con fruta madura.”", "Le dices para qué sirve, no qué es.")
contador(img, 2, TOTAL)
img.save(OUT + "slide_02.png")

# 3 A2 sobre negro: tachado
img = fondo_negro()
logo_esquina(img)
d = ImageDraw.Draw(img)
fh = inter(800, 84)
t = "Publica fotos de botellas."
lineas(d, M, 440, "Publica fotos\nde botellas.", fh, CREMA, 100)
for yy, txt in ((498, "Publica fotos"), (598, "de botellas.")):
    trazo_mano(d, M, M + d.textlength(txt, font=fh), yy)
lineas(d, M, 740, "Publica\ndecisiones.", inter(900, 116), ROJO, 130)
lineas(d, M, 1030, "Nadie busca un vino.\nBusca saber cuál llevar esta noche.", inter(400, 38), GRIS_TEXTO, 54)
contador(img, 3, TOTAL)
img.save(OUT + "slide_03.png")

# 4 B3: lista en papel
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

# 5 B2: suma (variante tiempo)
img = fondo_negro()
d = ImageDraw.Draw(img)
fl = inter(700, 70)
for i, t in enumerate(["12 ideas", "1 video por semana", "0 días pensando qué subir"]):
    linea_mixta(d, 460 + i * 88, [(t, fl, CREMA)])
d.line((ANCHO / 2, 690, ANCHO / 2, 810), fill=ROJO, width=4)
linea_mixta(d, 990, [("3 meses", serif(800, 190), ROJO)])
linea_mixta(d, 1090, [("de contenido resuelto.", inter(500, 36), GRIS_TEXTO)])
contador(img, 5, TOTAL)
img.save(OUT + "slide_05.png")

# 6 B5: frase fragmentada con Bodoni
img = fondo_negro()
d = ImageDraw.Draw(img)
fs, fb = inter(800, 94), bodoni(108)
filas = [[("El vino se", fs, CREMA)],
         [("disfruta", fb, ROJO)],
         [("en la copa,", fb, ROJO)],
         [("pero se ", fs, CREMA), ("elige", fs, CREMA, True)],
         [("en el celular.", fb, ROJO)]]
y = 400
for f in filas:
    linea_mixta(d, y, f); y += 140
logo_centrado(img, ALTO - 150, tamano=70)
contador(img, 6, TOTAL)
img.save(OUT + "slide_06.png")

# 7 CTA sobre resplandor burdeo, centrado
img = fondo_resplandor(luz=BURDEO, centro=(0.5, 0.5), radio=0.75, puntos=True)
logo_centrado(img, 110, tamano=90)
d = ImageDraw.Draw(img)
fc = inter(700, 60)
d.text(((ANCHO - d.textlength("Comenta", font=fc)) / 2, 400), "Comenta", font=fc, fill=BLANCO)
fb = inter(900, 128)
bb = d.textbbox((0, 0), "VINO", font=fb)
img, yb = etiqueta_cta(img, int((ANCHO - (bb[2] - bb[0] + 70)) / 2), 500, "VINO", fb)
d = ImageDraw.Draw(img)
f42 = inter(700, 42)
filas = [[("y te mando las 12 ideas con el", BLANCO)],
         [("guion de cada video, listas", BLANCO)],
         [("para grabar ", BLANCO), ("esta semana.", ROJO)]]
y = yb + 110
for fila in filas:
    x = (ANCHO - sum(d.textlength(t, font=f42) for t, _ in fila)) / 2
    for t, c in fila:
        d.text((x, y), t, font=f42, fill=c); x += d.textlength(t, font=f42)
    y += 62
contador(img, 7, TOTAL)
img.save(OUT + "slide_07_cta.png")

import glob
print(vista_previa(sorted(glob.glob(OUT + "slide_0*.png")), OUT + "vista_previa.png"))
