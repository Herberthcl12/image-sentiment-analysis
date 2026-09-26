"""
EJEMPLO DE REFERENCIA (estilo v2 aprobado por Herberth, sept. 2026).
Carrusel "Tu web puede desaparecer en un solo día" — 8 slides.
Úsalo como referencia de composición, tamaños y recursos; NO como plantilla
fija: el orden de los slides, la alineación (izquierda/centro) y la posición
del foco de luz se rotan en cada carrusel nuevo.
Ejecutar:  python3 ejemplos/carrusel_web_v2.py  (genera PNG en ./salida_ejemplo/)
"""
import sys, os, math
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "scripts"))
from generar_slide import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.join(os.getcwd(), "salida_ejemplo") + "/"
os.makedirs(OUT, exist_ok=True)
M = 90
TOTAL = 8
GRIS = "#AEB6C2"
AZUL_TXT = "#061323"

def fondo(pos=(0.92, 0.08), radio=0.95, inten=0.9):
    return fondo_foco(AZUL_NOCHE, posicion=pos, radio=radio, intensidad=inten, color_luz="#2C5C8F")

def contador(img, n, oscuro=True):
    d = ImageDraw.Draw(img)
    t = f"{n}/{TOTAL}"
    f = inter(500, 26)
    w = d.textlength(t, font=f)
    d.text((ANCHO - M - w, ALTO - 90), t, font=f, fill=GRIS if oscuro else "#7A828E")

def logo(img, variante="blanco"):
    pegar_logo(img, variante, "superior_izquierda", tamano=78, margen=M - 8)

def lineas(d, x, y, texto, f, fill, lh):
    for l in texto.split("\n"):
        d.text((x, y), l, font=f, fill=fill)
        y += lh
    return y

def wrap(d, texto, f, ancho):
    out, linea = [], ""
    for p in texto.split():
        pr = (linea + " " + p).strip()
        if d.textlength(pr, font=f) <= ancho: linea = pr
        else: out.append(linea); linea = p
    out.append(linea)
    return "\n".join(out)

def caja(img, x, y, texto, f, bg, fg, pad=(22, 10)):
    d = ImageDraw.Draw(img)
    b = d.textbbox((x, y), texto, font=f)
    d.rectangle((b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1] + 6), fill=bg)
    d.text((x, y), texto, font=f, fill=fg)
    return b

def trazo_mano(d, x0, x1, y, color, grosor=12):
    pts = []
    for i in range(41):
        t = i / 40
        x = x0 - 10 + (x1 - x0 + 40) * t
        pts.append((x, y + 6 * math.sin(t * math.pi * 1.3) - 8 * t))
    d.line(pts, fill=color, width=grosor, joint="curve")
    for px, py in (pts[0], pts[-1]):
        d.ellipse((px - grosor / 2, py - grosor / 2, px + grosor / 2, py + grosor / 2), fill=color)

# ---------- 1 ----------
img = fondo()
logo(img)
d = ImageDraw.Draw(img)
fh = inter(800, 92)
y = lineas(d, M, 300, "Tu web puede\ndesaparecer", fh, BLANCO, 108)
caja(img, M, y + 4, "en un solo día.", fh, ROJO, BLANCO)
y += 150
d.line((M, y + 30, M + 170, y + 30), fill=BLANCO, width=5)
lineas(d, M, y + 90, "Y no por un hackeo.\nPor un correo de\nrenovación que\nnadie leyó.", inter(800, 64), "#C9D0DA", 80)
contador(img, 1)
img.save(OUT + "slide_01.png")

# ---------- 2 ----------
img = fondo(pos=(0.8, 0.15), radio=1.2, inten=1.0)
d = ImageDraw.Draw(img)
fh = inter(800, 92)
d.text((M, 440), "No es un tema", font=fh, fill=BLANCO)
w = d.textlength("No es un tema", font=fh)
trazo_mano(d, M, M + w, 498, ROJO)
d.text((M, 548), "técnico.", font=fh, fill=BLANCO)
fr = inter(900, 104)
lineas(d, M, 710, "Es un tema\nde dueño.", fr, ROJO, 118)
cuerpo = wrap(d, "Si no sabes dónde vive tu web, quién la paga y a nombre de quién está, no la controlas tú.", inter(400, 38), ANCHO - 2 * M)
lineas(d, M, 990, cuerpo, inter(400, 38), "#C9D0DA", 54)
contador(img, 2)
img.save(OUT + "slide_02.png")

# ---------- 3 (fondo claro con grilla de puntos) ----------
img = Image.new("RGB", (ANCHO, ALTO), BLANCO)
d = ImageDraw.Draw(img)
for yy in range(20, ALTO, 34):
    for xx in range(20, ANCHO, 34):
        d.ellipse((xx - 1.5, yy - 1.5, xx + 1.5, yy + 1.5), fill="#D6DAE0")
