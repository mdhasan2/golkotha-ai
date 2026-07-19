
import streamlit as st

class StreamlitService:

    def __init__(self, predictor):

        self.predictor = predictor

    def visualize(self, features):
        
        st.title("⚽ GolKotha AI")

        if st.button("Predict Final"): 

            # Generate prediction
            probability = self.predictor.probability(features)

            argentina_prob = probability[1]
            spain_prob = probability[0]
            
            st.metric(
                "🇦🇷 Argentina Win Probability",
                f"{argentina_prob:.2%}"
            )
            st.progress(float(argentina_prob))
            st.metric(
                "🇪🇸 Spain Win Probability",
                f"{spain_prob:.2%}",
            )
            st.progress(float(spain_prob))
