from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class QdrantStorage:

    def __init__(
        self, url: str = "localhost:6333", collection_name: str = "documents", dim=3072
    ):
        self.client = QdrantClient(url=url, timeout=30)
        self.collection_name = collection_name
        self._ensure_collection()
        self.dim = dim

    def _ensure_collection(self):
        if not self.client.has_collection(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.dim, distance=Distance.COSINE),
            )

    def upsert(self, ids, vectors, payloads):
        points = [
            PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i])
            for i in range(len(ids))
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def add_document(self, doc_id: str, embedding: list[float], metadata: dict):
        point = PointStruct(id=doc_id, vector=embedding, payload=metadata)
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def search(self, query_vector, top_k: int = 5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
        )
        contexts = []
        sources = set()
        for result in results:
            paylod = getattr(result, "payload", None) or {}
            text = paylod.get("text", "")
            source = paylod.get("source", "")
            if text:
                contexts.append(text)
                sources.add(source)
        return {"contexts": contexts, "sources": list(sources)}
