import {
    getReport,
} from "@/lib/api";

import SummaryCards from "@/components/SummaryCards";

import FindingsTable from "@/components/FindingsTable";

export default async function ReportPage({
  params,
}: {
  params: Promise<{
    id: string;
  }>;
}) {
  const { id } =
    await params;

  const report =
    await getReport(id);

  return (
    <main className="mx-auto max-w-7xl p-6">
      <h1 className="mb-6 text-3xl font-bold">
        Shared Report
      </h1>

      <SummaryCards
        summary={
          report.summary
        }
      />

      <div className="mt-6">
        <FindingsTable
          findings={
            report.findings
          }
        />
      </div>
    </main>
  );
}