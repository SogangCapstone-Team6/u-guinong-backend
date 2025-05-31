from functools import lru_cache
from pydantic import BaseModel, Field
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from src.llm.state import State
from src.llm.utils import build_prompt
from src.rag import retrive_data

class Route(BaseModel):
    step: Literal["RAG", "LLM"] = Field(None)

llm = init_chat_model("gpt-4o-mini")
router = llm.with_structured_output(Route)

@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")
    return model


def route_decision(state: State):
    if state["decision"] == "RAG":
        return "RAG"
    elif state["decision"] == "LLM":
        return "LLM"


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


def call_model(state, config):
    prompt = build_prompt(state)
    model_name = config.get('configurable', {}).get("model_name", "openai")
    model = _get_model(model_name)
    response = model.invoke(prompt)
    return {"messages": [response]}
