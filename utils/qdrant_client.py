from qdrant_client import QdrantClient
from typing import List, Dict


def save_to_qdrant(
        vacancies_vectors: List[List[float]],
        vacancies: Dict,
        client: QdrantClient,
        collection_name: str) -> None:
    points = []
    for vector, vacancy in zip(vacancies_vectors, vacancies['items']):
        points.append({
            "id": int(vacancy['id']),
            "vector": vector.tolist(),
            "payload": {
                "name": vacancy['name'],
                "url": vacancy['alternate_url'],
                "employer": vacancy['employer']['name'],
                "area": vacancy["area"]["name"]
            }
        })
    client.upsert(collection_name=collection_name, points=points)

def search_qdrant(
        client: QdrantClient,
        collection_name: str,
        query_vector: List[float],
        top_k: int = 10) -> List[Dict[str, str]]:
    search_result = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )
    return [
        {
            "vacancy": hit.payload["name"],
            "similarity": hit.score,
            "url": hit.payload["url"],
            "employer": hit.payload["employer"],
            "area": hit.payload["area"]
        }
        for hit in search_result.points
    ]