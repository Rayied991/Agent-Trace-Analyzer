from trace_analyzer.analyzers.reasoning import (
    ReasoningAnalyzer,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
    StepType,
    TraceStep,
)


def test_unsupported_conclusion_detected():

    trace = NormalizedTrace(
        trace_id="reasoning-trace",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.LLM_CALL,
            content=(
                "Therefore the API supports OAuth2."
            ),
            input_tokens=100,
            output_tokens=50,
        )
    )

    analyzer = ReasoningAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 1

    assert findings[0].title == (
        "Unsupported conclusion detected"
    )


def test_supported_conclusion_not_flagged():

    trace = NormalizedTrace(
        trace_id="supported-trace",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.TOOL_RESULT,
            content="Retrieved API documentation.",
            tool_result=(
                "OAuth2 authentication supported."
            ),
        )
    )

    trace.add_step(
        TraceStep(
            step_id="2",
            step_type=StepType.LLM_CALL,
            content=(
                "Therefore the API supports OAuth2."
            ),
            input_tokens=100,
            output_tokens=50,
        )
    )

    analyzer = ReasoningAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 0


def test_normal_llm_text_not_flagged():

    trace = NormalizedTrace(
        trace_id="normal-trace",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.LLM_CALL,
            content=(
                "I will search for information."
            ),
            input_tokens=100,
            output_tokens=20,
        )
    )

    analyzer = ReasoningAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 0