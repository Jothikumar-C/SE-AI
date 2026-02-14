"""
Configuration Module
Loads environment variables and defines global settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Configurations
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

# Vector DB Path (Single Persistent Store)
VECTOR_STORE_PATH = "data/vector_store/physics_index.faiss"

# Retrieval Config
TOP_K = 4
SIMILARITY_THRESHOLD = 0.75
