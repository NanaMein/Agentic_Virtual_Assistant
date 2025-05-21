# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.llms.groq import Groq as ChatGroq
# from llama_index.vector_stores.milvus import MilvusVectorStore
# from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction, BM25BuiltInFunction
# from llama_index.core import (
#     VectorStoreIndex,
# )
# # from llama_index.core.text_splitter import SentenceSplitter
# from dotenv import load_dotenv
# import os
# # from memory_layer import (
# #     chat_memories,
# #     search_memories,
# #     add_memories,
# #     previous_memories,
# #     reset_memories
# # )
#
#
#
#
# from llama_index.core.llms.mock import MockLLM
# mllm = MockLLM()
# load_dotenv()
# print("starting to fucking work")
# embed_model = HuggingFaceEmbedding(model_name='intfloat/e5-base')
#
# llm = ChatGroq(
#     model=os.getenv('LLM_SMALL') or os.getenv('LLM') or os.getenv('groq/llama3-8b-8192'),
#     api_key=os.getenv('NEW_API_KEY'),
#     temperature=.3
# )
#
# vector_store = MilvusVectorStore(
#     uri=os.getenv('URI'),
#     token=os.getenv('TOKEN'),
#     collection_name='test_collections_v1',
#     dim=768,
#     embedding_field='embeddings',
#     enable_sparse=True,
#     enable_dense=True,
#     sparse_embedding_function=BGEM3SparseEmbeddingFunction(),
#     overwrite=False
# )
#
# index = VectorStoreIndex.from_vector_store(
#     vector_store=vector_store,
#     embed_model=embed_model
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
# from Flow_Crew_AI.Memory_Layer.memory_for_past_context import add_memories, previous_memories, reset_memories, add_memories_v1, chat_memories, search_memories
#
# print("deleteing by id")
#
#
# print("FIRST INITIALIZED")
# first_input = input("Write something you like (type 'exit' to quit): \n\n")
# query = query_engine_chat(first_input)
# add_memories(first_input,query)
# print(query)
# print("****************************************************************\n\n")
#
#
# while True:
#     print("SECOND PHASE AND SO ON\n")
#
#     recent_memories = previous_memories()
#
#     question = input("Say something else? (type 'exit' to quit): \n\n")
#
#     prompt_question = f"""
#         previous chat history: **{recent_memories}**
#         \n\n
#         using the current query input: **{question}** make an answer with the previous chat history
#         """
#
#     if question.lower() == "exitingloop":
#         print("Exiting the loop.")
#         reset_memories()
#         break
#
#     if question.lower() == "show_all":
#         print (recent_memories)
#
#     if question.lower() == "reset":
#         reset_memories()
#         print(recent_memories)
#
#     last_output = query_engine_chat(question)
#
#     add_memories(question, last_output)
#
#     print(last_output)
#
#     print("****************************************************************\n\n")
#
#

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq as ChatGroq
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction #BM25BuiltInFunction
from llama_index.core import (
    VectorStoreIndex,
    # SimpleDirectoryReader,
    # StorageContext
)
# from llama_index.core.text_splitter import SentenceSplitter
from dotenv import load_dotenv
import os

load_dotenv()
print("starting to fucking work")
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

from Flow_Crew_AI.Memory_Layer.memory_for_past_context import add_memories#, previous_memories
# from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.memory import Memory
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.llms import ChatMessage

memory = Memory.from_defaults(
    # chat_history=[],
    session_id="memory_session",
    chat_history_token_ratio=.8,
    token_limit=20000,
    token_flush_size=3000)

def add_to_memory(user_input: str, ai_output: str):
    memory.put(ChatMessage.from_str(content=user_input, role="user", metadata={"context": "conversation"}))
    memory.put(ChatMessage.from_str(content=ai_output, role="assistant", metadata={"context": "response"}))

def get_context_prompt():
    return memory.get()  # Returns last 5 messages

# Usage:
# add_to_memory("What's up?", "Not much!")
print(get_context_prompt())

while True:
    print("SECOND PHASE AND SO ON\n")

    question = input("Say something else? (type 'exit' to quit): \n\n")
    prompt = f""" 
    You are Fu Xuan, the most amazing ai assistant. You will help and answer any query [({question})].
    You will also check if there is chat history for additional context: [({get_context_prompt()})].
    With query and chat history, generate answer based on those."""

    if question.lower() == "exitingloop":
        print("Exiting the loop.")
        # reset_memories()
        break

    last_output = query_engine_chat(prompt)
    add_to_memory(user_input=question, ai_output=last_output)

    print(last_output)

    print("****************************************************************\n\n")



#
#
#


