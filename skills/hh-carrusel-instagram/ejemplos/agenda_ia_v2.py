import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from generar_slide import *
from PIL import ImageDraw

OUT = os.path.join(os.getcwd(), "salida_ejemplo") + "/"
os.makedirs(OUT, exist_ok=True)
TOTAL = 8
W = ANCHO - 2 * M

def cx(d, t, f): return (ANCHO - d.textlength(t, font=f)) / 2

# 1 HOOK centrado, recuadro en primera línea
img = fondo_hh(posicion=(0.5, 0.02), radio=1.0, intensidad=1.0)
logo_esquina(img)
d = ImageDraw.Draw(img)
fh = inter(800, 96)
caja_destacada(img, cx(d, "Tu agenda", fh), 330, "Tu agenda", fh)
d = ImageDraw.Draw(img)
y = lineas(d, 0, 450, "ya tiene tu\npróxima campaña.", fh, BLANCO, 112, centrado=True)
d.line((ANCHO / 2 - 85, y + 40, ANCHO / 2 + 85, y + 40), fill=BLANCO, width=5)
lineas(d, 0, y + 100, "Solo que hoy está repartida\nentre WhatsApp, un cuaderno\ny tu memoria.", inter(800, 56), GRIS_TEXTO, 72, centrado=True)
contador(img, 1, TOTAL)
img.save(OUT + "slide_01.png")

# 2 ESPEJO claro
img = fondo_claro_puntos()
d = ImageDraw.Draw(img)
lineas(d, M - 10, 110, "¿Te suena\nalguna?", inter(800, 88), AZUL_NOCHE, 102)
items = ["Confirmas cada hora a mano por WhatsApp.",
         "Alguien no llega y esa hora se pierde.",
         "No sabes quién dejó de venir hace dos meses.",
         "Publicas promociones sin saber a quién le llegan.",
         "Tus clientes son chats sueltos, no una base."]
y = 360
for i, t in enumerate(items):
    y = tarjeta_check(img, M - 30, y, ANCHO - M + 30, t, inter(700, 36), marcada=(i == 3)) + 26
pegar_logo(img, "azul", "inferior_izquierda", tamano=60, margen=M - 8)
contador(img, 2, TOTAL, oscuro=False)
img.save(OUT + "slide_02.png")

# 3 REENCUADRE tachado (izquierda, bloque bajo)
img = fondo_hh(posicion=(0.85, 0.12), radio=1.2, intensidad=1.0)
d = ImageDraw.Draw(img)
fh = inter(800, 92)
d.text((M, 470), "Te falta publicar", font=fh, fill=BLANCO)
trazo_mano(d, M, M + d.textlength("Te falta publicar", font=fh), 528)
d.text((M, 578), "más.", font=fh, fill=BLANCO)
lineas(d, M, 740, "Te falta usar\nlo que ya sabes.", inter(900, 104), ROJO, 118)
lineas(d, M, 1020, wrap(d, "Cada reserva te dice quién es, qué pidió, cuándo vino y si acepta recibir novedades.", inter(400, 36), W), inter(400, 36), GRIS_TEXTO, 50)
contador(img, 3, TOTAL)
img.save(OUT + "slide_03.png")

# 4 SECUENCIA
img = fondo_hh(posicion=(0.08, 0.5), radio=0.9, intensidad=0.8)
d = ImageDraw.Draw(img)
lineas(d, M, 150, "El marketing continuo tiene\ncuatro pasos, y van en orden.", inter(500, 44), GRIS_TEXTO, 60)
labels = ["AGENDA", "DATOS", "SEGMENTOS", "CAMPAÑAS"]
fn = inter(800, 150)
cy = 560
xs = [M + 80 + i * ((ANCHO - 2 * M - 250) / 3) for i in range(4)]
for i, lab in enumerate(labels):
    act = i == 3
    n = str(i + 1)
    d.text((xs[i] - d.textlength(n, font=fn) / 2, cy - 100), n, font=fn, fill=BLANCO if act else GRIS_APAGADO)
    fl = inter(700, 22)
    d.text((xs[i] - d.textlength(lab, font=fl) / 2, cy + 95), lab, font=fl, fill=ROJO if act else GRIS_APAGADO)
    if act:
        d.ellipse((xs[i] - 105, cy - 105, xs[i] + 105, cy + 85), outline=ROJO, width=7)
ax = xs[3]
flecha_curva(d, (ax - 120, 900), (ax - 130, 760), (ax - 20, 720))
ft = inter(800, 44)
t = "Tú empezaste acá."
img = texto_con_sombra(img, (ax - 160 - d.textlength(t, font=ft) / 2, 920), t, ft)
d = ImageDraw.Draw(img)
lineas(d, M, 1100, "Por eso publicas harto.\nY por eso no sabes qué funciona.", inter(800, 54), BLANCO, 70)
contador(img, 4, TOTAL)
img.save(OUT + "slide_04.png")

