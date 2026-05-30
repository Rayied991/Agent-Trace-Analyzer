interface Props {
  critical: number;
  warning: number;
  info: number;
}

export default function SeveritySummary({
  critical,
  warning,
  info,
}: Props) {
  const cards = [
    {
      label: "Critical",
      value: critical,
      className:
        "bg-red-50 text-red-700 ring-red-200",
    },
    {
      label: "Warning",
      value: warning,
      className:
        "bg-amber-50 text-amber-700 ring-amber-200",
    },
    {
      label: "Info",
      value: info,
      className:
        "bg-sky-50 text-sky-700 ring-sky-200",
    },
  ];

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
        Findings Breakdown
      </h3>

      <div className="space-y-3">
        {cards.map((card) => (
          <div
            key={card.label}
            className={`rounded-xl p-4 ring-1 ${card.className}`}
          >
            <p className="text-xs uppercase">
              {card.label}
            </p>

            <p className="mt-1 text-2xl font-bold">
              {card.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}