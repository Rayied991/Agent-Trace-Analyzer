"use client";

import { Finding } from "@/types/report";
import { useState } from "react";

type Filter = "all" | "critical" | "warning" | "info";

const SEVERITY_PILL: Record<string, string> = {
  critical: "bg-red-50 text-red-700 ring-1 ring-red-200",
  warning: "bg-amber-50 text-amber-700 ring-1 ring-amber-200",
  info: "bg-sky-50 text-sky-700 ring-1 ring-sky-200",
};

function impactLabel(finding: Finding): string | null {
  if (finding.token_impact != null) return `${finding.token_impact} tokens`;
  if (finding.reliability_impact != null) return `−${finding.reliability_impact} reliability`;
  if (finding.latency_impact_ms != null) return `${Math.round(finding.latency_impact_ms)} ms`;
  return null;
}

const TABS: { key: Filter; label: string }[] = [
  { key: "all", label: "All" },
  { key: "critical", label: "Critical" },
  { key: "warning", label: "Warning" },
  { key: "info", label: "Info" },
];

export default function FindingsTable({ findings }: { findings: Finding[] }) {
  const [filter, setFilter] = useState<Filter>("all");

  const visible = findings.filter((f) => filter === "all" || f.severity === filter);

  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-zinc-200">
      {/* Tab bar */}
      <div className="flex items-center gap-1 border-b border-zinc-100 px-4 py-2.5">
        <span className="mr-2 text-[10px] font-semibold uppercase tracking-widest text-zinc-400">
          Findings
        </span>
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={[
              "rounded-lg px-3 py-1 text-xs font-medium transition-colors",
              filter === tab.key
                ? "bg-zinc-900 text-white"
                : "text-zinc-500 hover:bg-zinc-100 hover:text-zinc-700",
            ].join(" ")}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Rows */}
      <div className="px-4 py-1">
        {visible.length === 0 ? (
          <p className="py-8 text-center text-sm text-zinc-400">No findings.</p>
        ) : (
          visible.map((finding, i) => (
            <div
              key={i}
              className="flex items-start gap-3 border-b border-zinc-100 py-3 last:border-0 transition-colors hover:bg-zinc-50 -mx-4 px-4"
            >
              <span
                className={`mt-0.5 rounded px-2 py-0.5 text-[11px] font-semibold capitalize ${
                  SEVERITY_PILL[finding.severity]
                }`}
              >
                {finding.severity}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-zinc-900">{finding.title}</p>
                <p className="mt-0.5 text-xs text-zinc-500">{finding.recommendation}</p>
              </div>
              {impactLabel(finding) && (
                <span className="shrink-0 text-xs text-zinc-400 mt-0.5">
                  {impactLabel(finding)}
                </span>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}