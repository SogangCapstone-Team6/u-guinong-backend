from state import State
from nodes import call_model
from langgraph.graph import StateGraph, START, END


def get_graph():
    workflow = StateGraph(State)

    workflow.add_node("model", call_model)

    workflow.add_edge(START, "model")
    workflow.add_edge("model", END)

    graph = workflow.compile()
    return graph