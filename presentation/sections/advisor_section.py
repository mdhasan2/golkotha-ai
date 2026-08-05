from typing import Any

import streamlit as st

from app.container import AdvisorContainer
from application.use_cases.generate_security_recommendations import GenerateSecurityRecommendations
# from application.models.recommendation_result import RecommendationResult

from domain.rag_models import GroundedRecommendation
from domain.security_models import SecurityAssessmentRequest

from infrastructure.rag.monitored_recommendation_service import (
    MonitoredRecommendationService,
)

from presentation.sections.feedback_section import render_feedback_section

def render_advisor_section(
        container: AdvisorContainer,
) -> None:
    st.header("4. AI Security Advisor")

    st.warning(
        "This is a baseline-only security assessment. "
        "SHAP explainability and FGSM adversarial testing "
        "have not been performed."
    )

    prediction=st.session_state.prediction
    features=st.session_state.features

    if prediction is None or features is None:
         st.warning(
              "Run the baseline prediction first."
         )
         return

    request = SecurityAssessmentRequest(
            model_name="GolKotha XGBoost",
            model_type="XGBoostClassifier",
            model_version="1.0",

            home_team=st.session_state.home_team,
            away_team=st.session_state.away_team,

            prediction=prediction,
            features=features,

            user_question=(
                "What should I implement to make this model "
                "more secure and trustworthy?"
            ),
    )

    if st.button(
        "Generate Baseline Security Assesment",
        type="primary",
        use_container_width=True,
    ):
        try:
            # recommendation = (
            #     container
            #     .generate_security_recommendations
            #     .execute(request)
            # )
            result = (
                    container
                    .generate_security_recommendations
                    .execute(request)
            )

            
            st.session_state.security_recommendation = result.recommendation
            st.session_state.last_interaction_id = result.interaction_id

        except Exception as error:
            st.error(
                "The security assessment could not "
                "be generated."
            )
            st.exception(error)
            return

    recommendation = st.session_state.security_recommendation

    if recommendation is None:
        st.info(
            "Generate an assessment to retrieve grounded  "
            "AI security guidance."
        )
        return

    _render_recommendation(recommendation)

    render_feedback_section(
         container.
    )


def _render_recommendation(
    recommendation: GroundedRecommendation,
) -> None:
    summary_column, risk_column = st.columns(
         [3,1]
    )

    print(f"{summary_column} \n {risk_column}")

    with summary_column:
         st.subheader("Executive summary")
         st.write(recommendation.summary
    )
    
    with risk_column:
        st.subheader("Preliminary Risk")
        st.markdown(
             "### "
             + recommendation.risk_level.upper()
    )

    # st.write(recommendation.summary)

    if recommendation.findings:
         st.subheader("Findings")

         for finding in recommendation.findings:
              st.markdown(f" - {finding}")

    st.subheader("Recommended mitigations")

    for index, mitigation in enumerate(
        recommendation.recommendations,
        start=1
    ):
         st.markdown(
              f"**{index}.** {mitigation}"
         )

    st.subheader("Analysis Limitations")

    for index, limitation in enumerate(
        recommendation.limitations,
        start=1
    ):
         st.markdown(
              f"**{index}.** {limitation}"
         )

    _render_citations(
         recommendation.citations
    )

    with st.expander("Raw grounded response"):
            st.code(
                recommendation.raw_response,
                language="json",
        )

def _render_citations(
    citations: tuple[Any, ...]
) -> None:
    st.subheader("Supporting RAG references")

    if not citations:
        st.warning(
                "No supporting references were returned."
        )
        return

    for citation in citations:
        st.markdown(
            (
                f"- **[{citation.citation_id}] "
                f"{citation.title}** - "
                f"{citation.source_name}  \n"
                f"  {citation.source_url}"
            )
        )




        