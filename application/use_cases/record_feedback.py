from application.ports.monitoring_repository import (
    MonitoringRepositoryPort
)
from domain.monitoring_models import UserFeedback

class RecordFeedback:
    def __init__(
        self,
        repository: MonitoringRepositoryPort,
    ) -> None:
        self.repository = repository

    def has_feedback(
        self,
        interaction_id: str,
    ) -> bool:
        return self.repository.feedback_exists(
            interaction_id
        )

    def execute(
        self,
        *,
        interaction_id: str,
        rating: int,
        comment: str | None = None,
    ) -> UserFeedback:
        if self.repository.feedback_exists(
            interaction_id
        ):
            # raise ValueError(
            #     "Feedback has already been submitted "
            #     "for this response."
            # )
            return None


        feedback = UserFeedback.create(
            interaction_id=interaction_id,
            rating=rating,
            comment=comment,
        )

        self.repository.save_feedback(
            feedback
        )

        return feedback