export interface Finding {
  finding_id: string;
  severity: "critical" | "warning" | "info";
  category: string;
  title: string;
  description: string;

  token_impact?: number | null;
  reliability_impact?: number | null;
  latency_impact_ms?: number | null;

  recommendation?: string | null;
}

export interface ReportSummary {
  total_steps: number;
  total_findings: number;

  critical_count: number;
  warning_count: number;
  info_count: number;

  quality_issues: number;
  reliability_score: number;

  total_tokens: number;
  wasted_tokens: number;

  waste_percentage: number;

  average_latency_ms?: number | null;

  top_issue?: string | null;
}

export interface AuditReport {
  report_id: string;
  trace_id: string;

  findings: Finding[];
  summary: ReportSummary;

  analyzer_version: string;
  generated_by: string;
}