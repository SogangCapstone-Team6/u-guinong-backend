from sentence_transformers import SentenceTransformer
import torch

class EmbeddingModel:
    def __init__(self, model_name="jhgan/ko-sroberta-multitask", device="cpu"):
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.device = device

        if device in ["cuda", "mps"]:
            self.model.to(self.device)

    def get_embedding(self, text: str):
        emb = self.model.encode([text], convert_to_numpy=True, device=self.device, show_progress_bar=True)[0]
        return emb.tolist()

    def get_embeddings(self, texts: list):
        embs = self.model.encode(texts, convert_to_numpy=True, device=self.device, show_progress_bar=True)
        return embs

if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

embedding_model = EmbeddingModel(model_name="jhgan/ko-sroberta-multitask", device=device)
