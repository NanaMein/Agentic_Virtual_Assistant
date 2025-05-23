# from Team_A_Crew.configs.crew_config import crew
# from Memory_Layer.memory_for_past_context import add_memories, previous_memories, reset_memories
# from Flow_Crew_AI.flow_sample import RouterFlow, flow_run
from Flow_Crew_AI.flow_engine import flow_run
def run():
    # print('hello world')
    # print("starting loop")
    # while True:
    #     print("Re-Looping")
    #     message = input("Please write anything you like to say: \n\n")
    #
    #     if message.lower()=="exit":
    #         reset_memories()
    #         break
    #
    #     inputs_parameter = {
    #         'human_message': message,
    #         'chat_history': previous_memories()
    #     }
    #
    #     response = crew().kickoff(inputs=inputs_parameter)
    #     add_memories(user_input=message, ai_output=str(response))
    #     print(response)
    #     print("*************************** END OF THE LINE ***************************")
    while True:
        print ("starting loop and looping again")
        input_message = input("Write something: \n\n")
        if input_message=="exitingloop":
            break
        # flow = flow_run(input_message=input_message)
        flow = flow_run(input_message=input_message)
        print(flow)
        print("\n*********************************ENDLINE**********************************\n\n")


if __name__ == '__main__':
    run()