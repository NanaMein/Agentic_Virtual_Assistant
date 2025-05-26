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

def llm_groq() -> LLM:
    return LLM(
        model=os.getenv('LLM_SMALL'),
        api_base=os.getenv('API_BASE_GROQ'),
        api_key=os.getenv('NEW_API_KEY'),
        temperature=0.75
    )


class RagCharacterCrew:


    def __init__(self):
        self.llm = llm_groq()
        self.rag_tool = RagTool()
        self.web_tool = CompoundBetaTool()

    def rag_agent(self) -> Agent:
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

    def roleplay_agent(self):
        return Agent(
            role=""" 
                    Roleplayer 
                    """,
            backstory="""You love cosplaying different characters and able to roleplay and act as an in character.
                    """,
            goal="""You will act and roleplay depending on the context provided
                    """,
            llm=self.llm,
            verbose=True,
            tools=[]
        )


    def generate_prompt_task(self) -> Task:
        return Task(
            description="""
            ### INPUT QUERY: 
                **{input_message}**
            ### INSTRUCTION: 
            You will first identify the input query first and then based on the context provided you answer and
            reply the 
            input query. Retrieve fu xuan character Lore, personality, and habits from the Character Lore Tool 
            provided. if input query is too complex and cant be found in the context. Use the Web Search Tool 
            provided in order to get relevant and complex query from the web.
            """,

            expected_output="""
            follow this format as output:
            1. input query and expected reply or predicted reply as raw output text
            2. the character(Fu Xuan) Lore, description, personality
            3. when input query is complex, use the tool provided to search the web. Skip this if ONLY IF it
            is a simple input query
            
            """,
            agent= self.rag_agent(),
            tools=[self.rag_tool, self.web_tool],
            # async_execution=True

        )

    def in_character_task(self) -> Task:
        return Task(
            description="""
            ### Input query: [{input_message}]
            ### Instructions:
                With the context provided, construct and generate an answer based on the input query.
            ### Tool usage:
                Use tools if you think you need help with searching the web by using Web Search Tool. Or if you
                want to know more about the context use the Character Lore Tool. 
            """,
            expected_output="""
                generate an answer based on input query in a normal or roleplay conversational answer as output 
                answer. DONT ADD ANY OTHER THOUGHTS. output answer should be in {int_sentence} sentence/s.
            """,
            agent=self.roleplay_agent(),
            tools=[self.rag_tool, self.web_tool],
            # async_execution=True,
            # context=[self.generate_prompt_task()]

        )
###****************************************************************************************************************************
# Example of how you would run a CrewAI crew asynchronously
# async def main_async_crew_run(input_str_async: str) -> CrewOutput:
#
#     crew_obj = RagCharacterCrew()
#     agent_obj = [crew_obj.rag_agent()]
#     task_obj = [crew_obj.in_character_task(), crew_obj.generate_prompt_task()]
#
#     # You would typically define a Crew with agents and tasks
#     # For a single agent/task, it's simpler, but the principle applies
#     random_int = random.randint(1,5)
#     my_crew = Crew(
#         agents=agent_obj,
#         tasks=task_obj,
#         process=Process.sequential, # Or hierarchical
#         verbose=True
#     )
#     # To run the crew asynchronously:
#     result = await my_crew.kickoff_async(inputs={'input_message': input_str_async , 'int_sentence' : random_int })
#     return result
#
# test_async = asyncio.run(main_async_crew_run("Nice to meet you my name is alice. How are you?"))
# print (test_async)
#************************************************************************************************************************
    async def crew_binder(self):
        return Crew(
            agents=[self.rag_agent(),self.roleplay_agent()],
            tasks=[self.generate_prompt_task(), self.in_character_task()],
            process=Process.sequential,
            verbose=True
        )

async def run_crew(input_str_async: str):
    obj = await RagCharacterCrew().crew_binder()
    random_int = random.randint(2, 5)
    return await obj.kickoff_async(inputs={'input_message': input_str_async, 'int_sentence': random_int})

async_obj = asyncio.run(run_crew(input_str_async="Nice to meet you my name is alice. How are you?"))
print(async_obj)
answer_2 = asyncio.run(run_crew(input_str_async="Nice to meet you my name is alice. Do you think Xianzhou will have renovations and lots of construction after the Abundance wreck havoc your land? "))