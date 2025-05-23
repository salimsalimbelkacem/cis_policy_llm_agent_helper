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

def init_chroma(persist_dir="./.chroma_db"):
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
            {"text": doc,}
            for doc in zip(
                results["documents"][0],
                )
            ]

import os
from pathlib import Path

def load_files(directory: str):
    file_data = []
    for filepath in Path(directory).glob("*"):
        with open(filepath, "r", encoding="utf-8") as f:
            file_data.append({
                    "text": f.read(),
                    "filename": filepath.name,
                    "filetype": filepath.suffix[1:]
                })
    return file_data

def chunk_text(text: str, chunk_size: int = 1000):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

def ingest_files( directory:str, collection=collection):
    print("loading files...")
    files = load_files(directory)


    print("chunking or whatever...")
    for file in files:
        for i, chunk in enumerate(chunk_text(file["text"])):
            print(f"chunk {i} :P")
            collection.add(
                        documents=[chunk],
                        metadatas=[{
                                "filename": file["filename"],
                                "chunk_num": i,
                                "filetype": file["filetype"]
                            }],
                        ids=[f"{file['filename']}_{i}"]
                    )
    print("done :P")

def retrieve_for_llm(
        query:str,
        collection = collection,
        top_k: int = 1
        ):

    results = collection.query(
                query_texts=[query],
                n_results=top_k,
                include=["documents", "metadatas"]
            )

    return [
                f"FILE: {meta['filename']}\nCONTENT: {doc}"
                for doc, meta in zip(results["documents"][0], results["metadatas"][0])
            ]
