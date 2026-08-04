import json


import pandas as pd
import plotly.express as px
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

        st.divider()

        self._requests_over_time(
            interactions
        )

        self._latency_over_time(
            interactions
        )

        self._latency_breakdown(
            interactions
        )

        self._strategy_usage(
            interactions
        )

        self._error_rate(
            interactions
        )

        self._citation_distribution(
            interactions
        )

        self._token_usage(
            interactions
        )

        self._estimated_cost_over_time(
            interactions
        )

        self._recent_interactions(
            interactions
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

        total_cost = interactions[
            "estimated_cost_usd"
        ].sum()

        columns = st.columns(4)

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

        columns[3].metric(
            "Estimated cost",
            f"${total_cost:.4f}",
        )

    @staticmethod
    def _requests_over_time(
        interactions: pd.DataFrame,
    ) -> None:
        daily = (
            interactions
            .set_index("created_at")
            .resample("D")
            .size()
            .reset_index(name="requests")
        )

        figure = px.line(
            daily,
            x="created_at",
            y="requests",
            title="1. Requests over time",
            markers=True
        )

        st.plotly_chart(
            figure,
            width='stretch',
        )

    @staticmethod
    def _latency_over_time(
        interactions: pd.DataFrame,
    ) -> None:
        daily = (
            interactions
            .set_index("created_at")
            ["latency_ms"]
            .resample("D")
            .mean()
            .reset_index()
        )

        figure = px.line(
            daily,
            x="created_at",
            y="latency_ms",
            title="2. Average latency over time",
            markers=True,
        )

        st.plotly_chart(
            figure,
            width='stretch',
        )

    @staticmethod
    def _latency_breakdown(
        interactions: pd.DataFrame
    ) -> None:
        latency = interactions[
            [
                "retrieval_latency_ms",
                "llm_latency_ms",
            ]
        ].mean().reset_index()

        latency.columns = [
            "component",
            "average_latency_ms",
        ]

        figure = px.bar(
            latency,
            x="component",
            y="average_latency_ms",
            title="3. Retrieval and LLM latency",
        )

        st.plotly_chart(
            figure,
            width='stretch'
        )

    @staticmethod
    def _strategy_usage(
        interactions: pd.DataFrame,
    ) -> None:
        usage = (
            interactions[
                "retrieval_strategy"
            ]
            .value_counts()
            .reset_index()
        )

        usage.columns = [
            "strategy",
            "requests",
        ]

        figure = px.bar(
            usage,
            x="strategy",
            y="requests",
            title="6. Retrieval strategy usage",
        )

        st.plotly_chart(
            figure,
            width='stretch'
        )

    @staticmethod
    def _error_rate(
        interactions: pd.DataFrame,
    ) -> None:
        daily = interactions.copy()

        daily["error"] = (
            ~daily["success"]
        ).astype(int)

        daily = (
            daily
            .set_index("created_at")
            ["error"]
            .resample("D")
            .mean()
            .reset_index()
        )

        figure = px.line(
            daily,
            x="created_at",
            y="error",
            title="7. Error rate over time",
            markers=True,
        )

        st.plotly_chart(
            figure,
            width='stretch',
        )

    @staticmethod
    def _citation_distribution(
            interactions: pd.DataFrame,
        ) -> None:
        figure = px.histogram(
            interactions,
            x="citation_count",
            title=(
                "8. Citations per recommendation"
            ),
        )

        st.plotly_chart(
            figure,
            width='stretch'
        )

    @staticmethod
    def _token_usage(
            interactions: pd. DataFrame,
        ) -> None:
        figure = px.scatter(
            interactions,
            x="created_at",
            y="total_tokens",
            title="9. Token usage per request",
            hover_data=[
                "retrieval_strategy",
                "prompt_strategy",
            ],
        )

        st.plotly_chart(
            figure,
            width='stretch',
        )

    @staticmethod
    def _estimated_cost_over_time(
        interactions: pd.DataFrame,
    ) -> None:
        daily = (
            interactions
            .set_index("created_at")
            ["estimated_cost_usd"]
            .resample("D")
            .sum()
            .reset_index()
        )

        figure = px.line(
            daily,
            x="created_at",
            y="estimated_cost_usd",
            title="10. Estimated cost over time",
            markers=True,
            labels={
                "created_at": "Date",
                "estimated_cost": (
                    "Estimated cost (USD)"
                ),
            },
        )

        figure.update_yaxes(
            tickprefix="$",
            tickformat=".4f",
        )

        st.plotly_chart(
            figure,
            width='stretch',
        )

    @staticmethod
    def _recent_interactions(
            interactions: pd.DataFrame,
        ) -> None:
        st.subheader("Recent interactions")

        columns = [
            "created_at",
            "user_query",
            "retrieval_strategy",
            "prompt_strategy",
            "latency_ms",
            "citation_count",
            "success",
            "error_message",
        ]

        st.dataframe(
            interactions[columns].head(50),
            width='stretch',
            hide_index=True,
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