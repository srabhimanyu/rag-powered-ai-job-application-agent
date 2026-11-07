import hashlib
import chromadb
from .config import CHROMA_PATH
from .llm import embed

COLLECTION_NAME = "candidate_and_job_documents"

def get_collection():
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

def chunk_text(text, chunk_size=900, overlap=150):
    text = " ".join(text.split())
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks

def index_document(text, doc_id, source, metadata=None):
    chunks = chunk_text(text)
    if not chunks:
        return 0
    collection = get_collection()
    ids = [f"{doc_id}-{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "doc_id": doc_id, **(metadata or {})}
                 for _ in chunks]
    # Replace old chunks for the same document, enabling resume updates.
    try:
        collection.delete(where={"doc_id": doc_id})
    except Exception:
        pass
    vectors = embed(chunks)
    collection.add(ids=ids, documents=chunks, embeddings=vectors, metadatas=metadatas)
    return len(chunks)

def retrieve(query, n_results=5):
    collection = get_collection()
    if collection.count() == 0:
        return []
    vector = embed([query])[0]
    result = collection.query(
        query_embeddings=[vector],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"]
    )
    hits = []
    for i, doc in enumerate(result.get("documents", [[]])[0]):
        hits.append({
            "text": doc,
            "metadata": result["metadatas"][0][i],
            "distance": result["distances"][0][i]
        })
    return hits

def collection_count():
    return get_collection().count()
