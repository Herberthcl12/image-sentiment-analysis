import { motion } from "motion/react";
import { Play, Star, TrendingUp } from "lucide-react";
import type { ReactNode } from "react";

import localAvatar1 from "./assets/1534528741775-53994a69daeb.jpg";
import localAvatar2 from "./assets/1507003211169-0a1dd7228f2d.jpg";
import localAvatar3 from "./assets/1494790108377-be9c29b29330.jpg";
import localAvatar4 from "./assets/1500648767791-00dcc994a43e.jpg";

// ---------------------------------------------------------------------------
// Mock data & types
// ---------------------------------------------------------------------------

const REMOTE_AVATARS = [
  "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=100&h=100",
  "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=100&h=100",
  "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=100&h=100",
  "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=100&h=100",
];

// El build de un solo archivo (SINGLEFILE=1) usa las mismas fotos guardadas en local,
// porque la vista publicada no carga imágenes de otros dominios.
const AVATARS: string[] = import.meta.env.VITE_LOCAL_AVATARS
  ? [localAvatar1, localAvatar2, localAvatar3, localAvatar4]
  : REMOTE_AVATARS;

interface CallItem {
  name: string;
  avatar: string;
  time: string;
  duration: string;
}

interface ClientCall {
  id: string;
  day: string;
  date: string;
  items: CallItem[];
}

const CLIENT_CALLS: ClientCall[] = [
  {
    id: "call-1",
    day: "MON",
    date: "18 JUL",
    items: [
      { name: "Sophie Laurent", avatar: AVATARS[0], time: "9:30 AM - 10:30 AM", duration: "1hr" },
      { name: "Marcus Reid", avatar: AVATARS[1], time: "11:00 AM - 11:45 AM", duration: "45m" },
    ],
  },
  {
    id: "call-2",
    day: "TUE",
    date: "19 JUL",
    items: [{ name: "Emily Carter", avatar: AVATARS[2], time: "2:00 PM - 3:00 PM", duration: "1hr" }],
  },
  {
    id: "call-3",
    day: "THU",
    date: "25 JUL",
    items: [
      { name: "Daniel Brooks", avatar: AVATARS[3], time: "10:00 AM - 10:30 AM", duration: "30m" },
      { name: "Sophie Laurent", avatar: AVATARS[0], time: "4:00 PM - 5:00 PM", duration: "1hr" },
    ],
  },
  {
    id: "call-4",
    day: "MON",
    date: "25 JUL",
    items: [{ name: "Marcus Reid", avatar: AVATARS[1], time: "1:30 PM - 2:30 PM", duration: "1hr" }],
  },
  {
    id: "call-5",
    day: "WED",
    date: "20 JUL",
    items: [
      { name: "Emily Carter", avatar: AVATARS[2], time: "9:00 AM - 9:45 AM", duration: "45m" },
      { name: "Daniel Brooks", avatar: AVATARS[3], time: "3:30 PM - 4:30 PM", duration: "1hr" },
    ],
  },
];

// ---------------------------------------------------------------------------
// Deep UI components
// ---------------------------------------------------------------------------

function DeepShadowIcon({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <div className={`relative inline-flex align-middle ${className}`}>
      <div className="absolute inset-0 rounded-2xl opacity-60 bg-[#F25C40] blur-[18px] scale-90 translate-y-1.5" />
      <div className="relative p-2 rounded-2xl bg-[#F25C40] shadow-[0px_0px_5px_rgba(255,255,255,0.5)_inset,0px_8px_20px_rgba(242,92,64,0.35)]">
        {children}
      </div>
    </div>
  );
}

function DeepShadowButton({ children, onClick }: { children: ReactNode; onClick?: () => void }) {
  return (
    <div className="group relative inline-flex">
      <div className="absolute inset-0 rounded-full opacity-40 bg-[#212121] blur-[25px] transition-transform duration-300 group-hover:scale-110 group-hover:translate-y-1" />
      <button
        type="button"
        onClick={onClick}
        className="relative rounded-full bg-[#202020] px-6 py-3.5 text-sm font-medium text-white shadow-[0px_0px_4px_rgba(255,255,255,0.25)_inset,0px_6px_19px_rgba(0,0,0,0.25)] transition-transform duration-300 hover:-translate-y-0.5 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#F25C40]"
      >
        {children}
      </button>
    </div>
  );
}

const AVATAR_SIZES = {
  sm: "size-8",
  md: "size-11",
  lg: "size-14",
} as const;

function DeepShadowAvatar({
  src,
  alt,
  size = "md",
  hasGlow = false,
}: {
  src: string;
  alt: string;
  size?: keyof typeof AVATAR_SIZES;
  hasGlow?: boolean;
}) {
  return (
    <div className={`relative shrink-0 ${AVATAR_SIZES[size]}`}>
      <div
        className={`absolute inset-0 rounded-full translate-y-2 ${
          hasGlow ? "bg-[#F25C40] opacity-60 blur-[18px]" : "bg-black blur-[12px] opacity-20"
        }`}
      />
      <img
        src={src}
        alt={alt}
        className="relative size-full rounded-full border-2 border-white object-cover"
      />
    </div>
  );
}

function AvatarWithShadow({ src, alt }: { src: string; alt: string }) {
  return (
    <div className="relative size-9 shrink-0">
      <div className="absolute inset-x-1 bottom-0 h-4 rounded-full bg-black opacity-25 blur-[10px]" />
      <img src={src} alt={alt} className="relative size-full rounded-full object-cover" />
    </div>
  );
}

