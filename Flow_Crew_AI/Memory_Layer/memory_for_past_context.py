# from groq import Groq, AsyncGroq
# from groq.types.chat import (
#     ChatCompletionAssistantMessageParam,
#     ChatCompletionUserMessageParam,
#     ChatCompletionSystemMessageParam
# )
from mem0 import Memory
from llama_index.core.memory import Memory as ChatMemory
from llama_index.core.llms import ChatMessage
from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4
from datetime import datetime
import pytz
import sqlite3
import os

from win32timezone import utcnow

load_dotenv()

print("MEMORY LAYER LOADING...")
url = os.getenv('NEW_URI')
token = os.getenv('NEW_TOKEN')
llm_model = os.getenv('LLM_SMALL')
groq = os.getenv('NEW_API_KEY')
os.environ['GROQ_API_KEY'] = groq



config = {
    "vector_store": {
        "provider": "milvus",
        "config": {
            "collection_name": "Mem0_Portfolio_Collection",
            "url": url,
            "token": token,
            "embedding_model_dims": "768",  # Change this according to your local model's dimensions
        },
    },
    "llm": {
        "provider": "groq",
        "config": {
            "model": llm_model,
            "temperature": 0.2,
            "max_tokens": 5000,
        },
    },
    "embedder": {
        "provider": "huggingface",
        "config": {"model": "intfloat/e5-base"},
    },
    "history_db_path": ":memory:",
    "version" : "v1.1"
}

mem0 = Memory.from_config(config)




def search_memories(user_query: str):
    related_memories = mem0.search(query=user_query, user_id="test_user")
    return related_memories

def reset_memories():
    mem0.reset()


def add_memories_v2(user_input: str, ai_output: str):
    # Escape quotes inline
    def escape_quotes(text: str) -> str:
        return text.replace('"', '\\"').replace("'", "\\'")

    memory_id = str(uuid4())

    messages = [
        {"role": "user", "content": escape_quotes(user_input)},
        {"role": "assistant", "content": escape_quotes(ai_output)},
    ]

    # Store memory with ID and metadata
    result = mem0.add(
        messages,
        user_id="test_user",
        memory_id=memory_id,
        metadata={
            "id": memory_id,
            "category": "default",
            "type": "conversation"
        }
    )
    return memory_id
#local history
memory = ChatMemory.from_defaults(
    # chat_history=[],
    session_id="memory_session",
    chat_history_token_ratio=.8,
    token_limit=20000,
    token_flush_size=3000
)

#learning user
def learning_knowledge (message: str):

    messages = {'role': 'user', 'content': message}
    metadatas = {
        'user message': 'conversational'
    }

    mem0.add(
        messages=messages,
        user_id="learning_user",
        metadata=metadatas
    )
#learning user
def search_learned_knowledge(knowledge: str):
    return mem0.search(query=knowledge, user_id="learning_user", limit=10)

#local history
def add_to_memory(user_input: str, ai_output: str) -> bool:
    try:
        memory.put(ChatMessage.from_str(content=user_input, role="user", metadata={"context": "conversation"}))
        memory.put(ChatMessage.from_str(content=ai_output, role="assistant", metadata={"context": "response"}))
        return True

    except Exception as e:  # Catching any potential errors
        print(f"Error adding to memory: {e}")  # Optional: Log the error
        return False


#local history
def get_memory_context_prompt():
    return memory.get()  # Returns last 5 messages

#learning_user
def memory_rag_experimental_prompt(message: str):
    local_chat_history = memory.get()
    vector_chat_history = mem0.search(query=message, user_id="learning_user")
    ph_time = datetime.now(pytz.timezone('Asia/Manila'))
    prompt_template = f"""
    <chat_history>
    previous chat context: [{local_chat_history}]
    </chat_history>

    <latest_input_query>
    User query: [{message}]
    </latest_input_query>
    
    <document_info_context>
    document: [{vector_chat_history}]
    </document_info_context>

    <date_time>
    [{ph_time.strftime('%Y-%m-%d %H:%M:%S %Z')}]
    </date_time>
    
    ### INSTRUCTION:
    Please summarize all the context provided, starting with chat history and 
    current user conversation but also document info context but this is optional or less importance.  
    But will be used as reference, when you cant find it in chat history.
    
    ### SYSTEM:
    You are a summarizing ai assistant. You are a specialist in conversational summarization. 
    You only summarize important details and emphasize the relation between entities.
    """
    return prompt_template

def reseting_local_memory():
    return memory.reset()
#
# async def tool_async(input_message: str):
#     client = AsyncGroq(api_key=os.environ.get('API_KEY'))
#
#     completion = await client.chat.completions.create(
#         messages=[
#             ChatCompletionSystemMessageParam(
#                 role="system",
#                 content="""You are a Context conversation specialist that can summarize any
#                     previous context. You will summarize and organize based on chat history,
#                     vector search, current user query and date time""",
#             ),
#             ChatCompletionUserMessageParam(
#                 role="user",
#                 content=input_message,
#             ),
#         ],
#         model="compound-beta-mini",
#     )
#     return completion.choices[0].message.content

new_memory = ChatMemory.from_defaults(
    # chat_history=[],
    session_id="new_memory_sessions",
    chat_history_token_ratio=.8,
    token_limit=5000,
    token_flush_size=1500
)
def add_local_chat_history(input:str , output:str):
    try:
        new_memory.put(ChatMessage.from_str(content=input, role="user", metadata={"context": "user query"}))
        new_memory.put(ChatMessage.from_str(content=output, role="assistant", metadata={"context": "ai response"}))
        return True

    except Exception as e:  # Catching any potential errors
        print(f"Error adding to memory: {e}")  # Optional: Log the error
        return False

def get_local_chat_history():
    return new_memory.get()

def delete_local_chat_history():
    return new_memory.reset()

print("MEMORY LAYER LOADING COMPLETE")