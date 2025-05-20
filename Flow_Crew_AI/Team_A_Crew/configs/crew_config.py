from crewai import Crew, Process
from agents_config import translator_agent, manager_agent
from tasks_config import first_task
# agents = [translator_agent(), manager_agent()]
# tasks = [first_task()]


agent1 = translator_agent()
agent2 = manager_agent()
task1 = first_task()

def crew() -> Crew:
    return Crew(
        agents=[agent1,agent2],
        tasks=[task1],
        process=Process.hierarchical,
        manager_agent=manager_agent(),
        verbose=True
    )


###************************************************************************************
from Memory_Layer.memory_for_past_context import add_memories, previous_memories, reset_memories

def run():
    print('hello world')
    print("starting loop")
    while True:
        print("Re-Looping")
        message = input("Please write anything you like to say: \n\n")

        if message.lower()=="exit":
            reset_memories()
            break

        inputs_parameter = {
            'human_message': message,
            'chat_history': previous_memories()
        }

        response = crew().kickoff(inputs=inputs_parameter)
        add_memories(user_input=message, ai_output=str(response))
        print(response)
        print("*************************** END OF THE LINE ***************************")


if __name__ == '__main__':
    run()