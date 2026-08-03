class LLMCostCalculator:

    PRICING = {
        (
            "openai",
            "gpt-5.4-mini",
        ): {
            "input": 0.00000075,
            "output": 0.0000045,
        },
    }


    def estimate(
        self,
        *,
        provider: str,
        model_name: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        pricing = self.PRICING[
            (provider, model_name)
        ]

        return (
            input_tokens * pricing["input"]
            + output_tokens * pricing["output"]
        )