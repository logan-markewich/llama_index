from typing import Any, List, Optional

from llama_index.core.bridge.pydantic import BaseModel
from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    CompletionResponse,
)
from llama_index.core.instrumentation.events.base import BaseEvent
from llama_index.core.prompts import BasePromptTemplate


class LLMPredictStartEvent(BaseEvent):
    """LLMPredictStartEvent.

    Args:
        template (BasePromptTemplate): Prompt template.
        template_args (Optional[dict]): Prompt template arguments.
    """

    template: BasePromptTemplate
    template_args: Optional[dict]

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMPredictStartEvent"


class LLMPredictEndEvent(BaseEvent):
    """LLMPredictEndEvent.

    The result of an llm.predict() call.

    Args:
        output (str): Output.
    """

    output: str

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMPredictEndEvent"


class LLMStructuredPredictStartEvent(BaseEvent):
    """LLMStructuredPredictStartEvent.

    Args:
        output_cls (Any): Output class to predict.
        template (BasePromptTemplate): Prompt template.
        template_args (Optional[dict]): Prompt template arguments.
    """

    output_cls: Any
    template: BasePromptTemplate
    template_args: Optional[dict]

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMStructuredPredictStartEvent"


class LLMStructuredPredictEndEvent(BaseEvent):
    """LLMStructuredPredictEndEvent.

    Args:
        output (BaseModel): Predicted output class.
    """

    output: BaseModel

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMStructuredPredictEndEvent"


class LLMCompletionStartEvent(BaseEvent):
    """LLMCompletionStartEvent.

    Args:
        prompt (str): The prompt to be completed.
        additional_kwargs (dict): Additional keyword arguments.
        model_dict (dict): Model dictionary.
    """

    prompt: str
    additional_kwargs: dict
    model_dict: dict

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMCompletionStartEvent"


class LLMCompletionEndEvent(BaseEvent):
    """LLMCompletionEndEvent.

    Args:
        prompt (str): The prompt to be completed.
        response (CompletionResponse): Completion response.
    """

    prompt: str
    response: CompletionResponse

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMCompletionEndEvent"


class LLMChatStartEvent(BaseEvent):
    """LLMChatStartEvent.

    Args:
        messages (List[ChatMessage]): List of chat messages.
        additional_kwargs (dict): Additional keyword arguments.
        model_dict (dict): Model dictionary.
    """

    messages: List[ChatMessage]
    additional_kwargs: dict
    model_dict: dict

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMChatStartEvent"


class LLMChatInProgressEvent(BaseEvent):
    """LLMChatInProgressEvent.

    Args:
        messages (List[ChatMessage]): List of chat messages.
        response (ChatResponse): Chat response currently beiung streamed.
    """

    messages: List[ChatMessage]
    response: ChatResponse

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMChatInProgressEvent"


class LLMChatEndEvent(BaseEvent):
    """LLMChatEndEvent.

    Args:
        messages (List[ChatMessage]): List of chat messages.
        response (ChatResponse): Chat response.
    """

    messages: List[ChatMessage]
    response: ChatResponse

    @classmethod
    def class_name(cls):
        """Class name."""
        return "LLMChatEndEvent"
