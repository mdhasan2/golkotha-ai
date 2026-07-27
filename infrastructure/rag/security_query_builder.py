from domain.rag_models import PredictionContext

class SecurityQueryBuilder:

    def build(
        self,
        context: PredictionContext,
        maximum_features: int = 10,
    ) -> str:
        important_feature_names = list(
            context.feature_values.keys()
        )[:maximum_features]

        feature_text = ",".join(
            important_feature_names
        ) or "not available"

        question = (
            context.user_question
            or (
                "What security controls, validation procedures,"
                "monitoring, governance, explainibility, and "
                "adversarial testing shold be implemented?"
            )
        )

        return "\n".join(
            [
                "AI and machine-learning secuirty guidance",
                f"model name: {context.model_name}",
                f"model type: {context.model_type}",
                (
                    "application purpose: predict the winner "
                    "of a football match"
                ),
                (
                    "current lifecycle stage: baseline machine-learning "
                    "model before explainability and adversarial testing"
                ),
                (
                    "explainability testing performed: no"
                ),
                f"model input features: {feature_text}",
                f"user security question: {question}",
                (
                    "Find guidance concerning AI risk mananagement," \
                    "model validation, secure ML development, input " \
                    "validation, adversarial testing, data integrity, " \
                    "monitoring, explainability, red teaming, RAG " \
                    "security, and deployment governance."
                )
            ]
        )
