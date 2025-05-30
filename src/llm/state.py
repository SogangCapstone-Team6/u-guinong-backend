from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    input: str
    decision: str
    disease: str
    retrived_data: list
