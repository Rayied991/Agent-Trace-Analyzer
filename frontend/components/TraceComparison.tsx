"use client";

import { analyzeTrace } from "@/lib/api";
import { AuditReport } from "@/types/report";
import { useCallback, useRef, useState } from "react";
import ComparisonCharts from "./ComparisonCharts";

type UploadState = "idle" | "dragging" | "loading" | "done" | "error";

interface UploadZoneProps {
  label: string;
  side: "A" | "B";
  state: UploadState;
  report: AuditReport | null;
  onFile: (file: File) => void;
}

function UploadZone({ label, side, state, report, onFile }: UploadZoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files?.[0];
      if (file?.name.endsWith(".json")) onFile(file);
    },
    [onFile]
  );

  const accentColor = side === "A" ? "#6366f1" : "#f59e0b";
  const accentBg = side === "A" ? "rgba(99,102,241,0.08)" : "rgba(245,158,11,0.08)";
  const accentBorder = side === "A" ? "rgba(99,102,241,0.4)" : "rgba(245,158,11,0.4)";

  return (
    <div
      className="upload-zone"
      style={{
        border: `1.5px dashed ${dragOver ? accentColor : accentBorder}`,
        borderRadius: "16px",
        padding: "32px 24px",
        background: dragOver ? accentBg : "rgba(255,255,255,0.03)",
        cursor: "pointer",
        transition: "all 0.2s ease",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "12px",
        position: "relative",
        minHeight: "180px",
        justifyContent: "center",
      }}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".json"
        style={{ display: "none" }}
        onChange={(e) => e.target.files?.[0] && onFile(e.target.files[0])}
      />

      {/* Side badge */}
      <div style={{
        position: "absolute",
        top: "12px",
        left: "16px",
        background: accentColor,
        color: "#fff",
        fontSize: "11px",
        fontWeight: 700,
        fontFamily: "'Space Mono', monospace",
        padding: "2px 10px",
        borderRadius: "99px",
        letterSpacing: "0.05em",
      }}>
        TRACE {side}
      </div>

      {state === "loading" ? (
        <>
          <Spinner color={accentColor} />
          <p style={{ color: "#94a3b8", fontSize: "13px", fontFamily: "'Space Mono', monospace" }}>
            Analyzing…
          </p>
        </>
      ) : state === "done" && report ? (
        <>
          <div style={{
            width: "44px", height: "44px", borderRadius: "50%",
            background: `${accentColor}22`, display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <CheckIcon color={accentColor} />
          </div>
          <p style={{ fontWeight: 600, fontSize: "14px", color: "#f1f5f9", fontFamily: "'DM Sans', sans-serif", textAlign: "center" }}>
            {label}
          </p>
          <p style={{ fontSize: "12px", color: "#64748b", fontFamily: "'Space Mono', monospace" }}>
            Click to replace
          </p>
        </>
      ) : (
        <>
          <UploadIcon color={accentColor} />
          <div style={{ textAlign: "center" }}>
            <p style={{ fontWeight: 600, color: "#e2e8f0", fontSize: "14px", fontFamily: "'DM Sans', sans-serif" }}>
              Drop JSON trace here
            </p>
            <p style={{ fontSize: "12px", color: "#475569", marginTop: "4px", fontFamily: "'Space Mono', monospace" }}>
              or click to browse
            </p>
          </div>
        </>
      )}
    </div>
  );
}

const METRICS = [
  { key: "reliability_score", label: "Reliability", higherIsBetter: true, suffix: "" },
  { key: "total_tokens", label: "Total Tokens", higherIsBetter: false, suffix: "" },
  { key: "wasted_tokens", label: "Wasted Tokens", higherIsBetter: false, suffix: "" },
  { key: "waste_percentage", label: "Waste %", higherIsBetter: false, suffix: "%" },
  { key: "total_findings", label: "Findings", higherIsBetter: false, suffix: "" },
  { key: "critical_count", label: "Critical", higherIsBetter: false, suffix: "" },
  { key: "warning_count", label: "Warning", higherIsBetter: false, suffix: "" },
  { key: "average_latency_ms", label: "Avg Latency", higherIsBetter: false, suffix: "ms" },
] as const;

type MetricKey = typeof METRICS[number]["key"];

function getWinner(
  left: number,
  right: number,
  higherIsBetter: boolean
): "left" | "right" | "tie" {
  if (left === right) return "tie";
  return higherIsBetter ? (left > right ? "left" : "right") : (left < right ? "left" : "right");
}

function MiniBar({ value, max, color }: { value: number; max: number; color: string }) {
  const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0;
  return (
    <div style={{
      height: "4px", width: "100%", background: "rgba(255,255,255,0.06)",
      borderRadius: "2px", marginTop: "6px", overflow: "hidden"
    }}>
      <div style={{
        height: "100%", width: `${pct}%`,
        background: color, borderRadius: "2px",
        transition: "width 0.6s cubic-bezier(0.4,0,0.2,1)",
      }} />
    </div>
  );
}

export default function TraceComparison() {
  const [left, setLeft] = useState<AuditReport | null>(null);
  const [right, setRight] = useState<AuditReport | null>(null);
  const [leftState, setLeftState] = useState<UploadState>("idle");
  const [rightState, setRightState] = useState<UploadState>("idle");
  const [leftName, setLeftName] = useState("");
  const [rightName, setRightName] = useState("");

  async function uploadLeft(file: File) {
    setLeftName(file.name);
    setLeftState("loading");
    try {
      setLeft(await analyzeTrace(file));
      setLeftState("done");
    } catch {
      setLeftState("error");
    }
  }

  async function uploadRight(file: File) {
    setRightName(file.name);
    setRightState("loading");
    try {
      setRight(await analyzeTrace(file));
      setRightState("done");
    } catch {
      setRightState("error");
    }
  }

  const bothReady = left && right;

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600;700&display=swap');

        .trace-row {
          transition: background 0.15s ease;
        }
        .trace-row:hover {
          background: rgba(255,255,255,0.03);
        }
        .winner-cell {
          position: relative;
        }
        .winner-cell::before {
          content: '';
          position: absolute;
          left: 0; top: 0; bottom: 0;
          width: 3px;
          border-radius: 0 2px 2px 0;
        }
        .winner-left::before { background: #6366f1; }
        .winner-right::before { background: #f59e0b; }
      `}</style>

      <div style={{ fontFamily: "'DM Sans', sans-serif" }}>

        {/* Upload Row */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "32px" }}>
          <UploadZone
            label={leftName}
            side="A"
            state={leftState}
            report={left}
            onFile={uploadLeft}
          />
          <UploadZone
            label={rightName}
            side="B"
            state={rightState}
            report={right}
            onFile={uploadRight}
          />
        </div>

        {/* Waiting hint */}
        {!bothReady && (
          <div style={{
            textAlign: "center", padding: "48px 0",
            color: "#334155", fontSize: "13px",
            fontFamily: "'Space Mono', monospace",
            letterSpacing: "0.05em",
          }}>
            {!left && !right
              ? "↑ upload two traces to compare"
              : "waiting for second trace…"}
          </div>
        )}

        {/* Comparison Table */}
        {bothReady && (
          <div style={{
            borderRadius: "18px",
            overflow: "hidden",
            border: "1px solid rgba(255,255,255,0.07)",
            background: "rgba(15,23,42,0.6)",
            backdropFilter: "blur(12px)",
            animation: "fadeUp 0.4s ease",
          }}>
            <style>{`
              @keyframes fadeUp {
                from { opacity: 0; transform: translateY(16px); }
                to   { opacity: 1; transform: translateY(0); }
              }
            `}</style>

            {/* Table header */}
            <div style={{
              display: "grid",
              gridTemplateColumns: "1.4fr 1fr 1fr",
              borderBottom: "1px solid rgba(255,255,255,0.07)",
              padding: "0",
            }}>
              {["METRIC", "TRACE A", "TRACE B"].map((h, i) => (
                <div key={h} style={{
                  padding: "14px 20px",
                  fontSize: "11px",
                  fontWeight: 700,
                  letterSpacing: "0.1em",
                  fontFamily: "'Space Mono', monospace",
                  color: i === 0 ? "#475569" : i === 1 ? "#6366f1" : "#f59e0b",
                  borderRight: i < 2 ? "1px solid rgba(255,255,255,0.05)" : undefined,
                }}>
                  {h}
                </div>
              ))}
            </div>

            {/* Metric rows */}
            {METRICS.map(({ key, label, higherIsBetter, suffix }, idx) => {
              const lv = left.summary[key as MetricKey] as number;
              const rv = right.summary[key as MetricKey] as number;
              const winner = getWinner(lv, rv, higherIsBetter);
              const maxVal = Math.max(lv, rv);

              return (
                <div
                  key={key}
                  className="trace-row"
                  style={{
                    display: "grid",
                    gridTemplateColumns: "1.4fr 1fr 1fr",
                    borderBottom: idx < METRICS.length - 1 ? "1px solid rgba(255,255,255,0.04)" : undefined,
                  }}
                >
                  {/* Metric label */}
                  <div style={{
                    padding: "16px 20px",
                    fontSize: "13px",
                    fontWeight: 500,
                    color: "#94a3b8",
                    borderRight: "1px solid rgba(255,255,255,0.05)",
                    display: "flex",
                    alignItems: "center",
                  }}>
                    {label}
                  </div>

                  {/* Left value */}
                  <div
                    className={winner === "left" ? "winner-cell winner-left" : "winner-cell"}
                    style={{
                      padding: "14px 20px",
                      borderRight: "1px solid rgba(255,255,255,0.05)",
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <span style={{
                        fontSize: "15px",
                        fontWeight: winner === "left" ? 700 : 400,
                        color: winner === "left" ? "#a5b4fc" : "#64748b",
                        fontFamily: "'Space Mono', monospace",
                        transition: "color 0.2s",
                      }}>
                        {lv}{suffix}
                      </span>
                      {winner === "left" && <WinBadge color="#6366f1" />}
                    </div>
                    <MiniBar value={lv} max={maxVal} color={winner === "left" ? "#6366f1" : "#1e293b"} />
                  </div>

                  {/* Right value */}
                  <div
                    className={winner === "right" ? "winner-cell winner-right" : "winner-cell"}
                    style={{ padding: "14px 20px" }}
                  >
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <span style={{
                        fontSize: "15px",
                        fontWeight: winner === "right" ? 700 : 400,
                        color: winner === "right" ? "#fcd34d" : "#64748b",
                        fontFamily: "'Space Mono', monospace",
                        transition: "color 0.2s",
                      }}>
                        {rv}{suffix}
                      </span>
                      {winner === "right" && <WinBadge color="#f59e0b" />}
                    </div>
                    <MiniBar value={rv} max={maxVal} color={winner === "right" ? "#f59e0b" : "#1e293b"} />
                  </div>
                </div>
              );
            })}

            {/* Footer summary */}
            <ComparisonSummary left={left} right={right} />
          </div>
        )}
     {bothReady && (
  <div className="mt-8">
    <ComparisonCharts
      reliabilityA={
        left.summary.reliability_score
      }
      reliabilityB={
        right.summary.reliability_score
      }

      tokensA={
        left.summary.total_tokens
      }
      tokensB={
        right.summary.total_tokens
      }

      wasteA={
        left.summary.waste_percentage
      }
      wasteB={
        right.summary.waste_percentage
      }

      latencyA={
        left.summary.average_latency_ms ?? 0
      }
      latencyB={
        right.summary.average_latency_ms ?? 0
      }
    />
  </div>
)}
      </div>
    </>
  );
}

function ComparisonSummary({ left, right }: { left: AuditReport; right: AuditReport }) {
  let aWins = 0, bWins = 0;
  METRICS.forEach(({ key, higherIsBetter }) => {
    const lv = left.summary[key as MetricKey] as number;
    const rv = right.summary[key as MetricKey] as number;
    const w = getWinner(lv, rv, higherIsBetter);
    if (w === "left") aWins++;
    if (w === "right") bWins++;
  });

  const overallWinner = aWins > bWins ? "A" : bWins > aWins ? "B" : null;
  const winnerColor = overallWinner === "A" ? "#6366f1" : overallWinner === "B" ? "#f59e0b" : "#64748b";

  return (
    <div style={{
      padding: "18px 20px",
      background: "rgba(255,255,255,0.02)",
      borderTop: "1px solid rgba(255,255,255,0.07)",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    }}>
      <div style={{ display: "flex", gap: "24px" }}>
        <span style={{ fontSize: "12px", fontFamily: "'Space Mono', monospace", color: "#6366f1" }}>
          A wins: {aWins}
        </span>
        <span style={{ fontSize: "12px", fontFamily: "'Space Mono', monospace", color: "#f59e0b" }}>
          B wins: {bWins}
        </span>
      </div>
      <div style={{
        fontSize: "12px",
        fontFamily: "'Space Mono', monospace",
        fontWeight: 700,
        color: winnerColor,
        padding: "4px 14px",
        border: `1px solid ${winnerColor}44`,
        borderRadius: "99px",
        background: `${winnerColor}11`,
      }}>
        {overallWinner ? `TRACE ${overallWinner} WINS` : "TIE"}
      </div>
    </div>
  );
}

// ─── Icons ────────────────────────────────────────────────────────────────────

function UploadIcon({ color }: { color: string }) {
  return (
    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="16 16 12 12 8 16" />
      <line x1="12" y1="12" x2="12" y2="21" />
      <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" />
    </svg>
  );
}

function CheckIcon({ color }: { color: string }) {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

function WinBadge({ color }: { color: string }) {
  return (
    <span style={{
      fontSize: "9px",
      fontWeight: 700,
      fontFamily: "'Space Mono', monospace",
      color,
      background: `${color}1a`,
      border: `1px solid ${color}44`,
      borderRadius: "4px",
      padding: "1px 5px",
      letterSpacing: "0.05em",
    }}>
      WIN
    </span>
  );
}

function Spinner({ color }: { color: string }) {
  return (
    <>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        .spin-ring { animation: spin 0.8s linear infinite; }
      `}</style>
      <svg className="spin-ring" width="32" height="32" viewBox="0 0 32 32" fill="none">
        <circle cx="16" cy="16" r="13" stroke="rgba(255,255,255,0.08)" strokeWidth="3" />
        <path d="M16 3 a13 13 0 0 1 13 13" stroke={color} strokeWidth="3" strokeLinecap="round" />
      </svg>
    </>
  );
}