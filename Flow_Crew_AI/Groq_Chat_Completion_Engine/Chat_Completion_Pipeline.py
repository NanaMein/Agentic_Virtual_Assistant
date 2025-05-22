import os
import asyncio
from groq import AsyncGroq
from groq.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam
)

async def tool_async(input_message: str):
    client = AsyncGroq(api_key=os.environ.get('API_KEY'))

    completion = await client.chat.completions.create(
        messages=[
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content="You are a very helpful ai tool",
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=input_message,
            ),
        ],
        model="compound-beta-mini",
    )
    return completion.choices[0].message.content


async def chat_groq_async(input_message: str):
    client = AsyncGroq(api_key=os.environ.get('API_KEY'))

    completion = await client.chat.completions.create(
        messages=[
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content="You are a very helpful ai tool",
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=input_message,
            ),
        ],
        model="compound-beta-mini",
    )
    return completion.choices[0].message.content
async def chat_completion(message: str):
    chat = await chat_groq_async(message)

asyncio.run(main())