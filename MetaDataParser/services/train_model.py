import os
import json
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import Dataset
import torch
from config.constants import ASPNETMVC_APP_CONFIG_PATH
from utils.logger import logger

class ModelTrainer:
    def __init__(self):
        logger.info("Initializing ModelTrainer with CodeBERT model")
        self.model_name = "microsoft/codebert-base"
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            logger.info("Successfully loaded model and tokenizer")
        except Exception as e:
            logger.error(f"Failed to load model or tokenizer: {str(e)}")
            raise

    def load_csharp_files(self):
        logger.info(f"Starting to load C# files from {ASPNETMVC_APP_CONFIG_PATH}")
        cs_files_data = []
        files_processed = 0
        files_failed = 0

        for root, _, files in os.walk(ASPNETMVC_APP_CONFIG_PATH):
            for file in files:
                if file.endswith('.cs'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            cs_files_data.append({
                                'file_path': file_path,
                                'content': content
                            })
                            files_processed += 1
                            logger.debug(f"Successfully processed file: {file_path}")
                    except Exception as e:
                        files_failed += 1
                        logger.error(f"Error reading file {file_path}: {str(e)}")

        logger.info(f"Finished loading C# files. Processed: {files_processed}, Failed: {files_failed}")
        return cs_files_data

    def tokenize_function(self, examples):
        """Tokenize the input texts."""
        return self.tokenizer(
            examples["content"],  # Changed from "text" to "content"
            padding="max_length",
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )

    def prepare_training_data(self, cs_files_data):
        logger.info("Preparing training data from C# files")
        training_examples = []
        
        for file_data in cs_files_data:
            csharp_code = file_data['content']
            # Store just the processed content for tokenization
            training_examples.append({
                "content": csharp_code,
                "metadata": {  # Store metadata separately
                    "filepath": file_data['file_path'],
                }
            })
        
        # Create dataset with the simplified structure
        dataset = Dataset.from_list(training_examples)
        
        # Tokenize the dataset
        tokenized_dataset = dataset.map(
            self.tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        
        # Validate the dataset
        if not all(isinstance(x, torch.Tensor) for x in tokenized_dataset['input_ids']):
            raise ValueError("Invalid input_ids format in dataset")
            
        logger.info(f"Prepared {len(tokenized_dataset)} tokenized training samples")
        return tokenized_dataset

    def train_model(self, epochs=5, batch_size=2, learning_rate=1e-5):
        logger.info("Starting model training process")
        cs_files_data = self.load_csharp_files()
        
        try:
            tokenized_dataset = self.prepare_training_data(cs_files_data)

            training_args = TrainingArguments(
                output_dir="./results",
                num_train_epochs=epochs,
                per_device_train_batch_size=batch_size,
                save_steps=500,
                save_total_limit=2,
                learning_rate=learning_rate,
                weight_decay=0.01,
                remove_unused_columns=False,
            )
            logger.info(f"Training arguments configured: {training_args}")

            try:
                trainer = Trainer(
                    model=self.model,
                    args=training_args,
                    train_dataset=tokenized_dataset,
                    tokenizer=self.tokenizer
                )
                logger.info("Starting training...")
                trainer.train()
                logger.info("Training completed successfully")

                logger.info("Saving fine-tuned model and tokenizer")
                self.model.save_pretrained("./fine_tuned_model")
                self.tokenizer.save_pretrained("./fine_tuned_model")
                logger.info("Model and tokenizer saved successfully")
            except Exception as e:
                logger.error(f"Training failed: {str(e)}")
                raise
        except Exception as e:
            logger.error(f"Error preparing training data: {str(e)}")
            raise

    def generate_response(self, prompt, filepath=None, max_length=200):
        logger.info(f"Generating response for prompt: {prompt[:50]}...")
        try:
            # Include filepath in the prompt if provided
            full_prompt = f"File: {filepath}\n\n{prompt}" if filepath else prompt
            inputs = self.tokenizer.encode(full_prompt, return_tensors="pt")
            outputs = self.model.generate(
                inputs, 
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.info("Response generated successfully")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def _convert_to_angular(self, csharp_code):
        """
        Placeholder method to convert C# code to Angular/TypeScript code.
        Implement your conversion logic here.
        """
        # TODO: Implement actual conversion logic
        return f"// Angular/TypeScript equivalent of:\n{csharp_code}"

