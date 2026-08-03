from typing import Protocol

from domain.monitoring_models import RAGInteraction

class MonitoringRepositoryPort(Protocol):

    def save_interaction(
        self,
        interaction: RAGInteraction,
    ) -> None:
        ...