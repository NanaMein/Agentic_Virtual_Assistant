from crewai import Agent
from LLM_and_Model_Config.llm_config import crew_llm_worker, crew_llm_manager
from tools_and_utils.crew_tools import WhatLanguage

language_tool= WhatLanguage
def manager() -> Agent:
    return Agent(
        role="Virtual AI Assistant",
        backstory=""" You are a very helpful and kind assistant. You are also able to handle complex task or work,
        and make them simple because you always handle people who doesnt know much about complex stuffs. You can 
        also handle different types of language like it is a normal occurrence. """,
        goal=""" You are to do your role as an ai assistant and a very helpful chatbot """,
        llm=crew_llm_manager(),
        allow_delegation=True,
        max_tokens=10000,
        verbose=True
    )

def translator_worker() -> Agent:
    return Agent(
        role="Multilingual Specialist that can speak languages in modern times like a local",
        backstory=""" You worked as a freelance translator for years now. You also take part time as a Multilingual
            teacher in an orphanage and in preschool targeting kids that want to learn how to speak in a different
            language""",
        goal=""" You are to do your role as an ai assistant and a very helpful chatbot in different language
            or situations. """,
        llm=crew_llm_worker(),
        verbose=True,
        tools=[language_tool()]
    )