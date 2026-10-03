import os
from dotenv import load_dotenv
from groq import Groq

from llm.prompt import build_prompt

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-20b"


def generate_response(question: str, retrieved_results: list, conversation_history=None) -> str:
    if not retrieved_results:
        return (
            "I couldn't find enough information in the available "
            "official documents to answer this accurately."
        )

    context_parts = []
    for result in retrieved_results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"Content:\n{result['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = build_prompt(
        question=question,
        context=context,
        conversation_history=conversation_history,
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=1000
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    from rag.retriever import get_retriever

    retriever = get_retriever()
    question = input("Ask your question: ")

    results = retriever.retrieve(
        question,
        k=5,
        min_score=0.3
    )

    answer = generate_response(question, results)

    print("\n" + "=" * 60)
    print("CIVIC SAATHI")
    print("=" * 60)
    print("\n" + answer)