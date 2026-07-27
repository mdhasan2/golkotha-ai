from collections.abc import Sequence

from sentence_transformers import SentenceTransformer

class SentenceTransformerEmbeddingService:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self._model_name = model_name,
        self._model = SentenceTransformer(model_name)

        # dimension = self._model.get_sentence_embedding_dimension()

        # self._dimension = int(dimension)

    # @property


    def embed_documents(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:

        vectors = self._model.encode(
            list(texts),
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return [
            vector.astype(float).tolist()
            for vector in vectors
        ]
    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        # print("you are here")
        # print(text)
        if not text.strip():
            raise ValueError(
                "Query text cannot be empty"
            )
        vector = self._model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=True,
        )
        return vector.astype(float).tolist()