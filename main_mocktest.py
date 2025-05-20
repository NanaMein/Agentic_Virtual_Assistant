from Team_A_Crew.configs.crew_config import crew
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