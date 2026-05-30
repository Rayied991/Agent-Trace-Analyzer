import TraceComparison from "@/components/TraceComparison";

export default function ComparePage() {
  return (
    <main className="min-h-screen p-8">
      <div className="mx-auto max-w-6xl">
        <h1 className="mb-8 text-4xl font-bold">
          Compare Traces
        </h1>

        <TraceComparison />
      </div>
    </main>
  );
}