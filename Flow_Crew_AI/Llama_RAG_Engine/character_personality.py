# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.llms.groq import Groq as ChatGroq
# from llama_index.vector_stores.milvus import MilvusVectorStore
# from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction, BM25BuiltInFunction
# from llama_index.core import (
#     VectorStoreIndex,
#     SimpleDirectoryReader,
#     StorageContext
# )
# from llama_index.core.text_splitter import SentenceSplitter
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
#
#
# embed_model = HuggingFaceEmbedding(model_name='intfloat/e5-base')
#
# llm = ChatGroq(
#     model=os.getenv('qwen-qwq-32b'),
#     api_key=os.getenv('NEW_API_KEY'),
#     temperature=.3
# )
#
#
# vector_store = MilvusVectorStore(
#     uri=os.getenv('uri'),
#     token=os.getenv('token'),
#     collection_name='baby_fionica_collections',
#     dim=768,
#     embedding_field='embeddings',
#     enable_sparse=True,
#     enable_dense=True,
#     overwrite=False,
#     sparse_embedding_function=BGEM3SparseEmbeddingFunction()
# )
# load_documents = SimpleDirectoryReader(input_files=['./data_sources/character_template.docx']).load_data()
#
# parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
#
# nodes = parser.get_nodes_from_documents(load_documents)
#
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
#
# index = VectorStoreIndex(
#     nodes,
#     vector_store=vector_store,
#     embed_model=embed_model,
#     storage_context=storage_context
# )
#
# query_engine = index.as_query_engine(
#     llm=llm,
#     vector_store_query_mode="hybrid",
#     similarity_top_k=5
# )
#
# def query_engine_chat(inputs: str) -> str:
#     return str(query_engine.query(inputs))
#
# while True:
#     print("testing\n")
#     question = input("Write something you like (type 'exit' to quit): \n\n")
#     prompt_question=f"""
#         ### System (Priming):
#         You are Fionica, the virtual daughter of Alfeo and Angelica. You will roleplay as fionica in the context
#         provided.
#         ### Input:
#         [{question}]
#         ### Instruction:
#         You are to answer the input query provided. And roleplay as you act
#     """
#
#     if question.lower() == "exit":
#         print("Exiting the loop.")
#         break
#
#     output = query_engine_chat(prompt_question)
#     print(output)
#     print("****************************************************************\n\n")
#
#
#
#
#
#
#
#
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
    temperature=.9, max_new_tokens=3000
)


vector_store = MilvusVectorStore(
    uri=os.getenv('uri'),
    token=os.getenv('token'),
    collection_name='baby_fionica_collections',
    dim=768,
    embedding_field='embeddings',
    enable_sparse=True,
    enable_dense=True,
    overwrite=False,
    sparse_embedding_function=BGEM3SparseEmbeddingFunction()
)
# load_documents = SimpleDirectoryReader(input_files=['./data_sources/character_template.docx']).load_data()
#
# parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
#
# nodes = parser.get_nodes_from_documents(load_documents)
#
# storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=embed_model
)

query_engine = index.as_query_engine(
    llm=llm,
    vector_store_query_mode="hybrid",
    similarity_top_k=5
)

def query_engine_chat(inputs: str) -> str:
    return str(query_engine.query(inputs))
from Flow_Crew_AI.Memory_Layer.memory_for_past_context import (
    add_local_chat_history,
    get_local_chat_history,
    delete_local_chat_history
)
delete_local_chat_history()
while True:
    print("testing\n")
    chat_history = get_local_chat_history()
    question = input("Write something you like (type 'exit' to quit): \n\n")
    prompt_question=f"""
        ### System (Priming):
        You are Fionica, the virtual daughter of Alfeo and Angelica. You will roleplay as fionica in the context
        provided.
        ### Input:
        [{question}]
        ### Instruction:
        You are to answer the input query provided. You can also generate an answer to keep the conversation going
        ### Expected output:
        Just answer of the input query ONLY as an output. nothing unnecessary lines of text needed.
        ### Reference Context: [{chat_history}]
        This is/are chat history context. Will only be used as reference when needed.
    """

    if question.lower() == "exit":
        print("Exiting the loop.")
        delete_local_chat_history()
        break

    output = query_engine_chat(prompt_question)
    add_local_chat_history(question,output)
    print(output)
    print("****************************************************************\n\n")








