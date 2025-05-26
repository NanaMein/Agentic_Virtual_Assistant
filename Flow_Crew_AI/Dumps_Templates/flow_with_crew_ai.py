import asyncio
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
# from Flow_Crew_AI.Llama_RAG_Engine.llama_index_rag_engine import query_engine_small, query_engine_big
from Memory_Layer.memory_for_past_context import get_memory_context_prompt, reseting_local_memory
# from Memory_Layer.memory_for_past_context import a

from datetime import datetime
import pytz

print("FLOW ENGINE LOADING...")


class FionicaState(BaseModel):
    input_flow_query: str = ""
    message: str = ""
    time: str = ""
    # output: str = ""
    chat_history: str = ""


class FionicaFlow(Flow[FionicaState]):

    @start()
    async def starting(self):
        try:
            self.state.chat_history = get_memory_context_prompt()
            self.state.time = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%d %H:%M:%S %Z')
            return "yes"
        except Exception as e:
            self.state.chat_history = f"{e}"
            return "no"

    @listen(starting)
    async def next(self):
        message = f"""
        ###Chat history: {self.state.chat_history}\n
        ###Time zone: {self.state.time}\n
        ###Input query: {self.state.input_flow_query}
        """
        self.state.message = message
        return "exiting"

    @listen("exiting")
    async def last(self):
        print("FINALLY FUCKED LAST FUNCTION")
        return self.state.message



async def flow_run(input_message: str) -> str:
    flow = FionicaFlow()
    # flow.()
    kickoff = await flow.kickoff_async(inputs={'input_flow_query': input_message})
    return str(kickoff)


print("FLOW ENGINE LOADING COMPLETE")

#
# def run():
#     while True:
#         print("starting loop and looping again")
#         input_message = input("Write something: \n\n")
#         if input_message == "exitingloop":
#             reseting_local_memory()
#             break
#         # flow = flow_run(input_message=input_message)
#         flow =asyncio.run(flow_run(input_message=input_message))
#         print(flow)
#         print("\n*********************************ENDLINE**********************************\n\n")
#
#
# if __name__ == '__main__':
#     run()

