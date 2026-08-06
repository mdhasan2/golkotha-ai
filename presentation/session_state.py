
from typing import Any

import streamlit as st

DEFAULT_STATE: dict[str, Any] = {
    "prediction": None,
    "features": None,

    "home_team": None,
    "away_team": None,

    "security_recommendation": None,
    "last_interaction_id": None,
}

def initialize_session_state() -> None:
    for key, default_value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def clear_previous_analysis() -> None:
    print("CLEARING ANALYSIS")
    st.session_state.baseline_prediction = None
    st.session_state.baseline_features = None

    st.session_state.security_recommendation = None