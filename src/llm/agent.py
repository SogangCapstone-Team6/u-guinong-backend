from .state import State
from .nodes import call_model, retrive_data
from langgraph.graph import StateGraph, START, END

from typing_extensions import Literal
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

class Route(BaseModel):
    step: Literal["RAG", "LLM"] = Field(None)

llm = init_chat_model("gpt-4o-mini")
router = llm.with_structured_output(Route)

checkpointer = MemorySaver()

def call_router(state: State):
    decision = router.invoke([
            SystemMessage(
                content="Route the input to RAG if it is related to crops. If not, route the input to LLM."
            ),
            HumanMessage(content=state["input"]),
        ])
    return {"decision": decision.step}

def call_rag(state: State):
    retrived_data = retrive_data(state);

    retrived_texts = [data["metadata"]["text"] for data in retrived_data]

    return {"retrived_data": retrived_texts}

def call_llm(state: State):
    pass

def route_decision(state: State):
    if state["decision"] == "RAG":
        return "RAG"
    elif state["decision"] == "LLM":
        return "LLM"


def get_graph():
    workflow = StateGraph(State)

    workflow.add_node("router", call_router)
    workflow.add_node("rag", call_rag)
    workflow.add_node("llm", call_model)

    workflow.add_edge(START, "router")
    workflow.add_conditional_edges(
        "router",
        route_decision,
        {
            "RAG": "rag",
            "LLM": "llm",
        }
    )
    workflow.add_edge("rag", "llm")
    workflow.add_edge("llm", END)

    graph = workflow.compile(checkpointer=checkpointer)
    return graph

graph = get_graph()
