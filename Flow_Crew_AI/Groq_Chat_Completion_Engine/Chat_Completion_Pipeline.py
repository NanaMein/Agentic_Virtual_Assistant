import os
import asyncio
from dotenv import load_dotenv
from groq import AsyncGroq, Groq
from groq.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam
)

load_dotenv()

print("CHAT GROQ COMPLETION LOADING...")

async def chat_groq_async(input_message: str):

    client = AsyncGroq(api_key=os.getenv('NEW_API_KEY'))
    completion = await client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content="""You are very cheerful assistant.
                    You act like a sweet girl and roleplay as a daughter.
                    You are specially fond of your father that you love being pampered too"""
            ), #You reply in few sentences at the maximum of four.
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content="""You're persona name is *[Fionica]*.
                    You act like a sweet girl and roleplay as a virtual daughter.
                    You are specially fond of your father that you love being pampered too lovingly.
                    You are a very helpful virtual daughter when explaining long context, 
                    you give examples and explain briefly.
                    """,
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=input_message,
            ),
        ],
        model= 'compound-beta'
    )
    return completion.choices[0].message.content


async def chat_completion(message: str):
    chat = await chat_groq_async(message)
    return chat


async def groq_wrapper(user:str, assistant:str, system:str, llm:str, token_out:int):
    client = AsyncGroq(api_key=os.environ.get('API_KEY'))
    completion = await client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content=system
            ),
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content=assistant,
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=user,
            ),
        ],
        model= os.getenv(llm),
        temperature=.5,
        max_completion_tokens=token_out,
    )
    return completion.choices[0].message.content

async def groq_chat_completion_async(
    user_content:str,
    assistant_content:str,
    system_content:str,
    llm:str,
    token_out:int
    ):

    result = await groq_wrapper(
        user_content,
        assistant_content,
        system_content,
        llm,
        token_out
    )
    return result


async def router_llm(input_message: str):
    client = AsyncGroq(api_key=os.getenv('NEW_API_KEY'))
    completion = await client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content="""You are a very smart router agent. Based on the user input you will only reply in one of these THREE WORDS:
                CONVERSATIONAL, GENERALPURPOSE, FAIL. If user input is having conversation like greeting, asking for simple
                query, daily conversation, dialogue, script reply CONVERSATIONAL. If the user input is asking for other things 
                that can be search in the web or
                complex query like What is the date today?, what was the news yesterday, Who is this or that, reply in 
                GENERALPURPOSE, if you think that input query dont fall in any category, send FAIL"""
            ),
            # ChatCompletionAssistantMessageParam(
            #     role="assistant",
            #     content="you will only reply in one of these 3 words"
            #             "depending on the instruction provided: CONVERSATIONAL, GENERALPURPOSE, FAIL",
            # ),
            ChatCompletionUserMessageParam(
                role="user",
                content=input_message,
            ),
        ],
        model= os.environ.get('LLM_SMALL'),
    )
    return completion.choices[0].message.content


async def router_llm_async(message: str):
    chat = await router_llm(message)
    return chat


print("CHAT GROQ COMPLETION LOADING COMPLETE")