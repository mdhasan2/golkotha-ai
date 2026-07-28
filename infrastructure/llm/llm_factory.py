import os

from application.ports.llm_port import LLMPort
from infrastructure.llm.openai_llm import OpenAILLM

def build_llm() -> LLMPort:

    provider = os.getenv(
        "LLM_PROVIDER",
    ).strip().lower()

    model = os.getenv(
        "LLM_MODEL",
    ).strip().lower()

    # print("You are here", provider)

    if provider == "openai":
        return OpenAILLM(
            model=model,
        )