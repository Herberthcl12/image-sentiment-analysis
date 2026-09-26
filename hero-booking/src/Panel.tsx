import { useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, Copy, Lock, LogOut, RotateCcw, Unlock } from "lucide-react";
import { useActions } from "./actions";
import { ADMIN_PIN, HOURS, clp, hh, iso, mondayOf, niceDate, parseIso, svc } from "./data";
import { useStore } from "./store";
import { DeepShadowButton, Eyebrow, GhostButton, Modal, SectionHead, inputCls } from "./ui";

function Yes({ on }: { on: boolean }) {
  return <span className={on ? "text-white" : "text-muted/50"}>{on ? "Sí" : "No"}</span>;
}

export function Panel() {
  const { state, update, reset, toast } = useStore();
  const { ask } = useActions();
  const [unlocked, setUnlocked] = useState(false);
  const [pin, setPin] = useState("");
  const [pinErr, setPinErr] = useState(false);
  const [day, setDay] = useState(iso(new Date()));
  const [csvOpen, setCsvOpen] = useState(false);

  const today = iso(new Date());
  const monday = mondayOf(new Date());
  const weekDates = Array.from({ length: 6 }).map((_, i) => iso(new Date(monday.getFullYear(), monday.getMonth(), monday.getDate() + i)));

  const kpis = useMemo(() => {
    const week = state.bookings.filter((b) => weekDates.includes(b.date));
    const users = Object.values(state.users);
    return [
      { label: "Reservas hoy", value: String(state.bookings.filter((b) => b.date === today).length), note: `de ${HOURS.length} bloques` },
      { label: "Reservas semana", value: String(week.length), note: `${Math.round((week.length / (HOURS.length * 6)) * 100)}% ocupación` },
      { label: "Ingreso estimado semana", value: clp(week.reduce((a, b) => a + svc(b.service).price, 0)), note: "servicios, sin productos" },
      { label: "Clientes con permiso", value: `${users.filter((u) => u.mkEmail || u.mkSms).length}/${users.length}`, note: "correo o WhatsApp" },
    ];
  }, [state, today]); // eslint-disable-line react-hooks/exhaustive-deps

  const csv = useMemo(() => {
    const rows = [["nombre", "telefono", "correo", "reservas", "mk_correo", "mk_whatsapp", "acepto_terminos"]];
    Object.values(state.users).forEach((u) =>
      rows.push([
        u.name,
        u.phone,
        u.email,
        String(state.bookings.filter((b) => b.email === u.email).length),
        u.mkEmail ? "si" : "no",
        u.mkSms ? "si" : "no",
        new Date(u.terms).toISOString().slice(0, 10),
      ])
    );
    return rows.map((r) => r.map((c) => `"${c.replace(/"/g, '""')}"`).join(",")).join("\n");
  }, [state]);

  const unlock = () => {
    if (pin === ADMIN_PIN) {
      setUnlocked(true);
      setPin("");
      setPinErr(false);
    } else {
      setPinErr(true);
      toast("PIN incorrecto");
    }
  };

  const shiftDay = (n: number) => {
    const d = parseIso(day);
    d.setDate(d.getDate() + n);
    if (d.getDay() === 0) d.setDate(d.getDate() + n);
    setDay(iso(d));
  };

  if (!unlocked) {
    return (
      <section className="mx-auto max-w-[1200px] px-4 py-20 sm:px-8" aria-labelledby="panel">
        <SectionHead id="panel" eyebrow="Solo para el barbero" title="Panel" />
        <form
          className="flex max-w-md flex-col gap-4 rounded-3xl border border-line bg-card p-6"
          onSubmit={(e) => {
            e.preventDefault();
            unlock();
          }}
        >
          <p className="text-sm text-muted">Ingresa el PIN para abrir o cerrar la agenda y ver clientes. En la demo es 1234.</p>
          <input
            id="panel-pin"
            className={`${inputCls} text-center text-2xl tracking-[0.5em]`}
            type="password"
            inputMode="numeric"
            maxLength={4}
            placeholder="••••"
            value={pin}
            aria-invalid={pinErr}
            onChange={(e) => setPin(e.target.value.replace(/\D/g, ""))}
          />
          <DeepShadowButton type="submit" className="w-full justify-center">
            <Unlock className="size-4" />
            Entrar
          </DeepShadowButton>
        </form>
      </section>
    );
  }

  const agenda = state.bookings.filter((b) => b.date === day);
  const users = Object.values(state.users);

  return (
    <section className="mx-auto max-w-[1200px] px-4 py-20 sm:px-8" aria-labelledby="panel">
      <SectionHead
        id="panel"
        eyebrow="Solo para el barbero"
        title="Panel"
        right={
          <div className="flex flex-wrap gap-2">
            <GhostButton className="px-4 py-2" onClick={() => setCsvOpen(true)}>
              <Copy className="size-4" />
              Contactos CSV
            </GhostButton>
            <GhostButton
              className="px-4 py-2"
              onClick={() =>
                ask("¿Reiniciar la demo?", "Se borran las reservas, clientes y reseñas nuevas y vuelven los datos de ejemplo.", () => {
                  reset();
                  toast("Demo reiniciada");
                })
              }
            >
              <RotateCcw className="size-4" />
              Reiniciar demo
            </GhostButton>
            <GhostButton className="px-4 py-2" onClick={() => setUnlocked(false)}>
              <LogOut className="size-4" />
              Salir
            </GhostButton>
          </div>
        }
      />

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {kpis.map((k) => (
          <div key={k.label} className="rounded-3xl border border-line bg-card p-5">
            <Eyebrow>{k.label}</Eyebrow>
            <p className="mt-3 font-heading text-4xl leading-none text-white tabular-nums">{k.value}</p>
            <p className="mt-1 text-xs text-muted">{k.note}</p>
          </div>
        ))}
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-[340px_1fr]">
        <div className="flex h-fit flex-col gap-4 rounded-3xl border border-line bg-card p-6">
          <Eyebrow>Reservas online</Eyebrow>
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="font-heading text-4xl uppercase leading-none text-white">{state.open ? "Abierto" : "Cerrado"}</p>
              <p className="mt-1 text-xs text-muted">
                {state.open ? "Los clientes pueden tomar horas libres." : "Nadie puede reservar hasta que abras."}
              </p>
            </div>
            <button
              type="button"
              role="switch"
              aria-checked={state.open}
              aria-label="Abrir o cerrar reservas"
              onClick={() => {
                update((s) => ({ ...s, open: !s.open }));
                toast(state.open ? "Agenda cerrada" : "Agenda abierta");
              }}
              className={`relative h-9 w-16 shrink-0 rounded-full border transition-colors ${
                state.open ? "border-white bg-white" : "border-line-2 bg-bg"
              }`}
            >
              <span
                className={`absolute top-1 size-6 rounded-full transition-all ${
                  state.open ? "left-8 bg-[#0B0B0C]" : "left-1 bg-muted"
                }`}
              />
            </button>
          </div>
          <p className="flex items-center gap-2 text-xs text-muted">
            <Lock className="size-3" /> Las horas ya tomadas se mantienen al cerrar.
          </p>
        </div>

        <div className="rounded-3xl border border-line bg-card p-6">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div>
              <Eyebrow>Agenda del día</Eyebrow>
              <p className="mt-1 font-semibold text-white">{niceDate(day)}</p>
            </div>
            <div className="flex gap-2">
              <button type="button" aria-label="Día anterior" onClick={() => shiftDay(-1)} className="grid size-9 place-items-center rounded-full border border-line-2 text-white">
                <ChevronLeft className="size-4" />
              </button>
              <button type="button" onClick={() => setDay(today)} className="rounded-full border border-line-2 px-3 text-xs text-white">
                Hoy
              </button>
              <button type="button" aria-label="Día siguiente" onClick={() => shiftDay(1)} className="grid size-9 place-items-center rounded-full border border-line-2 text-white">
                <ChevronRight className="size-4" />
              </button>
            </div>
          </div>
          <ul className="flex flex-col">
            {HOURS.map((h) => {
              const b = agenda.find((x) => x.hour === h);
              const u = b && state.users[b.email];
              return (
                <li key={h} className="flex flex-wrap items-center justify-between gap-3 border-b border-dotted border-line-2 py-2.5 text-sm last:border-b-0">
                  <span className="w-14 font-semibold text-white tabular-nums">{hh(h)}</span>
                  {b ? (
                    <>
                      <span className="min-w-0 flex-1">
                        <span className="text-white">{u?.name ?? b.email}</span>
                        <span className="text-muted"> · {svc(b.service).name}</span>
                        {u && <span className="block text-xs text-muted tabular-nums">{u.phone}</span>}
                      </span>
                      <button
                        type="button"
                        className="text-xs text-muted underline hover:text-white"
                        onClick={() =>
                          ask("¿Cancelar esta reserva?", `${hh(h)} · ${u?.name ?? b.email}. Avísale al cliente por WhatsApp.`, () => {
                            update((s) => ({ ...s, bookings: s.bookings.filter((x) => x.id !== b.id) }));
                            toast("Reserva cancelada");
                          })
                        }
                      >
                        Cancelar
                      </button>
                    </>
                  ) : (
                    <span className="flex-1 text-muted/60">Libre</span>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      </div>

      <div className="mt-6 rounded-3xl border border-line bg-card p-6">
        <Eyebrow>Clientes y permisos de marketing · {users.length}</Eyebrow>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[640px] text-left text-sm">
            <thead className="text-xs text-muted">
              <tr className="border-b border-line">
                <th className="py-2 pr-4 font-medium">Cliente</th>
                <th className="py-2 pr-4 font-medium">Teléfono</th>
                <th className="py-2 pr-4 font-medium">Correo</th>
                <th className="py-2 pr-4 text-right font-medium">Reservas</th>
                <th className="py-2 pr-4 font-medium">Mk correo</th>
                <th className="py-2 font-medium">Mk WhatsApp</th>
              </tr>
            </thead>
            <tbody className="tabular-nums">
              {users.map((u) => (
                <tr key={u.email} className="border-b border-line/60 last:border-b-0">
                  <td className="py-2.5 pr-4 text-white">{u.name}</td>
                  <td className="py-2.5 pr-4 text-muted">{u.phone}</td>
                  <td className="py-2.5 pr-4 text-muted">{u.email}</td>
                  <td className="py-2.5 pr-4 text-right text-white">{state.bookings.filter((b) => b.email === u.email).length}</td>
                  <td className="py-2.5 pr-4">
                    <Yes on={u.mkEmail} />
                  </td>
                  <td className="py-2.5">
                    <Yes on={u.mkSms} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal open={csvOpen} onClose={() => setCsvOpen(false)} title="Contactos CSV" subtitle="Cópialo y pégalo en Excel, Google Sheets o tu herramienta de correo." wide>
        <textarea id="csv-text" readOnly rows={10} value={csv} className={`${inputCls} whitespace-pre font-mono text-[11px]`} onFocus={(e) => e.target.select()} />
        <div className="mt-4 flex justify-end gap-3">
          <GhostButton onClick={() => setCsvOpen(false)}>Cerrar</GhostButton>
          <DeepShadowButton
            onClick={() => {
              navigator.clipboard
                .writeText(csv)
                .then(() => toast("CSV copiado"))
                .catch(() => {
                  (document.getElementById("csv-text") as HTMLTextAreaElement | null)?.select();
                  toast("Selecciona el texto y copia con Ctrl+C");
                });
            }}
          >
            <Copy className="size-4" />
            Copiar CSV
          </DeepShadowButton>
        </div>
      </Modal>
    </section>
  );
}
