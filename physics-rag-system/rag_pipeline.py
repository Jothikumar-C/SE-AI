"""
Main RAG Pipeline Logic
"""

from openai import OpenAI
from config import LLM_MODEL, OPENAI_API_KEY, TOP_K
from prompt_template import SYSTEM_PROMPT
from embeddings import generate_embeddings
from vector_store import VectorStore

client = OpenAI(api_key=OPENAI_API_KEY)


class PhysicsRAG:

    def __init__(self):
        self.vector_store = VectorStore()
        self.memory_cache = {}

    def build_index(self, documents):
        valid_docs = []

        for doc in documents:
            if doc["content"] and len(doc["content"].strip()) > 10:
                valid_docs.append(doc)

        if not valid_docs:
            raise ValueError("No valid document content found in PDF.")
        
        texts = [doc["content"] for doc in valid_docs]
        embeddings = generate_embeddings(texts)

        self.vector_store.add(embeddings, valid_docs)
        self.vector_store.save()

        

    def retrieve(self, query):
        query_embedding = generate_embeddings([query])[0]
        return self.vector_store.search(query_embedding, TOP_K)

    def generate_answer(self, query, contexts):

        context_text = "\n\n".join(
            [f"Page {c['page']}:\n{c['content']}" for c in contexts]
        )

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    def ask(self, query):
        if query in self.memory_cache:
            return self.memory_cache[query]

        contexts = self.retrieve(query)
        answer = self.generate_answer(query, contexts)

        self.memory_cache[query] = answer
        return answer
