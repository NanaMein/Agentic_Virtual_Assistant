import asyncio

from crewai.flow.flow import Flow, listen, router, start, or_, and_
from pydantic import BaseModel
# from Flow_Crew_AI.Llama_RAG_Engine.llama_index_rag_engine import query_engine_small, query_engine_big
from Groq_Chat_Completion_Engine.Chat_Completion_Pipeline import chat_completion, chat_groq
# from Memory_Layer.memory_for_past_context import a

from datetime import datetime
import pytz
print("FLOW ENGINE LOADING...")

class AssistantState(BaseModel):
    input_flow_query: str = ""
    message: str =""
    time: str =""
    # internal_message: str
    output: str = ""




class VirtualAssistantFlow(Flow[AssistantState]):


    @start()
    def entry(self):
        ph_time = datetime.now(pytz.timezone('Asia/Manila'))
        self.state.time = ph_time.strftime('%Y-%m-%d %H:%M:%S %Z')
        # output = asyncio.run(chat_completion(self.state.input_flow_query))
        output = chat_groq(self.state.input_flow_query)
        self.state.message = output

    @listen(entry)
    def middle(self):
        prompt= f"""
        \n
        ****************************************************************************************\n
        \n{self.state.input_flow_query}\n
        ****************************************************************************************\n
        \n{self.state.message}\n
        ****************************************************************************************\n
        \n{self.state.time}\n
        ****************************************************************************************\n\n
        \n
        """
        self.state.output = prompt

    @listen(middle)
    def end(self):
        return self.state.output









def safe_flow_loader():
    flow_load = VirtualAssistantFlow()
    return flow_load


def flow_run(input_message: str):
    flow = safe_flow_loader()
    kickoff = flow.kickoff(inputs={'input_flow_query': input_message})
    return kickoff

print("FLOW ENGINE LOADING COMPLETE")
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

