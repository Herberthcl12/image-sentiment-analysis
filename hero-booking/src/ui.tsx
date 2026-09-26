import { useEffect, type ButtonHTMLAttributes, type ReactNode } from "react";
import { AnimatePresence, motion } from "motion/react";
import { Star, X } from "lucide-react";
import { initials } from "./data";

// ---------------------------------------------------------------------------
// Deep UI (versión y2k: cromo blanco sobre negro)
// ---------------------------------------------------------------------------

export function DeepShadowIcon({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <span className={`relative inline-flex align-middle ${className}`}>
      <span className="absolute inset-0 rounded-2xl bg-white opacity-40 blur-[18px] scale-90 translate-y-1.5" />
      <span className="relative rounded-2xl bg-chrome p-2 shadow-[0px_0px_5px_rgba(255,255,255,0.8)_inset,0px_8px_20px_rgba(255,255,255,0.18)]">
        {children}
      </span>
    </span>
  );
}

type BtnProps = ButtonHTMLAttributes<HTMLButtonElement> & { children: ReactNode };

export function DeepShadowButton({ children, className = "", ...rest }: BtnProps) {
  return (
    <span className="group relative inline-flex">
      <span className="absolute inset-0 rounded-full bg-white opacity-25 blur-[25px] transition-transform duration-300 group-hover:scale-110 group-hover:translate-y-1" />
      <button
        type="button"
        {...rest}
        className={`relative inline-flex items-center gap-2 rounded-full bg-white px-6 py-3.5 text-sm font-semibold text-[#0B0B0C] shadow-[0px_0px_4px_rgba(0,0,0,0.25)_inset,0px_6px_19px_rgba(255,255,255,0.12)] transition-transform duration-300 hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0 ${className}`}
      >
        {children}
      </button>
    </span>
  );
}

export function GhostButton({ children, className = "", ...rest }: BtnProps) {
  return (
    <button
      type="button"
      {...rest}
      className={`inline-flex items-center justify-center gap-2 rounded-full border border-line-2 bg-card px-5 py-3 text-sm font-medium text-muted transition-colors hover:border-white/50 hover:text-white disabled:cursor-not-allowed disabled:opacity-40 ${className}`}
    >
      {children}
    </button>
  );
}

const AVATAR_SIZES = { sm: "size-8 text-[10px]", md: "size-11 text-xs", lg: "size-14 text-sm" } as const;

export function DeepShadowAvatar({
  src,
  name,
  size = "md",
  hasGlow = false,
}: {
  src?: string;
  name: string;
  size?: keyof typeof AVATAR_SIZES;
  hasGlow?: boolean;
}) {
  return (
    <span className={`relative shrink-0 ${AVATAR_SIZES[size]}`}>
      <span
        className={`absolute inset-0 translate-y-2 rounded-full ${
          hasGlow ? "bg-white opacity-50 blur-[18px]" : "bg-black opacity-60 blur-[12px]"
        }`}
      />
      <AvatarFace src={src} name={name} className="relative size-full border-2 border-bg" />
    </span>
  );
}

export function AvatarWithShadow({ src, name }: { src?: string; name: string }) {
  return (
    <span className="relative size-9 shrink-0 text-[11px]">
      <span className="absolute inset-x-1 bottom-0 h-4 rounded-full bg-black opacity-60 blur-[10px]" />
      <AvatarFace src={src} name={name} className="relative size-full" />
    </span>
  );
}

function AvatarFace({ src, name, className }: { src?: string; name: string; className: string }) {
  return src ? (
    <img src={src} alt={name} className={`rounded-full object-cover grayscale ${className}`} />
  ) : (
    <span className={`grid place-items-center rounded-full bg-chrome font-wide text-[#0B0B0C] ${className}`}>
      {initials(name)}
    </span>
  );
}

export function Stars({ n, className = "size-4" }: { n: number; className?: string }) {
  return (
    <span className="inline-flex gap-0.5" aria-label={`${n} de 5 estrellas`}>
      {Array.from({ length: 5 }).map((_, i) => (
        <Star key={i} className={`${className} ${i < Math.round(n) ? "fill-white text-white" : "text-line-2"}`} />
      ))}
    </span>
  );
}

export function Eyebrow({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <span className={`font-wide text-[10px] uppercase tracking-[0.18em] text-muted ${className}`}>{children}</span>;
}

export function SectionHead({ id, eyebrow, title, right }: { id: string; eyebrow: string; title: string; right?: ReactNode }) {
  return (
    <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div className="flex flex-col gap-2">
        <Eyebrow>{eyebrow}</Eyebrow>
        <h2 id={id} className="scroll-mt-32 font-heading text-5xl uppercase leading-none text-chrome sm:text-6xl">
          {title}
        </h2>
      </div>
      {right}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Formularios y modales
// ---------------------------------------------------------------------------

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-xs font-medium text-muted">{label}</span>
      {children}
    </label>
  );
}

export const inputCls =
  "w-full rounded-xl border border-line-2 bg-bg px-3.5 py-2.5 text-sm text-white placeholder:text-muted/60 outline-none transition-colors focus:border-white aria-[invalid=true]:border-[#ff6b6b]";

export function Check({
  id,
  checked,
  onChange,
  children,
  invalid = false,
}: {
  id: string;
  checked: boolean;
  onChange: (v: boolean) => void;
  children: ReactNode;
  invalid?: boolean;
}) {
  return (
    <label
      htmlFor={id}
      className={`flex cursor-pointer items-start gap-3 rounded-xl border px-3 py-2.5 text-xs leading-relaxed text-muted transition-colors ${
        invalid ? "border-[#ff6b6b]" : "border-line hover:border-line-2"
      }`}
    >
      <input
        id={id}
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="mt-0.5 size-4 shrink-0 accent-white"
      />
      <span>{children}</span>
    </label>
  );
}

export function Modal({
  open,
  onClose,
  title,
  subtitle,
  children,
  wide = false,
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  children: ReactNode;
  wide?: boolean;
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-50 flex items-end justify-center bg-black/70 p-0 backdrop-blur-sm sm:items-center sm:p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onMouseDown={(e) => e.target === e.currentTarget && onClose()}
        >
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-label={title}
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 40, opacity: 0 }}
            transition={{ type: "spring", damping: 26, stiffness: 300 }}
            className={`max-h-[92vh] w-full overflow-y-auto rounded-t-3xl border border-line bg-card p-6 pb-[max(1.5rem,env(safe-area-inset-bottom))] sm:rounded-3xl ${
              wide ? "sm:max-w-2xl" : "sm:max-w-md"
            }`}
          >
            <div className="mb-5 flex items-start justify-between gap-4">
              <div>
                <h3 className="font-heading text-3xl uppercase leading-none text-white">{title}</h3>
                {subtitle && <p className="mt-2 text-sm text-muted">{subtitle}</p>}
              </div>
              <button
                type="button"
                onClick={onClose}
                aria-label="Cerrar"
                className="grid size-9 shrink-0 place-items-center rounded-full border border-line-2 text-muted hover:text-white"
              >
                <X className="size-4" />
              </button>
            </div>
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export function Toast({ msg }: { msg: string | null }) {
  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-6 z-[60] flex justify-center px-4" aria-live="polite">
      <AnimatePresence>
        {msg && (
          <motion.div
            key={msg}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 20, opacity: 0 }}
            className="rounded-full bg-white px-5 py-3 text-sm font-semibold text-[#0B0B0C] shadow-[0_10px_30px_rgba(0,0,0,0.5)]"
          >
            {msg}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
