"""Vinos: 3 versiones de color con la misma estructura ordenada.
1 A1 · 2 B4 · 3 A2 · 4 B3 papel · 5 B5 · 6 A8"""
import sys, os, glob
import numpy as np
sys.path.insert(0, "/root/.claude/skills/synced/a83d7b8b-6484-4f1d-b672-5dde2b410928_0fec2520-89fe-4255-ba8e-9c8f4e367f11/hh-carrusel-instagram/scripts")
from generar_slide import *
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
TOTAL = 6
W = ANCHO - 2 * M

def bodoni(t):
    return fuente_tematica("Bodoni Moda", 700, italic=True, tamano=t) or serif(800, t)

def radial(c_centro, c_borde, centro=(0.4, 0.4), curva=1.4, grano=0.045):
    yy, xx = np.mgrid[0:ALTO, 0:ANCHO]
    d = np.sqrt(((xx / ANCHO) - centro[0]) ** 2 + (((yy / ALTO) - centro[1]) * ALTO / ANCHO) ** 2)
    t = np.clip(d / 0.85, 0, 1) ** curva
    a, b = np.array(c_centro, float), np.array(c_borde, float)
    img = Image.fromarray(np.clip(a + (b - a) * t[:, :, None], 0, 255).astype("uint8"))
    g = Image.effect_noise((ANCHO, ALTO), 45).convert("L")
    return Image.blend(img, Image.merge("RGB", (g, g, g)), grano)

NOCHE = dict(fondo=lambda c: radial((7, 8, 12), (12, 34, 64), centro=c, curva=1.3, grano=0.05),
             txt=BLANCO, txt2=GRIS_TEXTO, crema=CREMA, acento=ROJO, logo="blanco", meta=GRIS_META)

TEMAS = {
    "A_vino_noche": dict(
        nombre="Vino + noche",
        tapa=lambda: radial((150, 16, 34), (66, 6, 18), centro=(0.3, 0.35), curva=1.2),
        tapa_txt=BLANCO, tapa_txt2="#F3D9DD", tapa_caja=(AZUL_NOCHE, BLANCO), tapa_logo="blanco",
        tapa_meta="#F3D9DD", tapa_acento="#FFB3BE", dev=NOCHE),
    "B_crema_azul": dict(
        nombre="Crema + azul",
        tapa=lambda: radial((248, 245, 240), (214, 224, 238), centro=(0.3, 0.3), curva=1.3, grano=0.06),
        tapa_txt=AZUL_NOCHE, tapa_txt2="#3B4E66", tapa_caja=(AZUL_NOCHE, BLANCO), tapa_logo="azul",
        tapa_meta="#5B6B80", tapa_acento=ROJO, dev=NOCHE),
    "C_rosa_celeste": dict(
        nombre="Rosa + celeste",
        tapa=lambda: radial((252, 214, 222), (206, 226, 246), centro=(0.35, 0.3), curva=1.1, grano=0.05),
        tapa_txt=AZUL_NOCHE, tapa_txt2="#3B4E66", tapa_caja=(ROJO, BLANCO), tapa_logo="azul",
        tapa_meta="#5B6B80", tapa_acento=ROJO,
        dev=dict(fondo=lambda c: radial((244, 248, 253), (200, 222, 244), centro=c, curva=1.3, grano=0.05),
                 txt=AZUL_NOCHE, txt2="#4A5A70", crema=AZUL_NOCHE, acento=ROJO, logo="azul", meta="#5B6B80")),
}

def meta(img, n, color):
    d = ImageDraw.Draw(img); t = f"{n}/{TOTAL}"; f = inter(500, 26)
    d.text((ANCHO - M - d.textlength(t, font=f), ALTO - 90), t, font=f, fill=color)

