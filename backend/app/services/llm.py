import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class GeminiService:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.1-flash-lite"

    def generate(
        self,
        contents: Any,
        # response_schema :type,
        tools: list[types.Tool] | None = None,
        
    ) -> Any:
        config = types.GenerateContentConfig(
            tools=tools or [],
            # response_mime_type="application/json",
            # response_schema=response_schema,
        )

        return self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

    def generate_structured(
            self,
            contents: Any,
            response_schema: type,
        ) -> Any:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
            )

            return self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )