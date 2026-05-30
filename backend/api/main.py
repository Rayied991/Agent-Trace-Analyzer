import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)
from tempfile import NamedTemporaryFile
from pathlib import Path
from fastapi import Response
from backend.api.models import HealthResponse

from trace_analyzer.report.html_exporter import (
    HTMLReportExporter,
)
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/export/html")
async def export_html(
    file: UploadFile = File(...)
):
    contents = await file.read()

    raw_trace = json.loads(
        contents.decode("utf-8")
    )

    adapter = JSONTraceAdapter()

    trace = adapter.parse(raw_trace)

    findings = []

    for analyzer in ALL_ANALYZERS:
        findings.extend(
            analyzer.analyze(trace)
        )

    report = ReportGenerator().generate(
        trace=trace,
        findings=findings,
    )

    exporter = HTMLReportExporter()

    with NamedTemporaryFile(
        suffix=".html",
        delete=False,
    ) as tmp:

        exporter.export(
            report,
            tmp.name,
        )

        html = Path(
            tmp.name
        ).read_text(
            encoding="utf-8"
        )

    return Response(
        content=html,
        media_type="text/html",
        headers={
            "Content-Disposition":
            'attachment; filename="report.html"'
        },
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