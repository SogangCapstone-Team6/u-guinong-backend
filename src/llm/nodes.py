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
    system_prompt = """Be a helpful assistant"""
    
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model_name = config.get('configurable', {}).get("model_name", "openai")
    model = _get_model(model_name)
    response = model.invoke(messages)
    return {"messages": [response]}


def rag(state):
    query = state["input"]

    query_emb = embedding_model.get_embedding(query)
    top_sections = coarse_search_sections(query_emb, section_data, top_k=TOP_K_SECTIONS)
    top_chunks = fine_search_chunks(query_emb, chunk_index, target_sections=top_sections, top_k=TOP_K_CHUNKS)
    
    return top_chunks