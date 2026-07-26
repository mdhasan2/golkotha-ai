
from pathlib import Path

import httpx
import yaml


MANIFEST_PATH = Path("knowledge/manifest.yaml")

def load_manifest(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        content = yaml.safe_load(file)

    return content["sources"]

def download_source(
        client: httpx.Client,
        source: dict,
    ) -> None:
        url = source["url"]
        destination = Path(source["local_path"])

        destination.parent.mkdir(parents=True, exist_ok=True)
                
        response = client.get(url)

        destination.write_bytes(response.content)

        print(
             f"Downloaded {source["id"]}"
             f"to {destination} "
             f"({len(response.content)} bytes)"
        )



def main() -> None:
    sources = load_manifest(MANIFEST_PATH)

    headers = {
        "User-Agent": (
            "GolKotha-AI-Security-Lab/1.0 "
            "(educational secuirty research)"
        )
    }

    with httpx.Client(
        headers=headers,
        timeout=60.0,
        follow_redirects=True,
    ) as client:
        for source in sources:
            try:
                download_source(client, source)
            except httpx.HTTPError as exc:
                 print(f"Failed to download {source["id"]: {exc}}")

if __name__ == "__main__":
    main()