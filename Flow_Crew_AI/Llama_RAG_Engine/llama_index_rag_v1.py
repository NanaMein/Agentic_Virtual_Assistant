from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq as ChatGroq
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction, BM25BuiltInFunction
from llama_index.core import (
    VectorStoreIndex,
)
# from llama_index.core.text_splitter import SentenceSplitter
from dotenv import load_dotenv
import os
# from memory_layer import (
#     chat_memories,
#     search_memories,
#     add_memories,
#     previous_memories,
#     reset_memories
# )





load_dotenv()
print("starting to fucking work")
embed_model = HuggingFaceEmbedding(model_name='intfloat/e5-base')

llm = ChatGroq(
    model=os.getenv('LLM_SMALL') or os.getenv('LLM'),
    api_key=os.getenv('API_KEY'),
    temperature=.3
)

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


from Flow_Crew_AI.Memory_Layer.memory_for_past_context import add_memories, previous_memories, reset_memories, add_memories_v1, chat_memories, search_memories

print("deleteing by id")


print("FIRST INITIALIZED")
first_input = input("Write something you like (type 'exit' to quit): \n\n")
query = query_engine_chat(first_input)
add_memories(first_input,query)
print(query)
print("****************************************************************\n\n")


while True:
    print("SECOND PHASE AND SO ON\n")

    recent_memories = previous_memories()

    question = input("Say something else? (type 'exit' to quit): \n\n")

    prompt_question = f"""
        previous chat history: **{recent_memories}**
        \n\n
        using the current query input: **{question}** make an answer with the previous chat history
        """

    if question.lower() == "exitingloop":
        print("Exiting the loop.")
        reset_memories()
        break

    if question.lower() == "show_all":
        print (recent_memories)

    if question.lower() == "reset":
        reset_memories()
        print(recent_memories)

    last_output = query_engine_chat(question)

    add_memories(question, last_output)

    print(last_output)

    print("****************************************************************\n\n")



#
#
#


