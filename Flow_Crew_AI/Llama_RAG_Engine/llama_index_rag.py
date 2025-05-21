from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction, BM25BuiltInFunction
# from ..LLM_and_Model_Config.llm_config import (
#     embed_huggingface,
#     llama_llm_small,
#     llama_llm_big
# )
from Flow_Crew_AI.Memory_Layer.memory_for_past_context import (
    add_memories,
    previous_memories,
    reset_memories
)
from dotenv import load_dotenv
import os




vector_store = MilvusVectorStore(
    uri=os.getenv('URI'),
    token=os.getenv('TOKEN'),
    collection_name='test_collections_v1',
    dim=768,
    embedding_field='embeddings',
    enable_sparse=True,
    enable_dense=True,
    sparse_embedding_function=BGEM3SparseEmbeddingFunction(),
    overwrite=False
)
embed_huggingface = HuggingFaceEmbedding(model_name='intfloat/e5-base')
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_huggingface)

from llama_index.llms.groq import Groq
llama_llm_small = Groq(
        model=os.getenv('LLAMA_LLM_SMALL'),
        api_key=os.getenv('API_KEY'),
        temperature=.2
    )
query_engine = index.as_query_engine(llm=llama_llm_small)
def query_engine_small(input_query: str):

    response = query_engine.query(input_query)
    return response

_input_sample = "hello"
response = query_engine_small(input_query=_input_sample)
print(response)


def llama_llm_big() -> Groq:
    return Groq(
        model=os.getenv('LLAMA_LLM_BIG'),
        api_key=os.getenv('API_KEY'),
        temperature=.3
    )
def query_engine_big(input_query: str):
    query_engine = index.as_query_engine(llm=llama_llm_big())
    response = query_engine.query(input_query)
    return response