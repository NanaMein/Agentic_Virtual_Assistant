import asyncio
import os
from typing import Any
from dotenv import load_dotenv
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from groq import Groq
from typing import Type
from groq.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolParam,
    ChatCompletionToolMessageParam
)

load_dotenv()


class BaseCompoundBeta(BaseModel):
    argument: str = Field(..., description="Input for what you want to search in the web")


class CompoundBeta(BaseTool):
    name: str = "Web search query tool"
    description: str = "Tool for searching the web"
    args_schema: Type[BaseModel] = BaseCompoundBeta

    def _run(
            self,
            argument: str,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        client = Groq(api_key=os.environ.get('API_KEY'))
        completion = client.chat.completions.create(
            messages=[
                ChatCompletionAssistantMessageParam(
                    role="assistant",
                    content="You are a very helpful ai assistant tool",
                ),
                ChatCompletionUserMessageParam(
                    role="user",
                    content=argument,
                ),
            ],
            model="compound-beta-mini",
        )

        return completion.choices[0].message.content