def construir(clave, T):
    out = os.path.join(BASE, "versiones", clave) + "/"
    os.makedirs(out, exist_ok=True)
    D = T["dev"]

    # 1 portada
    img = T["tapa"](); logo_esquina(img, T["tapa_logo"])
    d = ImageDraw.Draw(img)
    y = lineas(d, M, 340, "Tu cliente\nno sabe de vino.", inter(800, 98), T["tapa_txt"], 114)
    caja_destacada(img, M, y + 12, "Y no tiene por qué.", bodoni(92), bg=T["tapa_caja"][0], fg=T["tapa_caja"][1])
    d = ImageDraw.Draw(img)
    d.line((M, y + 195, M + 170, y + 195), fill=T["tapa_txt"], width=5)
    lineas(d, M, y + 255, "Por eso compra el que\nalguien le explicó mejor.", inter(800, 56), T["tapa_txt2"], 72)
    meta(img, 1, T["tapa_meta"]); img.save(out + "slide_01.png")

    # 2 B4
    img = D["fondo"]((0.3, 0.3)); logo_esquina(img, D["logo"])
    d = ImageDraw.Draw(img)
    def bloque(y, et, frase, nota):
        d.text((M, y), et, font=inter(800, 40), fill=D["acento"])
        yy = lineas(d, M, y + 75, frase, inter(800, 54), D["txt"], 68)
        d.text((M, yy + 18), nota, font=serif_fina(44), fill=D["txt2"])
    bloque(260, "NO DIGAS:", "“Cabernet Sauvignon 2021,\nValle del Maipo.”", "(Eso es una ficha técnica.)")
    d.line((M, 690, ANCHO - M, 690), fill=D["acento"], width=3)
    bloque(790, "MEJOR DI:", "“El que llevas al asado:\nintenso y con fruta madura.”", "Le dices para qué sirve, no qué es.")
    meta(img, 2, D["meta"]); img.save(out + "slide_02.png")

    # 3 A2
    img = D["fondo"]((0.6, 0.35)); logo_esquina(img, D["logo"])
    d = ImageDraw.Draw(img)
    fh = inter(800, 84)
    lineas(d, M, 400, "Publica fotos\nde botellas.", fh, D["crema"], 100)
    for yy, txt in ((458, "Publica fotos"), (558, "de botellas.")):
        trazo_mano(d, M, M + d.textlength(txt, font=fh), yy, color=D["acento"])
    lineas(d, M, 700, "Publica\ndecisiones.", inter(900, 116), D["acento"], 130)
    lineas(d, M, 990, "Nadie busca un vino.\nBusca saber cuál llevar esta noche.", inter(400, 38), D["txt2"], 54)
    meta(img, 3, D["meta"]); img.save(out + "slide_03.png")

    # 4 B3 papel
    img = fondo_papel(); d = ImageDraw.Draw(img)
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
    img.save(out + "slide_04.png")

    # 5 B5
    img = D["fondo"]((0.4, 0.55)); logo_esquina(img, D["logo"])
    d = ImageDraw.Draw(img)
    fs, fb = inter(800, 94), bodoni(108)
    filas = [[("El vino se", fs, D["crema"])], [("disfruta", fb, D["acento"])], [("en la copa,", fb, D["acento"])],
             [("pero se ", fs, D["crema"]), ("elige", fs, D["crema"], True)], [("en el celular.", fb, D["acento"])]]
    y = 420
    for f in filas:
        linea_mixta(d, y, f, centrado=False); y += 140
    meta(img, 5, D["meta"]); img.save(out + "slide_05.png")

    # 6 CTA (espejo de la portada)
    img = T["tapa"](); logo_esquina(img, T["tapa_logo"])
    d = ImageDraw.Draw(img)
    d.text((M, 400), "Comenta", font=inter(700, 60), fill=T["tapa_txt"])
    img, yb = etiqueta_cta(img, M, 500, "VINO", bg=T["tapa_caja"][0], fg=T["tapa_caja"][1])
    d = ImageDraw.Draw(img)
    f42 = inter(700, 42); y = yb + 110
    for fila in [[("y te mando las 12 ideas con el", T["tapa_txt"])],
                 [("guion de cada video, listas", T["tapa_txt"])],
                 [("para grabar ", T["tapa_txt"]), ("esta semana.", T["tapa_acento"])]]:
        x = M
        for t, c in fila:
            d.text((x, y), t, font=f42, fill=c); x += d.textlength(t, font=f42)
        y += 62
    meta(img, 6, T["tapa_meta"]); img.save(out + "slide_06_cta.png")
    return vista_previa(sorted(glob.glob(out + "slide_0*.png")), out + "vista_previa.png", columnas=6, ancho_mini=300)

hojas = [construir(k, T) for k, T in TEMAS.items()]
# hoja comparativa con las 3 versiones apiladas y rotuladas
ims = [Image.open(h) for h in hojas]
etq = 70
comp = Image.new("RGB", (ims[0].width, sum(i.height + etq for i in ims)), (24, 24, 28))
d = ImageDraw.Draw(comp); y = 0
for (k, T), im in zip(TEMAS.items(), ims):
    d.text((20, y + 18), f"VERSIÓN {k[0]} · {T['nombre']}", font=inter(800, 34), fill=BLANCO)
    comp.paste(im, (0, y + etq)); y += im.height + etq
comp.save(os.path.join(BASE, "versiones", "comparacion_versiones.png"))
print("ok")
