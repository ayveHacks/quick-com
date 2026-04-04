"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { getAuthToken, workerApi } from "@/lib/api";
import { percent, prettyDate, titleCase } from "@/lib/format";
import { Disruption } from "@/types";

export default function WorkerDisruptionsPage() {
  const [items, setItems] = useState<Disruption[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const token = getAuthToken();

  useEffect(() => {
    const load = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      setLoading(true);
      try {
        const response = await workerApi.disruptions(token);
        setItems(response.items as Disruption[]);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load disruptions");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, [token]);

  if (!token) {
    return (
      <Card>
        <h1 className="text-2xl font-bold" style={{ fontFamily: "var(--font-heading)" }}>
          Disruption Timeline
        </h1>
        <p className="mt-2 text-slate-600">Login from the Worker Console first to view zone disruptions.</p>
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
          Zone Disruption Timeline
        </h1>
        <p className="mt-2 text-sm text-slate-600">
          Events detected by weather, AQI, traffic, outage, and civic-signal monitors.
        </p>
      </section>

      {error ? <p className="rounded-lg bg-rose-100 px-3 py-2 text-sm text-rose-700">{error}</p> : null}
      {loading ? <p className="text-sm text-slate-500">Loading disruptions...</p> : null}

      <section className="space-y-3">
        {items.map((item) => (
          <Card key={item._id || item.id}>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div>
                <h2 className="font-bold text-slate-900">{titleCase(item.type)}</h2>
                <p className="text-xs text-slate-500">
                  {item.city} | {item.affected_zones.join(", ")}
                </p>
              </div>
              <Badge tone={item.severity > 0.7 ? "alert" : "warn"}>Severity {percent(item.severity)}</Badge>
            </div>

            <p className="mt-2 text-sm text-slate-600">
              {prettyDate(item.start_time)} to {prettyDate(item.end_time)}
            </p>
            <button className="mt-3 rounded-lg border border-slate-300 bg-white px-3 py-1 text-xs font-semibold text-slate-700">
              Download PDF Receipt (Coming Soon)
            </button>
          </Card>
        ))}
      </section>
    </div>
  );
}



