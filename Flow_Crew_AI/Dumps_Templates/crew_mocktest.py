from crewai import Agent
from LLM_and_Model_Config.llm_config import crew_llm_worker, crew_llm_manager
# from Team_A_Crew.tools_and_utils.crew_tools import WhatLanguage
#
# language_tool= WhatLanguage


def manager_agent() -> Agent:
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

def translator_agent() -> Agent:
    return Agent(
        role="Multilingual Specialist that can speak languages in modern times like a local",
        backstory=""" You worked as a freelance translator for years now. You also take part time as a Multilingual
            teacher in an orphanage and in preschool targeting kids that want to learn how to speak in a different
            language""",
        goal=""" You are to do your role as an ai assistant and a very helpful chatbot in different language
            or situations. """,
        llm=crew_llm_worker(),
        verbose=True,
        tools=[]
    )

from crewai import Task
# from agents_config import translator_agent

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







from crewai import Crew, Process
# from agents_config import translator_agent, manager_agent
# from tasks_config import first_task
# agents = [translator_agent(), manager_agent()]
# tasks = [first_task()]

#
# agent1 = translator_agent()
# agent2 = manager_agent()
# task1 = first_task()

def crew() -> Crew:
    return Crew(
        agents=[translator_agent()],
        tasks=[first_task()],
        process=Process.sequential,
        # process=Process.hierarchical,
        # manager_agent=manager_agent(),
        verbose=True
    )


###************************************************************************************
from Memory_Layer.memory_for_past_context import add_memories, previous_memories, reset_memories
#
# def run():
#     print('hello world')
#     print("starting loop")
#     print ("testing the ")
#     while True:
#         print("Re-Looping")
#         message = input("Please write anything you like to say: \n\n")
#         counter = 1
#         if message.lower()=="exit":
#             reset_memories()
#             break
#
#         if counter == 1:
#             inputs_parameter = {
#                 'human_message': message,
#                 'chat_history': 'no chat history yet'
#             }
#             response = crew().kickoff(inputs=inputs_parameter)
#             add_memories(user_input=message, ai_output=str(response))
#             print(response)
#             print("*************************** END OF THE LINE ***************************")
#
#         inputs_parameter = {
#             'human_message': message,
#             'chat_history': previous_memories()
#         }
#
#         response = crew().kickoff(inputs=inputs_parameter)
#         add_memories(user_input=message, ai_output=str(response))
#         print(response)
#         print("*************************** END OF THE LINE ***************************")
#
#
# if __name__ == '__main__':
#     run()
#
#
def run():
    print('hello world')
    print("starting loop")
    print("testing the ")

    chat_history = []  # Initialize chat_history here

    while True:
        print("Re-Looping")
        message = input("Please write anything you like to say: \n\n")

        if message.lower() == "exit":
            reset_memories()  # Assuming this function is defined elsewhere
            break

        inputs_parameter = {
            'human_message': message,
            'chat_history': chat_history  # Use the list
        }

        response = crew().kickoff(inputs=inputs_parameter)  # Assuming crew() is defined

        chat_history.append({"user": message, "ai": str(response)}) # Update chat_history
        add_memories(user_input=message, ai_output=str(response)) #add to memories.

        print(response)
        print("*************************** END OF THE LINE ***************************")
        #counter +=1 #not needed

if __name__ == '__main__':
    run()