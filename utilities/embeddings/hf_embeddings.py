from sentence_transformers import SentenceTransformer
import numpy as np

class SentenceTransformerEmbeddings:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        """Embed a list of texts into a numpy array of embeddings."""
        embeddings = self.model.encode(texts, convert_to_tensor=False, show_progress_bar=False)
        return np.array(embeddings)
    
    def __call__(self, texts):
        """Make the class instance callable, forwarding to embed_documents."""
        return self.embed_documents(texts)
