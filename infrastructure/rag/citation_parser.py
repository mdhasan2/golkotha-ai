import json
from typing import Sequence

from domain.rag_models import Citation, RetrivedChunk

class InvalidLLMResponseError(ValueError):
    pass

class CitationParser:

    def parse(
        self,
        raw_response: str,
        retrieved: Sequence[RetrivedChunk],
    ) -> None:
        try:
            payload = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise InvalidLLMResponseError(
                "LLM response was not valid JSON"
            ) from exc

        allowed = {
            f"S{index}": result
            for index, result in enumerate(
                retrieved,
                start=1,
            )
        }

        requested_ids = payload.get(
            "citation_ids_used",
            [],
        )

        if not isinstance(requested_ids, list):
            raise InvalidLLMResponseError(
                "citation_ids_used must be a list"
            )

        unknown = [
            citation_id
            for citation_id in requested_ids
            if citation_id not in allowed
        ]

        if unknown:
            raise InvalidLLMResponseError(
                f"Unknown citation IDs: {unknown}"
            )

        