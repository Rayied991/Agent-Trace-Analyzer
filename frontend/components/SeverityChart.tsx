"use client";

import {
    Cell,
    Pie,
    PieChart,
    ResponsiveContainer,
    Tooltip,
} from "recharts";

interface SeverityChartProps {
  critical: number;
  warning: number;
  info: number;
}

export default function SeverityChart({
  critical,
  warning,
  info,
}: SeverityChartProps) {
  const data = [
  {
    name: "Critical",
    value: critical,
    color: "#ef4444",
  },
  {
    name: "Warning",
    value: warning,
    color: "#f59e0b",
  },
  {
    name: "Info",
    value: info,
    color: "#3b82f6",
  },
].filter(
  (item) => item.value > 0
);
  return (
   <div className="
rounded-2xl
bg-white
p-5
shadow-sm
ring-1
ring-zinc-200

dark:bg-zinc-900
dark:ring-zinc-800
">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-widest text-zinc-500 dark:text-zinc-400">
        Severity Breakdown
      </h3>

      <div className="h-64">
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              outerRadius={90}
              label
            >
              {data.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={entry.color}
                />
              ))}
            </Pie>

            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}