lineas(d, M - 10, 110, "¿Te suena\nalguna?", inter(800, 88), AZUL_TXT, 102)
items = ["Tu web la hizo alguien que ya no te contesta.",
         "No sabes cuánto pagas al año ni a quién.",
         "Tu correo es un Gmail, no @tunegocio.cl.",
         "El dominio está a nombre del diseñador.",
         "Te da miedo cambiar algo porque se cae."]
fi = inter(700, 36)
y = 360
for i, t in enumerate(items):
    marcado = i == 3
    txt = wrap(d, t, fi, ANCHO - 2 * M - 150)
    n = txt.count("\n") + 1
    h = 58 + n * 46
    x0, x1 = M - 30, ANCHO - M + 30
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((x0 + 4, y + 10, x1 + 4, y + h + 10), radius=18, fill=(6, 19, 35, 45))
    sombra = sombra.filter(ImageFilter.GaussianBlur(12))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sombra).convert("RGB"))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y, x1, y + h), radius=18, fill=AZUL_NOCHE if marcado else BLANCO, outline=None if marcado else "#E3E6EA", width=2)
    cb = (x0 + 36, y + h / 2 - 24, x0 + 84, y + h / 2 + 24)
    d.rounded_rectangle(cb, radius=8, outline=ROJO if marcado else AZUL_TXT, width=5)
    if marcado:
        d.line([(cb[0] + 11, cb[1] + 25), (cb[0] + 21, cb[1] + 35), (cb[0] + 38, cb[1] + 13)], fill=ROJO, width=6, joint="curve")
    lineas(d, x0 + 120, y + 29, txt, fi, BLANCO if marcado else AZUL_TXT, 46)
    y += h + 26
pegar_logo(img, "azul", "inferior_izquierda", tamano=60, margen=M - 8)
contador(img, 3, oscuro=False)
img.save(OUT + "slide_03.png")

# ---------- 4 (secuencia) ----------
img = fondo(pos=(0.1, 0.45), radio=0.9, inten=0.8)
d = ImageDraw.Draw(img)
lineas(d, M, 150, "Una web tiene cuatro piezas,\ny van en un orden.", inter(500, 44), "#C9D0DA", 60)
nums = ["1", "2", "3", "4"]
labels = ["DOMINIO", "DNS", "HOSTING", "DISEÑO"]
fn = inter(800, 150)
cy = 560
xs = [M + 80 + i * ((ANCHO - 2 * M - 250) / 3) for i in range(4)]
for i, (n, lab) in enumerate(zip(nums, labels)):
    activo = i == 3
    w = d.textlength(n, font=fn)
    col = BLANCO if activo else "#3B4E66"
    d.text((xs[i] - w / 2, cy - 100), n, font=fn, fill=col)
    fl = inter(700, 24)
    wl = d.textlength(lab, font=fl)
    d.text((xs[i] - wl / 2, cy + 95), lab, font=fl, fill=ROJO if activo else "#3B4E66")
    if activo:
        d.ellipse((xs[i] - 105, cy - 105, xs[i] + 105, cy + 85), outline=ROJO, width=7)
# flecha curva
ax = xs[3]
pts = []
for i in range(31):
    t = i / 30
    p0, p1, p2 = (ax - 120, 900), (ax - 130, 760), (ax - 20, 720)
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    yv = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    pts.append((x, yv))
d.line(pts, fill=ROJO, width=6, joint="curve")
ex, ey = pts[-1]
d.line([(ex - 34, ey - 12), (ex, ey), (ex - 22, ey + 26)], fill=ROJO, width=6, joint="curve")
ft = inter(800, 44)
t = "Tú empezaste acá."
img = texto_con_sombra(img, (ax - 120 - d.textlength(t, font=ft) / 2 - 40, 920), t, ft)
d = ImageDraw.Draw(img)
lineas(d, M, 1110, "Por eso se ve bien.\nY por eso no es tuya.", inter(800, 60), BLANCO, 74)
contador(img, 4)
img.save(OUT + "slide_04.png")

# ---------- 5 (las 4 piezas) ----------
img = fondo(pos=(0.95, 0.95), radio=0.8, inten=0.7)
logo(img)
d = ImageDraw.Draw(img)
lineas(d, M, 230, "Las 4 piezas,\nen simple.", inter(800, 84), BLANCO, 100)
piezas = [("Dominio", "La dirección. El nombre que la gente escribe."),
          ("DNS", "El letrero. Lleva a la gente al lugar correcto."),
          ("Hosting", "El local arrendado donde vive tu web."),
          ("Diseño", "La vitrina. Lo único que ve tu cliente.")]
