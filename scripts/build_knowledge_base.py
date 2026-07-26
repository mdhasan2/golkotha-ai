from pathlib import Path

import yaml

from infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore
)

from infrastructure.rag.document_chunker import (
    ChunkingConfig,
    DocumentChunker,
)

from infrastructure.rag.document_loader import DocumentLoader
from infrastructure.rag.knowledge_base_builder import (
    KnowledgeBaseBuilder
)

from infrastructure.rag.sentence_transformer_embeddings import (
    SentenceTransformerEmbeddingService
)



MANIFEST_PATH = Path("knowledge/manifest.yaml")

def load_manifest(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        content = yaml.safe_load(file)

    return content["sources"]


def main() -> None:
    loader = DocumentLoader()
    
    documents = [
        loader.load_from_manifest_entry(source)
        for source in load_manifest(MANIFEST_PATH)    
    ]
    
    # print(type(document))
    # for document in documents:
    #     print(document.text[:210])

    chunker = DocumentChunker(
        ChunkingConfig(
            max_characters=1_200,
            overlap_characters=200,
            minimumc_characters=150,
        )
    )

    embeddings = SentenceTransformerEmbeddingService()

    vector_store = ChromaVectorStore(
        persist_directory="knowledge/vector_store",
        collection_name="golkotha_ai_security",
    )

    builder = KnowledgeBaseBuilder(
        chunker=chunker,
        embedding_service=embeddings,
        vector_store=vector_store,
        batch_size=32,
    )

    builder.build(
        documents=documents,
        rebuild=True,
    )

if __name__ == "__main__":
    main()