import streamlit as st

from api import SportsAPI
from app.container import PredictionContainer
from application.services.build_match_feaures import (
    build_match_features,
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
        "Build Features and Predict",
        type="primary",
        use_container_width=True,
    )

    if build_clicked:
        features = build_match_features(
            footballapi,
            home_team="Argentina",
            away_team="Spain",
        )
        print(features)