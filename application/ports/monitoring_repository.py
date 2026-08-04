from typing import Any, Protocol

from domain.monitoring_models import RAGInteraction

class MonitoringRepositoryPort(Protocol):

    def save_interaction(
        self,
        interaction: RAGInteraction,
    ) -> None:
        ...

    def get_dashboard_metrics(
        self,
        limit: int = 1_000,
    ) -> dict[str, Any]:
        ...