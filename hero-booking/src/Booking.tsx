import { useEffect, useMemo, useState } from "react";
import { CalendarCheck, ChevronLeft, ChevronRight, Clock, Lock, Scissors } from "lucide-react";
import { useActions } from "./actions";
import { DAY_SHORT, HOURS, MONTHS, SERVICES, clp, hh, iso, isPast, mondayOf, niceDate, parseIso, svc, weekdayIdx } from "./data";
import { upsertUser, useStore } from "./store";
import { Check, DeepShadowButton, Field, GhostButton, Modal, SectionHead, inputCls } from "./ui";

// ---------------------------------------------------------------------------
// Servicios
// ---------------------------------------------------------------------------

export function Services() {
  const { pickDay } = useActions();
  return (
    <section className="mx-auto max-w-[1200px] px-4 py-20 sm:px-8" aria-labelledby="servicios">
      <SectionHead id="servicios" eyebrow="Precios con IVA · pagas en la barbería" title="Servicios" />
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {SERVICES.map((s, i) => (
          <article
            key={s.id}
            className={`flex flex-col justify-between gap-6 rounded-3xl border p-6 ${
              i === 1 ? "border-white/40 bg-white/[0.04]" : "border-line bg-card"
            }`}
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                {i === 1 && (
                  <span className="mb-3 inline-block rounded-full bg-white px-2.5 py-1 font-wide text-[9px] tracking-wider text-[#0B0B0C]">
                    MÁS PEDIDO
                  </span>
                )}
                <h3 className="text-lg font-semibold text-white">{s.name}</h3>
                <p className="mt-1 text-sm text-muted">{s.desc}</p>
              </div>
              <Scissors className="size-5 shrink-0 text-line-2" />
            </div>
            <div className="flex items-end justify-between gap-4">
              <div>
                <p className="font-heading text-4xl leading-none text-white tabular-nums">{clp(s.price)}</p>
                <p className="mt-1 flex items-center gap-1 text-xs text-muted">
                  <Clock className="size-3" /> {s.minutes} min · bloque de 1 hora
                </p>
              </div>
              <GhostButton onClick={() => pickDay(null, s.id)} className="px-4 py-2">
                Reservar
              </GhostButton>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Agenda
// ---------------------------------------------------------------------------

function firstBookableDay() {
  const d = new Date();
  for (let i = 0; i < 14; i++) {
    const x = new Date(d.getFullYear(), d.getMonth(), d.getDate() + i);
    const date = iso(x);
    if (weekdayIdx(x) >= 0 && HOURS.some((h) => !isPast(date, h))) return date;
  }
  return iso(d);
}

const MAX_WEEKS = 4;

export function Agenda() {
  const { state } = useStore();
  const { agendaDate, pickDay, agendaService, setAgendaService } = useActions();
  const selDate = agendaDate ?? firstBookableDay();
  const [pending, setPending] = useState<{ date: string; hour: number } | null>(null);

  const thisMonday = mondayOf(new Date());
  const selMonday = mondayOf(parseIso(selDate));
  const weekOffset = Math.round((selMonday.getTime() - thisMonday.getTime()) / (7 * 864e5));

  const days = useMemo(
    () =>
      Array.from({ length: 6 }).map((_, i) => {
        const d = new Date(selMonday);
        d.setDate(selMonday.getDate() + i);
        const date = iso(d);
        const taken = new Set(state.bookings.filter((b) => b.date === date).map((b) => b.hour));
        const free = HOURS.filter((h) => !taken.has(h) && !isPast(date, h)).length;
        return { d, date, free, past: HOURS.every((h) => isPast(date, h)) };
      }),
    [selMonday.getTime(), state.bookings] // eslint-disable-line react-hooks/exhaustive-deps
  );

  const shiftWeek = (n: number) => {
    const d = new Date(selMonday);
    d.setDate(d.getDate() + n * 7);
    const firstOpen = Array.from({ length: 6 })
      .map((_, i) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + i))
      .find((x) => HOURS.some((h) => !isPast(iso(x), h)));
    pickDay(iso(firstOpen ?? d));
  };

  const taken = new Map(state.bookings.filter((b) => b.date === selDate).map((b) => [b.hour, b]));
  const monthLabel = MONTHS[selMonday.getMonth()];

  return (
    <section className="mx-auto max-w-[1200px] px-4 py-20 sm:px-8" aria-labelledby="agenda">
      <SectionHead
        id="agenda"
        eyebrow={`Agenda · ${monthLabel}`}
        title="Reserva tu hora"
        right={
          <div className="flex items-center gap-2">
            <button
              type="button"
              aria-label="Semana anterior"
              disabled={weekOffset <= 0}
              onClick={() => shiftWeek(-1)}
              className="grid size-10 place-items-center rounded-full border border-line-2 text-white disabled:opacity-30"
            >
              <ChevronLeft className="size-4" />
            </button>
            <span className="min-w-28 text-center text-xs text-muted tabular-nums">
              {weekOffset === 0 ? "Esta semana" : weekOffset === 1 ? "Próxima semana" : `En ${weekOffset} semanas`}
            </span>
            <button
              type="button"
              aria-label="Semana siguiente"
              disabled={weekOffset >= MAX_WEEKS - 1}
              onClick={() => shiftWeek(1)}
              className="grid size-10 place-items-center rounded-full border border-line-2 text-white disabled:opacity-30"
            >
              <ChevronRight className="size-4" />
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-3 gap-2 sm:grid-cols-6">
        {days.map(({ d, date, free, past }, i) => {
          const on = date === selDate;
          return (
            <button
              key={date}
              type="button"
              disabled={past}
              onClick={() => pickDay(date)}
              className={`flex flex-col items-center gap-1 rounded-2xl border px-2 py-3 transition-colors disabled:opacity-30 ${
                on ? "border-white bg-white text-[#0B0B0C]" : "border-line bg-card text-white hover:border-line-2"
              }`}
            >
              <span className="font-wide text-[10px] tracking-wider">{DAY_SHORT[i]}</span>
              <span className="font-heading text-3xl leading-none tabular-nums">{d.getDate()}</span>
              <span className={`text-[11px] ${on ? "text-[#0B0B0C]/70" : "text-muted"}`}>
                {past ? "Pasado" : free === 0 ? "Completo" : `${free} libres`}
              </span>
            </button>
          );
        })}
      </div>

      <div className="relative mt-6 rounded-3xl border border-line bg-card p-5 sm:p-6">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-base font-semibold text-white">{niceDate(selDate)}</p>
            <p className="text-xs text-muted">Toca una hora libre para reservar</p>
          </div>
          <label className="flex items-center gap-2 text-xs text-muted">
            Servicio
            <select
              id="agenda-service"
              value={agendaService}
              onChange={(e) => setAgendaService(e.target.value)}
              className={`${inputCls} w-auto py-2`}
            >
              {SERVICES.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} · {clp(s.price)}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="grid grid-cols-3 gap-2 sm:grid-cols-5 lg:grid-cols-9">
          {HOURS.map((h) => {
            const b = taken.get(h);
            const past = isPast(selDate, h);
            const mine = b && state.session === b.email;
            const disabled = !!b || past || !state.open;
            return (
              <button
                key={h}
                type="button"
                disabled={disabled}
                onClick={() => setPending({ date: selDate, hour: h })}
                className={`flex flex-col items-center rounded-xl border px-2 py-3 text-sm tabular-nums transition-colors ${
                  mine
                    ? "border-white bg-white text-[#0B0B0C]"
                    : b
                      ? "border-line bg-bg text-muted line-through decoration-muted/60"
                      : past
                        ? "border-line bg-bg text-muted/40"
                        : "border-line-2 text-white hover:border-white hover:bg-white hover:text-[#0B0B0C]"
                }`}
              >
                <span className="font-semibold">{hh(h)}</span>
                <span className="text-[10px] no-underline opacity-70">
                  {mine ? "Tu hora" : b ? "Ocupada" : past ? "—" : "Libre"}
                </span>
              </button>
            );
          })}
        </div>

        {!state.open && (
          <div className="absolute inset-0 grid place-items-center rounded-3xl bg-bg/85 p-6 text-center backdrop-blur-sm">
            <div className="flex max-w-sm flex-col items-center gap-3">
              <Lock className="size-6 text-white" />
              <p className="font-heading text-3xl uppercase text-white">Agenda cerrada</p>
              <p className="text-sm text-muted">
                El barbero pausó las reservas online. Puedes apartar productos igual, o vuelve más tarde.
              </p>
            </div>
          </div>
        )}
      </div>

      <BookModal pending={pending} onClose={() => setPending(null)} />
    </section>
  );
}

// ---------------------------------------------------------------------------
// Modal de reserva
// ---------------------------------------------------------------------------

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const phoneOk = (p: string) => p.replace(/\D/g, "").length >= 8;

function BookModal({ pending, onClose }: { pending: { date: string; hour: number } | null; onClose: () => void }) {
  const { state, update, me, toast } = useStore();
  const { openTerms, goTo, agendaService, setAgendaService } = useActions();
  const [f, setF] = useState({ name: "", phone: "", email: "", terms: false, mkEmail: false, mkSms: false });
  const [tried, setTried] = useState(false);
  const [done, setDone] = useState<null | { date: string; hour: number; service: string }>(null);

  useEffect(() => {
    if (pending) {
      setTried(false);
      setDone(null);
    }
  }, [pending]);

  const s = svc(agendaService);
  const errs = me
    ? {}
    : {
        name: f.name.trim().length < 2,
        phone: !phoneOk(f.phone),
        email: !EMAIL_RE.test(f.email.trim()),
        terms: !f.terms,
      };
  const invalid = Object.values(errs).some(Boolean);

  const confirm = () => {
    if (!pending) return;
    setTried(true);
    if (invalid) return;
    if (!state.open) return toast("La agenda está cerrada");
    if (state.bookings.some((b) => b.date === pending.date && b.hour === pending.hour)) {
      toast("Esa hora se acaba de ocupar, elige otra");
      return onClose();
    }
    update((st) => {
      const next = me
        ? st
        : upsertUser(st, { name: f.name.trim(), phone: f.phone.trim(), email: f.email, mkEmail: f.mkEmail, mkSms: f.mkSms });
      const email = next.session!;
      return {
        ...next,
        bookings: [...next.bookings, { id: "b" + Date.now(), date: pending.date, hour: pending.hour, service: s.id, email }],
      };
    });
    setDone({ date: pending.date, hour: pending.hour, service: s.id });
    toast("Hora reservada");
  };

  const open = !!pending;
  return (
    <Modal
      open={open}
      onClose={onClose}
      title={done ? "Hora confirmada" : "Reservar"}
      subtitle={done ? "Te esperamos. Llega 5 minutos antes." : "Tus datos quedan guardados para la próxima."}
    >
      {pending && !done && (
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between rounded-2xl bg-white p-4 text-[#0B0B0C]">
            <div>
              <p className="text-xs font-medium opacity-70">{niceDate(pending.date)}</p>
              <p className="font-heading text-3xl leading-none tabular-nums">
                {hh(pending.hour)} – {hh(pending.hour + 1)}
              </p>
            </div>
            <div className="text-right">
              <p className="text-xs font-medium opacity-70">Total</p>
              <p className="font-heading text-3xl leading-none tabular-nums">{clp(s.price)}</p>
            </div>
          </div>

          <Field label="Servicio">
            <select id="book-service" value={s.id} onChange={(e) => setAgendaService(e.target.value)} className={inputCls}>
              {SERVICES.map((x) => (
                <option key={x.id} value={x.id}>
                  {x.name} · {clp(x.price)}
                </option>
              ))}
            </select>
          </Field>

          {me ? (
            <div className="flex items-center justify-between gap-3 rounded-2xl border border-line p-4 text-sm">
              <div>
                <p className="font-semibold text-white">{me.name}</p>
                <p className="text-xs text-muted">
                  {me.phone} · {me.email}
                </p>
              </div>
              <button
                type="button"
                className="text-xs text-muted underline hover:text-white"
                onClick={() => update((st) => ({ ...st, session: null }))}
              >
                No soy yo
              </button>
            </div>
          ) : (
            <>
              <Field label="Nombre">
                <input
                  id="book-name"
                  className={inputCls}
                  autoComplete="name"
                  placeholder="Ej: Matías Rojas"
                  value={f.name}
                  aria-invalid={tried && errs.name}
                  onChange={(e) => setF({ ...f, name: e.target.value })}
                />
              </Field>
              <Field label="Teléfono (WhatsApp)">
                <input
                  id="book-phone"
                  className={inputCls}
                  type="tel"
                  autoComplete="tel"
                  placeholder="+56 9 1234 5678"
                  value={f.phone}
                  aria-invalid={tried && errs.phone}
                  onChange={(e) => setF({ ...f, phone: e.target.value })}
                />
              </Field>
              <Field label="Correo">
                <input
                  id="book-email"
                  className={inputCls}
                  type="email"
                  autoComplete="email"
                  placeholder="tu@correo.com"
                  value={f.email}
                  aria-invalid={tried && errs.email}
                  onChange={(e) => setF({ ...f, email: e.target.value })}
                />
              </Field>
              <div className="flex flex-col gap-2">
                <Check id="book-terms" checked={f.terms} invalid={tried && errs.terms} onChange={(v) => setF({ ...f, terms: v })}>
                  <b className="text-white">*</b> Acepto los{" "}
                  <button type="button" className="underline hover:text-white" onClick={openTerms}>
                    Términos y la Política de Privacidad
                  </button>{" "}
                  de Marcut's Barber.
                </Check>
                <Check id="book-mk-email" checked={f.mkEmail} onChange={(v) => setF({ ...f, mkEmail: v })}>
                  Quiero recibir promociones y novedades por <b className="text-white">correo</b>.
                </Check>
                <Check id="book-mk-sms" checked={f.mkSms} onChange={(v) => setF({ ...f, mkSms: v })}>
                  Quiero recibir recordatorios y ofertas por <b className="text-white">WhatsApp / SMS</b>.
                </Check>
              </div>
              {tried && invalid && (
                <p className="text-xs text-[#ff6b6b]">
                  Revisa los campos marcados. El nombre, un teléfono de al menos 8 dígitos, un correo válido y aceptar los términos son obligatorios.
                </p>
              )}
            </>
          )}

          <div className="flex justify-end gap-3 pt-2">
            <GhostButton onClick={onClose}>Cancelar</GhostButton>
            <DeepShadowButton onClick={confirm}>
              <CalendarCheck className="size-4" />
              Confirmar hora
            </DeepShadowButton>
          </div>
        </div>
      )}

      {done && (
        <div className="flex flex-col gap-4">
          <div className="rounded-2xl border border-line p-4 text-sm">
            <p className="font-heading text-3xl uppercase leading-none text-white">{niceDate(done.date)}</p>
            <p className="mt-2 text-muted tabular-nums">
              {hh(done.hour)} – {hh(done.hour + 1)} · {svc(done.service).name} · {clp(svc(done.service).price)}
            </p>
          </div>
          <p className="text-xs text-muted">Puedes cancelar sin costo desde "Mis citas" hasta 3 horas antes.</p>
          <div className="flex justify-end gap-3">
            <GhostButton
              onClick={() => {
                onClose();
                goTo("mis-citas");
              }}
            >
              Ver mis citas
            </GhostButton>
            <DeepShadowButton onClick={onClose}>Listo</DeepShadowButton>
          </div>
        </div>
      )}
    </Modal>
  );
}
