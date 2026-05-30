"use client";

import {
    Bar,
    BarChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

interface ComparisonChartsProps {
  reliabilityA: number;
  reliabilityB: number;

  tokensA: number;
  tokensB: number;

  wasteA: number;
  wasteB: number;

  latencyA: number;
  latencyB: number;
}

function Chart({
  title,
  a,
  b,
}: {
  title: string;
  a: number;
  b: number;
}) {
  const data = [
    {
      name: "Trace A",
      value: a,
    },
    {
      name: "Trace B",
      value: b,
    },
  ];

  return (
    <div className="rounded-xl bg-white p-4 shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">
      <h3 className="mb-4 text-sm font-semibold">
        {title}
      </h3>

      <div className="h-56">
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function ComparisonCharts({
  reliabilityA,
  reliabilityB,
  tokensA,
  tokensB,
  wasteA,
  wasteB,
  latencyA,
  latencyB,
}: ComparisonChartsProps) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Chart
        title="Reliability Score"
        a={reliabilityA}
        b={reliabilityB}
      />

      <Chart
        title="Token Usage"
        a={tokensA}
        b={tokensB}
      />

      <Chart
        title="Waste Percentage"
        a={wasteA}
        b={wasteB}
      />

      <Chart
        title="Average Latency"
        a={latencyA}
        b={latencyB}
      />
    </div>
  );
}