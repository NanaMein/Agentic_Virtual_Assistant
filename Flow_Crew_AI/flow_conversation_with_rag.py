import asyncio

from crewai.flow.flow import Flow, listen, router, start, or_, and_
from pydantic import BaseModel
from Flow_Crew_AI.Llama_RAG_Engine.llama_index_rag_engine import query_engine_small, query_engine_big
from Groq_Chat_Completion_Engine.Chat_Completion_Pipeline import chat_completion, chat_groq
from Memory_Layer.memory_for_past_context import add_to_memory, get_memory_context_prompt, reseting_local_memory

# from Memory_Layer.memory_for_past_context import a

from datetime import datetime
import pytz
print("FLOW ENGINE LOADING...")

class ChatBotState(BaseModel):
    input_flow_query: str = ""
    message: str =""
    time: str = ""
    output: str = ""
    chat_history: str = ""

class ChatBotFlow(Flow[ChatBotState]):

    @start()
    def starting(self):
        try:
            self.state.chat_history = get_memory_context_prompt()
            self.state.time = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%d %H:%M:%S %Z')
            return "yes"
        except Exception as e:
            self.state.chat_history = f"{e}"
            return "no"



    @start()
    def chat_completion(self):
        document = query_engine_big(self.state.input_flow_query)

        prompt_template = f"""
            <document knowledge>
            DOCUMENT: [{document}]
            </document knowledge>
            
            <previous chat history context>
            HISTORY CONTEXT: [{self.state.chat_history}]
            </previous chat history context>
            
            <user current query>
            USER: [{self.state.input_flow_query}]
            </user current query>
            
            ### Date and Time:
            [{self.state.time}]
            
            ### INSTRUCTION:
            You are to give answer based on the context provided. Focus on the user query, generate new content every
            query user but also decide if you want to stay in the topic. 
            
        """
        #Document knowledge is optional but can be used for content generation.
        output = chat_groq(prompt_template)
        self.state.message = output


    @router(chat_completion)
    def memory(self):
        memory = add_to_memory(
            user_input=self.state.input_flow_query,
            ai_output= self.state.message
        )

        if memory:
            return "added_memory"
        return "no_memory"

    @listen("no_memory")
    def error_catcher(self):
        return "error try again later"

    @listen("added_memory")
    def context_history(self):
        return self.state.message

#
# #
# def safe_flow_loader():
#     flow_load = ChatBotFlow()
#     return flow_load
# #
#
def flow_run(input_message: str) -> str:
    flow = ChatBotFlow()
    # flow.()
    kickoff = flow.kickoff(inputs={'input_flow_query': input_message})
    return str(kickoff)

print("FLOW ENGINE LOADING COMPLETE")
def run():

    while True:
        print ("starting loop and looping again")
        input_message = input("Write something: \n\n")
        if input_message=="exitingloop":
            reseting_local_memory()
            break
        # flow = flow_run(input_message=input_message)
        flow = flow_run(input_message=input_message)
        print(flow)
        print("\n*********************************ENDLINE**********************************\n\n")


if __name__ == '__main__':
    run()

