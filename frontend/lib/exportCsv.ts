import { Finding } from "@/types/report";

export function exportFindingsCsv(
  findings: Finding[]
) {
  const rows = [
    [
      "Severity",
      "Title",
      "Category",
      "Recommendation",
      "Token Impact",
      "Reliability Impact",
    ],
    ...findings.map((f) => [
      f.severity,
      f.title,
      f.category,
      f.recommendation ?? "",
      f.token_impact ?? "",
      f.reliability_impact ?? "",
    ]),
  ];

  const csv = rows
    .map((r) => r.join(","))
    .join("\n");

  const blob = new Blob(
    [csv],
    { type: "text/csv" }
  );

  const url =
    URL.createObjectURL(blob);

  const a =
    document.createElement("a");

  a.href = url;
  a.download = "findings.csv";
  a.click();

  URL.revokeObjectURL(url);
}