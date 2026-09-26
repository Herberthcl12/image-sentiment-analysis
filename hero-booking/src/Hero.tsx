import { useMemo, useRef, useState } from "react";
import { motion, useAnimationFrame, useMotionValue } from "motion/react";
import { ArrowDown, CalendarCheck, Scissors } from "lucide-react";
import { useActions } from "./actions";
import { DAY_SHORT, HOURS, MONTHS_SHORT, hh, iso, isPast, publicName, svc, weekdayIdx } from "./data";
import { useStore, type State } from "./store";
import { AvatarWithShadow, DeepShadowAvatar, DeepShadowButton, DeepShadowIcon, Eyebrow, GhostButton, Stars } from "./ui";

// ---------------------------------------------------------------------------
// Datos para la marquesina: próximas reservas agrupadas por día
// ---------------------------------------------------------------------------

interface CallItem {
  name: string;
  avatar?: string;
  time: string;
  duration: string;
}

interface ClientCall {
  id: string;
  date: string;
  day: string;
  dateLabel: string;
  items: CallItem[];
  free: number;
}

function upcomingCalls(state: State): ClientCall[] {
  const out: ClientCall[] = [];
  const cursor = new Date();
  for (let i = 0; out.length < 6 && i < 21; i++) {
    const d = new Date(cursor.getFullYear(), cursor.getMonth(), cursor.getDate() + i);
    const wd = weekdayIdx(d);
    if (wd < 0) continue;
    const date = iso(d);
    const futureHours = HOURS.filter((h) => !isPast(date, h));
    if (futureHours.length === 0) continue;
    const dayBookings = state.bookings
      .filter((b) => b.date === date && futureHours.includes(b.hour))
      .sort((a, b) => a.hour - b.hour);
    if (dayBookings.length === 0) continue;
    out.push({
      id: date,
      date,
      day: DAY_SHORT[wd],
      dateLabel: `${d.getDate()} ${MONTHS_SHORT[d.getMonth()]}`,
      free: futureHours.length - dayBookings.length,
      items: dayBookings.slice(0, 2).map((b) => {
        const u = state.users[b.email];
        return {
          name: u ? publicName(u.name) : "Cliente",
          avatar: u?.avatar,
          time: `${hh(b.hour)} – ${hh(b.hour + 1)}`,
          duration: `${svc(b.service).minutes} min`,
        };
      }),
    });
  }
  return out;
}

function ClientCard({ call, index, onPick }: { call: ClientCall; index: number; onPick: (date: string) => void }) {
  return (
    <motion.button
      type="button"
      onClick={() => onPick(call.date)}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay: (index % 6) * 0.08 }}
      className={`${index % 2 === 0 ? "rotate-3" : "-rotate-3"} mx-auto block w-full max-w-sm rounded-3xl border border-line bg-card p-5 text-left shadow-[0_4px_20px_rgba(0,0,0,0.4)] transition-colors hover:border-white/40`}
      aria-label={`Ver agenda del ${call.day} ${call.dateLabel}`}
    >
      <div className="mb-2 flex items-center justify-between font-wide text-[11px] tracking-wider">
        <span className="text-white">{call.day}</span>
        <span className="text-muted">{call.dateLabel}</span>
      </div>
      <div className="flex flex-col">
        {call.items.map((item, i) => (
          <div key={i} className="flex items-center gap-3 border-b border-dotted border-line-2 py-3 last:border-b-0">
            <AvatarWithShadow src={item.avatar} name={item.name} />
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-white">{item.name}</p>
              <p className="text-xs tabular-nums text-muted">{item.time}</p>
            </div>
            <span className="rounded-full bg-bg px-2.5 py-1 text-xs font-medium tabular-nums text-muted">{item.duration}</span>
          </div>
        ))}
      </div>
      <div className="mt-2 flex items-center justify-between border-t border-line pt-3 text-xs">
        <span className="text-muted">{call.free > 0 ? `${call.free} ${call.free === 1 ? "hora libre" : "horas libres"}` : "Día completo"}</span>
        <span className="font-semibold text-white">{call.free > 0 ? "Ver horas →" : "Ver agenda →"}</span>
      </div>
    </motion.button>
  );
}

