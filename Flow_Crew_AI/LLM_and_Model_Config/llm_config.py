from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from crewai import LLM
from dotenv import load_dotenv
from functools import lru_cache
import os

load_dotenv()


def crew_llm_worker() -> LLM:
    return LLM(
        base_url="https://api.groq.com/openai/v1",
        model=os.getenv('LLM_SMALL'),
        api_key=os.getenv('API_KEY'),
        temperature=.3
    )

def crew_llm_manager() -> LLM:
    return LLM(
        base_url="https://api.groq.com/openai/v1",
        model=os.getenv('LLM_BIG'),
        api_key=os.getenv('API_KEY'),
        temperature=.3
    )

@lru_cache()
def embed_huggingface () -> HuggingFaceEmbedding:
    return HuggingFaceEmbedding(model_name='intfloat/e5-base')

@lru_cache()
def llama_llm_small() -> Groq:
    return Groq(
        model=os.getenv('LLAMA_LLM_SMALL'),
        api_key=os.getenv('API_KEY'),
        temperature=.2
    )

def llama_llm_big() -> Groq:
    return Groq(
        model=os.getenv('LLAMA_LLM_BIG'),
        api_key=os.getenv('API_KEY'),
        temperature=.3
    )