from crewai import Task
from agents_config import translator_agent

def first_task() -> Task:
    return Task(
        agent=translator_agent(),
        description=""" You can only reply in english or tagalog, or a mix of both. 
            Your reply will be based on """,
        expected_output=""" """
    )