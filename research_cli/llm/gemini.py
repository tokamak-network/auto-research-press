"""Google Gemini LLM provider implementation using the google-genai SDK."""

from typing import AsyncIterator, Optional

from google import genai
from google.genai import types

from .base import BaseLLM, LLMResponse, retry_llm_call


class GeminiLLM(BaseLLM):
    """Google Gemini provider.

    Supports Gemini 3.x and 2.x models.
    Uses the official google-genai SDK with native system_instruction,
    thinking_config, and request-level timeout support.
    """

    def __init__(self, api_key: str, model: str = "gemini-3-flash-preview"):
        super().__init__(api_key, model)
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=300_000),  # 5 min
        )

    @property
    def _is_thinking_model(self) -> bool:
        """Whether this model uses internal thinking tokens."""
        return any(v in self.model for v in ("2.5", "3-pro", "3-flash"))

    @property
    def _is_gemini3(self) -> bool:
        """Whether this model is a Gemini 3.x variant."""
        return any(v in self.model for v in ("3-pro", "3-flash"))

    def _build_config(
        self,
        temperature: float,
        max_tokens: int,
        system: Optional[str],
        **kwargs,
    ) -> types.GenerateContentConfig:
        """Build GenerateContentConfig with thinking and json_mode support."""
        effective_max_tokens = max_tokens
        if self._is_thinking_model:
            effective_max_tokens = max(max_tokens * 8, 8192)

        json_mode = kwargs.pop("json_mode", False)

        thinking_config = None
        if self._is_gemini3:
            thinking_config = types.ThinkingConfig(thinking_level="LOW")

        return types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=effective_max_tokens,
            system_instruction=system,
            thinking_config=thinking_config,
            response_mime_type="application/json" if json_mode else None,
        )

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        config = self._build_config(temperature, max_tokens, system, **kwargs)

        async def _call():
            response = await self.client.aio.models.generate_content(
                model=self.model, contents=prompt, config=config,
            )
            return self._parse_response(response)

        return await retry_llm_call(_call)

    async def generate_streaming(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        """Generate text using streaming to prevent proxy idle-connection timeouts.

        Behaves identically to generate() but uses the streaming API internally,
        keeping the HTTP connection alive with incremental chunks. Returns the
        same LLMResponse once the full message has been received.
        """
        config = self._build_config(temperature, max_tokens, system, **kwargs)

        async def _call():
            chunks_text = []
            last_chunk = None
            stream = await self.client.aio.models.generate_content_stream(
                model=self.model, contents=prompt, config=config,
            )
            async for chunk in stream:
                last_chunk = chunk
                if chunk.text:
                    chunks_text.append(chunk.text)

            content = "".join(chunks_text)
            return self._parse_response(last_chunk, content_override=content)

        return await retry_llm_call(_call)

    async def stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 4096,
        **kwargs,
    ) -> AsyncIterator[str]:
        config = self._build_config(temperature, max_tokens, system, **kwargs)

        stream = await self.client.aio.models.generate_content_stream(
            model=self.model, contents=prompt, config=config,
        )
        async for chunk in stream:
            if chunk.text:
                yield chunk.text

    async def close(self):
        """No-op for compatibility — writer.py calls self.llm.client.close()."""
        pass

    def _parse_response(self, response, *, content_override: Optional[str] = None) -> LLMResponse:
        """Extract content, token counts, and stop reason from a response object."""
        content = content_override if content_override is not None else (response.text if response else "")

        input_tokens = None
        output_tokens = None
        if response and hasattr(response, "usage_metadata") and response.usage_metadata:
            input_tokens = getattr(response.usage_metadata, "prompt_token_count", None)
            output_tokens = getattr(response.usage_metadata, "candidates_token_count", None)

        stop_reason = None
        if response and hasattr(response, "candidates") and response.candidates:
            finish_reason = response.candidates[0].finish_reason
            if finish_reason is not None:
                stop_reason = finish_reason.name if hasattr(finish_reason, "name") else str(finish_reason)

        return LLMResponse(
            content=content,
            model=self.model,
            provider="google",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            stop_reason=stop_reason,
        )

    @property
    def provider_name(self) -> str:
        return "google"
