import asyncio
from typing import Optional
from crewai.flow import persist, Flow, listen, start, or_, and_, router
from pydantic import BaseModel
from Flow_Crew_AI.Crew_Engine.hierarchical_v1 import run_crew_async
from datetime import datetime
import pytz

print("FLOW ENGINE LOADING...")

from .Groq_Chat_Completion_Engine.Chat_Completion_Pipeline import router_llm_async, chat_completion
from .Crew_Engine.agents_personality import query_engine_chat_async
from .Memory_Layer.llama_index_memory_context import indexed_chat_context, indexed_query_engine

class FionicaState(BaseModel):
    input_flow_query: str = ""
    output_crew: str = ""
    choice_route: str = ""
    output_result: str = ""
    prompt_for_input: str =""


class FionicaFlow(Flow[FionicaState]):

    def __init__(self):
        super().__init__()
        self.vector_memory = None
        self.vector_query = None


    # @start()
    # async def starting(self):
    #
    #     router = await router_llm_async(self.state.input_flow_query)
    #     self.state.choice_route = router


    @start()
    async def vector_memory_layer(self):
        query_instruction =f"""
            ### System(priming): You are a conversation summarizing context chatbot. \n
            
            ### Input query: [self.state.input_flow_query] \n
        
            ### Instruction: You are to retrieve relevant, similar, related information of 
                input query with the context you are provided. If data or information IS NOT
                found, with the 4 most recent utc time with conversation of user and 
                assitant, summarize your those conversations by explaining the context \n
            
            ### Expected output: You are to either retrieve the most relevant information or
                summarize the few most recent conversation based on utc time provided if 
                information you need is not found
            """
        self.vector_query = await indexed_query_engine(query_instruction)

        prompt_template = f""" 
            ### previous summarized chat context: [{self.vector_query}]
            
            ### Instruction: Use chat context as reference only, ignore it if its empty or 
            is not needed, instead, FOCUS more on the CURRENT INPUT CONTEXT
            
            ### Current input context: [{self.state.input_flow_query}]                  
            """
        self.state.prompt_for_input = prompt_template



    @router(vector_memory_layer)
    async def routing_section(self):
        self.state.choice_route = await router_llm_async(self.state.input_flow_query)

        if self.state.input_flow_query == "resetinglove":
            return "exit"
        elif self.state.choice_route == 'CONVERSATIONAL':
            return 'CONVERSATIONAL'
        elif self.state.choice_route == 'GENERALPURPOSE':
            return 'GENERALPURPOSE'
        elif self.state.choice_route == 'FAIL':
            return 'FAIL'
        else:
            return 'NONE'




    @listen("CONVERSATIONAL")
    async def converse(self):
        try:
            self.state.output_crew = await run_crew_async(self.state.prompt_for_input)

            self.vector_memory = await indexed_chat_context(
                self.state.input_flow_query,
                self.state.output_crew
            )
            return self.state.output_crew

        except Exception as e:
            print(f"error putangina: {e}")
            self.state.output_crew = await query_engine_chat_async(self.state.prompt_for_input)

            self.vector_memory = await indexed_chat_context(
                self.state.input_flow_query,
                self.state.output_crew
            )
            return self.state.output_crew



    @listen("GENERALPURPOSE")
    async def genpur(self):

        self.state.output_crew = await chat_completion(self.state.prompt_for_input)

        self.vector_memory = await indexed_chat_context(
            self.state.input_flow_query,
            self.state.output_crew
        )

        return self.state.output_crew

    @listen("FAIL")
    async def fail(self):
        output = (f"RouterResult{self.state.choice_route} + RawOutput{self.state.output_result}"
                  f"failure failure failure")
        return output


    @listen("NONE")
    async def exiting(self):
        # await self.persist_test()
        # self.state.testing_counter += 1

        return """Please try again later with a different query"""




async def flow_run(input_message: str):
    try:
        flow = FionicaFlow()
        flow_output = await flow.kickoff_async(inputs={'input_flow_query': input_message})
        return str(flow_output)
    except Exception as e:
        print(f"Error: {e}")
        return None

print("FLOW ENGINE LOADING COMPLETE")


#
# def run():
#     # Create a single event loop for the entire session
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#
#     try:
#         while True:
#             print("Starting conversation...")
#             input_message = input("Write something: \n\n")
#             if input_message.lower() == "exit the loop now":
#                 break
#
#             # Run async code in the existing loop
#             flow = loop.run_until_complete(flow_run(input_message))
#             print(flow)
#             print("\n" + "*" * 35 + " END " + "*" * 35 + "\n")
#
#     finally:
#         # Cleanup when done
#         loop.run_until_complete(asyncio.sleep(0))
#         loop.close()
#         print("Event loop closed properly")
#
#
# if __name__ == '__main__':
#     run()
