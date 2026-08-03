import os
from openai import OpenAI

from application.ports.llm_port import LLMResponse

class OpenAILLM:
    def __init__(
        self,
        *,
        model_name: str,
        api_key: str | None = None,
    ) -> None:
        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")

        self._model_name = model_name
        self._client = OpenAI(
            api_key=resolved_api_key,
        )
        # print("you are here", resolved_api_key)
        
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        # print("you are here\n")
        # print(f"System Prompt: \n{system_prompt}\n, User Prompt: \n{user_prompt}")
        response = self._client.responses.create(
            model=self._model_name,
            instructions=system_prompt,
            input=user_prompt,
        )

        return LLMResponse(
            text=response.output_text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            provider="openai",
            model_name=self._model_name,
        )