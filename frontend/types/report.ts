
export interface Finding {
  finding_id: string;

  severity:
    | "critical"
    | "warning"
    | "info";

  category: string;

  title: string;

  description: string;

  recommendation?: string;

  evidence?: string;

  affected_steps?: string[];

  metadata?: Record<
    string,
    unknown
  >;

  token_impact?: number;

  reliability_impact?: number;

  latency_impact_ms?: number;

  cost_impact_usd?: number | null;
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

  total_cost_usd?: number;

projected_savings_usd?: number;
}
export interface AnalyzerBreakdown {
  analyzer: string;
  findings: number;
}
export interface AuditReport {
  report_id: string;
  trace_id: string;

  findings: Finding[];
  summary: ReportSummary;

  analyzer_version: string;
  generated_by: string;

  metadata?: {
    step_latencies?: {
      step: string;
      latency_ms: number;
    }[];
  };

  analyzer_breakdown?: AnalyzerBreakdown[];
}

