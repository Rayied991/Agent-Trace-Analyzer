from trace_analyzer.analyzers.redundancy import (
    RedundancyAnalyzer,
)
from trace_analyzer.analyzers.token_efficiency import (
    TokenEfficiencyAnalyzer,
)
from trace_analyzer.analyzers.reasoning import (
    ReasoningAnalyzer,
)

ALL_ANALYZERS = [
    RedundancyAnalyzer(),
    TokenEfficiencyAnalyzer(),
    ReasoningAnalyzer(),
]