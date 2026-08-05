
from app.container import MonitoringContainer
import streamlit as st


def render_feedback_section(
    monitoring_container: MonitoringContainer,
    interaction_id: str,
) -> None:
    st.divider()
    st.subheader("Feedback")

