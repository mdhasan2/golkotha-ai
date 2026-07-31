
from typing import Any

import streamlit as st

DEFAULT_STATE: dict[str, Any] = {
    "baseline_prediction": None,
}


def initialize_session_state() -> None:
    for key, default_value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def clear_previous_analysis() -> None:
    st.session_state.baseline_prediction = None
    st.session_state.security_context = None
    st.session_state.security_recommendation = None