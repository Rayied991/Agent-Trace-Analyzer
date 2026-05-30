import json

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)

from backend.api.models import HealthResponse

from trace_analyzer.adapters.json_adapter import (
    JSONTraceAdapter,
)
from trace_analyzer.analyzers.registry import (
    ALL_ANALYZERS,
)
from trace_analyzer.report.generator import (
    ReportGenerator,
)
app = FastAPI(
    title="Agent Trace Analyzer API"
)


@app.get(
    "/",
    response_model=HealthResponse,
)
def root():
    return HealthResponse(
        status="ok"
    )

@app.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    return HealthResponse(
        status="healthy"
    )
    
@app.post("/analyze")
async def analyze_trace(
    file: UploadFile = File(...)
):
    contents = await file.read()

    # -----------------------------
    # Parse JSON
    # -----------------------------

    try:
        raw_trace = json.loads(
            contents.decode("utf-8")
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON file",
        )

    # -----------------------------
    # Normalize Trace
    # -----------------------------

    try:

        adapter = JSONTraceAdapter()

        trace = adapter.parse(
            raw_trace
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    # -----------------------------
    # Run Analyzers
    # -----------------------------

    findings = []

    for analyzer in ALL_ANALYZERS:

        findings.extend(
            analyzer.analyze(trace)
        )

    # -----------------------------
    # Generate Report
    # -----------------------------

    report = ReportGenerator().generate(
        trace=trace,
        findings=findings,
    )

    return report.model_dump()