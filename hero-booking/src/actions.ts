import { createContext, useContext } from "react";

/** Acciones de interfaz compartidas entre secciones (modales, scroll y agenda). */
export interface Actions {
  openLogin: (then?: () => void) => void;
  openTerms: () => void;
  ask: (title: string, text: string, onYes: () => void) => void;
  goTo: (sectionId: SectionId) => void;
  /** Abre la agenda en un día y, opcionalmente, con un servicio preseleccionado. */
  pickDay: (date: string | null, serviceId?: string) => void;
  agendaDate: string | null;
  agendaService: string;
  setAgendaService: (id: string) => void;
}

export type SectionId = "inicio" | "servicios" | "agenda" | "productos" | "resenas" | "mis-citas" | "panel";

export const ActionsCtx = createContext<Actions | null>(null);

export function useActions() {
  const a = useContext(ActionsCtx);
  if (!a) throw new Error("useActions fuera de ActionsCtx");
  return a;
}
