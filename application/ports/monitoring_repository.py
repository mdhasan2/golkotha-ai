from typing import Any, Protocol

from domain.monitoring_models import RAGInteraction, UserFeedback

class MonitoringRepositoryPort(Protocol):

    def save_interaction(
        self,
        interaction: RAGInteraction,
    ) -> None:
        ...

    def save_feedback(
        self,
        feedback: UserFeedback,
    ) -> None:
        ...

    def feedback_exists(
        self,
        interaction_id: str,
    ) -> bool:
        ...

    def get_dashboard_metrics(
        self,
        limit: int = 1_000,
    ) -> dict[str, Any]:
        ...