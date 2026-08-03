from time import perf_counter
from typing import Any

from application.ports.monitoring_repository import (
    MonitoringRepositoryPort,
)

from application.models.recommendation_result import RecommendationResult
from domain.monitoring_models import RAGInteraction

from infrastructure.llm.llm_cost_calculator import LLMCostCalculator

class MonitoredRecommendationService:
    def __init__(
        self,
        *,
        recommendation_use_case: Any,
        monitoring_repository: MonitoringRepositoryPort,
        retrieval_strategy: str,
        prompt_strategy: str,
    ):
        self._recommendation_use_case = recommendation_use_case
        self._monitoring_repository = monitoring_repository
        self._retrieval_strategy = retrieval_strategy
        self._prompt_strategy = prompt_strategy
        self._cost_calculator = LLMCostCalculator()
    def execute(
        self,
        request: Any,
    ) -> RecommendationResult:
        total_start = perf_counter()

        try:
            recommendation = self._recommendation_use_case.execute(
                request=request,
            )

            total_latency_ms =(
                perf_counter() - total_start
            ) * 1000

            # print(recommendation)

            cost = self._cost_calculator.estimate(
                provider=recommendation.provider,
                model_name=recommendation.model_name,
                input_tokens=recommendation.input_tokens,
                output_tokens=recommendation.output_tokens,
            )

            interaction = RAGInteraction.create(
                user_query=request.user_question,
                # answer=self._answer(
                #     recommendation,
                # ),
                recommendation=recommendation,
                retrieval_strategy=self._retrieval_strategy,
                prompt_strategy=self._prompt_strategy,
                latency_ms=total_latency_ms,
                # retrieval_latency_ms=recommendation.retrieval_latency_ms,
                # llm_latency_ms=recommendation.llm_latency_ms,
                # input_tokens=int(
                #     getattr(
                #         recommendation,
                #         "input_tokens",
                #         0,
                #     )
                # ),
                # output_tokens=int(
                #     getattr(
                #         recommendation,
                #         "output_tokens",
                #         0,
                #     )
                # ),
                cost=cost,
                success=True,
                # error_message=error_message,
                # created_at=utc_now(),
                metadata={
                    "risk_level": getattr(
                        recommendation,
                        "risk_level",
                        "unknown",
                    ),
                },
            )

            self._monitoring_repository.save_interaction(
                interaction=interaction,
            )

            print(interaction)

            return RecommendationResult(
                recommendation=recommendation,
                interaction_id=interaction.interaction_id,
                latency_ms=total_latency_ms,
            )
        # except Exception as error:
        #     total_latency_ms =(
        #         perf_counter() - total_start
        #     ) * 1000

        #     interaction = RAGInteraction.create(
        #         user_query=context.user_question,
        #         recommendation=None,
        #         retrieval_strategy=self._retrieval_strategy,
        #         prompt_strategy=self._prompt_strategy,
        #         latency_ms=total_latency_ms,
        #         # llm_latency_ms=0.0,
        #         success=False,
        #         error_message=str(error),
        #         metadata={
        #             "risk_level": "unknown",
        #         },
        #     )

        #     print(interaction)
        except Exception as error:
            print(type(error))
            print(error)
            raise

    @staticmethod
    def _answer(
        recommendation: Any,
    ) -> str:
        if hasattr(
            recommendation,
            "summary",
        ):
            return str(
                recommendation.summary
            )
        return str(recommendation)
        

        