import avatar1 from "./assets/1534528741775-53994a69daeb.jpg";
import avatar2 from "./assets/1507003211169-0a1dd7228f2d.jpg";
import avatar3 from "./assets/1494790108377-be9c29b29330.jpg";
import avatar4 from "./assets/1500648767791-00dcc994a43e.jpg";

// ---------------------------------------------------------------------------
// Negocio
// ---------------------------------------------------------------------------

export const BRAND = "Marcut's Barber";
export const ADMIN_PIN = "1234";
export const HOURS = [12, 13, 14, 15, 16, 17, 18, 19, 20]; // bloques de 60 min, el último termina 21:00
export const DAY_SHORT = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB"];
export const DAY_FULL = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
export const MONTHS = [
  "enero", "febrero", "marzo", "abril", "mayo", "junio",
  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
];
export const MONTHS_SHORT = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"];

export const AVATARS = [avatar1, avatar2, avatar3, avatar4];

export interface Service {
  id: string;
  name: string;
  desc: string;
  price: number;
  minutes: number;
}

export const SERVICES: Service[] = [
  { id: "corte", name: "Corte clásico / fade", desc: "Lavado, corte y peinado", price: 12000, minutes: 45 },
  { id: "combo", name: "Corte + barba", desc: "El combo completo", price: 17000, minutes: 60 },
  { id: "barba", name: "Barba & perfilado", desc: "Toalla caliente y navaja", price: 8000, minutes: 30 },
  { id: "diseno", name: "Corte + diseño", desc: "Líneas o freestyle", price: 15000, minutes: 60 },
  { id: "kids", name: "Corte niño (-12)", desc: "Paciencia incluida", price: 9000, minutes: 40 },
];

export type ProductCat = "Styling" | "Barba" | "Cuidado" | "Accesorios" | "Pro";

export interface Product {
  id: string;
  cat: ProductCat;
  name: string;
  desc: string;
  price: number;
  stock: number;
  badge?: string;
}

export const PRODUCTS: Product[] = [
  { id: "p1", cat: "Styling", name: "Pomada Matte Clay", desc: "Fijación fuerte, acabado mate. 100 g.", price: 12990, stock: 14, badge: "TOP" },
  { id: "p2", cat: "Styling", name: "Pomada Base Agua Shine", desc: "Brillo medio, se lava fácil. 120 g.", price: 10990, stock: 9 },
  { id: "p3", cat: "Styling", name: "Polvo Texturizador", desc: "Volumen instantáneo en raíz. 20 g.", price: 8990, stock: 18, badge: "NEW" },
  { id: "p4", cat: "Styling", name: "Spray Fijador Street Hold", desc: "Fijación 24 h sin rigidez. 250 ml.", price: 9490, stock: 7 },
  { id: "p5", cat: "Barba", name: "Aceite para Barba Cedro", desc: "Suaviza y quita la picazón. 30 ml.", price: 11490, stock: 11 },
  { id: "p6", cat: "Barba", name: "Bálsamo Barba Sandalwood", desc: "Control y forma para barba larga. 60 g.", price: 10490, stock: 6 },
  { id: "p7", cat: "Barba", name: "Kit Barba Starter", desc: "Aceite, bálsamo y peine de madera.", price: 24990, stock: 4, badge: "-15%" },
  { id: "p8", cat: "Cuidado", name: "Shampoo Anticaspa Carbón", desc: "Carbón activado y menta. 300 ml.", price: 9990, stock: 12 },
  { id: "p9", cat: "Cuidado", name: "After Shave Bálsamo Frío", desc: "Calma la piel después del perfilado. 100 ml.", price: 8490, stock: 10 },
  { id: "p10", cat: "Cuidado", name: "Minoxidil Espuma 5%", desc: "Para barba o entradas. Tratamiento de 1 mes.", price: 19990, stock: 5 },
  { id: "p11", cat: "Accesorios", name: "Peine Carbono Antiestático", desc: "Diente fino y grueso, no se quiebra.", price: 4990, stock: 25 },
  { id: "p12", cat: "Accesorios", name: "Durag Satín Negro", desc: "Para waves y proteger el peinado.", price: 6990, stock: 8 },
  { id: "p13", cat: "Pro", name: "Trimmer Inalámbrica", desc: "Mantén el perfilado en casa. Carga USB-C.", price: 39990, stock: 3, badge: "PRO" },
  { id: "p14", cat: "Pro", name: "Navaja Barbera + 10 hojas", desc: "Acero inoxidable, hoja intercambiable.", price: 14990, stock: 6 },
  { id: "p15", cat: "Pro", name: "Capa de corte Marcut's", desc: "Impermeable con logo, edición limitada.", price: 17990, stock: 4 },
];

