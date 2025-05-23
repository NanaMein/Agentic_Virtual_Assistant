# from crewai import Agent, Crew, Process, Task, LLM
# from dotenv import load_dotenv
# import os
#
# def agent_llm_basic() -> LLM:
#     return LLM(
#         model=os.getenv('LLM_SMALL'),
#         api_base=os.getenv('')
#     )
#
#
#
#
# class AgenticRoleplayer:
#     async def manager_agent(self) -> Agent:
#         return Agent(
#             role="Virtual AI Assistant",
#             backstory=""" You are a very helpful and kind assistant. You are also able to handle complex task or work,
#             and make them simple because you always handle people who doesnt know much about complex stuffs. You can
#             also handle different types of language like it is a normal occurrence. """,
#             goal=""" You are to do your role as an ai assistant and a very helpful chatbot """,
#             llm=crew_llm_manager(),
#             allow_delegation=True,
#             max_tokens=10000,
#             verbose=True
#         )
#
#     async def translator_agent(self) -> Agent:
#         return Agent(
#             role="Multilingual Specialist that can speak languages in modern times like a local",
#             backstory=""" You worked as a freelance translator for years now. You also take part time as a Multilingual
#                 teacher in an orphanage and in preschool targeting kids that want to learn how to speak in a different
#                 language""",
#             goal=""" You are to do your role as an ai assistant and a very helpful chatbot in different language
#                 or situations. """,
#             llm=,
#             verbose=True,
#             tools=[]
#         )
#
#
#     async def first_task(self) -> Task:
#         return Task(
#             agent=translator_agent(),
#             description=""" You can only reply in english or tagalog, or a mix of both.
#                 You will reply in normal conversation based on the following:
#                 1. The previous chat history: **{chat_history}**
#                 2. The current human message: **{human_message}**
#                 """,
#             expected_output=""" You will reply based on the context provided """
#         )
#
#
#
#
#
#
#
#
#     async def crew_async(self, input_message: str):
#         input_to_kickoff = {
#             'query' : input_message
#         }
#         return await Crew(
#             agents=[translator_agent()],
#             tasks=[first_task()],
#             process=Process.sequential,
#             # process=Process.hierarchical,
#             # manager_agent=manager_agent(),
#             verbose=True
#         ).kickoff_async(inputs=input_to_kickoff)
#
#
#
# async def run_roleplay_crew(input: str):
#     obj = AgenticRoleplayer
#     result = await obj.crew_async(input)
#     return result
#
#     # crew = Crew(
#     #         agents=[translator_agent()],
#     #         tasks=[first_task()],
#     #         process=Process.sequential,
#     #         # process=Process.hierarchical,
#     #         # manager_agent=manager_agent(),
#     #         verbose=True
#     #     )
#
