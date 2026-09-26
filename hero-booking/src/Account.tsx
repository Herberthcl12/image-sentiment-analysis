import { useEffect, useState } from "react";
import { CalendarX, LogIn, LogOut } from "lucide-react";
import { useActions } from "./actions";
import { PRODUCTS, clp, hh, isPast, niceDate, svc } from "./data";
import { upsertUser, useStore } from "./store";
import { Check, DeepShadowButton, Field, GhostButton, Modal, SectionHead, inputCls } from "./ui";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// ---------------------------------------------------------------------------
// Login
// ---------------------------------------------------------------------------

export function LoginModal({ open, onClose, onDone }: { open: boolean; onClose: () => void; onDone: () => void }) {
  const { state, update, toast } = useStore();
  const { openTerms } = useActions();
  const [f, setF] = useState({ name: "", phone: "", email: "", terms: false, mkEmail: false, mkSms: false });
  const [tried, setTried] = useState(false);

  useEffect(() => {
    if (open) setTried(false);
  }, [open]);

  // Si el correo ya existe, se completan sus datos y permisos guardados.
  const known = state.users[f.email.trim().toLowerCase()];
  const errs = {
    name: !known && f.name.trim().length < 2,
    phone: !known && f.phone.replace(/\D/g, "").length < 8,
    email: !EMAIL_RE.test(f.email.trim()),
    terms: !known && !f.terms,
  };
  const invalid = Object.values(errs).some(Boolean);

  const submit = () => {
    setTried(true);
    if (invalid) return;
    if (known) {
      update((s) => ({ ...s, session: known.email }));
      toast(`Hola de nuevo, ${known.name.split(" ")[0]}`);
    } else {
      update((s) => upsertUser(s, { name: f.name.trim(), phone: f.phone.trim(), email: f.email, mkEmail: f.mkEmail, mkSms: f.mkSms }));
      toast("Cuenta creada");
    }
    setF({ name: "", phone: "", email: "", terms: false, mkEmail: false, mkSms: false });
    onDone();
  };

  return (
    <Modal open={open} onClose={onClose} title="Iniciar sesión" subtitle="Sin contraseña: te identificamos por tu correo.">
      <div className="flex flex-col gap-4">
        <Field label="Correo">
          <input
            id="login-email"
            className={inputCls}
            type="email"
            autoComplete="email"
            placeholder="tu@correo.com"
            value={f.email}
            aria-invalid={tried && errs.email}
            onChange={(e) => setF({ ...f, email: e.target.value })}
          />
        </Field>
        {known ? (
          <p className="rounded-2xl border border-line p-4 text-sm text-muted">
            Encontramos tu cuenta: <b className="text-white">{known.name}</b> · {known.phone}
          </p>
        ) : (
          <>
            <Field label="Nombre">
              <input
                id="login-name"
                className={inputCls}
                autoComplete="name"
                value={f.name}
                aria-invalid={tried && errs.name}
                onChange={(e) => setF({ ...f, name: e.target.value })}
              />
            </Field>
            <Field label="Teléfono (WhatsApp)">
              <input
                id="login-phone"
                className={inputCls}
                type="tel"
                autoComplete="tel"
                placeholder="+56 9 1234 5678"
                value={f.phone}
                aria-invalid={tried && errs.phone}
                onChange={(e) => setF({ ...f, phone: e.target.value })}
              />
            </Field>
            <div className="flex flex-col gap-2">
              <Check id="login-terms" checked={f.terms} invalid={tried && errs.terms} onChange={(v) => setF({ ...f, terms: v })}>
                <b className="text-white">*</b> Acepto los{" "}
                <button type="button" className="underline hover:text-white" onClick={openTerms}>
                  Términos y la Política de Privacidad
                </button>
                .
              </Check>
              <Check id="login-mk-email" checked={f.mkEmail} onChange={(v) => setF({ ...f, mkEmail: v })}>
                Acepto marketing por <b className="text-white">correo</b>.
              </Check>
              <Check id="login-mk-sms" checked={f.mkSms} onChange={(v) => setF({ ...f, mkSms: v })}>
                Acepto marketing por <b className="text-white">WhatsApp / SMS</b>.
              </Check>
            </div>
          </>
        )}
        {tried && invalid && <p className="text-xs text-[#ff6b6b]">Completa los campos marcados.</p>}
        <p className="text-xs text-muted">Demo: prueba con benja@demo.cl para entrar a una cuenta con historial.</p>
        <div className="flex justify-end gap-3">
          <GhostButton onClick={onClose}>Cancelar</GhostButton>
          <DeepShadowButton onClick={submit}>
            <LogIn className="size-4" />
            Entrar
          </DeepShadowButton>
        </div>
      </div>
    </Modal>
  );
}

// ---------------------------------------------------------------------------
// Mis citas
// ---------------------------------------------------------------------------

