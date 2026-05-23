from trace_analyzer.analyzers.redundancy import (
    RedundancyAnalyzer,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
    StepType,
    TraceStep,
)


def test_detects_duplicate_tool_calls():

    trace = NormalizedTrace(
        trace_id="trace-1",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.TOOL_CALL,
            content="Search weather",
            tool_name="search",
            tool_args={
                "query": "weather paris"
            },
            input_tokens=100,
            output_tokens=20,
        )
    )

    trace.add_step(
        TraceStep(
            step_id="2",
            step_type=StepType.TOOL_CALL,
            content="Search weather again",
            tool_name="search",
            tool_args={
                "query": "weather paris"
            },
            input_tokens=120,
            output_tokens=25,
        )
    )

    analyzer = RedundancyAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 1

    finding = findings[0]

    assert (
        finding.category.value
        == "redundancy"
    )

    assert (
        finding.token_impact
        == 145
    )


def test_unique_tool_calls_produce_no_findings():

    trace = NormalizedTrace(
        trace_id="trace-2",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.TOOL_CALL,
            content="Weather search",
            tool_name="search",
            tool_args={
                "query": "weather paris"
            },
        )
    )

    trace.add_step(
        TraceStep(
            step_id="2",
            step_type=StepType.TOOL_CALL,
            content="News search",
            tool_name="search",
            tool_args={
                "query": "latest AI news"
            },
        )
    )

    analyzer = RedundancyAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 0


def test_non_tool_steps_are_ignored():

    trace = NormalizedTrace(
        trace_id="trace-3",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.REASONING,
            content="Thinking about response",
        )
    )

    trace.add_step(
        TraceStep(
            step_id="2",
            step_type=StepType.LLM_CALL,
            content="LLM generation",
        )
    )

    analyzer = RedundancyAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 0


def test_empty_trace_returns_no_findings():

    trace = NormalizedTrace(
        trace_id="trace-4",
    )

    analyzer = RedundancyAnalyzer()

    findings = analyzer.analyze(trace)

    assert findings == []