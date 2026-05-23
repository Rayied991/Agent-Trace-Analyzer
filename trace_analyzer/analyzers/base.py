from abc import ABC, abstractmethod

from trace_analyzer.schema.report import Finding
from trace_analyzer.schema.trace import NormalizedTrace


class Analyzer(ABC):
    """
    Base interface for all analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        trace: NormalizedTrace
    ) -> list[Finding]:
        """
        Analyze a trace and return findings.
        """
        pass