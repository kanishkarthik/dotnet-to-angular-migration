import ollama
import os
import chromadb
from chromadb.config import Settings
from config.constants import ASPNETMVC_APP_PATH

class OllamaService:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Use a persistent store
        self.collection = self.chroma_client.get_or_create_collection("dotnetapp")

    def generate_response(self, prompt: str, context: str) -> str:
        """
        Generates a response using Ollama LLM, leveraging stored embeddings from ChromaDB.
        """
        self.process_csharp_files()

        # Generate query embedding
        embedding_response = ollama.embeddings(model=self.model_name, prompt=prompt)
        query_embedding = embedding_response["embedding"]  # Extract list of floats

        # Query ChromaDB for similar documents
        results = self.collection.query(
            query_embeddings=[query_embedding],  # Ensure embeddings are passed correctly
            n_results=3
        )

        # Extract top matches
        relevant_docs = [doc for doc in results["documents"][0]] if results["documents"] else []
        context = "\n\n".join(relevant_docs)

        # Formulate prompt with context
        final_prompt = f"Context:\n{context}\n\nUser Query: {prompt}" if context else prompt

        # Generate response from Ollama
        response = ollama.generate(model=self.model_name, prompt=final_prompt)
        return response["response"]


    def process_csharp_files(self) -> None:
        """
        Reads C# files, generates embeddings, and stores them in ChromaDB.
        """
        for root, _, files in os.walk(ASPNETMVC_APP_PATH):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Generate embeddings
                        embedding_response = ollama.embeddings(model=self.model_name, prompt=content)

                        # Extract embedding values
                        embedding = embedding_response["embedding"]  # Ensure it's a list of floats

                        # Store in ChromaDB
                        self.collection.add(
                            embeddings=[embedding],  # Embeddings must be a list of lists
                            documents=[content],
                            metadatas=[{"file_path": file_path}],
                            ids=[file_path]
                        )
    def close(self):
        self.chroma_client.close()
