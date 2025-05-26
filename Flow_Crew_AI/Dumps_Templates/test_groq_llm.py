# from groq import Groq
# from crewai import Agent
# import json
# from crewai.llms.base_llm import BaseLLM
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# class CustomGroqLLM(BaseLLM):
#     def __init__(self, model_name, api_key=None, temperature=0.7):
#         super().__init__()
#         self.model = model_name
#         self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
#         self.temperature = temperature
#
#     def _process_tool_calls(self, response, available_functions):
#         """Handle tool calls from the LLM response"""
#         tool_calls = response.choices[0].message.tool_calls
#         if not tool_calls or not available_functions:
#             return None
#
#         # Process first tool call
#         tool_call = tool_calls[0]
#         function_name = tool_call.function.name
#         if function_name in available_functions:
#             try:
#                 arguments = json.loads(tool_call.function.arguments)
#                 return available_functions[function_name](**arguments)
#             except Exception as e:
#                 print(f"Error executing {function_name}: {str(e)}")
#         return None
#
#     def call(self, messages, tools=None, callbacks=None, available_functions=None):
#         try:
#             response = self.client.chat.completions.create(
#                 messages=messages,
#                 model=self.model,
#                 temperature=self.temperature,
#                 tools=tools or [],
#                 tool_choice="auto" if tools else None
#             )
#
#             # Handle tool calls
#             if response.choices[0].message.tool_calls:
#                 tool_result = self._process_tool_calls(response, available_functions)
#                 if tool_result:
#                     return tool_result
#
#             # Return standard response
#             return response.choices[0].message.content
#
#         except Exception as e:
#             print(f"Groq API Error: {str(e)}")
#             raise
#
# Initialize with preview model
# groq_llm = CustomGroqLLM(
#     model_name="llama3-groq-70b-8192-tool-use-preview",
#     api_key="your-api-key"
# )
#
# # Create agent with custom Groq LLM
# agent = Agent(
#     role="Researcher",
#     goal="Make comprehensive analysis",
#     backstory="Expert researcher",
#     llm=groq_llm,
#     verbose=True
# )
import json
import os
from typing import List, Dict, Optional, Any
from groq import Groq
from groq.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam
)
from typing import Optional
import os
from groq import Groq
from crewai.llms.base_llm import BaseLLM


class CustomGroqLLM(BaseLLM):
    def __init__(
            self,
            model_name: Optional[str] = None,
            api_key: Optional[str] = None,
            temperature: float = 0.7
    ):
        # Set model FIRST
        model = model_name or os.getenv('LLM_SMALL')
        if not model:
            raise ValueError(
                "Model name must be provided through either:\n"
                "1. model_name parameter\n"
                "2. LLM_SMALL environment variable\n"
                "Example: 'llama3-70b-8192' or 'mixtral-8x7b-32768'"
            )

        # Initialize parent with model BEFORE other attributes
        super().__init__(model=model)

        # Now set instance attributes
        self.model = model  # Store as instance variable if needed
        self.temperature = temperature

        # Handle API key
        self.api_key = api_key or os.getenv("NEW_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key required. Get one at: "
                "https://console.groq.com/keys\n"
                "Provide via:\n"
                "1. api_key parameter\n"
                "2. NEW_API_KEY environment variable"
            )

        self.client = Groq(api_key=self.api_key)

    def _process_tool_calls(self, response, available_functions):
        """Handle tool calls from the LLM response"""
        try:
            tool_calls = response.choices[0].message.tool_calls
            if not tool_calls or not available_functions:
                return None

            tool_call = tool_calls[0]
            function_name = tool_call.function.name
            if function_name in available_functions:
                arguments = json.loads(tool_call.function.arguments)
                return available_functions[function_name](**arguments)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
        except Exception as e:
            print(f"Tool execution error: {str(e)}")
        return None

    def call(self, messages, tools=None, callbacks=None, available_functions=None):
        try:
            # Convert messages to proper Groq format
            formatted_messages = []
            for msg in (messages if isinstance(messages, list) else [messages]):
                if isinstance(msg, str):
                    formatted_messages.append(
                        ChatCompletionUserMessageParam(
                            role="user",
                            content=msg
                        )
                    )
                else:
                    if msg["role"] == "system":
                        formatted_messages.append(
                            ChatCompletionSystemMessageParam(
                                role="system",
                                content=msg["content"]
                            )
                        )
                    elif msg["role"] == "assistant":
                        formatted_messages.append(
                            ChatCompletionAssistantMessageParam(
                                role="assistant",
                                content=msg["content"]
                            )
                        )
                    else:
                        formatted_messages.append(
                            ChatCompletionUserMessageParam(
                                role="user",
                                content=msg["content"]
                            )
                        )

            response = self.client.chat.completions.create(
                messages=formatted_messages,
                model=self.model,
                temperature=self.temperature,
                tools=tools or [],
                tool_choice="auto" if tools else None
            )

            # Handle tool calls
            if response.choices[0].message.tool_calls:
                tool_result = self._process_tool_calls(response, available_functions)
                if tool_result:
                    return tool_result

            return response.choices[0].message.content

        except Exception as e:
            print(f"Groq API Error: {str(e)}")
            raise