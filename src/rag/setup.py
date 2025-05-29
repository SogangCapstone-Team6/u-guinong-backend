import pickle
from src.core.config import SECTIONS_PATH, CHUNK_INDEX_PATH

section_data = None
chunk_index = None

with open(SECTIONS_PATH, "rb") as f:
    section_data = pickle.load(f)

with open(CHUNK_INDEX_PATH, "rb") as f:
    chunk_index = pickle.load(f)