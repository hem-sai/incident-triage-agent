from pathlib import Path

from langchain_aws import BedrockEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

RUNBOOK_DIR = Path(__file__).parent / "runbooks"
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
                },
            )
        )

    return documents


def build_index(chunk_size: int, chunk_overlap: int) -> InMemoryVectorStore:
    docs = load_runbooks()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks from {len(docs)} runbooks")
    embeddings = BedrockEmbeddings(model_id=EMBED_MODEL_ID, region_name=EMBED_REGION)
    return InMemoryVectorStore.from_documents(chunks, embeddings)


if __name__ == "__main__":
    store = build_index(chunk_size=500, chunk_overlap=50)
    question = "not getting mail from a specific sender"
    for hit in store.similarity_search(question, k=3):
        print(hit.metadata["runbook_id"])
