from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

model = SentenceTransformer("all-MiniLM-L6-v2")
import os

qdrant = QdrantClient(
    host=os.getenv("QDRANT_HOST", "localhost"),
    port=int(os.getenv("QDRANT_PORT", 6333))
)

COLLECTION_NAME = "documents"


def create_collection():
    collections = qdrant.get_collections().collections
    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME not in collection_names:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


def reset_collection():
    collections = qdrant.get_collections().collections
    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME in collection_names:
        qdrant.delete_collection(collection_name=COLLECTION_NAME)

    create_collection()


def chunk_text(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        # Skip useless small chunks
        if len(chunk) > 80:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def store_document(text, metadata=None):
    if metadata is None:
        metadata = {}

    chunks = chunk_text(text)
    vectors = model.encode(chunks)

    points = []

    for i, (chunk, vector) in enumerate(zip(chunks, vectors), start=1):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector.tolist(),
                payload={
                    "text": chunk,
                    "filename": metadata.get("filename", "unknown"),
                    "chunk_number": i
                }
            )
        )

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(points)


def search(query, top_k=3):
    query_vector = model.encode(query).tolist()

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    )

    output = []

    for point in results.points:
        output.append({
            "text": point.payload.get("text", ""),
            "filename": point.payload.get("filename", "unknown"),
            "chunk_number": point.payload.get("chunk_number"),
            "score": round(point.score, 4)
        })

    return output