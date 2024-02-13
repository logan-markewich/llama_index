from llama_index.core.llms.base import BaseLLM
from llama_index.llms.llama_api import LlamaAPI


def test_embedding_class():
    names_of_base_classes = [b.__name__ for b in LlamaAPI.__mro__]
    assert BaseLLM.__name__ in names_of_base_classes