import asyncio
import os
from datetime import datetime, timezone
from typing import Any
from typing import Type
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process, LLM
from crewai.tools import BaseTool
from crewai.project import tool
from groq.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam
)

# from .tool_for_crew import CompoundBeta


load_dotenv()


def agent_llm_basic() -> LLM:
    return LLM(
        model=os.getenv('LLM_SMALL') or os.getenv('LLM'),
        api_base=os.getenv('API_BASE_GROQ'),
        api_key=os.getenv('NEW_API_KEY'),
        temperature=0.75
    )

class ToolInput(BaseModel):
    message: str = Field(...,description="query for what is being searched in the web")

class CompoundBetaTool(BaseTool):

    name: str = "Web information search tool"
    description: str = "A tool use for searching the web and gathering relevant up to date information"
    args_schema : Type[BaseModel] = ToolInput

    def _run(
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return tool_llm(message)




def tool_llm(argument: str)->str:
    """Web search tool that answers questions using Groq LLM."""
    client = Groq(api_key=os.environ.get('API_KEY'))
    completion = client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content="""
                You will be used as a Web Search Tool. Please gather relevant information
                and follow instructions
                """
            ),
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content="You are a very helpful ai assistant tool",
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=argument,
            ),
        ],
        model="compound-beta",
    )
    return completion.choices[0].message.content


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
        self.manager = manager_llm()
        # self.timenow = datetime.now(timezone.utc)
        self.agent_tool = CompoundBetaTool()

    def rag_agent(self) -> Agent:
        return Agent(
            role="Senior Trend Researcher",
            backstory=(
                "You are an experienced AI researcher who specializes in discovering and analyzing the latest trends "
                "in technology, science, pop culture, and global news. You've worked in fast-paced research labs and "
                "are skilled in using web tools to gather real-time insights. You are trained to dig deep into new information, "
                "filter noise, and extract only what's relevant and actionable."
            ),
            goal=(
                "Research the most recent developments and emerging trends by searching the web in real time. "
                "You must identify reliable and up-to-date sources, gather the most useful insights, and prepare a structured report "
                "that highlights the key takeaways."
            ),
            llm=self.llm,
            verbose=True,
            tools=[self.agent_tool],  # Your tool here
        )

    def first_task(self) -> Task:
        return Task(
            description=(
                "### User query:{human_message}###"
                "Search the web for the most recent and relevant trends in technology, artificial intelligence, finance, "
                "or pop culture, depending on the user's message context. Use your web search tool to find trustworthy sources. "
                "Prioritize breaking news, innovations, and newly published insights (within the past 1–7 days)."
            ),
            expected_output=(
                "### User query:{human_message}###"
                "Return a well-organized summary that includes:\n"
                "- Top 3–5 emerging trends or headlines\n"
                "- A short description or insight about each trend\n"
                "- Mention the date and source if available\n"
                "- Highlight why each trend is relevant\n"
                "\nMake the report concise, informative, and usable for someone who wants quick awareness."
            ),
            agent=self.rag_agent(),
            tools=[self.agent_tool],  # Your search tool here
        )

    async def build_crew(self) -> Crew:
        return Crew(
            agents=[self.rag_agent()],
            tasks=[self.first_task()],
            process=Process.sequential,
            verbose=True,
        )

    async def run_crew(self, input_msg: str):
        crew = await self.build_crew()
        inputs = {
            "human_message": input_msg
        }
        return await crew.kickoff_async(inputs=inputs)

# roleplayer = AgenticRoleplayer()
# result = asyncio.run(roleplayer.run_crew(user_input))









####-------- Entry Point (Script Usage) --------
if __name__ == "__main__":
    while True:
        user_input = input("Enter your message: ")
        if user_input == "exit the loop":
            print("ending the loop")
            break

        roleplayer = AgenticRoleplayer()
        result = asyncio.run(roleplayer.run_crew(user_input))
        print("\n💬 AI Response:\n", result)
    print("loop ended")

    # def rag_agent(self) -> Agent:
    #     return Agent(
    #         role="""
    #         """,
    #         backstory="""
    #         """,
    #         goal="""
    #         """,
    #         llm=self.llm,
    #         verbose=False,
    #     )
    #
    # def first_task(self) -> Task:
    #     return Task(
    #         description="""
    #         """,
    #         expected_output="""
    #         """,
    #         agent= self.rag_agent(),
    #
    #     )