y = 500
for i, (t, desc) in enumerate(piezas):
    d.text((M, y), f"0{i+1}", font=inter(800, 40), fill=ROJO)
    d.text((M + 90, y - 4), t, font=inter(800, 46), fill=BLANCO)
    lineas(d, M + 90, y + 60, wrap(d, desc, inter(400, 34), ANCHO - 2 * M - 90), inter(400, 34), "#C9D0DA", 46)
    y += 185
    if i < 3:
        d.line((M + 90, y - 40, ANCHO - M, y - 40), fill="#1E3350", width=2)
contador(img, 5)
img.save(OUT + "slide_05.png")

# ---------- 6 (el orden correcto) ----------
img = fondo(pos=(0.9, 0.1), radio=0.9, inten=0.8)
logo(img)
d = ImageDraw.Draw(img)
d.text((M, 230), "El orden", font=inter(800, 84), fill=BLANCO)
caja(img, M, 340, "correcto.", inter(800, 84), ROJO, BLANCO)
d = ImageDraw.Draw(img)
pasos = [("Dominio a tu nombre", "Un .cl cuesta $9.990 al año en NIC Chile. Titular: tú o tu empresa."),
         ("DNS en un panel que tú controles", "Con tu propio usuario y clave, no con los de tu proveedor."),
         ("Hosting según lo que vendes", "Constructor visual, tienda online o hosting moderno."),
         ("Recién ahí, el diseño", "Sobre una base que es tuya, se puede cambiar sin perder nada.")]
y = 520
for i, (t, desc) in enumerate(pasos):
    d.ellipse((M, y + 2, M + 52, y + 54), fill=ROJO if i == 3 else None, outline=ROJO, width=4)
    n = str(i + 1)
    fnum = inter(800, 28)
    d.text((M + 26 - d.textlength(n, font=fnum) / 2, y + 10), n, font=fnum, fill=BLANCO)
    d.text((M + 80, y + 4), t, font=inter(800, 38), fill=BLANCO)
    lineas(d, M + 80, y + 58, wrap(d, desc, inter(400, 30), ANCHO - 2 * M - 80), inter(400, 30), "#C9D0DA", 42)
    y += 190
contador(img, 6)
img.save(OUT + "slide_06.png")

# ---------- 7 (frase) ----------
img = fondo(pos=(0.75, 0.2), radio=1.2, inten=1.0)
d = ImageDraw.Draw(img)
lineas(d, M, 360, "Una web bonita\nsin dueño", inter(800, 92), BLANCO, 108)
lineas(d, M, 590, "es un\narriendo.", inter(900, 116), ROJO, 130)
lineas(d, M, 900, wrap(d, "Si tu proveedor desaparece, tu dirección y tu correo se van con él.", inter(400, 38), ANCHO - 2 * M), inter(400, 38), "#C9D0DA", 54)
contador(img, 7)
img.save(OUT + "slide_07.png")

# ---------- 8 CTA ----------
img = fondo(pos=(0.15, 0.95), radio=0.9, inten=0.8)
logo(img)
d = ImageDraw.Draw(img)
d.text((M, 400), "Comenta", font=inter(700, 60), fill=BLANCO)
fb = inter(900, 128)
b = d.textbbox((0, 0), "DOMINIO", font=fb)
bw, bh = b[2] - b[0] + 70, b[3] - b[1] + 60
caja_img = Image.new("RGBA", (bw + 80, bh + 80), (0, 0, 0, 0))
cd = ImageDraw.Draw(caja_img)
cd.rounded_rectangle((40, 40, 40 + bw, 40 + bh), radius=10, fill=ROJO)
cd.text((40 + 35 - b[0], 40 + 30 - b[1]), "DOMINIO", font=fb, fill=BLANCO)
caja_img = caja_img.rotate(2, resample=Image.BICUBIC, expand=False)
sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((M + 10, 510, M + bw + 10, 510 + bh), radius=10, fill=(0, 0, 0, 120))
sh = sh.filter(ImageFilter.GaussianBlur(14))
base = Image.alpha_composite(img.convert("RGBA"), sh)
base.paste(caja_img, (M - 40, 490 - 40), caja_img)
img = base.convert("RGB")
d = ImageDraw.Draw(img)
fcta = inter(700, 42)
partes = [("y te mando la checklist exacta para revisar tu web ", BLANCO), ("en 10 minutos:", ROJO),
          (" quién es el dueño de tu dominio, dónde está alojada y cuánto pagas por ella.", BLANCO)]
x, y = M, 740
maxx = ANCHO - M
for texto, col in partes:
    for palabra in texto.split(" "):
        if not palabra: continue
        w = d.textlength(palabra + " ", font=fcta)
        if x + d.textlength(palabra, font=fcta) > maxx:
            x, y = M, y + 60
        d.text((x, y), palabra, font=fcta, fill=col)
        x += w
contador(img, 8)
img.save(OUT + "slide_08_cta.png")
print("ok")
