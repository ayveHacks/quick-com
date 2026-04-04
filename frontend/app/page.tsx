import Link from "next/link";
import { ArrowRight, CircleDollarSign, Radar, Shield, Zap } from "lucide-react";

import { Card } from "@/components/ui/Card";

const features = [
  {
    icon: <Radar className="h-5 w-5 text-teal-700" />,
    title: "Real-Time Parametric Triggers",
    description: "Weather, AQI, traffic, curfew, strike, store and server outages are monitored every cycle.",
  },
  {
    icon: <Zap className="h-5 w-5 text-orange-700" />,
    title: "Zero-Touch Claim Lifecycle",
    description: "No manual claim filing. Disruption events route directly to eligibility checks and payouts.",
  },
  {
    icon: <Shield className="h-5 w-5 text-emerald-700" />,
    title: "AI Fraud Scoring",
    description: "Multi-signal risk scoring combines GPS consistency, network anomalies, and activity mismatch.",
  },
  {
    icon: <CircleDollarSign className="h-5 w-5 text-rose-700" />,
    title: "Adaptive Pricing Engine",
    description: "Risk, exposure, and reliability continuously reprice premium and coverage for each worker.",
  },
];

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="glass relative overflow-hidden rounded-3xl border border-white/70 p-8 shadow-glow lg:p-12">
        <div className="absolute -right-16 -top-12 h-52 w-52 rounded-full bg-amber-300/40 blur-3xl" />
        <div className="absolute -bottom-16 left-1/3 h-56 w-56 rounded-full bg-teal-300/35 blur-3xl" />

        <p className="mb-4 inline-flex items-center rounded-full border border-orange-200 bg-orange-100/80 px-4 py-1 text-xs font-semibold uppercase tracking-widest text-orange-800">
          Production-Ready Fintech Insurance Simulation
        </p>
        <h1 className="max-w-4xl text-4xl font-extrabold leading-tight text-slate-900 lg:text-6xl" style={{ fontFamily: "var(--font-heading)" }}>
          GigProtect AI: autonomous parametric insurance for quick-commerce delivery partners.
        </h1>
        <p className="mt-5 max-w-3xl text-lg text-slate-700">
          Built for Blinkit, Zepto, and Instamart worker scenarios with instant payout simulation, fraud controls,
          and full-stack monitoring pipelines.
        </p>

        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            href="/worker"
            className="inline-flex items-center gap-2 rounded-full bg-ocean px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-700"
          >
            Launch Worker Dashboard
            <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="/admin"
            className="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white/80 px-6 py-3 text-sm font-semibold text-slate-800 transition hover:bg-white"
          >
            Open Admin Control Room
          </Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {features.map((feature) => (
          <Card key={feature.title} className="h-full">
            <div className="mb-3 inline-flex rounded-xl bg-white/90 p-2 shadow-sm">{feature.icon}</div>
            <h3 className="text-lg font-bold text-slate-900" style={{ fontFamily: "var(--font-heading)" }}>
              {feature.title}
            </h3>
            <p className="mt-2 text-sm text-slate-600">{feature.description}</p>
          </Card>
        ))}
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <Card>
          <h2 className="text-xl font-bold text-slate-900" style={{ fontFamily: "var(--font-heading)" }}>
            End-to-End Automation
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            Registration to policy pricing to disruption monitoring to claim adjudication to UPI payout simulation.
          </p>
        </Card>
        <Card>
          <h2 className="text-xl font-bold text-slate-900" style={{ fontFamily: "var(--font-heading)" }}>
            Judge-Ready Demonstration
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            Seed synthetic workers, run monitoring cycles, and trigger disruptions live from admin controls.
          </p>
        </Card>
        <Card>
          <h2 className="text-xl font-bold text-slate-900" style={{ fontFamily: "var(--font-heading)" }}>
            Modular Micro-Engines
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            Dedicated engines for risk analytics, premium optimization, claim orchestration, and fraud defense.
          </p>
        </Card>
      </section>
    </div>
  );
}


