from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq as ChatGroq
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction, BM25BuiltInFunction
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext
)
from llama_index.core.text_splitter import SentenceSplitter
from dotenv import load_dotenv
import os

load_dotenv()



embed_model = HuggingFaceEmbedding(model_name='intfloat/e5-base')

llm = ChatGroq(
    model=os.getenv('LLM_SMALL'),
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
load_documents = SimpleDirectoryReader(input_dir='./data_sources').load_data()

parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)

nodes = parser.get_nodes_from_documents(load_documents)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex(
    nodes,
    vector_store=vector_store,
    embed_model=embed_model,
    storage_context=storage_context
)

query_engine = index.as_query_engine(
    llm=llm,
    vector_store_query_mode="hybrid",
    similarity_top_k=5
)

def query_engine_chat(inputs: str) -> str:
    return str(query_engine.query(inputs))

while True:
    print("testing\n")
    question = input("Write something you like (type 'exit' to quit): \n\n")

    if question.lower() == "exit":
        print("Exiting the loop.")
        break

    output = query_engine_chat(question)
    print(output)
    print("****************************************************************\n\n")








