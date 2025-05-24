import asyncio
import os
import random
# from datetime import datetime, timezone
# from typing import Any
# from typing import Type
# from pydantic import BaseModel, Field
# from groq import Groq
# from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process, LLM, CrewOutput
# from crewai.tools import BaseTool
# from crewai.project import tool
# from groq.types.chat import (
#     ChatCompletionAssistantMessageParam,
#     ChatCompletionUserMessageParam,
#     ChatCompletionSystemMessageParam
# )
from tool_for_crew import RagTool, CompoundBetaTool

# def llm_groq() -> LLM:
#     return LLM(
#         model=os.getenv('LLM_SMALL'),
#         api_base=os.getenv('API_BASE_GROQ'),
#         api_key=os.getenv('NEW_API_KEY'),
#         temperature=0.75
#     )
from dotenv import load_dotenv

load_dotenv()


def manager_llm() -> LLM:
    return LLM(
        model=os.getenv('LLM_BIG'),
        api_base=os.getenv('API_BASE_GROQ'),
        api_key=os.getenv('NEW_API_KEY'),
        temperature=0.1
    )


class RagCharacterCrew:

    def __init__(self):
        self.llm = manager_llm()
        self.rag_tool = RagTool()
        self.web_tool = CompoundBetaTool()

    def boss_agent(self) -> Agent:
        return Agent(
            role=""" 
               The boss that has experience in delegating tasks to other people and distributing tasks efficiently
            """,
            backstory="""
                You are a business owner that handles 1000 employees without breaking a sweat. You efficiently 
                delegate tasks depending on the mission you need to achieve as a daily activity. You can do things
                alone, but prefer to ask someone to do things for you because you can guide them better than
                doing it yourself
            """,
            goal="""
                Orchestrate and Delegate tasks. You are the boss and the leader yourself. 
            """,
            llm=self.llm,
            verbose=False,
            tools=[]
        )
    def worker_agent(self) -> Agent:
        return Agent(
            role=""" 
                Retrieval Augmented Generation Specialist 
            """,
            backstory="""You are a reasercher and a detective.
            """,
            goal="""You will search and describe your findings
            """,
            llm=self.llm,
            verbose=False,
            tools=[]
        )

    def lore_task(self) -> Task:
        return Task(
            description="""
                ###
            """,

            expected_output="""
            
            """,
            agent=
        )

    def character_task(self) -> Task:
        return Task(
            description="""
    
                    """,

            expected_output="""
    
                    """,
            agent=
        )
    def complex_task(self) -> Task:
        return Task(
            description="""
    
                    """,

            expected_output="""
    
                    """,
            agent=
        )



    ###****************************************************************************************************************************
    # def rag_agent(self) -> Agent:
    #     return Agent(
    #         role="""
    #             Retrieval Augmented Generation Specialist
    #         """,
    #         backstory="""You are a reasercher and a detective.
    #         """,
    #         goal="""You will search and describe your findings
    #         """,
    #         llm=self.llm,
    #         verbose=False,
    #         tools=[]
    #     )
    # ************************************************************************************************************************
    async def crew_binder(self):
        return Crew(
            agents=[],
            tasks=[],
            process=Process.hierarchical,
            verbose=True,
            manager_agent=self.boss_agent()
        )


async def run_crew(input_str_async: str):
    obj = await RagCharacterCrew().crew_binder()
    random_int = random.randint(2, 5)
    return await obj.kickoff_async(inputs={'input_message': input_str_async, 'int_sentence': random_int})


async_obj = asyncio.run(run_crew(input_str_async="Nice to meet you my name is alice. How are you?"))
print(async_obj)
answer_2 = asyncio.run(run_crew(
    input_str_async="Nice to meet you my name is alice. Do you think Xianzhou will have renovations and lots of construction after the Abundance wreck havoc your land? "))