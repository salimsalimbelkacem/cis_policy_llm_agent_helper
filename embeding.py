import ollama_api
import faiss as fs
import numpy as np
import os
 
embeding_model="nomic-embed-text"

index_file_name = "indexes.faiss"

def embed(text:str):
    return ollama_api.ollama_post_(
            {
                "model": embeding_model,
                "prompt": text
                },
            "api/embeddings"
            ) ['embedding']


def store_embed_to_index(data):
    vectors = [embed(data)]

    if os.path.exists(index_file_name):
        index = fs.read_index(index_file_name)
    else:
        index = fs.IndexFlatL2(len(vectors[0]))  

    index.add(np.array(vectors).astype("float32"))
    fs.write_index(index, index_file_name)

"""
✅ Ollama	To run your AI models locally
✅ nomic-embed-text	To turn your scripts into searchable memory
✅ faiss-cpu	To store and search that memory
✅ numpy	To help with data formats
✅ requests	To communicate with Ollama using Python
"""
