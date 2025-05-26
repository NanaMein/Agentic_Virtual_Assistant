from llama_index.core.storage.docstore import BaseDocumentStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq as ChatGroq
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction, BM25BuiltInFunction
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Document
)
from llama_index.core.text_splitter import SentenceSplitter
from dotenv import load_dotenv
from functools import lru_cache
import os
# Get current time and 1 day ago
from datetime import datetime, timedelta, timezone

from pymilvus import DataType

load_dotenv()
print("starting embed")
#*******************************************************************************************
embed_model = HuggingFaceEmbedding(model_name='intfloat/e5-base')

llm = ChatGroq(
    model=os.getenv('LLM_SMALL'),
    api_key=os.getenv('NEW_API_KEY'),
    temperature=.3
)
print("MilvusVectorConnection")
@lru_cache(maxsize=1)
def get_vector_store():
    return MilvusVectorStore(
        uri=os.getenv('NEW_URI'),
        token=os.getenv('NEW_TOKEN'),
        collection_name='Portfolio_Chat_Context',
        dim=768,
        embedding_field='embeddings',
        enable_sparse=True,
        enable_dense=True,
        overwrite=True,# CHANGE IT FOR DEVELOPMENT STAGE ONLY
        sparse_embedding_function=BGEM3SparseEmbeddingFunction(),
        search_config={"nprobe": 20},
        similarity_metric="L2",  # or "IP"
        consistency_level="Strong",
        hybrid_ranker="WeightedRanker",
        hybrid_ranker_params={"weights": [0.7, 0.3]},


    )
def lazy_loader():

    return get_vector_store()

print("lazy loader on the roll")
lazy_vector = lazy_loader()

async def indexed_chat_context(user_content:str , assistant_content:str):
    message_store = [
        f"[Role => User// Content => {user_content}]",
        f"[Role => Assistant// Content => {assistant_content}]"
    ]
    current_timestamp = datetime.now(timezone.utc).isoformat()  # Or use `datetime.now()` for local time

    documents = [Document(
        text=text,metadata={
                "source": "chat_context",  # Required for Milvus
                "timestamp": current_timestamp  # Add timestamp
            })
        for text in message_store]

    parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)

    nodes = parser.get_nodes_from_documents(documents=documents)

    index = VectorStoreIndex(
        nodes=nodes,
        vector_store=lazy_vector,
        embed_model=embed_model,
        storage_context=StorageContext.from_defaults(
            vector_store=lazy_vector
        )
    )
async def indexed_query_engine(input_question: str) -> str:
    # now = int(datetime.now().timestamp())
    # one_day_ago = now - 86400

    # 1. Create proper metadata filters


    index = VectorStoreIndex.from_vector_store(
        vector_store=lazy_vector,
        embed_model=embed_model

    )
    query_engine = index.as_query_engine(
        llm=llm,
        vector_store_query_mode="hybrid",
        # filters=("timestamp" > str(one_day_ago)),  # Only recent documents
        similarity_top_k=5
    )
    obj_str = query_engine.query(input_question)
    return obj_str.response

# def query_engine_chat(inputs: str) -> str:
#     return str(query_engine.query(inputs))

# print("starting loop")
# while True:
#     print("testing\n")
#     question = input("Write something you like (type 'exit' to quit): \n\n")
#
#     if question.lower() == "exit":
#         print("Exiting the loop.")
#         break
#
#     output = indexed_query_engine(question)
#     indexed_chat_context(question,output.response)
#     print(output)
#     print("****************************************************************\n\n")








