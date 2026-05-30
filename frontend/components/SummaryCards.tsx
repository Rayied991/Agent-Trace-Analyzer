import { ReportSummary } from "@/types/report";

function scoreColor(score: number) {
  if (score >= 90) return "text-emerald-600";
  if (score >= 70) return "text-amber-500";
  return "text-red-500";
}

function fmt(n: number) {
  return n.toLocaleString();
}

function MetricCard({
  label,
  value,
  sub,
  valueClass = "text-zinc-900",
}: {
  label: string;
  value: string;
  sub?: string;
  valueClass?: string;
}) {
  return (
    <div className="rounded-xl bg-zinc-50 px-5 py-4 ring-1 ring-zinc-100 transition hover:ring-zinc-200">
      <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400">
        {label}
      </p>
      <p className={`mt-1 text-2xl font-semibold leading-none ${valueClass}`}>
        {value}
      </p>
      {sub && <p className="mt-1.5 text-xs text-zinc-400">{sub}</p>}
    </div>
  );
}

export default function SummaryCards({ summary }: { summary: ReportSummary }) {
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-6">
      <MetricCard
        label="Reliability"
        value={`${summary.reliability_score}/100`}
        valueClass={scoreColor(summary.reliability_score)}
      />
      <MetricCard
        label="Total Steps"
        value={fmt(summary.total_steps)}
      />
      <MetricCard
        label="Total Tokens"
        value={fmt(summary.total_tokens)}
      />
      <MetricCard
        label="Avg Latency"
        value={`${Math.round(summary.average_latency_ms ?? 0)} ms`}
      />
      <MetricCard
        label="Wasted Tokens"
        value={`${summary.waste_percentage}%`}
        sub={`${fmt(summary.wasted_tokens)} tokens`}
        valueClass={summary.waste_percentage > 20 ? "text-red-500" : "text-zinc-900"}
      />
      <MetricCard
      label="Analyzers"
      value="4"
    />
    </div>
  );
}