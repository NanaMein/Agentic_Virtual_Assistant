from typing import Any

from crewai.tools import BaseTool



class CheckIfValid(BaseTool):
    name: str = "Validator tool"
    description = "about the tool"




class WhatLanguage(BaseTool):

    def __init__(self):
        super().__init__()
        self.name = "Language validator tool"
        self.description = "This tool describe and instruct you what language to use if you dont know what to use"

    def _run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return """ You will only use Tagalog and English language.
        Your main language is English, so you reply in english most of the time. 
        But you can also use tagalog if you are asked in tagalog. You can mix tagalog and english together
        is also acceptable.
        """