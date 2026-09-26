import { useState } from "react";
import { Box, Brush, Check as CheckIcon, Droplets, PenLine, ShoppingBag, Sparkles, Wrench } from "lucide-react";
import { useActions } from "./actions";
import { PRODUCTS, SERVICES, ago, clp, publicName, type ProductCat } from "./data";
import { useStore } from "./store";
import { DeepShadowButton, Field, GhostButton, SectionHead, Stars, inputCls } from "./ui";

// ---------------------------------------------------------------------------
// Productos
// ---------------------------------------------------------------------------

const CAT_ICON: Record<ProductCat, typeof Box> = {
  Styling: Sparkles,
  Barba: Droplets,
  Cuidado: Brush,
  Accesorios: Box,
  Pro: Wrench,
};
const CATS: ("Todos" | ProductCat)[] = ["Todos", "Styling", "Barba", "Cuidado", "Accesorios", "Pro"];

export function Products() {
  const { state, update, me, toast } = useStore();
  const { openLogin } = useActions();
  const [cat, setCat] = useState<(typeof CATS)[number]>("Todos");
  const held = (me && state.held[me.email]) || [];
  const list = PRODUCTS.filter((p) => cat === "Todos" || p.cat === cat);
  const total = held.reduce((a, id) => a + (PRODUCTS.find((p) => p.id === id)?.price ?? 0), 0);

  const toggle = (id: string) => {
    const run = () =>
      update((s) => {
        const email = s.session!;
        const cur = s.held[email] ?? [];
        const has = cur.includes(id);
        toast(has ? "Producto liberado" : "Apartado · lo pagas en la barbería");
        return { ...s, held: { ...s.held, [email]: has ? cur.filter((x) => x !== id) : [...cur, id] } };
      });
    if (me) run();
    else openLogin(run);
  };

  return (
    <section className="mx-auto max-w-[1200px] px-4 py-20 sm:px-8" aria-labelledby="productos">
      <SectionHead id="productos" eyebrow="Aparta online · pagas al llegar" title="Productos" />

      <div className="mb-6 flex gap-2 overflow-x-auto pb-1 [scrollbar-width:none]">
        {CATS.map((c) => (
          <button
            key={c}
            type="button"
            onClick={() => setCat(c)}
            className={`shrink-0 rounded-full border px-4 py-2 text-xs font-medium transition-colors ${
              cat === c ? "border-white bg-white text-[#0B0B0C]" : "border-line-2 text-muted hover:text-white"
            }`}
          >
            {c}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {list.map((p) => {
          const Icon = CAT_ICON[p.cat];
          const on = held.includes(p.id);
          return (
            <article key={p.id} className={`flex flex-col gap-5 rounded-3xl border p-5 ${on ? "border-white/60 bg-white/[0.04]" : "border-line bg-card"}`}>
              <div className="flex items-start justify-between gap-3">
                <span className="grid size-12 place-items-center rounded-2xl bg-bg">
                  <Icon className="size-5 text-white" />
                </span>
                {p.badge && (
                  <span className="rounded-full bg-white px-2.5 py-1 font-wide text-[9px] tracking-wider text-[#0B0B0C]">{p.badge}</span>
                )}
              </div>
              <div className="flex-1">
                <p className="text-[11px] uppercase tracking-wider text-muted">{p.cat}</p>
                <h3 className="mt-1 font-semibold text-white">{p.name}</h3>
                <p className="mt-1 text-sm text-muted">{p.desc}</p>
              </div>
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="font-heading text-3xl leading-none text-white tabular-nums">{clp(p.price)}</p>
                  <p className="mt-1 text-xs text-muted">{p.stock <= 5 ? `Quedan ${p.stock}` : `${p.stock} en stock`}</p>
                </div>
                <button
                  type="button"
                  onClick={() => toggle(p.id)}
                  className={`inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                    on ? "bg-white text-[#0B0B0C]" : "border border-line-2 text-white hover:border-white"
                  }`}
                >
                  {on ? <CheckIcon className="size-4" /> : <ShoppingBag className="size-4" />}
                  {on ? "Apartado" : "Apartar"}
                </button>
              </div>
            </article>
          );
        })}
      </div>

      {held.length > 0 && (
        <div className="sticky bottom-4 z-30 mt-8 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-white/30 bg-card/95 px-5 py-4 backdrop-blur">
          <div>
            <p className="text-sm font-semibold text-white tabular-nums">
              {held.length} {held.length === 1 ? "producto apartado" : "productos apartados"} · {clp(total)}
            </p>
            <p className="text-xs text-muted">Se paga en la barbería: efectivo, débito o transferencia.</p>
          </div>
          <GhostButton className="px-4 py-2" onClick={() => update((s) => ({ ...s, held: { ...s.held, [me!.email]: [] } }))}>
            Vaciar
          </GhostButton>
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// Reseñas
// ---------------------------------------------------------------------------

export function Reviews() {
  const { state, update, me, toast } = useStore();
  const { openLogin } = useActions();
  const [writing, setWriting] = useState(false);
  const [stars, setStars] = useState(5);
  const [text, setText] = useState("");
  const [svcName, setSvcName] = useState(SERVICES[0].name);

  const n = state.reviews.length;
  const avg = n ? state.reviews.reduce((a, r) => a + r.stars, 0) / n : 0;
  const sorted = [...state.reviews].sort((a, b) => b.at - a.at);

  const start = () => (me ? setWriting(true) : openLogin(() => setWriting(true)));
  const publish = () => {
    if (text.trim().length < 10) return toast("Escribe al menos 10 caracteres");
    update((s) => ({
      ...s,
      reviews: [...s.reviews, { id: "r" + Date.now(), name: s.users[s.session!].name, stars, text: text.trim(), svc: svcName, at: Date.now() }],
    }));
    setWriting(false);
    setText("");
    setStars(5);
    toast("Reseña publicada");
  };

  return (
    <section className="mx-auto max-w-[1200px] px-4 py-20 sm:px-8" aria-labelledby="resenas">
      <SectionHead
        id="resenas"
        eyebrow={`${n} reseñas verificadas`}
        title="Reseñas"
        right={
          !writing && (
            <GhostButton onClick={start}>
              <PenLine className="size-4" />
              Escribir reseña
            </GhostButton>
          )
        }
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[280px_1fr]">
        <div className="flex h-fit flex-col gap-4 rounded-3xl border border-line bg-card p-6">
          <p className="font-heading text-7xl leading-none text-chrome tabular-nums">{avg.toFixed(1)}</p>
          <Stars n={avg} className="size-5" />
          <div className="flex flex-col gap-1.5">
            {[5, 4, 3, 2, 1].map((k) => {
              const c = state.reviews.filter((r) => r.stars === k).length;
              return (
                <div key={k} className="flex items-center gap-2 text-xs text-muted tabular-nums">
                  <span className="w-3">{k}</span>
                  <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-bg">
                    <span className="block h-full rounded-full bg-white" style={{ width: `${n ? (c / n) * 100 : 0}%` }} />
                  </span>
                  <span className="w-4 text-right">{c}</span>
                </div>
              );
            })}
          </div>
        </div>

        <div className="flex flex-col gap-4">
          {writing && (
            <div className="flex flex-col gap-4 rounded-3xl border border-white/40 bg-card p-6">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <p className="text-sm text-white">Tu calificación</p>
                <span className="flex gap-1">
                  {[1, 2, 3, 4, 5].map((k) => (
                    <button
                      key={k}
                      type="button"
                      aria-label={`${k} estrellas`}
                      onClick={() => setStars(k)}
                      className={`text-2xl leading-none ${k <= stars ? "text-white" : "text-line-2"}`}
                    >
                      ★
                    </button>
                  ))}
                </span>
              </div>
              <Field label="Servicio">
                <select id="rev-service" className={inputCls} value={svcName} onChange={(e) => setSvcName(e.target.value)}>
                  {SERVICES.map((s) => (
                    <option key={s.id}>{s.name}</option>
                  ))}
                </select>
              </Field>
              <Field label={`Comentario (${text.length}/280)`}>
                <textarea
                  id="rev-text"
                  className={inputCls}
                  rows={3}
                  maxLength={280}
                  placeholder="¿Cómo te quedó el corte?"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                />
              </Field>
              <div className="flex justify-end gap-3">
                <GhostButton onClick={() => setWriting(false)}>Cancelar</GhostButton>
                <DeepShadowButton onClick={publish}>Publicar</DeepShadowButton>
              </div>
            </div>
          )}

          {sorted.map((r) => (
            <article key={r.id} className="rounded-3xl border border-line bg-card p-5">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="font-semibold text-white">{publicName(r.name)}</p>
                <Stars n={r.stars} />
              </div>
              <p className="mt-3 text-sm leading-relaxed text-text">{r.text}</p>
              <p className="mt-3 text-xs text-muted">
                {r.svc} · {ago(r.at)}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
