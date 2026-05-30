import { AnalyzerBreakdown as Item } from "@/types/report";

export default function AnalyzerBreakdown({
  items,
}: {
  items: Item[];
}) {
  if (!items.length) return null;

  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-900 dark:ring-zinc-800">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-widest text-zinc-500">
        Analyzer Results
      </h3>

      <div className="space-y-3">
        {items.map((item) => (
          <div
            key={item.analyzer}
            className="flex justify-between"
          >
            <span>
              {item.analyzer}
            </span>

            <span>
              {item.findings}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}