import asyncio
from datetime import datetime, timezone
import os
from typing import Any
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process, LLM
from .tool_for_crew import CompoundBeta


load_dotenv()


def agent_llm_basic() -> LLM:
    return LLM(
        model=os.getenv('LLM_SMALL'),
        api_base=os.getenv('API_BASE_GROQ'),
        api_key=os.getenv('NEW_API_KEY'),
        temperature=0.75
    )
def tool_llm() -> LLM:
    return LLM(
        model="groq/compound-beta",
        api_base=os.getenv('API_BASE_GROQ'),
        api_key=os.getenv('NEW_API_KEY'),
        temperature=0.75
    )
def manager_llm()-> LLM:
    return LLM(
        model=os.getenv('LLM_BIG'),
        api_base=os.getenv('API_BASE_GROQ'),
        api_key=os.getenv('NEW_API_KEY'),
        temperature=0.75
    )



# Main class that builds and runs the crew
class AgenticRoleplayer:


    def __init__(self):
        self.llm = agent_llm_basic()
        self.tool = tool_llm()
        self.manager = manager_llm()
        self.real_tool = CompoundBeta()
        self.timenow = datetime.now(timezone.utc)

    def translator_agent(self) -> Agent:
        return Agent(
            role="Multilingual Specialist",
            backstory=(
                "You worked as a freelance translator for years. "
                "You also teach multilingual communication to children and adults alike."
            ),
            goal=(
                "Act as a friendly and helpful AI assistant capable of switching between languages "
                "like English and Tagalog naturally during a conversation."
                "You can speak english and tagalog separately in a sentence or a mix of both"
                "Able to use modern english and tagalog slangs, expressions, and cursing words"
            ),
            llm=self.llm,
            verbose=False,
            tools=[self.real_tool]

        )

    def first_task(self) -> Task:

        return Task(
            description=(
                "You can only reply in English or Tagalog, or a mix of both. "
                "Conversational scenarios. Always generate new content, conversation,"
                "topics, comedy and much more in your imagination"
                "Use tools if cant understand other words "
            ),
            agent=self.translator_agent(),
            expected_output="You will reply based on the context provided."
                            "<context>{human_message}</context>"
                            "<real_time>"
                            f"###UTC Time: {self.timenow}"
                            "Please convert UTC time to Philippine Time"
                            "</real_time>",
            tools=[self.real_tool]

        )

    def build_crew(self) -> Crew:
        agent = self.translator_agent()
        task = [self.first_task()]
        return Crew(
            agents=[agent],
            tasks=task,
            process=Process.sequential,
            verbose=False,
            function_calling_llm=self.tool,
            # planning=True,
            # manager_llm=self.manager
        )

    # async def run_crew(self, input_msg: str):
    #     crew = self.build_crew(input_msg)
    #     inputs = {
    #         "human_message": input_msg
    #           # Optionally extend this later with memory
    #     }
    #     return await crew.kickoff_async(inputs=inputs)
    def run_crew(self, input_msg: str):
        crew = self.build_crew()
        inputs = {
            "human_message": input_msg
        }
        return crew.kickoff(inputs=inputs)

# -------- Entry Point (Script Usage) --------
# if __name__ == "__main__":
#     user_input = input("Enter your message: ")
#     roleplayer = AgenticRoleplayer()
#     result = asyncio.run(roleplayer.run_crew(user_input))
#     print("\n💬 AI Response:\n", result)
