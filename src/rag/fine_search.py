import numpy as np

def fine_search_chunks(query_emb, chunk_index, target_sections, top_k=10):
    section_titles = [sec["section"] for sec in target_sections]  # "title" -> "section"으로 변경

    candidates = [
        item for item in chunk_index
        if item["metadata"]["section"] in section_titles  # "section_title" -> "section"으로 변경
    ]

    results = []
    qv = np.array(query_emb)
    q_norm = np.linalg.norm(qv)
    for c in candidates:
        emb = np.array(c["embedding"])
        dot = np.dot(qv, emb)
        denom = np.linalg.norm(emb) * q_norm + 1e-8
        cos_val = dot / denom
        results.append((cos_val, c))

    results.sort(key=lambda x: x[0], reverse=True)
    top_results = [r[1] for r in results[:top_k]]
    return top_results