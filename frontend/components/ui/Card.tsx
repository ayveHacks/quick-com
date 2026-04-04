import clsx from "clsx";
import { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <section className={clsx("glass rounded-2xl border border-white/60 p-5 shadow-lg", className)}>
      {children}
    </section>
  );
}


