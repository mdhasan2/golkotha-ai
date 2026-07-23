
import streamlit as st

from application.use_cases.predict_match import PredictMatch
from domain.models import MatchFeatures
from domain.rag_models import GroundedRecommendation

class StreamlitService:

    def __init__(self, predict_match: PredictMatch,) -> None: 

        self._predict_match = predict_match
    
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
         # You are here

    def visualize(self, features:MatchFeatures,) -> None:
        
        st.title("⚽ GolKotha AI")

        if st.button("Predict Final"): 

            # Generate prediction
            # probability = self.predictor.probability(features)

            prediction = self._predict_match.execute(features)

            print(prediction)

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

   
