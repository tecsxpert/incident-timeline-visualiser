import logging
import os

logger = logging.getLogger(__name__)

model = None
collection = None


def load_model():
    global model
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")


def init_chroma():
    global collection
    try:
        import chromadb
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
        os.makedirs(persist_dir, exist_ok=True)
        client = chromadb.PersistentClient(path=persist_dir)
        collection = client.get_or_create_collection(name="incident_knowledge")
        logger.info(f"ChromaDB ready. Documents: {collection.count()}")
    except Exception as e:
        logger.error(f"Failed to init ChromaDB: {e}")


def get_status():
    return {
        "model_loaded": model is not None,
        "chroma_ready": collection is not None,
        "chroma_doc_count": collection.count() if collection else 0
    }