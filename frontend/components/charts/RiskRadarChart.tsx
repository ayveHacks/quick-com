"use client";

import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

interface ProbabilityRow {
  disruption: string;
  probability: number;
}

export function RiskRadarChart({ data }: { data: ProbabilityRow[] }) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} outerRadius="72%">
          <PolarGrid stroke="rgba(15,23,42,0.2)" />
          <PolarAngleAxis dataKey="disruption" tick={{ fontSize: 12, fill: "#1f2937", fontWeight: 600 }} />
          <Radar dataKey="probability" stroke="#0ea5a4" fill="#0ea5a4" fillOpacity={0.5} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}


