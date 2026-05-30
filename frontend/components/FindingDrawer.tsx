"use client";

import { Finding } from "@/types/report";
import { toast } from "sonner";
interface FindingDrawerProps {
  finding: Finding | null;
  onClose: () => void;
}

async function copyText(
  value: string
) {
  await navigator.clipboard.writeText(
    value
  );

  toast.success(
    "Copied to clipboard"
  );
}

export default function FindingDrawer({
  finding,
  onClose,
}: FindingDrawerProps) {
  if (!finding) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-40 bg-black/30"
        onClick={onClose}
      />

      {/* Drawer */}
      <div className="fixed right-0 top-0 z-50 h-full w-full max-w-xl overflow-y-auto bg-white p-6 shadow-2xl dark:bg-zinc-900">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-100">
            Finding Details
          </h2>

          <button
            onClick={onClose}
            className="rounded-lg px-3 py-2 text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800"
          >
            ✕
          </button>
        </div>

        {/* Title */}
        <section className="mb-6">
          <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
            Title
          </p>

          <p className="mt-2 text-lg font-semibold text-zinc-900 dark:text-zinc-100">
            {finding.title}
          </p>
        </section>

        {/* Description */}
        <section className="mb-6">
          <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
            Description
          </p>

          <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
            {finding.description}
          </p>
        </section>

        {/* Evidence */}
        {finding.evidence && (
          <section className="mb-6">
            <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
              Evidence
            </p>

            <pre className="mt-2 overflow-x-auto rounded-lg bg-zinc-100 p-3 text-xs text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
              {finding.evidence}
            </pre>

            <button
                onClick={() =>
                    copyText(
                    finding.evidence ?? ""
                    )
                }
                className="mb-2 text-xs text-blue-500"
                >
                Copy
                </button>
          </section>
        )}

        {/* Affected Steps */}
       {(finding.affected_steps?.length ?? 0) > 0 && (
            <section className="mb-6">
                <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
                Affected Steps
                </p>

                <div className="mt-2 flex flex-wrap gap-2">
                {finding.affected_steps!.map(
                    (step: string) => (
                    <span
                        key={step}
                        className="rounded-md bg-zinc-100 px-2 py-1 text-xs dark:bg-zinc-800"
                    >
                        {step}
                    </span>
                    )
                )}
                </div>
            </section>
            )} 

        {/* Metadata */}
{finding.metadata &&
  Object.keys(finding.metadata).length > 0 && (
    <section className="mb-6">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
          Metadata
        </p>

        <button
          onClick={() =>
            copyText(
              JSON.stringify(
                finding.metadata,
                null,
                2
              )
            )
          }
          className="text-xs text-blue-500 hover:text-blue-600"
        >
          Copy
        </button>
      </div>

      <pre className="mt-2 overflow-x-auto rounded-lg bg-zinc-100 p-3 text-xs text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
        {JSON.stringify(
          finding.metadata,
          null,
          2
        )}
      </pre>
    </section>
)}

        {/* Recommendation */}
        {finding.recommendation && (
          <section>
            <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
              Recommendation
            </p>

            <div className="mt-2 rounded-lg bg-emerald-50 p-4 text-sm text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-300">
              {finding.recommendation}
            </div>

            <button
                onClick={() =>
                    copyText(
                    finding.recommendation ?? ""
                    )
                }
                className="mb-2 text-xs text-blue-500"
                >
                Copy
                </button>
          </section>
        )}
      </div>
    </>
  );
}