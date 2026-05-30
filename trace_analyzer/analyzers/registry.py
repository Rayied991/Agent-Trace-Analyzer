from trace_analyzer.analyzers.redundancy import (
    RedundancyAnalyzer,
)
from trace_analyzer.analyzers.token_efficiency import (
    TokenEfficiencyAnalyzer,
)
from trace_analyzer.analyzers.reasoning import (
    ReasoningAnalyzer,
)
from trace_analyzer.analyzers.latency import (
    LatencyAnalyzer,
)
ALL_ANALYZERS = [
    RedundancyAnalyzer(),
    TokenEfficiencyAnalyzer(),
    ReasoningAnalyzer(),
    LatencyAnalyzer(),
]