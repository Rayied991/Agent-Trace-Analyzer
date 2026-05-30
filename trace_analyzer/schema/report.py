from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# =========================================================
# Severity Levels
# =========================================================

class Severity(str, Enum):
    """
    Represents the severity level
    of an audit finding.
    """

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


# =========================================================
# Finding Categories
# =========================================================

class FindingCategory(str, Enum):
    """
    Represents the category/type
    of issue detected in the trace.
    """

    REDUNDANCY = "redundancy"
    REASONING = "reasoning"
    TOKEN_WASTE = "token_waste"
    HALLUCINATION = "hallucination"
    RETRY_STORM = "retry_storm"
    CONTEXT_BLOAT = "context_bloat"
    WORKFLOW = "workflow"
    LATENCY = "latency"
    TOOLING = "tooling"
    EFFICIENCY = "efficiency"
    REASONING_GAP = "reasoning_gap"


# =========================================================
# Individual Finding
# =========================================================

class Finding(BaseModel):
    """
    Represents a single issue detected
    during trace analysis.
    """

    # -----------------------------
    # Core Identity
    # -----------------------------
    finding_id: str = Field(
        ...,
        description="Unique identifier for the finding"
    )

    severity: Severity = Field(
        ...,
        description="Severity level of the finding"
    )

    category: FindingCategory = Field(
        ...,
        description="Category/type of finding"
    )

    # -----------------------------
    # Human Readable Information
    # -----------------------------
    title: str = Field(
        ...,
        description="Short summary title"
    )

    description: str = Field(
        ...,
        description="Detailed description of the issue"
    )

    # -----------------------------
    # Trace References
    # -----------------------------
    affected_steps: List[str] = Field(
        default_factory=list,
        description="List of affected step IDs"
    )

    # -----------------------------
    # Optimization Metrics
    # -----------------------------
    token_impact: Optional[int] = Field(
        default=None,
        ge=0,
        description="Estimated wasted tokens"
    )
    
    reliability_impact: Optional[int] = Field(
    default=None,
    ge=0,
    description="Estimated reliability impact score"
    )

    cost_impact_usd: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated cost impact in USD"
    )

    latency_impact_ms: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated latency impact in milliseconds"
    )

    # -----------------------------
    # Recommendations
    # -----------------------------
    recommendation: Optional[str] = Field(
        default=None,
        description="Suggested fix or optimization"
    )

    # -----------------------------
    # Supporting Evidence
    # -----------------------------
    evidence: Optional[str] = Field(
        default=None,
        description="Supporting trace evidence"
    )

    # -----------------------------
    # Additional Metadata
    # -----------------------------
    metadata: dict = Field(
        default_factory=dict,
        description="Additional metadata"
    )

    model_config = {
        "extra": "allow",
        "validate_assignment": True,
        "frozen": False
    }


# =========================================================
# Report Summary
# =========================================================

class ReportSummary(BaseModel):
    """
    Aggregated summary statistics
    for the audit report.
    """

    total_steps: int = Field(
        default=0,
        ge=0,
        description="Total number of execution steps"
    )

    total_findings: int = Field(
        default=0,
        ge=0,
        description="Total findings detected"
    )

    critical_count: int = Field(
        default=0,
        ge=0,
        description="Critical findings count"
    )

    warning_count: int = Field(
        default=0,
        ge=0,
        description="Warning findings count"
    )

    info_count: int = Field(
        default=0,
        ge=0,
        description="Info findings count"
    )
    
    quality_issues: int = Field(
    default=0,
    ge=0,
    description="Number of reliability issues detected"
)

    reliability_score: float = Field(
    default=100.0,
    ge=0,
    le=100,
    description="Overall reliability score"
    )

    total_tokens: int = Field(
        default=0,
        ge=0,
        description="Total tokens consumed"
    )

    wasted_tokens: int = Field(
        default=0,
        ge=0,
        description="Estimated wasted tokens"
    )

    waste_percentage: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Estimated waste percentage"
    )

    total_cost_usd: float = Field(
        default=0.0,
        ge=0,
        description="Total execution cost"
    )

    projected_savings_usd: float = Field(
        default=0.0,
        ge=0,
        description="Estimated savings after optimization"
    )

    average_latency_ms: Optional[float] = Field(
        default=None,
        ge=0,
        description="Average step latency"
    )

    top_issue: Optional[str] = Field(
        default=None,
        description="Most severe or impactful issue"
    )

    model_config = {
        "extra": "allow",
        "validate_assignment": True,
        "frozen": False
    }


# =========================================================
# Full Audit Report
# =========================================================

class AuditReport(BaseModel):
    """
    Final structured audit report
    produced after analyzing a trace.
    """

    # -----------------------------
    # Report Identity
    # -----------------------------
    report_id: str = Field(
        ...,
        description="Unique report identifier"
    )

    trace_id: str = Field(
        ...,
        description="Associated trace ID"
    )

    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when report was generated"
    )

    # -----------------------------
    # Findings
    # -----------------------------
    findings: List[Finding] = Field(
        default_factory=list,
        description="List of audit findings"
    )

    # -----------------------------
    # Summary
    # -----------------------------
    summary: ReportSummary = Field(
        ...,
        description="Aggregated report summary"
    )

    # -----------------------------
    # Metadata
    # -----------------------------
    analyzer_version: Optional[str] = Field(
        default=None,
        description="Analyzer version"
    )

    generated_by: Optional[str] = Field(
        default=None,
        description="System/user that generated the report"
    )

    metadata: dict = Field(
        default_factory=dict,
        description="Additional report metadata"
    )

    

    model_config = {
        "extra": "allow",
        "validate_assignment": True,
        "frozen": False
    }

    # =====================================================
    # Helper Properties
    # =====================================================

    @property
    def has_critical_findings(self) -> bool:
        """
        Returns True if critical findings exist.
        """

        return any(
            finding.severity == Severity.CRITICAL
            for finding in self.findings
        )

    @property
    def total_findings_count(self) -> int:
        """
        Returns total findings count.
        """

        return len(self.findings)

    # =====================================================
    # Helper Methods
    # =====================================================

    def add_finding(self, finding: Finding) -> None:
        """
        Add a finding to the report.
        """

        self.findings.append(finding)

    def get_findings_by_severity(
        self,
        severity: Severity
    ) -> List[Finding]:
        """
        Retrieve findings filtered by severity.
        """

        return [
            finding
            for finding in self.findings
            if finding.severity == severity
        ]

    def get_findings_by_category(
        self,
        category: FindingCategory
    ) -> List[Finding]:
        """
        Retrieve findings filtered by category.
        """

        return [
            finding
            for finding in self.findings
            if finding.category == category
        ]