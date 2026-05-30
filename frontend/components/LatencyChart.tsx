"use client";

import {
    Bar,
    BarChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

interface LatencyChartProps {
  data: {
    step: string;
    latency_ms: number;
  }[];
}

export default function LatencyChart({
  data,
}: LatencyChartProps) {
  if (!data.length) return null;

  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-widest text-zinc-500">
        Step Latencies
      </h3>

      <div className="h-72">
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="step" />

            <YAxis />

            <Tooltip
              formatter={(value) => [
                `${value} ms`,
                "Latency",
              ]}
            />

            <Bar
              dataKey="latency_ms"
              name="Latency (ms)"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}