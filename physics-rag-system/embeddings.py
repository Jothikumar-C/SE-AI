"""
Embedding Engine using OpenAI text-embedding-3-small
Hardened against invalid input
"""

from openai import OpenAI
from config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def clean_text(text: str) -> str:
    """
    Cleans and validates text before sending to embedding API.
    """
    if not text:
        return None

    text = text.strip()

    if len(text) < 10:  # Skip extremely small chunks
        return None

    # Hard limit safety (8192 tokens approx ~ 30k chars safe guard)
    if len(text) > 30000:
        text = text[:30000]

    return text


def generate_embeddings(texts):
    """
    Generates embeddings only for valid cleaned text.
    """

    cleaned_texts = []

    for t in texts:
        cleaned = clean_text(t)
        if cleaned:
            cleaned_texts.append(cleaned)

    if not cleaned_texts:
        raise ValueError("No valid text chunks available for embedding.")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=cleaned_texts
    )

    return [item.embedding for item in response.data]
