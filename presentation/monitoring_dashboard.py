import streamlit as st

from application.ports.monitoring_repository import (
    MonitoringRepositoryPort
)

class MonitoringDashboard:
    
    def __init__(
        self,
        repository: MonitoringRepositoryPort,
    ) -> None:
        self.repository = repository

    def render(self) -> None:
        st.title("📊 Golkotha AI Monitoring")