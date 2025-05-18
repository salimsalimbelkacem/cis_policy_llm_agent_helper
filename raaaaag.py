#!/home/salim/.venv/bin/python3
import chromadb
import ollama_api
import time

from chromadb import EmbeddingFunction, Embeddings, Documents

class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name: str = "nomic-embed-text"):
        self.model_name = model_name

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            response = ollama_api.ollama_post_(
                {"model": self.model_name, "prompt": text},
                "api/embeddings"
            ).json()

            embeddings.append(response['embedding'])
        return embeddings

def test_chroma_conectivity(client):
    try:
        client.heartbeat()
    except Exception as e:
        raise ConnectionError(f"Failed to initialize ChromaDB: {str(e)}")

def init_chroma(persist_dir="./chroma_db"):
    client = chromadb.PersistentClient(path=persist_dir)

    test_chroma_conectivity(client)

    collection = client.get_or_create_collection(
            name = "conversation_history",
            # metadata = {"hnsw:space": "cosine"},
            embedding_function=OllamaEmbeddingFunction()
            )
    return client, collection

client, collection = init_chroma()

def store_message(
        conversation_id: str,
        user_message: str,
        ai_response: str,
        collection = collection,
        ):
    document_id = f"{conversation_id}_{int(time.time() * 1000)}"

    collection.add(
            documents=[f"User: {user_message}\nAI: {ai_response}"],
            metadatas=[{ "timestamp": int(time.time()) }],
            ids=[document_id]
            )

def search_messages(
        query_text: str,
        collection,
        conversation_id: str | None = None,
        n_results: int = 3
        ):

    return collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"conversation_id": conversation_id} if conversation_id else None,
            include=["documents", "metadatas", "distances"]
            )

def semantic_search(
        query: str,
        conversation_id: str | None = None,
        collection = collection,
        top_k: int = 5,
        min_similarity: float = 0.3
        ) -> list[dict]:

    results = search_messages(
            query_text=query,
            collection=collection,
            conversation_id=conversation_id,
            n_results=top_k
            )

    return [
            {
                "text": doc,
                "distance": float(dist),
                "timestamp": meta["timestamp"],
                "metadata": {k:v for k,v in meta.items() if k != "timestamp"}
                }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
                )
            if dist >= min_similarity
            ]

# import os
# from pathlib import Path
#
# def load_files(directory: str):
#     file_data = []
#     for filepath in Path(directory).glob("*"):
#         if filepath.suffix.lower() in [".txt", ".md", ".pdf"]:
#             with open(filepath, "r", encoding="utf-8") as f:
#                 file_data.append({
#                     "text": f.read(),
#                     "filename": filepath.name,
#                     "filetype": filepath.suffix[1:]
#                 })
#     return file_data
#
# def chunk_text(text: str, chunk_size: int = 1000):
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield " ".join(words[i:i + chunk_size])
#
# def ingest_files(collection, directory: str):
#     files = load_files(directory)
#     for file in files:
#         for i, chunk in enumerate(chunk_text(file["text"])):
#             collection.add(
#                 documents=[chunk],
#                 metadatas=[{
#                     "filename": file["filename"],
#                     "chunk_num": i,
#                     "filetype": file["filetype"]
#                 }],
#                 ids=[f"{file['filename']}_{i}"]
#             )
#
# def retrieve_for_llm(query: str, collection = collection, top_k: int = 3):
#     results = collection.query(
#         query_texts=[query],
#         n_results=top_k,
#         include=["documents", "metadatas"]
#     )
#     return [
#         f"FILE: {meta['filename']}\nCONTENT: {doc}"
#         for doc, meta in zip(results["documents"][0], results["metadatas"][0])
#     ]
#
# def query_documents(
#     collection,
#     query: str,
#     file_types: list[str] = ["txt", "md"],
#     top_k: int = 3
# ) -> list[str]:
#     results = collection.query(
#         query_texts=[query],
#         n_results=top_k,
#         where={"filetype": {"$in": file_types}},
#         include=["documents", "metadatas"]
#     )
#     return [
#         f"FILE: {meta['filename']}\nCONTENT: {doc}"
#         for doc, meta in zip(results["documents"][0], results["metadatas"][0])
#     ]
#
# def rag_query(
#     collection,
#     query: str,
#     file_filter: list[str] | None = None,
#     top_k: int = 3
# ) -> str:
#     results = collection.query(
#         query_texts=[query],
#         n_results=top_k,
#         where={"filetype": {"$in": file_filter}} if file_filter else None,
#         include=["documents", "metadatas"]
#     )
#
#     context = "\n".join(
#         f"[From {meta['filename']}]: {doc}"
#         for doc, meta in zip(results["documents"][0], results["metadatas"][0])
#         )
#
#     return f"Context:\n{context}\n\nQuestion: {query}"
