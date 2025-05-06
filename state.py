from typing import TypedDict, Annotated, Sequence
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

