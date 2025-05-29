from functools import lru_cache
from langchain_openai import ChatOpenAI

from src.core.config import TOP_K_CHUNKS, TOP_K_SECTIONS
from src.rag.setup import section_data, chunk_index
from src.rag.embedding_model import embedding_model
from src.rag.section_coarse_search import coarse_search_sections
from src.rag.fine_search import fine_search_chunks

@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")
    return model

def call_model(state, config):
    system_prompt = """
    You are an agricultural expert specializing in helping young people who have returned to farming in rural areas. Based on the information provided, please give the best possible advice. But it should be only based on fact and given information. If you don't know, just say you don't know
    """

    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    if(state["decision"] == "RAG"):
        rag_prompt = "Here is some information you can refer\n"
        for data in state["retrived_data"]:
            rag_prompt = rag_prompt + data + "\n"
        messages = messages + [{"role": "system", "content": rag_prompt}]

    model_name = config.get('configurable', {}).get("model_name", "openai")
    model = _get_model(model_name)
    response = model.invoke(messages)
    return {"messages": [response]}


def retrive_data(state):
    query = state["input"]

    query_emb = embedding_model.get_embedding(query)
    top_sections = coarse_search_sections(query_emb, section_data, top_k=TOP_K_SECTIONS)
    top_chunks = fine_search_chunks(query_emb, chunk_index, target_sections=top_sections, top_k=TOP_K_CHUNKS)
    
    return top_chunks