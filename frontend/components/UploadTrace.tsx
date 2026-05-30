"use client";

import { analyzeTrace, exportHtml } from "@/lib/api";
import type { AuditReport } from "@/types/report";
import { useCallback, useRef, useState } from "react";
import FindingsTable from "./FindingsTable";
import SeverityChart from "./SeverityChart";
import SeveritySummary from "./SeveritySummary";
import SummaryCards from "./SummaryCards";

type Stage = "idle" | "dragging" | "analyzing" | "done" | "error";

const ANALYSIS_STEPS = [
  "Parsing trace structure…",
  "Running token efficiency checks…",
  "Evaluating reliability patterns…",
  "Scoring error surface…",
  "Compiling findings…",
];

type StepState = "done" | "active" | "pending";

function StepItem({ label, state }: { label: string; state: StepState }) {
  return (
    <li className="flex items-center gap-3 text-sm">
      <span
        className={[
          "flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs transition-colors",
          state === "done"
            ? "bg-emerald-50 text-emerald-600 ring-1 ring-emerald-200"
            : state === "active"
            ? "bg-zinc-100"
            : "bg-zinc-50",
        ].join(" ")}
      >
        {state === "done" ? (
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
            <path d="M2 5l2.5 2.5L8 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        ) : state === "active" ? (
          <span className="h-3 w-3 animate-spin rounded-full border border-zinc-300 border-t-zinc-700" />
        ) : (
          <span className="h-1 w-1 rounded-full bg-zinc-300" />
        )}
      </span>
      <span
        className={
          state === "pending"
            ? "text-zinc-300"
            : state === "active"
            ? "text-zinc-800"
            : "text-zinc-500 dark:text-zinc-400"
        }
      >
        {label}
      </span>
    </li>
  );
}

