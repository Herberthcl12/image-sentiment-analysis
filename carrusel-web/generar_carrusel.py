import sys
sys.path.insert(0, "/root/.claude/skills/synced/a83d7b8b-6484-4f1d-b672-5dde2b410928_0fec2520-89fe-4255-ba8e-9c8f4e367f11/hh-carrusel-instagram/scripts")
from generar_slide import *
from PIL import ImageDraw

OUT = "/home/user/image-sentiment-analysis/carrusel-web/"
M = 90  # margen lateral
GRIS = GRIS_CLARO
LINEA = "#1E2A3A"

def wrap(draw, texto, font, ancho):
    out = []
    for parrafo in texto.split("\n"):
        palabras, linea = parrafo.split(), ""
        for p in palabras:
            prueba = (linea + " " + p).strip()
            if draw.textlength(prueba, font=font) <= ancho:
                linea = prueba
            else:
                out.append(linea); linea = p
        out.append(linea)
    return "\n".join(out)

def alto_texto(draw, texto, font, ls=1.3):
    h = 0
    for l in texto.split("\n"):
        b = draw.textbbox((0, 0), l or "A", font=font)
        h += (b[3] - b[1]) * ls
    return h

def cuerpo(draw, texto, x, y, font, fill, ancho, ls=1.35):
    t = wrap(draw, texto, font, ancho)
    y0 = y
    for l in t.split("\n"):
        draw.text((x, y), l, font=font, fill=fill)
        b = draw.textbbox((0, 0), l or "A", font=font)
        y += (b[3] - b[1]) * ls + 6
    return y

def header(img, titulo, clave, y=110):
    d = ImageDraw.Draw(img)
    ft = fuente("league_gothic", 132)
    d.text((M, y), titulo, font=ft, fill=BLANCO)
    b = d.textbbox((M, y), titulo, font=ft)
    fk = fuente("montserrat_bold", 34)
    d.text((M, b[3] + 22), clave, font=fk, fill=ROJO)
    kb = d.textbbox((M, b[3] + 22), clave, font=fk)
    return kb[3]

def swipe(img):
    d = ImageDraw.Draw(img)
    d.text((M, ALTO - 50 - 40), "DESLIZA  →", font=fuente("montserrat_semibold", 26), fill=GRIS)

def lista(img, items, y_ini, y_fin):
    d = ImageDraw.Draw(img)
    fn = fuente("league_gothic", 110)
    ftit = fuente("montserrat_bold", 38)
    fdesc = fuente("montserrat", 30)
    xt = M + 150
    ancho = ANCHO - xt - M
    bloques = []
    for num, tit, desc in items:
        h = alto_texto(d, wrap(d, tit, ftit, ancho), ftit, 1.3) + 14 + alto_texto(d, wrap(d, desc, fdesc, ancho), fdesc, 1.35) + 6 * desc.count(" ") * 0
        bloques.append(h)
    total = sum(bloques)
    hueco = (y_fin - y_ini - total) / (len(items))
    y = y_ini + hueco / 2
    for (num, tit, desc), h in zip(items, bloques):
        d.text((M, y - 18), num, font=fn, fill=ROJO)
        yy = cuerpo(d, tit, xt, y, ftit, BLANCO, ancho, 1.3)
        cuerpo(d, desc, xt, yy + 8, fdesc, GRIS, ancho)
        y += h + hueco
        if (num, tit, desc) != items[-1]:
            d.line((xt, y - hueco / 2, ANCHO - M, y - hueco / 2), fill=LINEA, width=2)

# ---------- 1 PORTADA ----------
img = fondo_foco(AZUL_NOCHE, posicion=(0.85, 0.9), radio=0.75)
d = ImageDraw.Draw(img)
ft = fuente("league_gothic", 210)
y = 300
for l in ["TU WEB", "FUNCIONA COMO", "UN LOCAL"]:
    d.text((M, y), l, font=ft, fill=BLANCO)
    y += 205
img = texto_con_sombra(img, (M, y + 40), "Dominio, hosting y DNS", fuente("montserrat_bold", 50))
d = ImageDraw.Draw(img)
d.text((M, y + 115), "explicados sin tecnicismos", font=fuente("montserrat", 40), fill=GRIS)
pegar_logo(img, "blanco", "superior_derecha", tamano=90, margen=60)
swipe(img)
img.save(OUT + "slide_01_portada.png")

