# ============================================================
# Script     : Build_RAG_Pipeline.py
# Domain     : Generative AI
# Purpose    : End-to-End Retrieval Augmented Generation
# Platform   : Azure OpenAI + Databricks Vector Search
# ============================================================

from typing import List
from dataclasses import dataclass

# ============================================================
# Configuration
# ============================================================

EMBEDDING_MODEL = "text-embedding-3-large"

CHAT_MODEL = "gpt-4o"

VECTOR_INDEX = (
    "novabank_prod.genai.policy_vector_index"
)

TOP_K = 5

# ============================================================
# Data Model
# ============================================================

@dataclass
class RetrievedDocument:

    document_id: str

    title: str

    content: str

    source: str

    similarity_score: float

# ============================================================
# Embedding Generation
# ============================================================

def generate_embedding(query: str):

    """
    Generate embedding for user query.
    """

    embedding = (
        azure_openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query
        )
    )

    return embedding.data[0].embedding

# ============================================================
# Vector Search Retrieval
# ============================================================

def retrieve_documents(
    query: str,
    top_k: int = TOP_K
) -> List[RetrievedDocument]:

    query_embedding = (
        generate_embedding(query)
    )

    search_results = (
        vector_search_client.similarity_search(
            index_name=VECTOR_INDEX,
            query_vector=query_embedding,
            k=top_k
        )
    )

    documents = []

    for result in search_results:

        documents.append(

            RetrievedDocument(
                document_id=result["document_id"],
                title=result["title"],
                content=result["content"],
                source=result["source"],
                similarity_score=result["score"]
            )

        )

    return documents

# ============================================================
# Context Builder
# ============================================================

def build_context(
    documents: List[RetrievedDocument]
) -> str:

    context = ""

    for doc in documents:

        context += f"""

        DOCUMENT: {doc.title}

        SOURCE: {doc.source}

        CONTENT:

        {doc.content}

        -----------------------

        """

    return context

# ============================================================
# Prompt Builder
# ============================================================

def build_prompt(
    query: str,
    context: str
):

    prompt = f"""

You are NovaBank AI Assistant.

Answer only using the provided context.

If the answer is not found in the context,
state that the information is unavailable.

CONTEXT:

{context}

QUESTION:

{query}

Provide:

1. Answer
2. Summary
3. Source References

"""

    return prompt

# ============================================================
# Azure OpenAI Response
# ============================================================

def generate_response(
    query: str
):

    documents = retrieve_documents(
        query
    )

    context = build_context(
        documents
    )

    prompt = build_prompt(
        query,
        context
    )

    response = azure_openai.chat.completions.create(

        model=CHAT_MODEL,

        messages=[
            {
                "role": "system",
                "content":
                    "You are a banking assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1
    )

    return {

        "response":
            response.choices[0].message.content,

        "documents_used":
            len(documents),

        "documents":
            documents

    }

# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":

    t is the KYC process "
        "for high-risk customers?"

    )

    result = generate_response(
        question
    )

    print(
        result["response"]
    )
