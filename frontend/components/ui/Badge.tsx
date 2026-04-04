import clsx from "clsx";
import { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  tone?: "neutral" | "good" | "alert" | "warn";
}

const toneClasses = {
  neutral: "bg-slate-100 text-slate-700",
  good: "bg-emerald-100 text-emerald-700",
  alert: "bg-rose-100 text-rose-700",
  warn: "bg-amber-100 text-amber-700",
};

export function Badge({ children, tone = "neutral" }: BadgeProps) {
  return (
    <span className={clsx("rounded-full px-3 py-1 text-xs font-semibold", toneClasses[tone])}>
      {children}
    </span>
  );
}


