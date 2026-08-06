import json
import sqlite3
from pathlib import Path
from typing import Any

from application.ports.monitoring_repository import MonitoringRepositoryPort

from domain.monitoring_models import (
    RAGInteraction,
    UserFeedback,
)

class SQLiteMonitoringRepository(MonitoringRepositoryPort):
    def __init__(
        self,
        database_path: str | Path,
    ) -> None:
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
              parents=True,
              exist_ok=True
        )
        self.initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path,
        )

        connection.row_factory = sqlite3.Row

        return connection

    def initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS interactions (
                    interaction_id TEXT PRIMARY KEY,
                    user_query TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    model_name TEXT NOT NULL,
                    retrieval_strategy TEXT NOT NULL,
                    prompt_strategy TEXT NOT NULL,
                    retrieved_document_ids TEXT NOT NULL,
                    citation_ids TEXT NOT NULL,
                    latency_ms REAL NOT NULL,
                    retrieval_latency_ms REAL NOT NULL,
                    llm_latency_ms REAL NOT NULL,
                    input_tokens INTEGER NOT NULL,
                    output_tokens INTEGER NOT NULL,
                    estimated_cost_usd REAL NOT NULL,
                    success INTEGER NOT NULL,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                );

                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id TEXT PRIMARY KEY,
                    interaction_id TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating IN (-1, 1)),
                    comment TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (interaction_id)
                        REFERENCES interactions(interaction_id)
                );

                CREATE INDEX IF NOT EXISTS
                    idx_interactions_created_at
                ON interactions (created_at);

                CREATE INDEX IF NOT EXISTS
                    idx_interactions_strategy
                ON interactions (retrieval_strategy);

                CREATE INDEX IF NOT EXISTS
                    idx_feedback_interaction
                ON feedback(interaction_id);
                """
            )

    def save_interaction(
        self,
        interaction: RAGInteraction,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO interactions (
                    interaction_id,
                    user_query,
                    answer,
                    provider,
                    model_name,
                    retrieval_strategy,
                    prompt_strategy,
                    retrieved_document_ids,
                    citation_ids,
                    latency_ms,
                    retrieval_latency_ms,
                    llm_latency_ms,
                    input_tokens,
                    output_tokens,
                    estimated_cost_usd,
                    success,
                    error_message,
                    created_at,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    interaction.interaction_id,
                    interaction.user_query,
                    interaction.answer,
                    interaction.provider,
                    interaction.model_name,
                    interaction.retrieval_strategy,
                    interaction.prompt_strategy,
                    json.dumps(
                        interaction.retrieved_document_ids,
                    ),
                    json.dumps(
                        interaction.citation_ids,
                    ),
                    interaction.latency_ms,
                    interaction.retrieval_latency_ms,
                    interaction.llm_latency_ms,
                    interaction.input_tokens,
                    interaction.output_tokens,
                    interaction.estimated_cost_usd,
                    int(interaction.success),
                    interaction.error_message,
                    interaction.created_at.isoformat(),
                    json.dumps(interaction.metadata),
                ),
            )

    def save_feedback(
        self,
        feedback: UserFeedback,
    ) -> None:
        print("Saving feedback:", feedback)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO feedback (
                    feedback_id,
                    interaction_id,
                    rating,
                    comment,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    feedback.feedback_id,
                    feedback.interaction_id,
                    feedback.rating,
                    feedback.comment,
                    feedback.created_at.isoformat(),
                ),
            )

    def feedback_exists(
        self,
        interaction_id: str,
        ) -> bool:
            with self._connect() as connection:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM feedback
                    WHERE interaction_id = ?
                    LIMIT 1
                    """,
                    (interaction_id,),
                ).fetchone()

            return row is not None
    
    def get_dashboard_metrics(
        self,
        limit: int = 1_000,
    ) -> dict[str, Any]:
        with self._connect() as connection:
            interactions = connection.execute(
                """
                SELECT *
                FROM interactions
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return {
            "interactions": [
                dict(row)
                for row in interactions
            ],
        }