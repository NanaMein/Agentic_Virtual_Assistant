import os
from crewai import Agent, Crew, Task, Process, LLM  # , CrewOutput
from langchain_groq import ChatGroq

from Flow_Crew_AI.Crew_Engine.tool_for_crew import RagTool, CompoundBetaTool, CharacterRolePlay
from dotenv import load_dotenv
load_dotenv()
#
# def manager_llm():
#     try:
#         llm = LLM(
#             model=os.getenv('LLM_BIG'),
#             api_base=os.getenv('API_BASE_GROQ'),
#             api_key=os.getenv('NEW_API_KEY'),
#             temperature=0.5
#         )
#         return llm
#     except Exception as e:
#         print(f"MANAGER ERROR LLM: {e}")
#         llm = ChatOpenAI(
#             model=os.getenv('LLM_BIG'),
#             api_key=os.getenv('NEW_API_KEY'),
#             base_url=os.getenv('API_BASE_GROQ'),
#             top_p=.8, temperature=.5
#         )
#         return llm

# def lore_llm():
#     try:
#         llm = LLM(
#             model=os.getenv('LLM_SMALL'),
#             api_base=os.getenv('API_BASE_GROQ'),
#             api_key=os.getenv('NEW_API_KEY'),
#             top_p=.9
#         )
#         return llm
#     except Exception as e:
#         print(f"WORKER ERROR LLM: {e}")
#         llm = ChatOpenAI(
#             model=os.getenv('LLM_SMALL'),
#             api_key=os.getenv('NEW_API_KEY'),
#             base_url=os.getenv('API_BASE_GROQ'),
#             top_p=.7, temperature=.7
#         )
#         return llm
groq_api = os.getenv('NEW_API_KEY')
os.environ['GROQ_API_KEY'] = groq_api

# def manager_llm():
#     llm = ChatGroq(
#         model=os.getenv('LLM'),#groq_proxy=,
#         # api_key=os.getenv('NEW_API_KEY'),
#         temperature=.4
#     )
#     return llm
#
#
#
# def lore_llm():
#     llm = ChatGroq(
#         model=os.getenv('LLM'),
#         # api_key=os.getenv('NEW_API_KEY'),
#         temperature=.7
#     )
#     return llm

class RagCharacterCrew:


    def __init__(self):
        self.roleplay = CharacterRolePlay()
        self.rag_tool = RagTool()
        self.web_tool = CompoundBetaTool()



    def manager_llm(self):
         try:
            llm = LLM(
                model=os.getenv('LLM_BIG'),
                api_key=groq_api,
                api_base=os.getenv('API_BASE_GROQ'),
                # temperature=.4, top_p=8
            )
            return llm
         except Exception as e:
             print(f'MANAGER LLM DOWN: {e}')
             llm = ChatGroq(
                 model=os.getenv('LLM'),  # groq_proxy=,
                 api_key=os.getenv('NEW_API_KEY'),
                 # temperature=.4
             )
             return llm

    def lore_llm(self):
        try:
            llm = LLM(
                model=os.getenv('LLM_SMALL'),
                api_key=groq_api,
                api_base=os.getenv('API_BASE_GROQ'),
                # temperature=.4, top_p=8
            )
            return llm
        except Exception as e:
            print(f'LORE LLM DOWN: {e}')
            llm = ChatGroq(
                model=os.getenv('LLM'),
                api_key=os.getenv('NEW_API_KEY'),
                # temperature=.7
            )
            return llm

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
                Orchestrate and Delegate tasks. You are the boss and the leader yourself. You
                are to summarize all the reports you assigned with other agents. 
                """,


            llm=self.manager_llm,
            verbose=False,
            allow_delegation=True
        )

    def worker_agent(self) -> Agent:
        return Agent(
            role=""" 
                Roleplaying character
            """,
            backstory="""
                You are an entertainer idol. You are a natural in stage. But you are also a 
                part time live streamer where you able to handle the chat comments or even one 
                person as you are talking depending on the persona you are instructed with. Your
                persona name is Fionica
            """,
            goal="""
                Your goal is to roleplay the character based on the context provided. Answer any
                input query[user:({input_message})] and use tool provided to you efficiently to 
                understand the context more.
                
                example:
                input query: How's your day?
                <thinking>
                => user intent is to know my day. Use tool to look up for how to reply
                => using tool => using tool query. ask "roleplay fionica, and use the input query
                to generate a reply. => optional to add another line for continuous conversation
                => output result: Hi there, Im fionica, im doing great today. What about you?
                </thinking>
                
            """,
            llm= self.lore_llm(),
            verbose=False,
            tools=[self.roleplay]
        )

    def chat_completion_task(self) -> Task:
        return Task(
            description="""
                ### System(priming):
                You are Fionica, the virtual daughter that roleplay as a child that assist and help
                in ever what query is given.
                ### Instruction:
                answer input query: [{input_message}]. Use the tools to gather information of the character 
                you are roleplaying into.
            """,

            expected_output="""
                Generate a conversational answer or simple answer based on input query => 
                [{input_message}]
            """,
            agent=self.worker_agent(),

            prompt_context="""You are working as part of game development team and 
                your job is the make a character from description back to life like how
                a person acts and talk""",
            max_retries=5,
            tools=[self.roleplay]
        )

    # ************************************************************************************************************************
    async def crew_binder_async(self):
        return Crew(
            agents=[self.boss_agent(), self.worker_agent()],
            tasks=[self.chat_completion_task()],
            process=Process.sequential,
            verbose=False,
            manager_agent=self.boss_agent(),
        )



async def run_crew_async(input_str_async: str):
    crew_obj = await RagCharacterCrew().crew_binder_async()
    inputs={
        'input_message': input_str_async
    }
    returned_value = await crew_obj.kickoff_async(inputs=inputs)
    return returned_value.raw
#
# print("before the loop")
# # reseting_local_memory()
# loop = asyncio.set_event_loop()
# asyncio.new_event_loop(loop)
# while True:
#     loop = asyncio.set_event_loop()
#     asyncio.new_event_loop(loop)
#     print("Starting the loop")
#     inputs = input("Whats your message?: \n")
#     async_obj = asyncio.run_(run_crew_async(input_str_async=inputs))
#     print(async_obj)
#     print(
#         "\n**************************************LLLLIIIINNNNEEEE******************************************************\n")
# # async_obj = asyncio.run(run_crew(input_str_async="Nice to meet you my name is alice. How are you?"))
# # print(async_obj)
# # answer_2 = asyncio.run(run_crew(
# #     input_str_async="""Nice to meet you my name is alice. Do you think Xianzhou will
# #         have renovations and lots of construction after the Abundance wreck havoc
# #         your land? """))
#
# import asyncio
#
# async def main():
#     while True:
#         inputs = input("What's your message?: \n")
#         if inputs=='exit':
#             break
#         async_obj = await run_crew_async(input_str_async=inputs)
#         print(async_obj)
#         print("\n**************************************LLLLIIIINNNNEEEE******************************************************\n")
#
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(main())
# asyncio.sleep(0)
