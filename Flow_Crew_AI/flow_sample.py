import random
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel
from Flow_Crew_AI.Llama_RAG_Engine.llama_index_rag import query_engine_small, query_engine_big

class ExampleState(BaseModel):
    # success_flag: bool = False
    input_flow_query: str=""
    message: str =""

class RouterFlow(Flow[ExampleState]):

    # @start()
    # def entry_query(self):
    #     self.state.message = query_engine_small(self.state.input_flow_query)

    @start()
    def checking_query(self):
        prompt = f"""You will ONLY answer as an output of PASSED or FAILED. You are an ai that validates
        if the query *({self.state.input_flow_query})* is relevant to the context you are provided with. 
        Also simple daily conversational scenario is acceptable or PASSED. 
        
        For example 
        user: -> Hello there. 
        assistant: -> Hey there! Great day were having!
        
        also if the query is not relevant or similar or cant find about the topic, then it is FAILED"""

        response_text = query_engine_small(prompt)
        self.state.message = str(response_text).strip()
    @router(checking_query)
    def second_method(self):
        if self.state.message == "PASSED".lower():
            return "success"
        else:
            return "failed"

    @listen("success")
    def third_method(self):
        print(f"{self.state.input_flow_query} is a Success")
        return f"{self.state.input_flow_query} is a Success"

    @listen("failed")
    def fourth_method(self):
        print(f"{self.state.input_flow_query} is a Failed")
        return f"{self.state.input_flow_query} is a Failed"


# flow = RouterFlow()
#
# def flow_run (input_message: str):
#     kick = flow.kickoff(inputs={'input_flow_query': input_message})
#     return kick


