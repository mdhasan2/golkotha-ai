import yaml
from pathlib import Path
from typing import Any
from domain.rag_models import KnowledgeDocument

class DocumentLoader:

    def load_from_manifest_entry(
        self,
        source: dict[str, Any],
    ) -> KnowledgeDocument:

        path = Path(source["local_path"])

        document_format = source["format"]

        loaders = {
            "yaml": self._load_yaml,
        }

        loader = loaders.get(document_format)

        text = loader(path)

        return KnowledgeDocument(
            document_id=source["id"],
            title=source["title"],
            text=self._normalize_whitespace(text),
            source_name=source["publisher"],
            source_url=source["url"],
        )

    def _load_yaml(self,path:Path) -> str:
        with path.open("r", encoding="utf-8") as file:
            content = yaml.safe_load(file)

        return self._structured_data_to_text(content)

    def _structured_data_to_text(
        self,
        value: Any,
        path: str = "",
    ) -> str:
        """
        Flatten structure security data while retaining field names.
        """
        lines: list[str] = []

        if isinstance(value, dict):
            for key, child in value.items():
                child_path=f"{path}.{key}" if path else str(key)
                lines.extend(self._structured_data_to_text(child, child_path).splitlines())

        elif isinstance(value, list):
            for index, child in enumerate(value):
                child_path=f"{path}[{index}]"
                lines.extend(self._structured_data_to_text(child, child_path).splitlines())
            
        elif value is not None:
            lines.append(f"{path}: {value}")

        return "\n".join(line for line in lines if line)

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        lines = [
            " ".join(line.split())
            for line in text.splitlines()
        ]

        return "\n".join(
            line for line in lines if line
        ).strip()