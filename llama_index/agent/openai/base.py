"""OpenAI Agent.

Simple wrapper around AgentRunner + OpenAIAgentWorker.

For the legacy implementation see:
```python
from llama_index.agent.legacy.openai.base import OpenAIAgent
```
"""


from typing import (
    Any,
    List,
    Optional,
    Type,
)

from llama_index.agent.executor.base import AgentRunner
from llama_index.agent.openai.step import OpenAIAgentWorker
from llama_index.agent.types import BaseAgent
from llama_index.callbacks import (
    CallbackManager,
)
from llama_index.chat_engine.types import AgentChatResponse, StreamingAgentChatResponse
from llama_index.llms.base import ChatMessage
from llama_index.llms.llm import LLM
from llama_index.llms.openai import OpenAI
from llama_index.memory.chat_memory_buffer import ChatMemoryBuffer
from llama_index.memory.types import BaseMemory
from llama_index.objects.base import ObjectRetriever
from llama_index.tools import BaseTool

DEFAULT_MODEL_NAME = "gpt-3.5-turbo-0613"

DEFAULT_MAX_FUNCTION_CALLS = 5


class OpenAIAgent(BaseAgent):
    """OpenAI agent.

    Simple wrapper around AgentRunner + OpenAIAgentWorker.

    For the legacy implementation see:
    ```python
    from llama_index.agent.legacy.openai.base import OpenAIAgent
    ```

    """

    def __init__(
        self,
        tools: List[BaseTool],
        llm: OpenAI,
        memory: BaseMemory,
        prefix_messages: List[ChatMessage],
        verbose: bool = False,
        max_function_calls: int = DEFAULT_MAX_FUNCTION_CALLS,
        callback_manager: Optional[CallbackManager] = None,
        tool_retriever: Optional[ObjectRetriever[BaseTool]] = None,
    ) -> None:
        super().__init__(callback_manager=callback_manager or llm.callback_manager)

        self._step_engine = OpenAIAgentWorker.from_tools(
            tools=tools,
            tool_retriever=tool_retriever,
            llm=llm,
            verbose=verbose,
            max_function_calls=max_function_calls,
            callback_manager=self.callback_manager,
            prefix_messages=prefix_messages,
        )
        self._agent_runner = AgentRunner(
            self._step_engine,
            memory=memory,
            llm=llm,
            callback_manager=self.callback_manager,
        )

    @classmethod
    def from_tools(
        cls,
        tools: Optional[List[BaseTool]] = None,
        tool_retriever: Optional[ObjectRetriever[BaseTool]] = None,
        llm: Optional[LLM] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        memory: Optional[BaseMemory] = None,
        memory_cls: Type[BaseMemory] = ChatMemoryBuffer,
        verbose: bool = False,
        max_function_calls: int = DEFAULT_MAX_FUNCTION_CALLS,
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        prefix_messages: Optional[List[ChatMessage]] = None,
        **kwargs: Any,
    ) -> "OpenAIAgent":
        """Create an OpenAIAgent from a list of tools.

        Similar to `from_defaults` in other classes, this method will
        infer defaults for a variety of parameters, including the LLM,
        if they are not specified.

        """
        tools = tools or []

        chat_history = chat_history or []
        llm = llm or OpenAI(model=DEFAULT_MODEL_NAME)
        if not isinstance(llm, OpenAI):
            raise ValueError("llm must be a OpenAI instance")

        if callback_manager is not None:
            llm.callback_manager = callback_manager

        memory = memory or memory_cls.from_defaults(chat_history, llm=llm)

        if not llm.metadata.is_function_calling_model:
            raise ValueError(
                f"Model name {llm.model} does not support function calling API. "
            )

        if system_prompt is not None:
            if prefix_messages is not None:
                raise ValueError(
                    "Cannot specify both system_prompt and prefix_messages"
                )
            prefix_messages = [ChatMessage(content=system_prompt, role="system")]

        prefix_messages = prefix_messages or []

        return cls(
            tools=tools,
            tool_retriever=tool_retriever,
            llm=llm,
            memory=memory,
            prefix_messages=prefix_messages,
            verbose=verbose,
            max_function_calls=max_function_calls,
            callback_manager=callback_manager,
        )

    @property
    def chat_history(self) -> List[ChatMessage]:
        """Chat history."""
        return self._agent_runner.memory.get_all()

    def reset(self) -> None:
        self._agent_runner.memory.reset()

    def chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        """Chat."""
        return self._agent_runner.chat(message=message, chat_history=chat_history)

    async def achat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> AgentChatResponse:
        """Chat."""
        return await self._agent_runner.achat(
            message=message, chat_history=chat_history
        )

    def stream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        """Stream chat."""
        return self._agent_runner.stream_chat(
            message=message, chat_history=chat_history
        )

    async def astream_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> StreamingAgentChatResponse:
        """Async stream chat."""
        return await self._agent_runner.astream_chat(
            message=message, chat_history=chat_history
        )