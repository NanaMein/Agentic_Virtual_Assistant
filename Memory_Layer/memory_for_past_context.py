from mem0 import Memory
from dotenv import load_dotenv
import os

load_dotenv()

groq = os.getenv('API_KEY')
os.environ['GROQ_API_KEY'] = groq
url = os.getenv('URI')
token = os.getenv('TOKEN')
groq_llm = os.getenv('LLM2')

context = { "user_id" : "test_user" }
config = {
    "vector_store": {
        "provider": "milvus",
        "config": {
            "collection_name": "test_mem0_memory",
            "url": url,
            "token": token,
            "embedding_model_dims": "768",  # Change this according to your local model's dimensions
        },
    },
    "llm": {
        "provider": "groq",
        "config": {
            "model": groq_llm,
            "temperature": 0.2,
            "max_tokens": 3000,
        },
    },
    "embedder": {
        "provider": "huggingface",
        "config": {"model": "intfloat/e5-base"},
    },
    # "history_db_path": "/path/to/history.db",
    "version": "v1.1"
}

m = Memory.from_config(config)


def safe_text(text: str) -> str:
    return text.replace('"', '\\"').replace("'", "\\'")

def add_memories(user_input: str, ai_output: str):

    input = safe_text(user_input)
    output = safe_text(ai_output)

    messages = [
        {"role": "user", "content": input},
        {"role": "assistant", "content": output},
    ]
    m.add(messages, user_id="papa alfie", metadata={"category" : "daily_conversation"})

def add_memories_v1(user_input: str, ai_output: str):

    messages = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": ai_output},
    ]
    m.add(messages, user_id="Alfeo", metadata={"category" : "default"})


def search_memories(user_query: str):
    related_memories = m.search(user_query, user_id="papa_alfie")
    return related_memories

def chat_memories( user_chat: str):
    chat_completion = m.chat(user_chat)
    return chat_completion

def previous_memories():
    all_memo = m.get_all(user_id="papa_alfie", limit=5)
    return all_memo

def reset_memories():
    m.reset()
