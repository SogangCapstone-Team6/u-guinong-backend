from .state import State
from langgraph.graph import StateGraph, START, END

from langgraph.checkpoint.memory import MemorySaver

from src.llm.nodes import call_model, call_rag, call_router, route_decision

checkpointer = MemorySaver()

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
