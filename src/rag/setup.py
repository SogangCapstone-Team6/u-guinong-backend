import json
from src.core.config import SECTIONS_PATH, CHUNK_INDEX_PATH

section_data = None
chunk_index = None

with open(SECTIONS_PATH, "r", encoding="utf-8") as f:
    section_data = json.load(f)

with open(CHUNK_INDEX_PATH, "r", encoding="utf-8") as f:
    chunk_index = json.load(f)

