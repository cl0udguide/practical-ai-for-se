"""
Simple RAG (Retrieval-Augmented Generation) example using Ollama with pgvector

This script demonstrates how to:
- Read all .md files from the rag-documents directory
- Store embeddings in the 'agno_rag' table in the public schema
- Use hybrid search (semantic + full-text) for retrieval
- Apply markdown-aware chunking (respects markdown structure, chunk_size=1000, no overlap)

Prerequisites:
- PostgreSQL with pgvector extension running (see docker/docker-compose.yml)
- Ollama running with nomic-embed-text and granite4:micro-h models pulled
"""

# Import the core Agent class from Agno framework
from agno.agent import Agent
# Import Ollama embedder for generating vector embeddings locally
from agno.knowledge.embedder.ollama import OllamaEmbedder
# Import Knowledge class - manages document storage and retrieval
from agno.knowledge.knowledge import Knowledge
# Import Ollama model wrapper for running local LLMs
from agno.models.ollama import Ollama
# Import PgVector for PostgreSQL-based vector storage with pgvector extension
from agno.vectordb.pgvector import PgVector, SearchType
# Import ReaderFactory to create document readers (markdown, pdf, etc.)
from agno.knowledge.reader import ReaderFactory
# Import chunking strategies for splitting documents into smaller pieces
from agno.knowledge.chunking.strategy import ChunkingStrategyFactory, ChunkingStrategyType
# Import ollama client directly to query embedding dimensions
import ollama
# Import Path for file system operations
from pathlib import Path

# PostgreSQL connection string - connects to the pgvector database
# Format: postgresql+psycopg://user:password@host:port/database
db_url = "postgresql+psycopg://postgres:your_secure_password@localhost:5432/n8n_rag"

# Get actual embedding dimension from Ollama (nomic-embed-text produces 768 dimensions)
# This is needed because the embedder might report incorrect dimensions
test_embedding = ollama.embeddings(model="nomic-embed-text", prompt="test")
actual_dimension = len(test_embedding["embedding"])

# Create embedder using nomic-embed-text model for generating embeddings
# This model runs locally via Ollama and produces 768-dimensional vectors
embedder = OllamaEmbedder(id="nomic-embed-text")
embedder.dimensions = actual_dimension  # Override incorrect dimension

# Create markdown-aware chunking strategy that respects markdown delimiters
# This ensures chunks don't break in the middle of sections or code blocks
chunking_strategy = ChunkingStrategyFactory.create_strategy(
    ChunkingStrategyType.MARKDOWN_CHUNKER, 
    chunk_size=1000,  # Smaller chunks for better retrieval precision
    overlap=0  # No overlap between chunks
)

# Create markdown reader with the markdown-aware chunking strategy
markdown_reader = ReaderFactory.create_reader("markdown")
markdown_reader.chunking_strategy = chunking_strategy

# Create Knowledge instance - the central component for RAG
# Combines vector database, embedder, and document readers
knowledge = Knowledge(
    # Use PgVector as the vector database with hybrid search
    # Hybrid search combines semantic similarity with full-text keyword search
    vector_db=PgVector(
        table_name="agno_rag",  # Table name for storing embeddings
        schema="public",  # PostgreSQL schema
        db_url=db_url,  # Database connection string
        search_type=SearchType.hybrid,  # Semantic + full-text search for better results
        embedder=embedder,  # Embedder for generating vectors
    ),
    readers=[markdown_reader],  # List of document readers to use
    max_results=5,  # Limit to 5 most relevant chunks in retrieval
)


# Read all markdown files from rag-documents directory and add to knowledge base
rag_documents_dir = Path("rag-documents")
markdown_files = list(rag_documents_dir.glob("*.md"))

print(f"\nFound {len(markdown_files)} markdown files to process:")
for md_file in markdown_files:
    print(f"  - {md_file.name}")
    # Add each file to the knowledge base - this chunks, embeds, and stores the content
    knowledge.add_content(path=str(md_file))

# Create Ollama model with system prompt optimized for RAG
# Low temperature (0.2) ensures factual, precise responses based on context
model = Ollama(
    id="granite4:micro-h",
    system_prompt="""You are a helpful assistant that answers questions based STRICTLY on the provided knowledge base context. 

CRITICAL RULES:
1. ONLY use information that is explicitly present in the provided context
2. NEVER guess, infer, or make up information not in the context
3. If the provided context does not contain sufficient information to answer the question, you MUST refuse to answer and clearly state: "I cannot answer this question based on the provided context. The necessary information is not available in the knowledge base."
4. DO NOT attempt to answer partially or provide general knowledge - either answer completely from the context or refuse
5. Be accurate, concise, and cite relevant parts when providing answers""",
    options={"temperature": 0.2}  # Low temperature for factual, precise RAG responses
)

# Create Agent with knowledge base integration
agent = Agent(
    model=model,
    knowledge=knowledge,  # Attach the knowledge base
    add_knowledge_to_context=True,  # Include retrieved documents in the prompt context
    search_knowledge=False,  # Manual retrieval only, no automatic search
    markdown=True,  # Enable markdown formatting in responses
    debug_mode=True,  # Uncomment to see reasoning and retrieval details
)

# Run the agent with a question - it will retrieve relevant chunks and generate an answer
agent.print_response(
    "What are the licensing changes in VCF 9.0?", stream=True
#    "What is the weather like in Warsaw?", stream=True  # Test with out-of-context question
)
