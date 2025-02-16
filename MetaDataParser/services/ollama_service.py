import os
import ollama
import chromadb
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings
)
from llama_index.core.schema import Document
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from config.constants import ASPNETMVC_APP_PATH, CHROMA_DB_PATH
from utils.logger import logger

class OllamaRAGService:
    def __init__(self, model_name: str):
        self.model_name = model_name
        logger.info(f"Initializing OllamaRAGService with model: {model_name}")

        # Initialize ChromaDB for persistent storage
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_client.get_or_create_collection("dotnetapp"))
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

        # Set up LLM (Ollama)
        self.llm = Ollama(model=model_name)
        Settings.llm = self.llm

        # Check if we need to reprocess C# files
        changed_files = self.needs_processing()
        if changed_files:
            logger.info(f"Changes detected in {len(changed_files)} C# files, updating index.")
            self.index = self.build_index(changed_files)
        else:
            logger.info("No changes detected in C# files, loading existing index.")
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store
            )

        # Configure Query Engine with RAG
        self.query_engine = self.index.as_query_engine()

    def needs_processing(self) -> list:
        """
        Checks if C# files have changed and returns list of files that need reprocessing.
        """
        logger.info("Checking if C# files need processing...")
        changed_files = []

        # Get collection info
        collection = self.chroma_client.get_collection("dotnetapp")
        if collection.count() == 0:
            # Get all .cs files if no index exists
            for root, _, files in os.walk(ASPNETMVC_APP_PATH):
                for file in files:
                    if file.endswith(".cs") and "Core" not in file:
                        changed_files.append(os.path.join(root, file))
            return changed_files

        # Get stored documents and their metadata
        stored_data = collection.get(include=["metadatas"])
        stored_metadatas = stored_data.get("metadatas", [])
        stored_ids = stored_data.get("ids", [])

        # Create a mapping of file paths to their last modified times
        stored_file_times = {
            file_id: metadata.get("last_modified", 0)
            for file_id, metadata in zip(stored_ids, stored_metadatas)
        }

        scan_dirs = ["Controllers", "ViewConfigurations", "ViewModels", "Views"]

        # Check current files
        for root, _, files in os.walk(ASPNETMVC_APP_PATH):
            if not any(scan_dir in root for scan_dir in scan_dirs):
                continue

            for file in files:
                if file.endswith(".cs") and "Core" not in file:
                    file_path = os.path.join(root, file)
                    current_mtime = os.path.getmtime(file_path)

                    # Check if file is new or modified
                    if file_path in stored_file_times:
                        if current_mtime > stored_file_times[file_path]:
                            changed_files.append(file_path)
                    else:
                        changed_files.append(file_path)

        # Handle deleted files
        for stored_id in stored_ids:
            if not os.path.exists(stored_id):
                self.vector_store.client.delete(ids=[stored_id])

        return changed_files

    def build_index(self, changed_files: list):
        """
        Reads and indexes only the changed C# files, updating ChromaDB.
        """
        logger.info(f"Building index for {len(changed_files)} C# files...")
        documents = []
        processed_count = 0

        for file_path in changed_files:
            logger.info(f"Processing C# file: {file_path}")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = self.extract_relevant_content(f.read())

                doc = Document(text=content, metadata={"file_path": file_path})
                documents.append(doc)

                # Delete old entry if exists
                self.vector_store.client.delete(ids=[file_path])

                # Store in ChromaDB
                self.vector_store.client.add(
                    documents=[content],
                    embeddings=[ollama.embeddings(model=self.model_name, prompt=content)["embedding"]],
                    metadatas=[{"last_modified": os.path.getmtime(file_path)}],
                    ids=[file_path]
                )
                processed_count += 1
                logger.info(f"Successfully indexed: {file_path}")

            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")

        logger.info(f"Completed processing {processed_count} C# files.")

        # Create LlamaIndex for fast retrieval
        return VectorStoreIndex.from_vector_store(self.vector_store)

    def generate_response(self, query: str) -> str:
        """
        Uses RAG to retrieve relevant C# code snippets and generate a response.
        """
        logger.info(f"Generating response for: {query}")

        # Retrieve relevant C# code snippets
        retrieved_docs = self.query_engine.query(query).response

        # Ensure retrieved docs are properly formatted
        if isinstance(retrieved_docs, str):
            logger.warning("Retrieved response is a string instead of a document. Adjusting format.")
            retrieved_docs = f"Extracted Content:\n{retrieved_docs}"

        final_prompt = f"Context:\n{retrieved_docs}\n\nUser Query: {query}"
        response = ollama.generate(model=self.model_name, prompt=final_prompt)

        return response["response"]

    @staticmethod
    def extract_relevant_content(content: str) -> str:
        """
        Extracts meaningful sections of C# code to improve embeddings.
        """
        return "\n".join(line.strip() for line in content.split("\n") if line.strip().startswith(("class", "public", "private", "//")))

    def close(self):
        logger.info("Closing ChromaDB connection")
        self.chroma_client.close()
