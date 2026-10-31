from langchain_chroma import Chroma

from rag.index import build_index

FETCH_CHUNKS = 50


def ranked_runbook_ids(store: Chroma, question: str) -> list[str]:
    """All unique runbook ids for the question, best first."""
    hits = store.similarity_search(question, k=FETCH_CHUNKS)
    ids = [hit.metadata["runbook_id"] for hit in hits]
    return list(dict.fromkeys(ids))


def retrieve(store: Chroma, question: str, k: int) -> list[str]:
    return ranked_runbook_ids(store, question)[:k]

if __name__ == "__main__":
    store = build_index(chunk_size=500, chunk_overlap=50)
    print(retrieve(store, "not internet wifi is connected", 3))