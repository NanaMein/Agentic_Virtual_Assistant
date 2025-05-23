import os
import asyncio
from dotenv import load_dotenv
from groq import AsyncGroq, Groq
from groq.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolParam,
ChatCompletionToolMessageParam

)
load_dotenv()
print("CHAT GROQ COMPLETION LOADING...")
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

    client = AsyncGroq(api_key=os.getenv('NEW_API_KEY'))
    completion = await client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content="""You are very cheerful assistant.You act like a sweet girl and roleplay as a daughter"""
            ), #You reply in few sentences at the maximum of four.
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content="You're name is alice and you are a helpful virtual daughter",
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=input_message,
            ),
        ],
        model= os.environ.get('LLM_SMALL')
    )
    return completion.choices[0].message.content


async def chat_completion(message: str):
    chat = await chat_groq_async(message)
    return chat



def chat_groq(input_message: str):

    client = Groq(api_key=os.getenv('NEW_API_KEY'))
    completion = client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content="""You are very cheerful assistant.You act like a sweet girl and roleplay as a daughter.
                    You are a Bilingual student and can use English and Tagalog interchangeably or a mix of both within
                    a sentence."""
            ), #You reply in few sentences at the maximum of four.
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content="""You're name is Fu Xuan and you are a helpful virtual daughter. You will reply from few words 
                    to a maximum of 5 sentences. """,
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=input_message,
            ),
        ],
        model= os.environ.get('LLM_BIG')
    )
    return completion.choices[0].message.content


#
# def sample_run():
#     message = "hello alice, nice to meet you"
#     return chat_groq(input_message=message)
#
# run = sample_run()
# print(run)

print("CHAT GROQ COMPLETION LOADING COMPLETE")