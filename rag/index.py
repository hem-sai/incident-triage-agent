import hashlib
from pathlib import Path

from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

RUNBOOK_DIR = Path(__file__).parent / "runbooks"
CHROMA_DIR = Path(__file__).parent / ".chroma"
EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"
EMBED_REGION = "eu-north-1"


def load_runbooks() -> list[Document]:
    documents: list[Document] = []

    for txt_file in sorted(RUNBOOK_DIR.glob("*.txt")):
        content = txt_file.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "runbook_id": txt_file.stem
                }
            )
        )

    return documents


def build_index(chunk_size: int, chunk_overlap: int) -> Chroma:
    docs = load_runbooks()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)

    # one collection per (config, corpus): editing a runbook gives a new name, so no stale vectors
    corpus_hash = hashlib.sha256("".join(d.page_content for d in docs).encode()).hexdigest()[:8]
    name = f"runbooks_{chunk_size}_{chunk_overlap}_{corpus_hash}"
    embeddings = BedrockEmbeddings(model_id=EMBED_MODEL_ID, region_name=EMBED_REGION)
    store = Chroma(
        collection_name=name,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_metadata={"hnsw:space": "cosine"},  # same metric as InMemoryVectorStore
    )
    if store._collection.count() == len(chunks):
        print(f"Loaded {len(chunks)} chunks from disk ({name}), no Bedrock calls")
    else:
        store.reset_collection()  # half-written earlier run: start clean
        store.add_documents(chunks)
        print(f"Embedded {len(chunks)} new chunks from {len(docs)} runbooks into {name}")
    return store


if __name__ == "__main__":
    store = build_index(chunk_size=500, chunk_overlap=50)
    question = "not getting mail from a specific sender"
    for hit in store.similarity_search(question, k=3):
        print(hit.metadata["runbook_id"])
