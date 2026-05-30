"use client";

import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

interface Props {
  totalTokens: number;
  wastedTokens: number;
}

export default function TokenWasteChart({
  totalTokens,
  wastedTokens,
}: Props) {
  const usefulTokens =
  Math.max(
    0,
    totalTokens - wastedTokens
  );

const data = [
  {
    name: "Useful",
    value: usefulTokens,
    color: "#10b981",
  },
  {
    name: "Wasted",
    value: wastedTokens,
    color: "#ef4444",
  },
];

  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-widest text-zinc-500">
        Token Efficiency
      </h3>

      <div className="h-72">
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