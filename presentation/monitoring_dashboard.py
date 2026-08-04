import json

import streamlit as st

import pandas as pd

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

        payload = (
            self.repository
            .get_dashboard_metrics()
        )

        interactions = pd.DataFrame(
            payload["interactions"]
        )

        if interactions.empty:
            st.info(
                "No monitored interactions are "
                "available yet."
            )
            return

        interactions["created_at"] = (
            pd.to_datetime(
                interactions["created_at"],
                utc=True,
            )
        )

        interactions["success"] = (
            interactions["success"].astype(bool)
        )

        interactions["citation_count"] = (
            interactions["citation_ids"]
            .apply(self._json_length)
        )

        interactions["total_tokens"] = (
            interactions["input_tokens"]
            + interactions["output_tokens"]
        )

        self._render_summary_metrics(
            interactions,
        )

    @staticmethod
    def _render_summary_metrics(
        interactions: pd.DataFrame,
    ) -> None:
        total_requests = len(interactions)

        successful_requests = int(
            interactions["success"].sum()
        )

        success_rate = (
            successful_requests
            / total_requests
        )

        average_letency = (
            interactions["latency_ms"].mean()
        )

        columns = st.columns(3)

        columns[0].metric(
            "Total requests",
            total_requests,
        )

        columns[1].metric(
            "Success rate",
            f"{success_rate:.1%}",
        )

        columns[2].metric(
            "Average latency",
            f"{average_letency:.0f} ms",
        )

    @staticmethod
    def _json_length(
        value: str,
    ) -> int:
        try:
            parsed = json.loads(value)
            return len(parsed)
        except (
            TypeError,
            json.JSONDecodeError
        ):
            return 0