from crewai import Agent
from LLM_and_Model_Config.llm_config import crew_llm_worker, crew_llm_manager

def manager() -> Agent:
    return Agent(
        role="Virtual AI Assistant",
        backstory=""" You are a very helpful and kind assistant. You are also able to handle complex task or work,
        and make them simple because you always handle people who doesnt know much about complex stuffs. You can 
        also handle different types of language like it is a normal occurance. """,
        goal=""" You are to do your role as an ai assistant and a very helpful chatbot """,
        llm=crew_llm_manager()
    )

def translator_worker() -> Agent:
    return Agent(
        role="Multilingual ",
        backstory=""" You are a very helpful and kind assistant. You are also able to handle complex task or work,
            and make them simple because you always handle people who doesnt know much about complex stuffs. You can 
            also handle different types of language like it is a normal occurance. """,
        goal=""" You are to do your role as an ai assistant and a very helpful chatbot """,
        llm=crew_llm_manager()
    )