export function MyAppointments() {
  const { state, update, me, toast } = useStore();
  const { openLogin, ask, pickDay, goTo } = useActions();

  if (!me) {
    return (
      <section className="mx-auto max-w-[1200px] px-4 py-20 sm:px-8" aria-labelledby="mis-citas">
        <SectionHead id="mis-citas" eyebrow="Tu cuenta" title="Mis citas" />
        <div className="flex flex-col items-start gap-4 rounded-3xl border border-line bg-card p-6 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-muted">Inicia sesión con tu correo para ver, cancelar o repetir tus horas.</p>
          <DeepShadowButton onClick={() => openLogin(() => goTo("mis-citas"))}>
            <LogIn className="size-4" />
            Iniciar sesión
          </DeepShadowButton>
        </div>
      </section>
    );
  }

  const mine = state.bookings.filter((b) => b.email === me.email).sort((a, b) => (a.date + hh(a.hour)).localeCompare(b.date + hh(b.hour)));
  const upcoming = mine.filter((b) => !isPast(b.date, b.hour));
  const past = mine.filter((b) => isPast(b.date, b.hour)).reverse().slice(0, 4);
  const held = (state.held[me.email] ?? []).map((id) => PRODUCTS.find((p) => p.id === id)!).filter(Boolean);

  const cancel = (id: string, label: string) =>
    ask("¿Cancelar esta hora?", label, () => {
      update((s) => ({ ...s, bookings: s.bookings.filter((b) => b.id !== id) }));
      toast("Hora cancelada");
    });

  const setPref = (k: "mkEmail" | "mkSms", v: boolean) =>
    update((s) => ({ ...s, users: { ...s.users, [me.email]: { ...s.users[me.email], [k]: v } } }));

  return (
    <section className="mx-auto max-w-[1200px] px-4 py-20 sm:px-8" aria-labelledby="mis-citas">
      <SectionHead
        id="mis-citas"
        eyebrow={`${me.name} · ${me.phone}`}
        title="Mis citas"
        right={
          <GhostButton
            onClick={() => {
              update((s) => ({ ...s, session: null }));
              toast("Sesión cerrada");
            }}
          >
            <LogOut className="size-4" />
            Cerrar sesión
          </GhostButton>
        }
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_340px]">
        <div className="flex flex-col gap-3">
          <p className="text-xs font-medium uppercase tracking-wider text-muted">Próximas</p>
          {upcoming.length === 0 && (
            <div className="flex flex-wrap items-center justify-between gap-3 rounded-3xl border border-dashed border-line-2 p-5 text-sm text-muted">
              No tienes horas agendadas.
              <GhostButton className="px-4 py-2" onClick={() => pickDay(null)}>
                Reservar hora
              </GhostButton>
            </div>
          )}
          {upcoming.map((b) => {
            const s = svc(b.service);
            const label = `${niceDate(b.date)} · ${hh(b.hour)} · ${s.name}`;
            return (
              <article key={b.id} className="flex flex-wrap items-center justify-between gap-4 rounded-3xl border border-line bg-card p-5">
                <div>
                  <p className="font-heading text-2xl uppercase leading-none text-white">{niceDate(b.date)}</p>
                  <p className="mt-1.5 text-sm text-muted tabular-nums">
                    {hh(b.hour)} – {hh(b.hour + 1)} · {s.name} · {clp(s.price)}
                  </p>
                </div>
                <GhostButton className="px-4 py-2" onClick={() => cancel(b.id, label)}>
                  <CalendarX className="size-4" />
                  Cancelar
                </GhostButton>
              </article>
            );
          })}

          {past.length > 0 && (
            <>
              <p className="mt-4 text-xs font-medium uppercase tracking-wider text-muted">Historial</p>
              {past.map((b) => (
                <div key={b.id} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-line px-5 py-3 text-sm text-muted">
                  <span className="tabular-nums">
                    {niceDate(b.date)} · {hh(b.hour)} · {svc(b.service).name}
                  </span>
                  <button type="button" className="text-xs text-white underline" onClick={() => pickDay(null, b.service)}>
                    Repetir
                  </button>
                </div>
              ))}
            </>
          )}
        </div>

        <aside className="flex flex-col gap-4">
          <div className="rounded-3xl border border-line bg-card p-5">
            <p className="mb-3 text-xs font-medium uppercase tracking-wider text-muted">Productos apartados</p>
            {held.length === 0 ? (
              <p className="text-sm text-muted">Nada apartado todavía.</p>
            ) : (
              <ul className="flex flex-col gap-2 text-sm">
                {held.map((p) => (
                  <li key={p.id} className="flex items-center justify-between gap-3">
                    <span className="text-white">{p.name}</span>
                    <span className="flex items-center gap-3 tabular-nums text-muted">
                      {clp(p.price)}
                      <button
                        type="button"
                        aria-label={`Quitar ${p.name}`}
                        className="text-xs underline hover:text-white"
                        onClick={() => update((s) => ({ ...s, held: { ...s.held, [me.email]: (s.held[me.email] ?? []).filter((x) => x !== p.id) } }))}
                      >
                        Quitar
                      </button>
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="flex flex-col gap-2 rounded-3xl border border-line bg-card p-5">
            <p className="mb-1 text-xs font-medium uppercase tracking-wider text-muted">Tus permisos de marketing</p>
            <Check id="pref-email" checked={me.mkEmail} onChange={(v) => setPref("mkEmail", v)}>
              Promociones por correo
            </Check>
            <Check id="pref-sms" checked={me.mkSms} onChange={(v) => setPref("mkSms", v)}>
              Recordatorios y ofertas por WhatsApp / SMS
            </Check>
            <p className="text-[11px] text-muted">Puedes cambiarlos cuando quieras. Los recordatorios de tu hora llegan igual.</p>
          </div>
        </aside>
      </div>
    </section>
  );
}