/** Pista vertical infinita que se pausa al pasar el mouse. */
function Track({
  calls,
  offset = 0,
  onPick,
  className = "",
}: {
  calls: ClientCall[];
  offset?: number;
  onPick: (date: string) => void;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const y = useMotionValue(0);
  const [paused, setPaused] = useState(false);
  const looped = useMemo(() => [...calls, ...calls, ...calls], [calls]);

  useAnimationFrame((_, delta) => {
    const el = ref.current;
    if (!el || paused) return;
    const third = el.scrollHeight / 3;
    if (third === 0) return;
    // ~30 px por segundo, equivalente al recorrido de 1200 px en 40 s
    let next = y.get() - (delta / 1000) * 30;
    if (next <= -third - offset) next += third;
    if (next > -offset) next = -offset;
    y.set(next);
  });

  return (
    <motion.div
      ref={ref}
      style={{ y }}
      className={`flex flex-col gap-6 py-6 ${className}`}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={() => setPaused(false)}
    >
      {looped.map((call, i) => (
        <ClientCard key={`${call.id}-${i}`} call={call} index={i} onPick={onPick} />
      ))}
    </motion.div>
  );
}

export default function Hero() {
  const { state } = useStore();
  const { goTo, pickDay } = useActions();
  const calls = useMemo(() => upcomingCalls(state), [state]);

  const avg = state.reviews.length ? state.reviews.reduce((a, r) => a + r.stars, 0) / state.reviews.length : 0;
  const faces = Object.values(state.users).filter((u) => u.avatar).slice(0, 4);

  const onPick = (date: string) => pickDay(date);
  const todayWd = weekdayIdx(new Date());

  return (
    <main
      id="inicio"
      className="scroll-mt-32 mx-auto grid max-w-[1440px] grid-cols-1 gap-12 px-4 py-12 sm:px-8 lg:h-[calc(100vh-88px)] lg:min-h-[680px] lg:grid-cols-[1.2fr_0.8fr] lg:px-16 lg:py-0"
    >
      {/* Propuesta */}
      <section className="flex flex-col justify-center gap-8 lg:py-16">
        <button
          type="button"
          onClick={() => goTo("agenda")}
          className={`inline-flex w-fit items-center gap-2 rounded-full border px-3 py-1.5 ${
            state.open ? "border-white/30 bg-white/5" : "border-line-2 bg-card"
          }`}
        >
          <span
            className={`size-2 rounded-full ${
              state.open ? "animate-pulse bg-white shadow-[0_0_8px_rgba(255,255,255,0.8)]" : "bg-[#55555c]"
            }`}
          />
          <span className={`font-wide text-[10px] uppercase tracking-[0.14em] ${state.open ? "text-white" : "text-muted"}`}>
            {state.open ? "Agenda abierta · Lun–Sáb 12–21" : "Agenda cerrada por hoy"}
          </span>
        </button>

        <h1 className="font-heading text-[clamp(3.25rem,9vw,7.5rem)] uppercase leading-[0.9] tracking-[-0.01em] text-balance">
          <span className="text-chrome">Elige tu hora</span>{" "}
          <DeepShadowIcon className="mx-1 -translate-y-2 -rotate-6">
            <Scissors className="size-8 text-[#0B0B0C] sm:size-12" strokeWidth={2.5} />
          </DeepShadowIcon>{" "}
          <br className="hidden sm:block" />
          <span className="text-outline">y llega directo</span> <span className="text-chrome">a la silla</span>
        </h1>

        <p className="max-w-xl text-lg leading-relaxed text-muted">
          Fade, barba y diseño de lunes a sábado, de 12:00 a 21:00. Bloques de 1 hora, sin escribir por WhatsApp. Aparta tus
          productos y pagas al llegar.
        </p>

        <div className="flex flex-wrap items-center gap-4 sm:gap-6">
          <DeepShadowButton onClick={() => pickDay(null)}>
            <CalendarCheck className="size-4" />
            Reservar hora
          </DeepShadowButton>
          <GhostButton onClick={() => goTo("servicios")}>
            <ArrowDown className="size-4" />
            Ver servicios y precios
          </GhostButton>
        </div>

        <div className="flex flex-col gap-8 pt-2 sm:flex-row sm:items-center sm:gap-10">
          <button type="button" onClick={() => goTo("resenas")} className="flex flex-col gap-4 text-left">
            <Eyebrow>Clientes de la semana</Eyebrow>
            <span className="flex items-center -space-x-2">
              {faces.map((u, i) => (
                <DeepShadowAvatar key={u.email} src={u.avatar} name={u.name} size={i % 2 === 0 ? "md" : "lg"} hasGlow={i === 1} />
              ))}
            </span>
          </button>

          <div className="hidden h-16 w-px bg-line-2 sm:block" />

          <button type="button" onClick={() => goTo("resenas")} className="flex flex-col gap-4 text-left">
            <Eyebrow>
              {avg.toFixed(1)}/5 · {state.reviews.length} reseñas
            </Eyebrow>
            <Stars n={avg} className="size-5" />
          </button>
        </div>
      </section>

      {/* Marquesina de próximas reservas */}
      <section aria-label="Próximas reservas" className="relative h-[600px] overflow-hidden lg:h-full">
        <div className="pointer-events-none absolute inset-x-0 top-0 z-10 h-20 bg-gradient-to-b from-bg to-transparent sm:h-40" />
        <div className="pointer-events-none absolute inset-x-0 bottom-0 z-10 h-20 bg-gradient-to-t from-bg to-transparent sm:h-40" />
        <div className="absolute left-1/2 top-4 z-20 -translate-x-1/2">
          <Eyebrow className="rounded-full border border-line bg-bg/80 px-3 py-1.5 backdrop-blur">
            {todayWd < 0 ? "Próximas reservas" : "Reservas en vivo"}
          </Eyebrow>
        </div>

        {calls.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 px-2 md:grid-cols-2 lg:grid-cols-1">
            <Track calls={calls} onPick={onPick} />
            <Track calls={[...calls].reverse()} offset={0} onPick={onPick} className="hidden md:flex lg:hidden" />
          </div>
        ) : (
          <div className="grid h-full place-items-center text-center text-sm text-muted">
            Agenda libre esta semana. Toma la primera hora.
          </div>
        )}
      </section>
    </main>
  );
}

