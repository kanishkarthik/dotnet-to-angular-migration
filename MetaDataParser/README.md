# Metadata Generator

## Overview
Python-based Flask application that analyzes ASP.NET MVC configurations and generates metadata for Angular UI rendering.
## Features
- Web interface for metadata generation
- AI-powered configuration analysis (Groq/Gemini)
- Automatic metadata validation
- File system storage integration
- Multiple AI model support

## Project Structure

## Technical Architecture

### MetadataGenerator Service
- **Core Orchestrator**: Manages the overall metadata generation workflow
- **Key Components**:
  - Configuration management for country-payment method combinations
  - File system operations for reading .NET configurations
  - Service routing based on AI model selection
  - Metadata persistence handling
- **Flow**:
  1. Receives request with country code, payment method, and AI model
  2. Loads corresponding configuration from config file
  3. Reads .NET source files
  4. Routes to appropriate AI service
  5. Optionally saves generated metadata

### Groq Service
- **Direct LLM Integration**
- **Components**:
  - Groq API client initialization
  - Prompt engineering system
  - JSON response parsing
- **Technical Flow**:
  1. Initializes Groq client with API key
  2. Constructs structured prompt with:
     - System role definition
     - Configuration content
     - Metadata structure template
  3. Sends chat completion request
  4. Extracts and validates JSON from response
- **Error Handling**: Comprehensive exception management with logging

### Groq Ingest Service
- **Vector Database Integration**
- **Key Components**:
  - Document ingestion pipeline
  - Vector index management
  - Query engine configuration
- **Technical Process**:
  1. **Index Management**:
     - Persists indexes to disk
     - Supports index clearing and rebuilding
     - Uses BAAI/bge-small-en-v1.5 embedding model
  2. **Document Processing**:
     - Recursively reads .cs files
     - Creates document vectors
     - Builds searchable index
  3. **Query Processing**:
     - Custom prompt templates
     - Context-aware querying
     - Region-based filtering

### Gemini Service
- **Google AI Integration**
- **Components**:
  - Gemini API configuration
  - Generative model handling
  - Response processing
- **Technical Flow**:
  1. Configures Google AI client
  2. Constructs detailed prompt with:
     - Expert system definition
     - Configuration analysis instructions
     - Metadata structure template
  3. Generates content using model
  4. Processes and validates JSON response

## Common Features Across Services
- JSON metadata structure validation
- Comprehensive error handling and logging
- Custom prompt support
- Response sanitization and formatting

## System Requirements
- Python 3.8+
- Required API keys:
  - Groq API key
  - Google AI (Gemini) API key
- Sufficient disk space for vector storage

## Configuration
- Environment variables for API keys
- Config files for country-payment method mappings
- Index storage path configuration
- Logging configuration

## Error Handling
- Hierarchical exception management
- Detailed logging at each step
- Service-specific error responses
- Validation checks at multiple levels

## Performance Considerations
- Vector index caching
- Response validation optimization
- Configurable batch processing
- Resource management for large files
