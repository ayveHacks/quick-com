import { ReactNode } from "react";

interface MetricTileProps {
  title: string;
  value: string;
  hint?: string;
  icon?: ReactNode;
  valueClassName?: string;
  hintClassName?: string;
}

export function MetricTile({ title, value, hint, icon, valueClassName, hintClassName }: MetricTileProps) {
  return (
    <article className="glass rounded-2xl border border-white/60 p-4 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-xs uppercase tracking-widest text-slate-500">{title}</p>
        {icon}
      </div>
      <h3 className={`text-2xl font-semibold text-slate-900 ${valueClassName || ""}`.trim()}>{value}</h3>
      {hint ? <p className={`mt-1 text-sm text-slate-500 ${hintClassName || ""}`.trim()}>{hint}</p> : null}
    </article>
  );
}


