
import pandas as pd
import streamlit as st



from api import SportsAPI
from app.container import PredictionContainer
from application.services.build_match_feaures import (
    build_match_features,
)
from presentation.session_state import (
    clear_previous_analysis,
)

def render_baseline_section(
        footballapi: SportsAPI,
        container: PredictionContainer,
) -> None:
    st.header("1. Baseline Model")

    st.write(
        "Run the original model and inspect its prediction "
        "and probability distribution. "
    )

    build_clicked = st.button(
        "⚽ Build Features & Predict",
        type="primary",
        use_container_width=True,
    )

    home_team="Argentina"
    away_team="Spain"

    if build_clicked:
        features = build_match_features(
            footballapi,
            home_team=home_team,
            away_team=away_team,
        )
        # print(features)

        clear_previous_analysis()

        try:
            prediction = container.predict_match.execute(
                features
            )

            st.session_state.prediction = prediction
            st.session_state.features = features

            st.session_state.home_team = home_team
            st.session_state.away_team = away_team

        except Exception as error:
            st.error(
                "The baseline prediction clould not "
                "be generated."
            )
            st.exception(error)
            return

    prediction = st.session_state.prediction

    if prediction is None:
        st.info(
            "Run the baseline model to view its results."
        )
        return

    st.subheader("Prediction results")

    argentina_probability = prediction.probability_for(1)
    spain_probability = prediction.probability_for(0)

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

    st.session_state.baseline_prediction = (prediction)

    prediction_column, confidence_column = st.columns(2)

    # print(prediction_column, confidence_column)

    with prediction_column:
        st.metric(
            "Prediction",
            prediction.predicted_label
        )

    with confidence_column:
        st.metric(
            "Confidence",
            prediction.probability_for(prediction.predicted_label)
        )

    probability_data = pd.DataFrame(
        {
            "Outcome": [
                        item.label
                        for item in prediction.probabilities
            ],
            "Probability": [
                float(item.probability)
                for item in prediction.probabilities
            ]
        }
    )

    st.subheader("Probability distribution")

    st.dataframe(
        probability_data,
        hide_index=True,
        width='stretch',
        column_config={
            "Probability": (
                st.column_config.ProgressColumn(
                    "Probability",
                    min_value=0.0,
                    max_value=1.0,
                    format="percent",
                )
            )
        }
    )
    