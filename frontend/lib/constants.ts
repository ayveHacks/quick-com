export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export const STORAGE_KEYS = {
  token: "gigprotect_token",
  worker: "gigprotect_worker",
};

export const DISRUPTION_COLORS: Record<string, string> = {
  rain: "#0ea5a4",
  flood: "#0284c7",
  traffic: "#f97316",
  heat: "#ef4444",
  pollution: "#84cc16",
  curfew: "#475569",
  strike: "#c2410c",
  store_outage: "#7c3aed",
  server_outage: "#dc2626",
  power_outage: "#0f766e",
};