# ---------- 2 CARDS: LAS 4 PIEZAS ----------
img = fondo_con_vida(AZUL_NOCHE, "plano")
yb = header(img, "LAS 4 PIEZAS", "de cualquier web")
d = ImageDraw.Draw(img)
cards = [("DOMINIO", "La dirección", "El nombre que la gente escribe: tunegocio.cl"),
         ("HOSTING", "El local arrendado", "El servidor siempre encendido donde vive tu web"),
         ("DNS", "El letrero", "Conecta tu nombre con tu hosting y tu correo"),
         ("CORREO", "El buzón", "hola@tunegocio.cl en vez de un Gmail genérico")]
gap = 26
cw = (ANCHO - 2 * M - gap) / 2
y0 = yb + 70
ch = (ALTO - 150 - y0 - gap) / 2
for i, (t, s, desc) in enumerate(cards):
    x = M + (i % 2) * (cw + gap)
    y = y0 + (i // 2) * (ch + gap)
    d.rounded_rectangle((x, y, x + cw, y + ch), radius=28, fill="#0B1D33", outline="#1E3350", width=2)
    d.text((x + 36, y + 40), t, font=fuente("league_gothic", 92), fill=BLANCO)
    d.text((x + 36, y + 160), s, font=fuente("montserrat_bold", 32), fill=ROJO)
    cuerpo(d, desc, x + 36, y + 225, fuente("montserrat", 27), GRIS, cw - 72)
pegar_logo(img, "blanco", "inferior_derecha", tamano=60)
img.save(OUT + "slide_02.png")

# ---------- 3 LISTA: DOMINIO ----------
img = fondo_con_vida(AZUL_NOCHE, "plano")
yb = header(img, "EL DOMINIO", "se arrienda, no se compra")
lista(img, [
    ("01", "Pagas por año", "Un .cl cuesta $9.990 al año en NIC Chile. La renovación vale lo mismo."),
    ("02", "Si no renuevas, lo pierdes", "Cuando vence, cualquier persona lo puede registrar. Activa la renovación automática."),
    ("03", "Los subdominios son gratis", "Con tunegocio.cl puedes crear reservas.tunegocio.cl sin pagar nada extra."),
], yb + 40, ALTO - 150)
pegar_logo(img, "blanco", "inferior_derecha", tamano=60)
img.save(OUT + "slide_03.png")

# ---------- 4 LISTA: HOSTING ----------
img = fondo_con_vida(AZUL_NOCHE, "plano")
yb = header(img, "EL HOSTING", "3 tipos según lo que necesitas")
lista(img, [
    ("01", "Constructor visual", "Wix, Squarespace o Framer. Editas tú, sin programar. Pagas una mensualidad por sitio."),
    ("02", "Tienda online", "Shopify o Jumpseller. Carrito, pagos y stock. Mensualidad más comisión por venta."),
    ("03", "Hosting moderno", "Cloudflare Pages, Vercel o Netlify. Webs a medida, rápidas y desde $0 al mes."),
], yb + 40, ALTO - 150)
pegar_logo(img, "blanco", "inferior_derecha", tamano=60)
img.save(OUT + "slide_04.png")

# ---------- 5 DIAGRAMA: RECORRIDO ----------
img = fondo_con_vida(AZUL_NOCHE, "plano")
yb = header(img, "QUÉ PASA CUANDO", "alguien escribe tunegocio.cl")
d = ImageDraw.Draw(img)
pasos = [("Tu cliente escribe", "tunegocio.cl en el celular"),
         ("El DNS busca", "en qué hosting vive tu web"),
         ("El hosting responde", "y muestra tu página"),
         ("La base de datos guarda", "la reserva o la compra")]
xl = M + 30
ytop, ybot = yb + 110, ALTO - 190
paso_h = (ybot - ytop) / (len(pasos) - 1)
d.line((xl, ytop, xl, ybot), fill=GRIS, width=4)
for i, (t, s) in enumerate(pasos):
    y = ytop + i * paso_h
    clave = i == 1
    r = 26 if clave else 20
    d.ellipse((xl - r, y - r, xl + r, y + r), fill=ROJO if clave else BLANCO)
    d.text((xl + 70, y - 40), t, font=fuente("montserrat_bold", 40), fill=ROJO if clave else BLANCO)
    d.text((xl + 70, y + 14), s, font=fuente("montserrat", 32), fill=GRIS)
pegar_logo(img, "blanco", "inferior_derecha", tamano=60)
img.save(OUT + "slide_05.png")

# ---------- 6 LISTA: ERROR CLÁSICO ----------
img = fondo_con_vida(AZUL_NOCHE, "plano")
yb = header(img, "EL ERROR CLÁSICO", "tu dominio a nombre del diseñador")
d = ImageDraw.Draw(img)
yb = cuerpo(d, "Si el dominio está a nombre de quien hizo tu web, esa persona controla tu dirección y tu correo. Si terminan mal, los pierdes.",
            M, yb + 50, fuente("montserrat_semibold", 32), BLANCO, ANCHO - 2 * M)
lista(img, [
    ("01", "Revisa quién es el titular", "Busca tu dominio en nic.cl. El titular aparece de forma pública."),
    ("02", "Debe decir tu nombre", "O el de tu empresa. Nunca el de la agencia ni el del diseñador."),
    ("03", "La agencia administra", "Puede tener acceso para gestionarlo, pero el dueño eres tú."),
], yb + 10, ALTO - 150)
pegar_logo(img, "blanco", "inferior_derecha", tamano=60)
img.save(OUT + "slide_06.png")

# ---------- 7 CHECKLIST ----------
img = fondo_con_vida(AZUL_NOCHE, "plano")
yb = header(img, "CHECKLIST", "de una web que sí sirve")
d = ImageDraw.Draw(img)
items = ["Candado de HTTPS activo",
         "Se ve bien en el celular",
         "Botón “Reservar” o “Comprar” visible sin bajar",
         "Precios a la vista",
         "Conectada a tu Perfil de Empresa de Google",
         "Dominio a tu nombre, con renovación automática"]
ytop, ybot = yb + 80, ALTO - 170
step = (ybot - ytop) / len(items)
f = fuente("montserrat_semibold", 36)
for i, t in enumerate(items):
    y = ytop + i * step + (step - 56) / 2
    d.rounded_rectangle((M, y, M + 56, y + 56), radius=10, outline=ROJO, width=4)
    d.line((M + 13, y + 29, M + 25, y + 41), fill=ROJO, width=6)
    d.line((M + 25, y + 41, M + 44, y + 16), fill=ROJO, width=6)
    cuerpo(d, t, M + 90, y + 6, f, BLANCO, ANCHO - 2 * M - 90)
pegar_logo(img, "blanco", "inferior_derecha", tamano=60)
img.save(OUT + "slide_07.png")

# ---------- 8 CIERRE ----------
img = fondo_con_vida(AZUL_NOCHE, "vineta")
d = ImageDraw.Draw(img)
logo_w = 220
pegar_logo(img, "blanco", "centro", tamano=logo_w)
# mover bloque: logo arriba del texto -> redibujar en posición
img = fondo_con_vida(AZUL_NOCHE, "vineta")
from PIL import Image as _I
import os
logo = _I.open(os.path.join(LOGOS, "logo_hh_blanco.png")).convert("RGBA")
logo = logo.resize((logo_w, int(logo.height * logo_w / logo.width)))
ft = fuente("league_gothic", 150)
lineas = ["UNA WEB BONITA", "NO BASTA"]
d = ImageDraw.Draw(img)
alto_bloque = logo.height + 70 + 2 * 150 + 40 + 60 + 70 + 3 * 48
y = (ALTO - alto_bloque) / 2
img.paste(logo, ((ANCHO - logo.width) // 2, int(y)), logo)
y += logo.height + 70
for l in lineas:
    w = d.textlength(l, font=ft)
    d.text(((ANCHO - w) / 2, y), l, font=ft, fill=BLANCO)
    y += 150
fr = fuente("montserrat_bold", 44)
frase = "tiene que ser tuya y funcionar"
w = d.textlength(frase, font=fr)
img = texto_con_sombra(img, ((ANCHO - w) / 2, y + 40), frase, fr)
d = ImageDraw.Draw(img)
y += 40 + 60 + 70
fc = fuente("montserrat", 34)
cta = wrap(d, "Escríbenos WEB por DM y revisamos contigo\nquién es el dueño de tu dominio\ny qué le falta a tu web.", fc, ANCHO - 2 * M - 40)
for l in cta.split("\n"):
    w = d.textlength(l, font=fc)
    d.text(((ANCHO - w) / 2, y), l, font=fc, fill=GRIS)
    y += 48
img.save(OUT + "slide_08_cierre.png")
print("ok")
