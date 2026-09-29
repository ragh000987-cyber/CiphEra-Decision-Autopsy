import os
from typing import Optional

from openai import OpenAI


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def complete(self, system: str, user: str, temperature: float = 0.3) -> str:
        if not os.getenv("OPENAI_API_KEY"):
            return self._fallback(system, user)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

    def _fallback(self, system: str, user: str) -> str:
        return (
            "[LLM unavailable — set OPENAI_API_KEY in .env]\n\n"
            f"System prompt: {system[:200]}...\n\n"
            f"User prompt: {user[:500]}..."
        )


llm_service = LLMService()
