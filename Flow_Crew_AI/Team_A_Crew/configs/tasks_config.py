from crewai import Task
from agents_config import translator_agent

def first_task() -> Task:
    return Task(
        agent=translator_agent(),
        description=""" You can only reply in english or tagalog, or a mix of both. 
            You will reply in normal conversation based on the following:
            1. The previous chat history: **{chat_history}** 
            2. The current human message: **{human_message}**
            """,
        expected_output=""" You will reply based on the context provided """
    )