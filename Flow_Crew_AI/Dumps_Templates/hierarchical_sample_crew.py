# import asyncio
# import os
# import random
# # from datetime import datetime, timezone
# # from typing import Any
# # from typing import Type
# # from pydantic import BaseModel, Field
# # from groq import Groq
# # from dotenv import load_dotenv
# from crewai import Agent, Crew, Task, Process, LLM, CrewOutput
# # from crewai.tools import BaseTool
# # from crewai.project import tool
# # from groq.types.chat import (
# #     ChatCompletionAssistantMessageParam,
# #     ChatCompletionUserMessageParam,
# #     ChatCompletionSystemMessageParam
# # )
# from tool_for_crew import RagTool, CompoundBetaTool
#
# # def llm_groq() -> LLM:
# #     return LLM(
# #         model=os.getenv('LLM_SMALL'),
# #         api_base=os.getenv('API_BASE_GROQ'),
# #         api_key=os.getenv('NEW_API_KEY'),
# #         temperature=0.75
# #     )
# from dotenv import load_dotenv
#
# load_dotenv()
#
#
# def manager_llm() -> LLM:
#     return LLM(
#         model=os.getenv('LLM_BIG'),
#         api_base=os.getenv('API_BASE_GROQ'),
#         api_key=os.getenv('NEW_API_KEY'),
#         temperature=0.5
#     )
# def lore_llm() -> LLM:
#     return LLM(
#         model=os.getenv('LLM_SMALL'),
#         api_base=os.getenv('API_BASE_GROQ'),
#         api_key=os.getenv('NEW_API_KEY'),
#         temperature=0.1
#     )
#
# class RagCharacterCrew:
#
#     def __init__(self):
#         self.llm_worker = lore_llm()
#         self.llm = manager_llm()
#         self.rag_tool = RagTool()
#         self.web_tool = CompoundBetaTool()
#
#     def boss_agent(self) -> Agent:
#         return Agent(
#             role="""
#                The boss that has experience in delegating tasks to other people and distributing tasks efficiently
#             """,
#             backstory="""
#                 You are a business owner that handles 1000 employees without breaking a sweat. You efficiently
#                 delegate tasks depending on the mission you need to achieve as a daily activity. You can do things
#                 alone, but prefer to ask someone to do things for you because you can guide them better than
#                 doing it yourself
#             """,
#             goal="""
#                 Orchestrate and Delegate tasks. You are the boss and the leader yourself.
#             """,
#             llm=self.llm,
#             verbose=True,
#             allow_delegation=True,
#             system_template="You are an Agentic Manager"
#         )
#     def worker_agent(self) -> Agent:
#         return Agent(
#             role="""
#                 an undercover agent
#             """,
#             backstory="""You are a researcher and a detective.
#             """,
#             goal="""You will search and describe your findings as a researcher for love of mysteries and curiosity
#             for being a detective
#             """,
#             llm=self.llm_worker,
#             verbose=False,
#             tools=[self.rag_tool, self.web_tool]
#         )
#
#     def lore_task(self) -> Task:
#         return Task(
#             description="""
#                 ### System: You are a character lore search machine.
#                 ### User Input:
#                 User: {input_message}
#
#                 ### User intent:
#                 You are to understand the emotion or expression of user input.
#
#                 ### Tool:
#                 Use Character Lore Tool to look up for the context you want to find and use the Web Search Tool for
#                 other stuffs like complex, or details that Character lore cant be find
#
#                 <Tool use example>
#                 user: Im feeling good today, what about your?
#                 ai: You think that user is feeling great today so you will use the tool and ask, "if user is happy,
#                 should i reply in sarcasm or be grateful too? what are personality of Fu xuan"
#                 </Tool use example>
#
#             """,
#
#             expected_output="""
#                 Using the user input, use tool to search the what lore, personality, behavior, or even habits.
#                 final output or format would be User input and About the character from the tool.
#             """,
#             agent=self.worker_agent(),
#         )
#
#     def chat_task(self) -> Task:
#         return Task(
#             description="""
#                 ### system: You are a user query machine. You will reply based on the knowledge you have back to the user
#
#                 <User input> USER: {input_message} </User input>
#
#                 <Instruction>
#                 Using the Character Lore Tool, you will generate an answer as raw output based on the User input.
#                 But if an event, situation, unknown knowledge, or cant find the desired content and context, Use the
#                 Web Search Tool.
#                 </Instruction>
#                     """,
#
#             expected_output="""
#                 You will be the chat completion and reply based on the context provided. Use Character lore tool for
#                 primary knowledge, and Web search tool as fail catch secondary knowledge.
#                     """,
#             agent=self.worker_agent()
#         )
#     def bind_all_task(self) -> Task:
#         return Task(
#             description="""
#                 ### System you will be a roleplayer:
#                 Generate an answer based on context provided as a roleplayer
#                             """,
#
#             expected_output="""
#                 make an answer out of the context. output should be a sentence or sentences used as a conversational dialogue
#                             """,
#             agent=self.boss_agent(),
#             context=[self.chat_task(), self.lore_task()]
#         )
#     # ************************************************************************************************************************
#     async def crew_binder_async(self):
#         return Crew(
#             agents=[self.boss_agent(), self.worker_agent()],
#             tasks=[self.chat_task(), self.lore_task()],
#             process=Process.hierarchical,
#             verbose=True,
#             manager_agent=self.boss_agent(),
#         )
#
#
# async def run_crew_async(input_str_async: str):
#     crew_obj = await RagCharacterCrew().crew_binder_async()
#     random_int = random.randint(2, 8)
#     return await crew_obj.kickoff_async(inputs={'input_message': input_str_async, 'int_sentence': random_int})
#
# print("before the loop")
# while True:
#     print("Starting the loop")
#     inputs = input("Whats your message?: \n")
#     async_obj = asyncio.run(run_crew_async(input_str_async=inputs))
#     print(async_obj)
#     print("\n**************************************LLLLIIIINNNNEEEE******************************************************\n")
# # async_obj = asyncio.run(run_crew(input_str_async="Nice to meet you my name is alice. How are you?"))
# # print(async_obj)
# # answer_2 = asyncio.run(run_crew(
# #     input_str_async="""Nice to meet you my name is alice. Do you think Xianzhou will
# #         have renovations and lots of construction after the Abundance wreck havoc
# #         your land? """))