export default function UploadTrace() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<AuditReport | null>(null);
  const [stage, setStage] = useState<Stage>("idle");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [analyzeStep, setAnalyzeStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const runWithFile = useCallback(async (f: File) => {
    if (!f.name.endsWith(".json")) {
      setErrorMsg("Please upload a .json file.");
      setStage("error");
      return;
    }
    setFile(f);
    setStage("analyzing");
    setAnalyzeStep(0);
    setProgress(0);
    setResult(null);
    setErrorMsg(null);

    let step = 0;
    const interval = setInterval(() => {
      step++;
      setAnalyzeStep(step);
      setProgress(Math.round((step / ANALYSIS_STEPS.length) * 100));
      if (step >= ANALYSIS_STEPS.length) clearInterval(interval);
    }, 460);

    try {
      const report = await analyzeTrace(f);
      clearInterval(interval);
      setAnalyzeStep(ANALYSIS_STEPS.length);
      setProgress(100);
      await new Promise((r) => setTimeout(r, 350));
      setResult(report);
      setStage("done");
    } catch (err) {
      clearInterval(interval);
      console.error(err);
      setErrorMsg("Analysis failed. Please try again.");
      setStage("error");
    }
  }, []);

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setStage("dragging");
  };
  const onDragLeave = () => {
    if (stage === "dragging") setStage("idle");
  };
  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const f = e.dataTransfer.files?.[0];
    if (f) runWithFile(f);
  };
  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) runWithFile(f);
  };

  const exportJson = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "trace_report.json";
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const exportHtmlReport = async () => {
    if (!file) return;
    try {
      const blob = await exportHtml(file);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "trace_report.html";
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
    }
  };

  const reset = () => {
    setStage("idle");
    setFile(null);
    setResult(null);
    setErrorMsg(null);
    setAnalyzeStep(0);
    setProgress(0);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const summary = result?.summary;
  const findings = result?.findings ?? [];
  const criticalCount = summary?.critical_count ?? findings.filter((f) => f.severity === "critical").length;
  const warningCount = summary?.warning_count ?? findings.filter((f) => f.severity === "warning").length;
  const infoCount = summary?.info_count ?? findings.filter((f) => f.severity === "info").length;

  const isUpload = stage === "idle" || stage === "dragging" || stage === "error";

  return (
    <div className="mt-8 space-y-4">

      {/* ── Upload / Error ── */}
      {isUpload && (
        <div className="rounded-2xl bg-white dark:bg-zinc-900 p-6 shadow-sm ring-1 ring-zinc-200 dark:ring-zinc-800">
          <div
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => fileInputRef.current?.click()}
            tabIndex={0}
            role="button"
            aria-label="Upload trace JSON file"
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") fileInputRef.current?.click();
            }}
            className={[
              "flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-8 py-14 transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-zinc-400",
              stage === "dragging"
                ? "scale-[1.012] border-zinc-900 bg-zinc-50"
                : "border-zinc-200 dark:border-zinc-700 hover:border-zinc-400 hover:bg-zinc-50",
            ].join(" ")}
          >
            <svg
              className={[
                "mb-3 h-7 w-7 transition-transform duration-200",
                stage === "dragging" ? "-translate-y-1 text-zinc-700" : "text-zinc-300",
              ].join(" ")}
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M12 16V4m0 0-3.5 3.5M12 4l3.5 3.5" />
              <path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />
            </svg>
            <p className="text-sm font-semibold text-zinc-700">Drop your trace file here</p>
            <p className="mt-1 text-xs text-zinc-400">or click to browse · .json only</p>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept=".json"
            className="hidden"
            onChange={onFileChange}
          />

          {errorMsg && (
            <div className="mt-4 flex items-center gap-2 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600 ring-1 ring-red-200">
              <svg className="h-4 w-4 shrink-0" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm0 4a.75.75 0 0 1 .75.75v3a.75.75 0 0 1-1.5 0v-3A.75.75 0 0 1 8 5zm0 6.5a.875.875 0 1 1 0-1.75.875.875 0 0 1 0 1.75z" />
              </svg>
              {errorMsg}
            </div>
          )}
        </div>
      )}

      {/* ── Analyzing ── */}
      {stage === "analyzing" && (
        <div className="rounded-2xl bg-white dark:bg-zinc-900 p-8 shadow-sm ring-1 ring-zinc-200 dark:ring-zinc-800">
          <p className="mb-5 text-sm font-medium text-zinc-500 dark:text-zinc-400">
            Analyzing{" "}
            <span className="font-mono text-zinc-900 dark:text-zinc-100">{file?.name}</span>
          </p>

          <div className="mb-7 h-1.5 overflow-hidden rounded-full bg-zinc-100">
            <div
              className="h-full rounded-full bg-zinc-900 transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>

          <ul className="space-y-3">
            {ANALYSIS_STEPS.map((label, i) => {
              const state: StepState =
                i < analyzeStep ? "done" : i === analyzeStep ? "active" : "pending";
              return <StepItem key={i} label={label} state={state} />;
            })}
          </ul>
        </div>
      )}

      {/* ── Result ── */}
      {stage === "done" && result && (
        <>
          {/* Header */}
          <div className="flex items-center justify-between rounded-2xl bg-white dark:bg-zinc-900 px-6 py-4 shadow-sm ring-1 ring-zinc-200 dark:ring-zinc-800">
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400">
                Trace ID
              </p>
              <p className="font-mono font-semibold text-zinc-900 dark:text-zinc-100">{result.trace_id}</p>
            </div>
            <button
              onClick={reset}
              className="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm text-zinc-500 dark:text-zinc-400 ring-1 ring-zinc-200 dark:ring-zinc-800 transition hover:bg-zinc-50 hover:text-zinc-800"
            >
              <svg className="h-3.5 w-3.5" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M13.5 8A5.5 5.5 0 1 1 8 2.5a5.47 5.47 0 0 1 3.5 1.27" />
                <path d="M13.5 2.5v3h-3" />
              </svg>
              New trace
            </button>
          </div>

          {summary && <SummaryCards summary={summary} />}

          {/* <SeverityChart critical={criticalCount} warning={warningCount} info={infoCount} /> */}
          <div className="grid gap-4 lg:grid-cols-3">

              <div className="lg:col-span-2">
                <SeverityChart
                  critical={criticalCount}
                  warning={warningCount}
                  info={infoCount}
                />
              </div>

              <SeveritySummary
                critical={criticalCount}
                warning={warningCount}
                info={infoCount}
              />

            </div>

          <FindingsTable findings={findings} />

          {summary?.top_issue && (
            <div className="rounded-xl bg-amber-50 px-5 py-4 ring-1 ring-amber-200">
              <p className="text-[10px] font-semibold uppercase tracking-widest text-amber-500">
                Top Issue
              </p>
              <p className="mt-1 text-sm font-medium text-amber-800">{summary.top_issue}</p>
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={exportJson}
              className="flex flex-1 items-center justify-center gap-2 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-50"
            >
              <svg className="h-4 w-4" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M8 2v8m0 0-3-3m3 3 3-3M3 13h10" />
              </svg>
              Export JSON
            </button>
            <button
              onClick={exportHtmlReport}
              className="flex flex-1 items-center justify-center gap-2 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-50"
            >
              <svg className="h-4 w-4" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 6l-2 2 2 2M12 6l2 2-2 2M9 3l-2 10" />
              </svg>
              Export HTML
            </button>
            <button
              onClick={reset}
              className="flex-1 rounded-xl bg-zinc-900 py-3 text-sm font-medium text-white transition hover:bg-zinc-700"
            >
              Analyze another
            </button>
          </div>
        </>
      )}
    </div>
  );
}