# 5 EXPLICACIÓN
img = fondo_hh(posicion=(0.95, 0.95), radio=0.8, intensidad=0.7)
logo_esquina(img)
d = ImageDraw.Draw(img)
d.text((M, 230), "Lo que hace sola", font=inter(800, 80), fill=BLANCO)
caja_destacada(img, M, 330, "una agenda automática.", inter(800, 64))
d = ImageDraw.Draw(img)
piezas = [("Reserva 24/7", "Tu cliente elige hora sin escribirte."),
          ("Confirma y recuerda", "Un aviso antes de la cita, sin que tú lo mandes."),
          ("Pide permiso", "Registra quién acepta recibir novedades."),
          ("Arma tu base", "Nombre, teléfono, servicio y última visita.")]
y = 520
for i, (t, desc) in enumerate(piezas):
    d.text((M, y), f"0{i+1}", font=inter(800, 40), fill=ROJO)
    d.text((M + 90, y - 4), t, font=inter(800, 46), fill=BLANCO)
    lineas(d, M + 90, y + 60, wrap(d, desc, inter(400, 34), W - 90), inter(400, 34), GRIS_TEXTO, 46)
    y += 180
    if i < 3:
        d.line((M + 90, y - 38, ANCHO - M, y - 38), fill="#1E3350", width=2)
contador(img, 5, TOTAL)
img.save(OUT + "slide_05.png")

# 6 PROCESO: dónde entra la IA
img = fondo_hh(posicion=(0.12, 0.08), radio=0.9, intensidad=0.8)
logo_esquina(img, esquina="superior_derecha")
d = ImageDraw.Draw(img)
d.text((M, 230), "Y ahí entra", font=inter(800, 84), fill=BLANCO)
d.text((M, 334), "la IA.", font=inter(900, 84), fill=ROJO)
pasos = [("Detecta a quien no vuelve", "Por ejemplo, clientes sin reserva en 45 días."),
         ("Escribe el mensaje", "Un texto distinto según el servicio que tomó."),
         ("Lo envía solo a quien aceptó", "Por correo o WhatsApp, con opción de darse de baja."),
         ("Mide quién reservó después", "Así sabes qué campaña trajo clientes y cuál no.")]
y = 520
for i, (t, desc) in enumerate(pasos):
    d.ellipse((M, y + 2, M + 52, y + 54), fill=ROJO if i == 3 else None, outline=ROJO, width=4)
    n = str(i + 1); fnum = inter(800, 28)
    d.text((M + 26 - d.textlength(n, font=fnum) / 2, y + 10), n, font=fnum, fill=BLANCO)
    d.text((M + 80, y + 4), t, font=inter(800, 38), fill=BLANCO)
    lineas(d, M + 80, y + 58, wrap(d, desc, inter(400, 30), W - 80), inter(400, 30), GRIS_TEXTO, 42)
    y += 180
contador(img, 6, TOTAL)
img.save(OUT + "slide_06.png")

# 7 SENTENCIA centrada
img = fondo_hh(posicion=(0.5, 1.0), radio=1.1, intensidad=1.0)
d = ImageDraw.Draw(img)
y = lineas(d, 0, 330, "Publicar es\nhablarle a todos.", inter(800, 92), BLANCO, 108, centrado=True)
y = lineas(d, 0, y + 50, "Tu agenda te\ndice a quién.", inter(900, 108), ROJO, 122, centrado=True)
cuerpo = "Y desde diciembre de 2026, la Ley 21.719\nte exige demostrar el permiso\nde cada contacto."
lineas(d, 0, y + 70, cuerpo, inter(400, 36), GRIS_TEXTO, 52, centrado=True)
contador(img, 7, TOTAL)
img.save(OUT + "slide_07.png")

# 8 CTA centrado
img = fondo_hh(posicion=(0.9, 0.9), radio=0.95, intensidad=0.85)
logo_esquina(img)
d = ImageDraw.Draw(img)
fc = inter(700, 60)
d.text((cx(d, "Comenta", fc), 380), "Comenta", font=fc, fill=BLANCO)
fb = inter(900, 128)
bb = d.textbbox((0, 0), "AGENDA", font=fb)
bw = bb[2] - bb[0] + 70
img, yb = etiqueta_cta(img, int((ANCHO - bw) / 2), 490, "AGENDA", fb)
d = ImageDraw.Draw(img)
f42 = inter(700, 42)
bloque = [("y te mando el mapa de las", BLANCO), ("4 automatizaciones", ROJO), ("que puedes activar", BLANCO),
          ("esta semana:", ROJO), ("qué hace cada una", BLANCO), ("y cuánto cuesta.", BLANCO)]
# líneas centradas armadas a mano
filas = [[("y te mando el mapa de las", BLANCO)],
         [("4 automatizaciones que puedes", BLANCO)],
         [("activar ", BLANCO), ("esta semana:", ROJO)],
         [("qué hace cada una y cuánto cuesta.", BLANCO)]]
y = yb + 110
for fila in filas:
    total_w = sum(d.textlength(t, font=f42) for t, _ in fila)
    x = (ANCHO - total_w) / 2
    for t, c in fila:
        d.text((x, y), t, font=f42, fill=c); x += d.textlength(t, font=f42)
    y += 62
contador(img, 8, TOTAL)
img.save(OUT + "slide_08_cta.png")
print("ok")
