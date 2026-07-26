import hashlib
import re
from dataclasses import dataclass

from domain.rag_models import DocumentChunk, KnowledgeDocument

@dataclass(frozen=True)
class ChunkingConfig:
    max_characters: int = 1_200
    overlap_characters: int = 200
    minimumc_characters: int = 150

    def __post_init__(self) -> None:
        if self.max_characters <= 0:
            raise ValueError("max_characters must be positive")

        if self.overlap_characters <= 0:
            raise ValueError(
                "overlap_characters cannot be negative"
            )

        if self.overlap_characters >= self.max_characters:
            raise ValueError(
                "overlap must be smaller than max_characters"
            )

class DocumentChunker:

    def __init__(
        self,
        config: ChunkingConfig | None = None,
    ) -> None:
        self._config = config or ChunkingConfig()


    def chunk(
        self,
        document: KnowledgeDocument,
    ) -> list[DocumentChunk]:
        sections = self._split_into_sections(document.text)
        raw_chunks: list[str] = []

        for section in sections:
            raw_chunks.extend(self._split_section(section))

        chunks: list[DocumentChunk] = []

        for index, text in enumerate(raw_chunks):
            clean_text = text.strip()

            if len(clean_text) < self._config.minimumc_characters:
                print( f"{index} \n {clean_text}")

            chunk_id = self._create_chunk_id(
                document.document_id,
                index,
                clean_text,
            )

            metadata = dict(document.metadata)
            metadata.update(
                {
                    "document_id": document.document_id,
                    "chunk_index": index,
                    "version": document.version or "",
                    "published_at": document.published_at or "",
                }
            )
            
            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document.document_id,
                    text=clean_text,
                    title=document.title,
                    source_name=document.source_name,
                    source_url=document.source_url,
                    chunk_index=index,
                    metadata=metadata,
                )
            )
        return chunks

            

    def _split_into_sections(self, text: str) -> list[str]:
        """
        Split on blank lines while preserving paragraph-sized units.
        """
        return [
            section.strip() 
            for section in re.split(r"\n{2,}", text)
            if section.strip()
        ]

    def _split_section(self, section: str) -> list[str]:
        max_size = self._config.max_characters
        overlap = self._config.overlap_characters

        if len(section) <= max_size:
            return [section]

        chunks: list[str] = []
        start = 0

        while start < len(section):
            proposed_end = min(start + max_size, len(section))
            end = self._find_sentence_boundary(
                section,
                start,
                proposed_end,
            )

            chunk = section[start:end].strip()

            if chunk:
                chunks.append(chunk)
                # print(chunk)

            if end >= len(section):
                break
            
            start = max(end - overlap, start + 1)
            # print(f"Start: {start}, Proposed End: {proposed_end}, Actual End: {end}\n")

        return chunks
    @staticmethod
    def _find_sentence_boundary(
            text: str,
            start: int,
            proposed_end: int,
        ) -> int:
            if proposed_end >= len(text):
                return len(text)

            boundary_candidates = [
                text.rfind(". ", start, proposed_end),
                text.rfind("? ", start, proposed_end),
                text.rfind("! ", start, proposed_end),
                text.rfind("\n", start, proposed_end),                
            ]

            boundary = max(boundary_candidates)

            minimum_acceptable = start + int(
                (proposed_end - start) * 0.60
            )

            if boundary >= minimum_acceptable:
                return boundary + 1

            return proposed_end

    @staticmethod
    def _create_chunk_id(
        document_id: str,
        index: int,
        text: str,
    ) -> str:
        digest = hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()[:12]

        return f"{document_id}:{index}:{digest}"
    
            