export const SEED_REVIEWS = [
  { name: "Benja Soto", stars: 5, text: "El mejor fade que me han hecho. Llegué a mi hora exacta y en 40 min estaba listo.", svc: "Corte clásico / fade", days: 3 },
  { name: "Nico Fuentes", stars: 5, text: "Reservar por acá es demasiado cómodo, cero mensajes de \"¿tienes hora?\". El diseño quedó perfecto.", svc: "Corte + diseño", days: 6 },
  { name: "Diego Paredes", stars: 4, text: "Muy buen perfilado de barba y el aceite de cedro vale la pena. Solo había poco espacio para estacionar.", svc: "Barba & perfilado", days: 9 },
  { name: "Tomás Vera", stars: 5, text: "Lo llevé con mi hijo, los dos salimos impecables. Buena música y buena onda.", svc: "Corte niño (-12)", days: 14 },
  { name: "Joaquín Lagos", stars: 5, text: "Aparté la pomada mate desde la web y me la tenían lista en caja. Corte + barba 10/10.", svc: "Corte + barba", days: 18 },
  { name: "Felipe Araya", stars: 4, text: "Buen corte, precio justo. Me hubiese gustado que abrieran el domingo.", svc: "Corte clásico / fade", days: 25 },
];

// ---------------------------------------------------------------------------
// Utilidades
// ---------------------------------------------------------------------------

export const clp = (n: number) => "$" + n.toLocaleString("es-CL");
export const hh = (h: number) => String(h).padStart(2, "0") + ":00";
export const svc = (id: string) => SERVICES.find((s) => s.id === id) ?? SERVICES[0];

export function iso(d: Date) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
export function parseIso(s: string) {
  const [y, m, d] = s.split("-").map(Number);
  return new Date(y, m - 1, d);
}
export function mondayOf(d: Date) {
  const x = new Date(d.getFullYear(), d.getMonth(), d.getDate());
  x.setDate(x.getDate() - ((x.getDay() + 6) % 7));
  return x;
}
export function isPast(date: string, hour: number) {
  const d = parseIso(date);
  d.setHours(hour, 0, 0, 0);
  return d < new Date();
}
/** Índice 0–5 (lunes–sábado) o -1 para domingo. */
export const weekdayIdx = (d: Date) => (d.getDay() === 0 ? -1 : d.getDay() - 1);
export function niceDate(date: string) {
  const d = parseIso(date);
  return `${DAY_FULL[weekdayIdx(d)] ?? "Domingo"} ${d.getDate()} de ${MONTHS[d.getMonth()]}`;
}
export const initials = (n: string) =>
  n.trim().split(/\s+/).slice(0, 2).map((w) => w[0]).join("").toUpperCase();
/** "Benja Soto" → "Benja S." para mostrar reservas en público sin exponer datos. */
export const publicName = (n: string) => {
  const [first, last] = n.trim().split(/\s+/);
  return last ? `${first} ${last[0]}.` : first;
};
export function ago(t: number) {
  const d = Math.max(0, Math.round((Date.now() - t) / 864e5));
  if (d === 0) return "hoy";
  if (d === 1) return "ayer";
  if (d < 7) return `hace ${d} días`;
  const w = Math.round(d / 7);
  return w === 1 ? "hace 1 semana" : `hace ${w} semanas`;
}
