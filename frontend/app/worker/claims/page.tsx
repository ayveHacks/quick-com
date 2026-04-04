"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";

import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { getAuthToken, workerApi } from "@/lib/api";
import { currencyINR, percent, prettyDate, titleCase } from "@/lib/format";
import { Claim } from "@/types";

export default function WorkerClaimsPage() {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const token = getAuthToken();

  useEffect(() => {
    const load = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      setLoading(true);
      try {
        const response = await workerApi.claims(token);
        setClaims(response.items as Claim[]);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load claims");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, [token]);

  const totals = useMemo(() => {
    const approved = claims.filter((claim) => claim.status === "approved");
    return {
      total: claims.length,
      approved: approved.length,
      payout: approved.reduce((sum, claim) => sum + claim.payout_amount, 0),
    };
  }, [claims]);

  if (!token) {
    return (
      <Card>
        <h1 className="text-2xl font-bold" style={{ fontFamily: "var(--font-heading)" }}>
          Claims History
        </h1>
        <p className="mt-2 text-slate-600">Login from the Worker Console first to view claim records.</p>
        <Link href="/worker" className="mt-4 inline-block rounded-xl bg-ocean px-4 py-2 text-sm font-semibold text-white">
          Go to Worker Console
        </Link>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <section className="glass rounded-3xl border border-white/70 p-6">
        <h1 className="text-3xl font-extrabold" style={{ fontFamily: "var(--font-heading)" }}>
          Claim Ledger
        </h1>
        <p className="mt-2 text-sm text-slate-600">Every claim here was created automatically by disruption triggers.</p>

        <div className="mt-4 grid gap-3 md:grid-cols-3">
          <div className="rounded-2xl border border-white/60 bg-white/80 p-4">
            <p className="text-xs uppercase tracking-widest text-slate-500">Total Claims</p>
            <p className="mt-1 text-2xl font-semibold">{totals.total}</p>
          </div>
          <div className="rounded-2xl border border-white/60 bg-white/80 p-4">
            <p className="text-xs uppercase tracking-widest text-slate-500">Approved</p>
            <p className="mt-1 text-2xl font-semibold text-emerald-700">{totals.approved}</p>
          </div>
          <div className="rounded-2xl border border-white/60 bg-white/80 p-4">
            <p className="text-xs uppercase tracking-widest text-slate-500">Total Payout</p>
            <p className="mt-1 text-2xl font-semibold text-teal-700">{currencyINR(totals.payout)}</p>
          </div>
        </div>
      </section>

      {error ? <p className="rounded-lg bg-rose-100 px-3 py-2 text-sm text-rose-700">{error}</p> : null}
      {loading ? <p className="text-sm text-slate-500">Loading claims...</p> : null}

      <section className="space-y-3">
        {claims.map((claim) => (
          <Card key={claim._id || claim.id}>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div>
                <h2 className="font-bold text-slate-900">{titleCase(claim.disruption_type)}</h2>
                <p className="text-xs text-slate-500">{prettyDate(claim.created_at)}</p>
              </div>
              <Badge
                tone={
                  claim.status === "approved"
                    ? "good"
                    : claim.status === "under_review"
                      ? "warn"
                      : "alert"
                }
              >
                {titleCase(claim.status)}
              </Badge>
            </div>

            <div className="mt-3 grid gap-2 text-sm md:grid-cols-4">
              <p>
                Work Loss: <strong>{percent(claim.work_loss_ratio)}</strong>
              </p>
              <p>
                Fraud Risk: <strong>{percent(claim.fraud_risk_score)}</strong>
              </p>
              <p>
                Duration: <strong>{claim.duration_hours.toFixed(2)}h</strong>
              </p>
              <p>
                Payout: <strong>{currencyINR(claim.payout_amount)}</strong>
              </p>
            </div>
            <button className="mt-3 rounded-lg border border-slate-300 bg-white px-3 py-1 text-xs font-semibold text-slate-700">
              Download PDF Receipt (Coming Soon)
            </button>
            {claim.reason ? <p className="mt-2 text-sm text-slate-600">{claim.reason}</p> : null}
          </Card>
        ))}
      </section>
    </div>
  );
}


