import os
from openai import OpenAI

class OpenAILLM:
    def __init__(
        self,
        *,
        model: str,
        api_key: str | None = None,
    ) -> None:
        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")

        self._model = model
        self._client = OpenAI(
            api_key=resolved_api_key,
        )
        # print("you are here", resolved_api_key)
        
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        # print("you are here\n")
        # print(f"System Prompt: \n{system_prompt}\n, User Prompt: \n{user_prompt}")
        response = self._client.responses.create(
            model=self._model,
            instructions=system_prompt,
            input=user_prompt,
        )

        return response.output_text