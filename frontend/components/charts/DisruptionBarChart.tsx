"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface ChartRow {
  type: string;
  count: number;
  avg_severity: number;
}

export function DisruptionBarChart({ data }: { data: ChartRow[] }) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(15,23,42,0.14)" />
          <XAxis dataKey="type" tick={{ fontSize: 11 }} />
          <YAxis yAxisId="left" tick={{ fontSize: 11 }} />
          <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 11 }} />
          <Tooltip
            contentStyle={{
              borderRadius: 16,
              border: "1px solid #fff",
              background: "rgba(255,255,255,0.94)",
            }}
          />
          <Bar yAxisId="left" dataKey="count" fill="#0ea5a4" radius={[8, 8, 0, 0]} />
          <Bar yAxisId="right" dataKey="avg_severity" fill="#f97316" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}


