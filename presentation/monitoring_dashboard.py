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

        print(payload)

        interactions = pd.DataFrame(
            payload["interactions"]
        )

        feedback = pd.DataFrame(
            payload["feedback"]
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
            feedback,
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

        self._feedback_distribution(
            feedback
        )

        self._feedback_rate_over_time(
            interactions,
            feedback,
        )

        self._helpful_percentage_over_time(
            feedback,
        )

        self._feedback_sentiment_over_time(
            feedback,
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
        feedback: pd.DataFrame,
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

        feedback_count = len(feedback)

        positive_feedback_rate = 0.0

        if not feedback.empty:
            positive_feedback_rate = (
                feedback["rating"]
                .eq(1)
                .mean()
            )

        total_cost = interactions[
            "estimated_cost_usd"
        ].sum()

        columns = st.columns(6)

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
            "Feedback responses",
            feedback_count,
        )

        columns[4].metric(
            "Helpful feedback",
            f"{positive_feedback_rate:.1%}",
        )

        columns[5].metric(
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
    def _feedback_distribution(
        feedback: pd.DataFrame,
    ) -> None:
        if feedback.empty:
            st.info(
                "4. No user feedback has been "
                "submitted yet."
            )
            return

        distribution = (
            feedback["rating"]
            .map({
                1: "Helpful",
                -1: "Not helpful",
                })
                .value_counts()
                .reset_index()
        )

        distribution.columns = [
            "rating",
            "count",
        ]

        figure = px.pie(
            distribution,
            names="rating",
            values="count",
            title="4. User feedback distribution",
        )

        st.plotly_chart(
            figure,
            width='stretch'
        )

    @staticmethod
    def _feedback_rate_over_time(
        interactions: pd.DataFrame,
        feedback: pd.DataFrame,
    ) -> None:
        daily_requests = (
            interactions
            .set_index("created_at")
            .resample("D")
            .size()
            .rename("requests")
        )

        if feedback.empty:
            daily_feedback = pd.Series(
                dtype=float,
                name="feedback_count",
            )
        else:
            feedback = feedback.copy()

            feedback["created_at"] = (
                pd.to_datetime(
                    feedback["created_at"],
                    utc=True,
                )
            )

            daily_feedback = (
                feedback
                .set_index("created_at")
                .resample("D")
                .size()
                .rename("feedback_count")
            )

        combined = pd.concat(
            [
                daily_requests,
                daily_feedback,
            ],
            axis=1,
        ).fillna(0)

        combined["feedback_rate"] = (
            combined["feedback_count"]
            / combined["requests"].replace(0, pd.NA)
        ).fillna(0)

        combined = combined.reset_index()

        figure = px.line(
            combined,
            x="created_at",
            y="feedback_rate",
            title="5. Feedback response rate",
            markers=True,
        )

        st.plotly_chart(
            figure,
            width='stretch'
        )

    @staticmethod
    def _helpful_percentage_over_time(
        feedback: pd.DataFrame,
    ) -> None:

        if feedback.empty:
            st.info(
                "No feedback has been collected yet."
            )
            return

        feedback = feedback.copy()

        feedback["created_at"] = pd.to_datetime(
            feedback["created_at"],
            utc=True,
        )

        feedback["helpful"] = (
            feedback["rating"] == 1
        ).astype(int)

        daily = (
            feedback
            .set_index("created_at")
            .resample("D")
            .agg(
                helpful=("helpful", "sum"),
                total=("helpful", "count"),
            )
            .reset_index()
        )

        daily["helpful_percentage"] = (
            daily["helpful"]
            / daily["total"]
            * 100
        )

        figure = px.line(
            daily,
            x="created_at",
            y="helpful_percentage",
            title="6. Helpful feedback percentage",
            markers=True,
        )

        figure.update_yaxes(
            title="Helpful %",
            range=[0, 100],
        )

        st.plotly_chart(
            figure,
            width='stretch'
        )
        
    @staticmethod    
    def _feedback_sentiment_over_time(
        feedback: pd.DataFrame,
    ) -> None:

        if feedback.empty:
            st.info(
                "No feedback has been collected yet."
            )
            return

        feedback = feedback.copy()

        feedback["created_at"] = pd.to_datetime(
            feedback["created_at"],
            utc=True,
        )

        feedback["sentiment"] = feedback["rating"].map(
            {
                1: "Helpful",
                -1: "Not Helpful",
            }
        )

        daily = (
            feedback
            .groupby(
                [
                    pd.Grouper(
                        key="created_at",
                        freq="D",
                    ),
                    "sentiment",
                ]
            )
            .size()
            .reset_index(name="count")
        )

        figure = px.bar(
            daily,
            x="created_at",
            y="count",
            color="sentiment",
            title="7. Helpful vs Not Helpful",
            barmode="stack",
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
            title="8. Retrieval strategy usage",
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
            title="9. Error rate over time",
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
                "10. Citations per recommendation"
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
            title="11. Token usage per request",
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
            title="12. Estimated cost over time",
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