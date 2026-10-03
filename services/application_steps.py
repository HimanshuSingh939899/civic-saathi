"""
Service wrapper: given a scheme/service name, ask the existing RAG+LLM
pipeline specifically for the application steps, and return just that
section of the answer.

Does NOT duplicate any RAG/LLM logic — it only shapes the question and
post-processes the existing response_generator output.
"""
from rag.retriever import get_retriever
from llm.response_generator import generate_response
from utils.helpers import extract_section


def get_application_steps(scheme_name: str) -> str:
    """
    Return the numbered application procedure for a given scheme,
    e.g. get_application_steps("PM Kisan")
    """
    retriever = get_retriever()
    question = f"What are the step-by-step instructions to apply for {scheme_name}?"

    results = retriever.retrieve(question, k=5, min_score=0.3)
    full_answer = generate_response(question, results)

    steps = extract_section(full_answer, "Steps")

    if not steps:
        # Fall back to the full answer if the LLM didn't use the
        # "### Steps" heading for this question (e.g. no procedure exists
        # in the documents, so it returned the "not enough information" line)
        return full_answer

    return steps


if __name__ == "__main__":
    scheme = input("Enter scheme/service name: ")
    print("\n" + "=" * 60)
    print(f"APPLICATION STEPS — {scheme}")
    print("=" * 60)
    print(get_application_steps(scheme))