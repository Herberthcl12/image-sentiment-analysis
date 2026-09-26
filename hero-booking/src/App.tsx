import { useCallback, useMemo, useRef, useState } from "react";
import { LogIn } from "lucide-react";
import { ActionsCtx, useActions, type Actions, type SectionId } from "./actions";
import { LoginModal, MyAppointments } from "./Account";
import { Agenda, Services } from "./Booking";
import { Products, Reviews } from "./Extras";
import Hero from "./Hero";
import { Panel } from "./Panel";
import { BRAND, SERVICES, clp, initials, isPast } from "./data";
import { StoreProvider, useStore } from "./store";
import { DeepShadowButton, GhostButton, Modal, Toast } from "./ui";

const NAV: { id: SectionId; label: string }[] = [
  { id: "agenda", label: "Reservar" },
  { id: "servicios", label: "Servicios" },
  { id: "productos", label: "Productos" },
  { id: "resenas", label: "Reseñas" },
  { id: "mis-citas", label: "Mis citas" },
];

function Ticker() {
  const { state } = useStore();
  const combo = SERVICES.find((s) => s.id === "combo")!;
  const text = `✦ ${BRAND.toUpperCase()} ✦ LUN–SÁB 12:00–21:00 ✦ ${state.open ? "RESERVAS ABIERTAS" : "RESERVAS CERRADAS"} ✦ CORTE + BARBA ${clp(combo.price)} ✦ APARTA PRODUCTOS Y PAGA AL LLEGAR ✦ FRESH CUTS ONLY `;
  return (
    <div className="overflow-hidden whitespace-nowrap border-b border-line bg-white font-wide text-[10px] tracking-[0.08em] text-[#0B0B0C]" aria-hidden="true">
      <span className="inline-block animate-ticker py-1.5">
        {text}
        {text}
      </span>
    </div>
  );
}

function Header() {
  const { state, me } = useStore();
  const { goTo, openLogin } = useActions();
  const myCount = me ? state.bookings.filter((b) => b.email === me.email && !isPast(b.date, b.hour)).length : 0;

  return (
    <header className="sticky top-[env(safe-area-inset-top,0px)] z-40 border-b border-line bg-bg/85 backdrop-blur-md">
      <Ticker />
      <div className="mx-auto flex max-w-[1440px] items-center justify-between gap-4 px-4 py-3 sm:px-8 lg:px-16">
        <button type="button" onClick={() => goTo("inicio")} className="flex items-center gap-3">
          <span className="grid size-10 place-items-center rounded-full bg-chrome font-heading text-lg text-[#0B0B0C] shadow-[0_0_0_2px_#000,0_0_0_3px_#34343a]">
            M
          </span>
          <span className="hidden font-wide text-xs tracking-wide text-white sm:inline">MARCUT'S BARBER</span>
        </button>

        <nav className="flex min-w-0 flex-1 justify-start gap-1 overflow-x-auto lg:justify-center [scrollbar-width:none]" aria-label="Secciones">
          {NAV.map((n) => (
            <button
              key={n.id}
              type="button"
              onClick={() => goTo(n.id)}
              className="relative shrink-0 rounded-full px-3 py-2 text-xs font-semibold uppercase tracking-[0.12em] text-muted transition-colors hover:text-white"
            >
              {n.label}
              {n.id === "mis-citas" && myCount > 0 && (
                <span className="ml-1.5 rounded-full bg-white px-1.5 py-0.5 text-[10px] text-[#0B0B0C] tabular-nums">{myCount}</span>
              )}
            </button>
          ))}
        </nav>

        {me ? (
          <button
            type="button"
            onClick={() => goTo("mis-citas")}
            className="grid size-10 shrink-0 place-items-center rounded-full border border-line-2 bg-card font-wide text-[10px] text-white"
            aria-label={`Cuenta de ${me.name}`}
          >
            {initials(me.name)}
          </button>
        ) : (
          <GhostButton className="shrink-0 px-4 py-2" onClick={() => openLogin()}>
            <LogIn className="size-4" />
            <span className="hidden sm:inline">Entrar</span>
          </GhostButton>
        )}
      </div>
    </header>
  );
}

function Footer() {
  const { goTo, openTerms } = useActions();
  return (
    <footer className="border-t border-line">
      <div className="mx-auto flex max-w-[1200px] flex-col gap-6 px-4 py-12 text-sm text-muted sm:flex-row sm:items-end sm:justify-between sm:px-8">
        <div>
          <p className="font-heading text-5xl uppercase leading-none text-chrome">Marcut's</p>
          <p className="mt-2">Lunes a sábado · 12:00 a 21:00 · Bloques de 1 hora</p>
          <p>Pagos en local: efectivo, débito o transferencia.</p>
        </div>
        <div className="flex flex-wrap gap-4">
          <button type="button" className="underline hover:text-white" onClick={openTerms}>
            Términos y privacidad
          </button>
          <button type="button" className="underline hover:text-white" onClick={() => goTo("panel")}>
            Panel del barbero
          </button>
        </div>
      </div>
    </footer>
  );
}

function TermsModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const items = [
    ["1. Reservas", "Cada reserva bloquea 60 minutos entre las 12:00 y las 21:00, de lunes a sábado. Se espera al cliente hasta 10 minutos después de la hora; pasado ese tiempo la hora puede liberarse."],
    ["2. Cancelaciones", "Puedes cancelar desde \"Mis citas\" sin costo hasta 3 horas antes. Tres inasistencias sin aviso pueden bloquear la reserva online."],
    ["3. Productos apartados", "Se guardan hasta el cierre del día de tu cita y se pagan en la barbería. Los precios incluyen IVA."],
    ["4. Datos personales", "Usamos tu nombre, teléfono y correo para gestionar tus reservas y enviarte confirmaciones y recordatorios. No vendemos ni cedemos tus datos a terceros."],
    ["5. Marketing (opcional)", "Si marcas las casillas de marketing, aceptas recibir promociones de Marcut's Barber por correo y/o WhatsApp/SMS, con un máximo de 4 mensajes al mes. Puedes retirarlo cuando quieras desde \"Mis citas\" o respondiendo BAJA. No aceptarlo no afecta tu reserva."],
    ["6. Tus derechos", "Puedes pedir acceso, corrección o eliminación de tus datos escribiendo a hola@marcutsbarber.cl."],
  ];
  return (
    <Modal open={open} onClose={onClose} title="Términos y privacidad" subtitle="Última actualización: septiembre 2026" wide>
      <div className="flex flex-col gap-4 text-sm leading-relaxed">
        {items.map(([h, p]) => (
          <div key={h}>
            <p className="font-semibold text-white">{h}</p>
            <p className="text-muted">{p}</p>
          </div>
        ))}
        <div className="flex justify-end">
          <DeepShadowButton onClick={onClose}>Entendido</DeepShadowButton>
        </div>
      </div>
    </Modal>
  );
}

function Shell() {
  const { toastMsg } = useStore();
  const [loginOpen, setLoginOpen] = useState(false);
  const [termsOpen, setTermsOpen] = useState(false);
  const [askState, setAskState] = useState<{ title: string; text: string; onYes: () => void } | null>(null);
  const [agendaDate, setAgendaDate] = useState<string | null>(null);
  const [agendaService, setAgendaService] = useState(SERVICES[0].id);
  const afterLogin = useRef<(() => void) | undefined>(undefined);

  const goTo = useCallback((id: SectionId) => {
    requestAnimationFrame(() => document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" }));
  }, []);

  const actions: Actions = useMemo(
    () => ({
      openLogin: (then) => {
        afterLogin.current = then;
        setLoginOpen(true);
      },
      openTerms: () => setTermsOpen(true),
      ask: (title, text, onYes) => setAskState({ title, text, onYes }),
      goTo,
      pickDay: (date, serviceId) => {
        if (date) setAgendaDate(date);
        if (serviceId) setAgendaService(serviceId);
        goTo("agenda");
      },
      agendaDate,
      agendaService,
      setAgendaService,
    }),
    [goTo, agendaDate, agendaService]
  );

  return (
    <ActionsCtx.Provider value={actions}>
      <Header />
      <Hero />
      <div className="border-t border-line">
        <Agenda />
      </div>
      <div className="border-t border-line bg-bg-2/60">
        <Services />
      </div>
      <div className="border-t border-line">
        <Products />
      </div>
      <div className="border-t border-line bg-bg-2/60">
        <Reviews />
      </div>
      <div className="border-t border-line">
        <MyAppointments />
      </div>
      <div className="border-t border-line bg-bg-2/60">
        <Panel />
      </div>
      <Footer />

      <LoginModal
        open={loginOpen}
        onClose={() => setLoginOpen(false)}
        onDone={() => {
          setLoginOpen(false);
          const then = afterLogin.current;
          afterLogin.current = undefined;
          then?.();
        }}
      />
      <TermsModal open={termsOpen} onClose={() => setTermsOpen(false)} />
      <Modal open={!!askState} onClose={() => setAskState(null)} title={askState?.title ?? ""} subtitle={askState?.text}>
        <div className="flex justify-end gap-3">
          <GhostButton onClick={() => setAskState(null)}>Volver</GhostButton>
          <DeepShadowButton
            onClick={() => {
              askState?.onYes();
              setAskState(null);
            }}
          >
            Sí, confirmar
          </DeepShadowButton>
        </div>
      </Modal>
      <Toast msg={toastMsg} />
    </ActionsCtx.Provider>
  );
}

export default function App() {
  return (
    <StoreProvider>
      <Shell />
    </StoreProvider>
  );
}
