from sentence_transformers import SentenceTransformer
from typing import List

model = SentenceTransformer('DeepPavlov/rubert-base-cased-sentence')

def vectorize(text: str) -> List[float]:
    return model.encode(text).tolist()