from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    provider: str
    model_name: str

class LLMPort(Protocol):

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        ...