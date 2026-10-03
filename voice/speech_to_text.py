"""
Voice input for Civic Saathi.

listen() just does speech-to-text and returns the transcribed string —
kept separate from the RAG/LLM pipeline so it can be reused (e.g. for a
future language dropdown) without dragging in unrelated imports.

ask_via_voice() is the convenience wrapper that takes a spoken question
all the way through to a generated answer, reusing the existing
retriever + response_generator (no duplicated logic).
"""
import speech_recognition as sr


_last_error = ""


def get_last_error() -> str:
    """Return the latest user-facing voice error, if one occurred."""
    return _last_error


def _set_error(message: str) -> None:
    global _last_error
    _last_error = message


def listen(timeout: int = 8, phrase_time_limit: int = 10) -> str:
    """
    Record from the microphone and return the transcribed text.

    timeout: seconds to wait for speech to START before giving up
             (prevents an infinite hang if the user says nothing).
    phrase_time_limit: max seconds to record ONCE speech starts.
    """
    global _last_error
    _last_error = ""
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            try:
                audio = recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
            except sr.WaitTimeoutError:
                _set_error("No speech detected before the listening timeout. Please try again.")
                return ""
    except (OSError, PermissionError, AttributeError) as error:
        print("Microphone error:", error)
        _set_error(
            "Microphone unavailable or blocked. Check Windows microphone permissions and try again."
        )
        return ""

    print("Processing...")
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text

    except sr.UnknownValueError:
        _set_error("I could not understand the recording. Speak clearly and try again.")
        return ""

    except sr.RequestError as error:
        print("Speech recognition service error:", error)
        _set_error("Speech recognition is unavailable right now. Check your internet connection and try again.")
        return ""

    except Exception as error:
        print("Unexpected speech recognition error:", error)
        _set_error("Voice input could not be completed. Please type your question instead.")
        return ""


def ask_via_voice() -> str:
    """
    Records a spoken question, then runs it through the existing
    retriever + response_generator pipeline and returns the LLM's answer.
    Returns "" if nothing was understood (no question is sent in that case).
    """
    from rag.retriever import get_retriever
    from llm.response_generator import generate_response

    question = listen()
    if not question:
        return ""

    retriever = get_retriever()
    results = retriever.retrieve(question, k=5, min_score=0.3)
    return generate_response(question, results)


if __name__ == "__main__":
    answer = ask_via_voice()
    if answer:
        print("\n" + "=" * 60)
        print("CIVIC SAATHI")
        print("=" * 60)
        print("\n" + answer)
    else:
        print("Voice input failed:", get_last_error() or "Unknown error")