function ClientCard({ call, index }: { call: ClientCall; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay: (index % CLIENT_CALLS.length) * 0.08 }}
      className={`${index % 2 === 0 ? "rotate-3" : "-rotate-3"} mx-auto w-full max-w-sm rounded-3xl bg-white p-5 shadow-[0_4px_20px_rgba(0,0,0,0.03)]`}
    >
      <div className="mb-3 flex items-center justify-between text-xs font-semibold tracking-wider text-neutral-400">
        <span className="text-[#202020]">{call.day}</span>
        <span>{call.date}</span>
      </div>
      <div className="flex flex-col">
        {call.items.map((item, i) => (
          <div
            key={i}
            className="flex items-center gap-3 border-b border-dotted border-neutral-200 py-3 last:border-b-0 last:pb-0"
          >
            <AvatarWithShadow src={item.avatar} alt={item.name} />
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-[#202020]">{item.name}</p>
              <p className="text-xs text-neutral-500">{item.time}</p>
            </div>
            <span className="rounded-full bg-[#F7F7F7] px-2.5 py-1 text-xs font-medium text-neutral-500">
              {item.duration}
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

// ---------------------------------------------------------------------------
// Hero
// ---------------------------------------------------------------------------

const LOOPED_CALLS = [...CLIENT_CALLS, ...CLIENT_CALLS, ...CLIENT_CALLS];

export default function App() {
  return (
    <div className="min-h-screen bg-[#F7F7F7]">
      <main className="mx-auto grid max-w-[1440px] grid-cols-1 gap-12 px-4 py-12 sm:px-8 lg:grid-cols-[1.2fr_0.8fr] lg:h-screen lg:min-h-[720px] lg:px-16 lg:py-0">
        {/* Left side: value prop */}
        <section className="flex flex-col justify-center gap-8 lg:py-24">
          <div className="inline-flex w-fit items-center gap-2 rounded-full border border-[#D1F2D1] bg-white px-3 py-1.5">
            <span className="size-2 rounded-full bg-[#52D352] animate-pulse shadow-[0_0_8px_rgba(82,211,82,0.6)]" />
            <span className="text-xs font-semibold uppercase tracking-wider text-[#52D352]">
              Booking for summer
            </span>
          </div>

          <h1 className="font-heading text-5xl leading-[1.05] tracking-[-0.02em] text-[#202020] sm:text-6xl xl:text-7xl text-balance">
            Expanding{" "}
            <DeepShadowIcon className="mx-1 -rotate-6">
              <TrendingUp className="size-8 text-white sm:size-10" strokeWidth={2.5} />
            </DeepShadowIcon>{" "}
            reach <br className="hidden sm:block" />
            with every lead
          </h1>

          <p className="max-w-xl text-lg leading-relaxed text-neutral-500">
            Automating lead systems and funnels, we design scalable growth engines for your next venture.
          </p>

          <div className="flex flex-wrap items-center gap-4 sm:gap-6">
            <DeepShadowButton>Scale revenue now</DeepShadowButton>
            <button
              type="button"
              className="inline-flex items-center gap-2 rounded-full border border-neutral-200 bg-white px-6 py-3.5 text-sm font-medium text-neutral-600 transition-colors hover:border-neutral-300 hover:text-[#202020]"
            >
              <Play className="size-4" />
              Start Here
            </button>
          </div>

          <div className="flex flex-col gap-8 pt-4 sm:flex-row sm:items-center sm:gap-10">
            <div className="flex flex-col gap-4">
              <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                Verified clients
              </span>
              <div className="flex items-center -space-x-2">
                {AVATARS.map((src, i) => (
                  <DeepShadowAvatar
                    key={src}
                    src={src}
                    alt={`Verified client ${i + 1}`}
                    size={i % 2 === 0 ? "md" : "lg"}
                    hasGlow={i === 1}
                  />
                ))}
              </div>
            </div>

            <div className="hidden h-16 w-px bg-neutral-200 sm:block" />

            <div className="flex flex-col gap-4">
              <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                Top tier quality 5/5
              </span>
              <div className="flex items-center gap-1">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} className="size-5 text-[#FFB648] fill-[#FFB648]" />
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Right side: infinite client marquee */}
        <section
          aria-label="Upcoming client calls"
          className="relative h-[600px] overflow-hidden lg:h-full"
        >
          <div className="pointer-events-none absolute inset-x-0 top-0 z-10 h-20 bg-gradient-to-b from-[#F7F7F7] to-transparent sm:h-40" />
          <div className="pointer-events-none absolute inset-x-0 bottom-0 z-10 h-20 bg-gradient-to-t from-[#F7F7F7] to-transparent sm:h-40" />

          <div className="grid grid-cols-1 gap-6 px-2 md:grid-cols-2 lg:grid-cols-1">
            <motion.div
              className="flex flex-col gap-6 py-6"
              animate={{ y: [0, -1200] }}
              transition={{ repeat: Infinity, duration: 40, ease: "linear" }}
            >
              {LOOPED_CALLS.map((call, i) => (
                <ClientCard key={`a-${call.id}-${i}`} call={call} index={i} />
              ))}
            </motion.div>

            <motion.div
              className="hidden flex-col gap-6 py-6 md:flex lg:hidden"
              animate={{ y: [-600, -1800] }}
              transition={{ repeat: Infinity, duration: 40, ease: "linear" }}
            >
              {LOOPED_CALLS.map((call, i) => (
                <ClientCard key={`b-${call.id}-${i}`} call={call} index={i + 1} />
              ))}
            </motion.div>
          </div>
        </section>
      </main>
    </div>
  );
}
