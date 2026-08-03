
import streamlit as st

from api import SportsAPI
from app.container import(
     AdvisorContainer,
     MonitoringContainer,
     PredictionContainer,
)

from application.mapper.prediction_context_mapper import PredictionContextMapper
from application.use_cases.generate_security_recommendations import GenerateSecurityRecommendations
from application.use_cases.predict_match import PredictMatch
from domain.models import MatchFeatures
from domain.rag_models import GroundedRecommendation

from presentation.session_state import(
     initialize_session_state,
)

from presentation.sections.baseline_section import (
     render_baseline_section,
)

from presentation.sections.advisor_section import (
     render_advisor_section,
)

from presentation.sections.monitoring_section import(
     render_monitoring_section
)

class StreamlitService:

    # def __init__(self, predict_match: PredictMatch,) -> None: 
    def __init__(
        self,
        football_api: SportsAPI,
        prediction_container: PredictionContainer,
        advisor_container: AdvisorContainer,
        monitoring_container: MonitoringContainer,
    ) -> None:
        self._football_api = football_api
        self._prediction_container = (
              prediction_container
        )
        self._advisor_container = advisor_container
        self._monitoring_container = monitoring_container
        
    def run(self) -> None:

         st.set_page_config(
               page_title="GolKotha AI Security Lab",
               page_icon="🛡️",
               layout="wide"
          )
                   
         page = st.sidebar.radio(
              "Navigation",
              (
                   "AI Security Workbench",
                   "RAG Evaluation",
                   "Monitoring Dashboard",
              ),
         )

         if page == "AI Security Workbench":
               self.render_security_workbench()

         elif page == "RAG Evaluation":
               self.render_rag_evaluation()

         elif page == "Monitoring Dashboard":
              render_monitoring_section(
                    container=self._monitoring_container,
               )

    def render_security_workbench(self) -> None:

          initialize_session_state()
          
          st.title("🛡️ GolKotha AI Security Lab")

          st.write(
               "Inspect a baseline prediction and generate "
               "grounded AI security recommendations."
          )

          st.caption(
               "Current implementation: Baseline Model + RAG "
               "Security Advisor. SHAP and FGSM are planned."
          )

          (
               baseline_tab,
               explainability_tab,
               attack_tab,
               advisor_tab,
          ) = st.tabs(
               [
                    "📊 Baseline Model",
                    "🔍 Explainability",
                    "⚔️ Adversarial Attack",
                    "🛡️ AI Security Advisor",
               ]
          )

          with baseline_tab:
               render_baseline_section(
                    self._football_api,
                    container=self._prediction_container,
               )

          with advisor_tab:
               render_advisor_section(
                    container=self._advisor_container,
               )
     
    def render_rag_evaluation(self):
         ...

#     def render_monitoring_section(
#           container: MonitoringContainer,
#     ) -> None:
#          dashboard = Moni
         

         
    def security_question(self) -> str:
            return st.text_area(
                "Ask an AI security question",
                value=(
                    "What security, validation, mnitoring, and "
                    "governance controls should be implemented "
                    "before deploying this model?"
                ),
            )
        
    def display_security_recommendations(
              self,
              result: GroundedRecommendation,
    ) -> None:
        
        if st.button("Generate Security Recommendations"):
             
            st.subheader("AI Security Guidance")

            st.metric(
                "Current Security Assessment",
                result.risk_level.upper(),
            )

            st.write(result.summary)

            st.markdown("### Current Findings")

            for finding in result.findings:
                st.markdown(f" - {finding}")

            st.markdown("### Recommended Next Steps")

            for recommendation in result.recommendations:
                 st.markdown(f" - {recommendation}")

            st.markdown("### Analysis Limitations")

            for limitation in result.limitations:
                 st.markdown(f"- {limitation}")

            st.markdown("### Sources")

            for citation in result.citations:
                 st.markdown(
                      (
                           f"- **[{citation.citation_id}] "
                           f"{citation.title}** - "
                           f"{citation.source_name}  \n"
                           f"  {citation.source_url}"
                      )
                 )

            with st.expander("Raw grounded response"):
                 st.code(
                      result.raw_response,
                      language="json",
                 )

    def visualize(self, features:MatchFeatures,) -> None:
        
        st.title("⚽ GolKotha AI")

        if st.button("Predict Final"): 

            # Generate prediction
            # probability = self.predictor.probability(features)

            prediction = self._predict_match.execute(features)

            print(prediction)

            context = PredictionContextMapper().map(
                 model_name="GolKotha XGBoost",
                 model_type="XGBoostClassifier",
                 model_version="1.0",
                 home_team="Argentian",
                 away_team="Spain",
                 predicted_label=prediction.predicted_label,
                 predicted_team="Argentina",
                 confidence=prediction.probability_for(
                      prediction.predicted_label
                 ),
                 class_probabilities={
                    #   "Draw": prediction.probability_for(0),
                    "Spain": prediction.probability_for(0),
                    "Argentina": prediction.probability_for(1),
                    #   "Spain": prediction.probability_for(2),
                 },
                 feature_values=features.to_dict(),
                 user_question=(
                      "What should I implement to make this model "
                      "more secure and trustworthy?"
                 ),
            )
            # self._generate_security_recommendations=GenerateSecurityRecommendations()
            # recommendations = (
            #         self._generate_security_recommendations.execute(context)
            #      )

            # argentina_prob = probability[1]
            # spain_prob = probability[0]

            # Keep these labels aligned with model.classes_.

            spain_probability = prediction.probability_for(0)
            argentina_probability = prediction.probability_for(1)
            
            st.metric(
                "🇦🇷 Argentina Win Probability",
                f"{argentina_probability:.2%}"
            )
            st.progress(float(argentina_probability))
            st.metric(
                "🇪🇸 Spain Win Probability",
                f"{spain_probability:.2%}",
            )
            st.progress(float(spain_probability))



   
