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
        
        # Retrieve existing file metadata
        stored_data = self.collection.get()
        existing_files = set(stored_data["ids"]) if "ids" in stored_data else set()
        
        current_files = set()
        modified_files = set()
        
        for root, _, files in os.walk(ASPNETMVC_APP_PATH):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    current_files.add(file_path)
                    
                    if file_path in existing_files:
                        # Get stored modification time
                        db_metadata = self.collection.get(ids=[file_path])["metadatas"][0]
                        stored_mtime = db_metadata.get("last_modified", 0)
                        current_mtime = os.path.getmtime(file_path)
                        
                        if current_mtime > stored_mtime:
                            modified_files.add(file_path)

        # If any file is modified, new, or deleted, we need processing
        if modified_files or (current_files - existing_files) or (existing_files - current_files):
            logger.info(f"Changes detected. New files: {len(current_files - existing_files)}, "
                        f"Modified: {len(modified_files)}, Deleted: {len(existing_files - current_files)}")
            return True

        logger.info("No changes detected in C# files. Skipping processing.")
        return False


    def generate_response(self, prompt: str, context: str = '') -> str:
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
                n_results=10  # Retrieve more documents for better accuracy
            )

            # Extract relevant documents
            relevant_docs = results["documents"][0] if results["documents"] else []
            logger.info(f"Retrieved {len(relevant_docs)} relevant documents from ChromaDB")

            if not relevant_docs:
                logger.warning("No relevant documents found! The response might lack accuracy.")

            # Construct an informative context
            structured_context = self.build_context(relevant_docs)

            # Formulate the final prompt
            final_prompt = f"Context:\n{structured_context}\n\nUser Query: {prompt}" if structured_context else prompt

            # Generate response from Ollama
            response = ollama.generate(model=self.model_name, prompt=final_prompt)
            logger.info("Successfully generated response")
            return response["response"]
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def process_csharp_files(self) -> None:
        logger.info("Starting C# files processing")

        # Get existing file metadata
        stored_data = self.collection.get()
        existing_files = set(stored_data["ids"]) if "ids" in stored_data else set()

        processed_count = 0
        scan_files = ["Controllers", "ViewConfigurations", "ViewModels", "Views"]
        for root, _, files in os.walk(ASPNETMVC_APP_PATH):
            if not any(scan_dir in root for scan_dir in scan_files):
                continue  # Skip directories that are not in scan_files

            for file in files:
                if file.endswith(".cs") and "Core" not in file:
                    file_path = os.path.join(root, file)
                    
                    # Check if the file is new or modified
                    needs_update = file_path not in existing_files or os.path.getmtime(file_path) > \
                                self.collection.get(ids=[file_path])["metadatas"][0].get("last_modified", 0)

                    if not needs_update:
                        continue  # Skip processing if the file is already up to date

                    logger.info(f"Processing file: {file_path}")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                            # Extract meaningful sections from the code
                            extracted_content = self.extract_relevant_content(content)

                            # Generate embeddings
                            embedding_response = ollama.embeddings(model=self.model_name, prompt=extracted_content)
                            if not embedding_response or "embedding" not in embedding_response:
                                logger.error(f"Embedding generation failed for {file_path}")
                                continue

                            embedding = embedding_response["embedding"]

                            # Store in ChromaDB with last modified time
                            self.collection.add(
                                embeddings=[embedding],
                                documents=[extracted_content],
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


    def extract_relevant_content(self, content: str) -> str:
        """
        Extract relevant sections (e.g., class names, methods, comments, attributes) 
        from C# code to improve embeddings.
        """
        extracted_lines = []
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("class ") or line.startswith("public") or line.startswith("private") or line.startswith("//"):
                extracted_lines.append(line)
        
        return "\n".join(extracted_lines)

    def build_context(self, documents: list) -> str:
        """
        Construct a structured context for better prompt engineering.
        """
        context_sections = []
        for doc in documents:
            context_sections.append(f"Relevant Code Snippet:\n{doc}")

        return "\n\n".join(context_sections)

    def close(self):
        logger.info("Closing ChromaDB connection")
        self.chroma_client.close()
