import numpy as np

def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    dot = np.dot(v1, v2)
    denom = (np.linalg.norm(v1) * np.linalg.norm(v2)) + 1e-8
    return dot / denom

def coarse_search_sections(query_emb, sections: list, beta=0.3, top_k=5):
    scored = []
    for sec in sections:
        title_emb = sec.get("title_emb")
        chunk_emb = sec.get("avg_chunk_emb")
        if title_emb is None or chunk_emb is None:
            continue
        sim_title = cosine_similarity(query_emb, title_emb)
        sim_chunk = cosine_similarity(query_emb, chunk_emb)
        final_score = beta * sim_title + (1 - beta) * sim_chunk
        scored.append((final_score, sec))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored[:top_k]]
