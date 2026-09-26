import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { AVATARS, HOURS, SEED_REVIEWS, SERVICES, iso } from "./data";

export interface User {
  name: string;
  phone: string;
  email: string;
  mkEmail: boolean;
  mkSms: boolean;
  terms: number;
  avatar?: string;
}

export interface Booking {
  id: string;
  date: string;
  hour: number;
  service: string;
  email: string;
}

export interface Review {
  id: string;
  name: string;
  stars: number;
  text: string;
  svc: string;
  at: number;
}

export interface State {
  open: boolean;
  users: Record<string, User>;
  bookings: Booking[];
  reviews: Review[];
  session: string | null;
  /** productos apartados por correo de cliente */
  held: Record<string, string[]>;
}

const KEY = "marcuts_barber_hero_v1";

function seed(): State {
  const now = Date.now();
  const users: Record<string, User> = {
    "benja@demo.cl": { name: "Benja Soto", phone: "+56 9 8123 4411", email: "benja@demo.cl", mkEmail: true, mkSms: true, terms: now, avatar: AVATARS[1] },
    "nico@demo.cl": { name: "Nico Fuentes", phone: "+56 9 7654 0923", email: "nico@demo.cl", mkEmail: true, mkSms: false, terms: now, avatar: AVATARS[3] },
    "cata@demo.cl": { name: "Cata Muñoz", phone: "+56 9 6612 7780", email: "cata@demo.cl", mkEmail: false, mkSms: true, terms: now, avatar: AVATARS[0] },
    "vale@demo.cl": { name: "Vale Rojas", phone: "+56 9 5520 1184", email: "vale@demo.cl", mkEmail: true, mkSms: true, terms: now, avatar: AVATARS[2] },
    "joaquin@demo.cl": { name: "Joaquín Lagos", phone: "+56 9 9031 5567", email: "joaquin@demo.cl", mkEmail: false, mkSms: false, terms: now },
  };
  const emails = Object.keys(users);
  const bookings: Booking[] = [];
  // Reservas demo deterministas: desde el inicio del mes hasta 3 semanas adelante.
  const today = new Date();
  const start = new Date(today.getFullYear(), today.getMonth(), 1);
  let k = 0;
  for (let i = 0; i < 60; i++) {
    const dt = new Date(start);
    dt.setDate(start.getDate() + i);
    if (dt.getDay() === 0) continue;
    const d = dt.getDate() + i;
    const n = (d * 7 + 3) % 5; // 0–4 reservas por día
    for (let j = 0; j < n; j++) {
      const hour = HOURS[(d * 3 + j * 4) % HOURS.length];
      const date = iso(dt);
      if (bookings.some((b) => b.date === date && b.hour === hour)) continue;
      bookings.push({ id: "seed" + k++, date, hour, service: SERVICES[(d + j) % SERVICES.length].id, email: emails[(d + j) % emails.length] });
    }
  }
  const reviews = SEED_REVIEWS.map((r, i) => ({ id: "r" + i, name: r.name, stars: r.stars, text: r.text, svc: r.svc, at: now - r.days * 864e5 }));
  return { open: true, users, bookings, reviews, session: null, held: {} };
}

function load(): State {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return JSON.parse(raw) as State;
  } catch {
    /* sin almacenamiento: se usa la demo */
  }
  return seed();
}

type Updater = (s: State) => State;

interface Store {
  state: State;
  update: (fn: Updater) => void;
  reset: () => void;
  me: User | null;
  toast: (msg: string) => void;
  toastMsg: string | null;
}

const Ctx = createContext<Store | null>(null);

export function StoreProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<State>(load);
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  useEffect(() => {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch {
      /* ignorado */
    }
  }, [state]);

  useEffect(() => {
    if (!toastMsg) return;
    const t = setTimeout(() => setToastMsg(null), 2600);
    return () => clearTimeout(t);
  }, [toastMsg]);

  const update = useCallback((fn: Updater) => setState((s) => fn(s)), []);
  const reset = useCallback(() => setState(seed()), []);
  const toast = useCallback((msg: string) => setToastMsg(msg), []);
  const me = state.session ? state.users[state.session] ?? null : null;

  const value = useMemo(() => ({ state, update, reset, me, toast, toastMsg }), [state, update, reset, me, toast, toastMsg]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useStore() {
  const s = useContext(Ctx);
  if (!s) throw new Error("useStore fuera de StoreProvider");
  return s;
}

/** Crea o actualiza el cliente y deja la sesión abierta. */
export function upsertUser(s: State, u: Omit<User, "terms" | "avatar">): State {
  const email = u.email.trim().toLowerCase();
  const prev = s.users[email];
  return {
    ...s,
    session: email,
    users: { ...s.users, [email]: { ...prev, ...u, email, terms: prev?.terms ?? Date.now() } },
  };
}
