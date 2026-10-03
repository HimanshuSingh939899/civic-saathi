"""
Service wrapper: given a scheme name, ask the existing RAG+LLM pipeline
for the required documents.

Does NOT duplicate RAG/LLM logic — only shapes the question and
post-processes the output.
"""
from rag.retriever import get_retriever
from llm.response_generator import generate_response
from utils.helpers import extract_section


def get_required_documents(scheme_name: str) -> str:
    """
    Return the list of required documents for a given scheme.
    """
    retriever = get_retriever()
    question = f"What documents are required to apply for {scheme_name}?"

    results = retriever.retrieve(question, k=5, min_score=0.3)
    full_answer = generate_response(question, results)

    documents = extract_section(full_answer, "Required Documents")

    if not documents:
        # LLM didn't use the "### Required Documents" heading — either no
        # documents are mentioned in the source, or it's the "not enough
        # information" fallback. Return the full answer either way.
        return full_answer

    return documents


if __name__ == "__main__":
    scheme = input("Enter scheme/service name: ")
    print("\n" + "=" * 60)
    print(f"REQUIRED DOCUMENTS — {scheme}")
    print("=" * 60)
    print(get_required_documents(scheme))