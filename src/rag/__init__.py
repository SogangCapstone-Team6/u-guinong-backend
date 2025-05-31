from src.core.config import TOP_K_CHUNKS, TOP_K_SECTIONS
from src.rag.setup import section_data, chunk_index
from src.rag.embedding_model import embedding_model
from src.rag.section_coarse_search import coarse_search_sections
from src.rag.fine_search import fine_search_chunks

def retrive_data(state):
    query = state["input"]

    query_emb = embedding_model.get_embedding(query)
    top_sections = coarse_search_sections(query_emb, section_data, top_k=TOP_K_SECTIONS)
    top_chunks = fine_search_chunks(query_emb, chunk_index, target_sections=top_sections, top_k=TOP_K_CHUNKS)
    
    return top_chunks