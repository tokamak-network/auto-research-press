"""Abstract base class for LLM providers."""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Retry configuration
LLM_MAX_RETRIES = 3
LLM_BASE_DELAY = 10  # seconds
LLM_MAX_DELAY = 60   # seconds


async def retry_llm_call(coro_factory, max_retries=LLM_MAX_RETRIES, base_delay=LLM_BASE_DELAY, max_delay=LLM_MAX_DELAY):
    """Retry an async LLM call with exponential backoff.

    Args:
        coro_factory: Callable that returns a coroutine (called fresh each retry)
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds before first retry
        max_delay: Maximum delay cap in seconds

    Returns:
        The result of the coroutine

    Raises:
        The last exception if all retries are exhausted
    """
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            return await coro_factory()
        except Exception as e:
            last_exception = e
            error_name = type(e).__name__
            error_str = str(e)[:200]

            # Don't retry on clearly non-transient errors
            non_retryable = ("invalid_api_key", "authentication", "permission", "not_found")
            if any(keyword in error_str.lower() for keyword in non_retryable):
                logger.warning(f"LLM call failed with non-retryable error: {error_name}: {error_str}")
                raise

            if attempt < max_retries:
                delay = min(base_delay * (2 ** attempt), max_delay)
                logger.warning(
                    f"LLM call failed (attempt {attempt + 1}/{max_retries + 1}): "
                    f"{error_name}: {error_str}. Retrying in {delay}s..."
                )
                await asyncio.sleep(delay)
            else:
                logger.error(
                    f"LLM call failed after {max_retries + 1} attempts: "
                    f"{error_name}: {error_str}"
                )
    raise last_exception


@dataclass
class LLMResponse:
    """Standard response format from any LLM provider."""

    content: str
    model: str
    provider: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    stop_reason: Optional[str] = None  # "end_turn"/"stop" = normal, "max_tokens"/"length" = truncated

    @property
    def total_tokens(self) -> Optional[int]:
        """Total tokens used (input + output)."""
        if self.input_tokens is not None and self.output_tokens is not None:
            return self.input_tokens + self.output_tokens
        return None


class BaseLLM(ABC):
    """Abstract interface for LLM providers.

    All provider implementations must support synchronous generation
    and optional streaming. This allows consistent usage across
    Claude, Gemini, GPT, and future providers.
    """

    def __init__(self, api_key: str, model: str):
        """Initialize LLM provider.

        Args:
            api_key: API authentication key
            model: Model identifier (e.g., "claude-opus-4-5", "gpt-4")
        """
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 4096,
        **kwargs
    ) -> LLMResponse:
        """Generate text completion.

        Args:
            prompt: User prompt/message
            system: System prompt (provider-specific handling)
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters

        Returns:
            LLMResponse with generated content and metadata
        """
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 4096,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream text completion (optional, can raise NotImplementedError).

        Args:
            prompt: User prompt/message
            system: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters

        Yields:
            Text chunks as they are generated
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Provider identifier (e.g., 'anthropic', 'openai', 'google')."""
        pass
