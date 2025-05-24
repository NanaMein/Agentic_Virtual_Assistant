import random
from crewai.flow.flow import Flow, listen, router, start, or_, and_
from pydantic import BaseModel
from Flow_Crew_AI.Llama_RAG_Engine.llama_index_rag_engine import query_engine_small, query_engine_big

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
        if the query  is relevant to the context you are provided is considered Passed. 
        Also simple daily conversational scenario is acceptable or PASSED. 
        
        For example 
        user: -> Hello there. 
        user: how is the weather?
        user: do you know fu xuan?
        user: where does fu xuan lives?
        
        If the query is not relevant or similar or cant find about the topic, then it is FAILED

        query => *({self.state.input_flow_query})*"""

        response_text = query_engine_small(prompt)
        self.state.message = str(response_text).strip()
        print(self.state.message)
    @router(checking_query)
    def second_method(self):
        if self.state.message.lower() == "passed":  # Ensuring case insensitivity
            return "success"
        elif self.state.message.lower() == "failed":  # Adding a proper condition
            return "failed"
        else:
            return "WHATDAFUCKISDIZSHIT?"  # If none of the conditions match


    @listen("success")
    def third_method(self):
        print(f"{self.state.input_flow_query} is a Success")
        self.state.message = "Lottery win motherfucker"
        return f"{self.state.input_flow_query} is a Success"

    @listen("failed")
    def fourth_method(self):
        print(f"{self.state.input_flow_query} is a Failed")
        self.state.message = "failure bitch"
        return f"{self.state.input_flow_query} is a Failed"

    @listen("WHATDAFUCKISDIZSHIT")
    def fifth_method_shit(self):
        print(f"{self.state.input_flow_query} is a Failed")
        self.state.message = "I DONT EVEN KNOW A GODDAMN SHIT"
        return f"{self.state.input_flow_query} is a FUUUUUUUUUUUCCCCCCCCKKKKKKKKKKKKKKKK"

    @listen(or_(third_method,fourth_method,fifth_method_shit))
    def final_method(self):
        print("FUCKK YOUUUU")
        return self.state.message

def safe_flow_loader():
    flow_load = RouterFlow()
    return flow_load

def flow_run (input_message: str):
    flow = safe_flow_loader()
    kickoff = flow.kickoff(inputs={'input_flow_query': input_message})
    return kickoff


