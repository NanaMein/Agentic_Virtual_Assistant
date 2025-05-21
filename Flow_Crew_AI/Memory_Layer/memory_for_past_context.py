from mem0 import Memory
from llama_index.core.memory import Memory as ChatMemory
from llama_index.core.llms import ChatMessage
from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4
import sqlite3
import os

load_dotenv()

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

# from pathlib import Path
# from uuid import uuid4
# import sqlite3
# history_path = Path("./memory_history/history.db")
# history_path.parent.mkdir(exist_ok=True)
# history_path.touch()
# config["history_db_path"] = str(history_path.absolute())
#
# def safe_text(text: str) -> str:
#     return text.replace('"', '\\"').replace("'", "\\'")
#
# def add_memories(user_input: str, ai_output: str) -> bool:
#     try:
#         input_text = f"{safe_text(user_input)}"
#         output_text = f"{safe_text(ai_output)}"
#
#         messages = [
#             {"role": "user", "content": input_text},
#             {"role": "assistant", "content": output_text},
#         ]
#         m.add(messages, user_id="test_user", metadata={"category": "default"})
#         return True
#     except Exception as e:
#         # Optional: log the exception details for debugging
#         print(f"Error adding memories: {e}")
#         return False
mem0 = Memory.from_config(config)

def search_memories(user_query: str):
    related_memories = mem0.search(query=user_query, user_id="test_user")
    return related_memories

def reset_memories():
    mem0.reset()

# def get_context_prompt():
#     try:
#         memories = m.get_all(user_id="test_user", limit=5)
#         context_lines = []
#         for mem in memories:
#             content = mem.get("content") if isinstance(mem, dict) else str(mem)
#             context_lines.append(content)
#         return "\n".join(context_lines)
#     except Exception as e:
#         print(f"[Error getting context]: FUCKKKKKKK {e} YYOOOOUUUUUU")
#         memories = m.search(query="", user_id="test_user", limit=5)
#         context_lines = []
#         for mem in memories:
#             content = mem.get("content") if isinstance(mem, dict) else str(mem)
#             context_lines.append(content)
#         return "\n".join(context_lines)
# def safe_text(text: str) -> str:
#     return text.replace('"', '\\"').replace("'", "\\'")
#
# def add_memories_v2(user_input: str, ai_output: str):
#
#     memory_id = str(uuid4())  # Generate unique ID
#     input_text = f"{safe_text(user_input)}"
#     output_text = f"{safe_text(ai_output)}"
#
#     messages = [
#         {"role": "user", "content": input_text},
#         {"role": "assistant", "content": output_text},
#     ]
#     # Store with explicit ID and metadata
#     result = m.add(
#         messages,
#         user_id="test_user",
#         memory_id=memory_id,
#         metadata={
#             "id": memory_id,
#             "category": "default",
#             "type": "conversation"
#         }
#     )
#     return memory_id
#
#
# from uuid import uuid4


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

memory = ChatMemory.from_defaults(
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
