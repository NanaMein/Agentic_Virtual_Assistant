from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq as ChatGroq
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction
from llama_index.core import VectorStoreIndex
from dotenv import load_dotenv
import os

load_dotenv()

embed_model = HuggingFaceEmbedding(model_name='intfloat/e5-base')

llm = ChatGroq(
    model=os.getenv('LLM_SMALL'),
    api_key=os.getenv('NEW_API_KEY'),
    temperature=.3
)
llm2 = ChatGroq(
    model=os.getenv('LLM_BIG'),
    api_key=os.getenv('NEW_API_KEY'),
    temperature=.3
)

vector_store = MilvusVectorStore(
    uri=os.getenv('NEW_URI'),
    token=os.getenv('NEW_TOKEN'),
    collection_name='Character_Collections_v1',
    dim=768,
    embedding_field='embeddings',
    enable_sparse=True,
    enable_dense=True,
    overwrite=False,
    sparse_embedding_function=BGEM3SparseEmbeddingFunction()
)


index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=embed_model
)

query_engine = index.as_query_engine(
    llm=llm,
    vector_store_query_mode="hybrid",
    similarity_top_k=5
)

def query_engine_small(input_query: str) -> str:
    return str(query_engine.query(input_query))


def query_engine_big(input_query: str) -> str:
    engine = index.as_query_engine(
        llm=llm2,
        vector_store_query_mode="hybrid",
        similarity_top_k=5
    )
    return str(engine.query(input_query))







