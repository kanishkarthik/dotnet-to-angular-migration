import ollama
import os
import chromadb
from utils.logger import logger
from chromadb.config import Settings
from config.constants import ASPNETMVC_APP_PATH

class OllamaService:
    def __init__(self, model_name: str):
        self.model_name = model_name
        logger.info(f"Initializing OllamaService with model: {model_name}")
        
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Use a persistent store
        self.collection = self.chroma_client.get_or_create_collection("dotnetapp")
        logger.info("ChromaDB connection established")

    def needs_processing(self) -> bool:
        logger.info("Checking if C# files need processing")
        existing_files = set(self.collection.get()["ids"])
        current_files = set()
        
        for root, _, files in os.walk(ASPNETMVC_APP_PATH):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    current_files.add(file_path)
                    
                    # If file exists in DB, check if it was modified
                    if file_path in existing_files:
                        db_metadata = self.collection.get(ids=[file_path])["metadatas"][0]
                        stored_mtime = db_metadata.get("last_modified", 0)
                        current_mtime = os.path.getmtime(file_path)
                        
                        if current_mtime > stored_mtime:
                            logger.info("Found changes in C# files, processing needed")
                            return True
        
        # Check if there are new files or deleted files
        if len(current_files) != len(existing_files):
            logger.info("Found changes in C# files, processing needed")
            return True
        logger.info("No changes detected in C# files")
        return False

    def generate_response(self, prompt: str, context: str = "") -> str:
        logger.info("Generating response for prompt")

        # Process C# files if needed
        if self.needs_processing():
            logger.info("Processing C# files before generating response")
            self.process_csharp_files()

        try:
            # Generate query embedding
            embedding_response = ollama.embeddings(model=self.model_name, prompt=prompt)
            query_embedding = embedding_response["embedding"]

            logger.info("Querying ChromaDB for relevant context")
            # Query ChromaDB for similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=5  # Increase results for better context
            )

            # Extract top matches
            if results["documents"]:
                relevant_docs = [doc for doc in results["documents"][0] if doc]  # Ensure non-empty docs
                context = "\n\n".join(relevant_docs) if relevant_docs else context
                logger.info(f"Retrieved {len(relevant_docs)} relevant documents from ChromaDB")
            else:
                logger.warning("No relevant documents found in ChromaDB")
            
            # Ensure there's enough context
            if not context:
                logger.warning("No context available! Ollama might return a generic response.")

            # Formulate prompt with retrieved context
            final_prompt = f"Context:\n{context}\n\nUser Query: {prompt}" if context else prompt

            # Generate response from Ollama
            response = ollama.generate(model=self.model_name, prompt=final_prompt)
            logger.info("Successfully generated response")
            return response["response"]
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise


    def process_csharp_files(self) -> None:
        logger.info("Starting C# files processing")

        # Fetch existing document IDs
        existing_ids = self.collection.get()["ids"]

        # Delete existing records only if they exist
        if existing_ids:
            self.collection.delete(ids=existing_ids)
            logger.info(f"Deleted {len(existing_ids)} existing records from ChromaDB")

        processed_count = 0
        for root, _, files in os.walk(ASPNETMVC_APP_PATH):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    logger.info(f"Processing file: {file_path}")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                            # Generate embeddings
                            embedding_response = ollama.embeddings(model=self.model_name, prompt=content)
                            if not embedding_response or "embedding" not in embedding_response:
                                logger.error(f"Embedding generation failed for {file_path}")
                                continue

                            embedding = embedding_response["embedding"]

                            # Store in ChromaDB with last modified time
                            self.collection.add(
                                embeddings=[embedding],
                                documents=[content],
                                metadatas=[{
                                    "file_path": file_path,
                                    "last_modified": os.path.getmtime(file_path)
                                }],
                                ids=[file_path]
                            )
                            processed_count += 1
                    except Exception as e:
                        logger.error(f"Error processing file {file_path}: {str(e)}")

        logger.info(f"Completed processing {processed_count} C# files")



    def close(self):
        logger.info("Closing ChromaDB connection")
        self.chroma_client.close()
