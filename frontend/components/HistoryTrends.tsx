"use client";

import {
    CartesianGrid,
    Legend,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

interface TrendPoint {
  trace: string;
  reliability: number;
  tokens: number;
  waste: number;
  latency: number;
}

export default function HistoryTrends({
  data,
}: {
  data: TrendPoint[];
}) {
  if (!data.length) {
    return (
      <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-widest text-zinc-500">
          Historical Trends
        </h3>

        <div className="flex h-64 items-center justify-center text-sm text-zinc-400">
          Upload multiple traces to see trends.
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">
      <div className="mb-4">
        <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-500">
          Historical Trends
        </h3>

        <p className="mt-1 text-xs text-zinc-400">
          Reliability, tokens, waste, and latency across uploaded traces
        </p>
      </div>

      <div className="h-[420px]">
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <LineChart
            data={data}
            margin={{
              top: 10,
              right: 20,
              left: 0,
              bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="trace" />

            <YAxis />

            <Tooltip />

            <Legend />

            <Line
              type="monotone"
              dataKey="reliability"
              name="Reliability"
              stroke="#22c55e"
              strokeWidth={2}
            />

            <Line
              type="monotone"
              dataKey="tokens"
              name="Tokens"
              stroke="#3b82f6"
              strokeWidth={2}
            />

            <Line
              type="monotone"
              dataKey="waste"
              name="Waste %"
              stroke="#f59e0b"
              strokeWidth={2}
            />

            <Line
              type="monotone"
              dataKey="latency"
              name="Latency (ms)"
              stroke="#ef4444"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}