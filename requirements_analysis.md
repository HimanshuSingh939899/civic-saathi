# Civic Saathi Requirements Analysis

## Scope

This analysis covers all Python files in the workspace, including `app.py`, `rag/`, `llm/`, `services/`, `voice/`, `utils/`, `ui/`, `checker.py`, and `voice/test.py`. Standard-library modules are excluded from the dependency list.

The existing `requirements.txt` contains 145 pinned package entries and appears to be a full environment freeze rather than a project-level dependency file.

## 1. Required Packages

| Package | Why it is used | Files |
| --- | --- | --- |
| `streamlit==1.64.0` | Runs the web UI, session state, sidebar, chat messages, widgets, and styling. | `app.py`, `ui/components.py`, `ui/state.py`, `ui/styles.py` |
| `numpy==2.5.3` | Provides embedding arrays and numeric vector handling. | `rag/embeddings.py`, `rag/vector_store.py` |
| `faiss-cpu==1.15.1` | Loads, searches, and saves the FAISS vector index. | `rag/vector_store.py` |
| `sentence-transformers==6.1.0` | Loads the local sentence-transformer embedding model. | `rag/embeddings.py` |
| `python-dotenv==1.2.3` | Loads `GROQ_API_KEY` and RAG path configuration from `.env`. | `llm/response_generator.py`, `rag/ingest.py`, `rag/retriever.py` |
| `groq==1.7.0` | Calls the existing Groq chat-completions LLM integration. | `llm/response_generator.py` |
| `SpeechRecognition==3.17.0` | Captures microphone audio and sends it to the existing speech-recognition engine. | `voice/speech_to_text.py`, `voice/test.py` |
| `PyAudio==0.2.14` | Supplies the microphone audio backend used by `speech_recognition.Microphone`. | Runtime dependency of `voice/speech_to_text.py` and `voice/test.py` |

## 2. Optional Packages

| Package | Feature/script | Why it remains |
| --- | --- | --- |
| `requests==2.34.2` | `checker.py` background notification polling | The checker fetches official notification pages with `requests.get()`. It is not needed for the Streamlit chat path, but the existing checker feature requires it. |
| `beautifulsoup4` | `checker.py` HTML parsing | The checker imports `BeautifulSoup` from `bs4` to extract visible page text. It is currently missing from the environment and requirements, so it must be added. |

The checker is an optional background script, but these packages are retained because the requested project scope explicitly includes `checker.py`.

## 3. Unused Packages

The following current requirements entries have no direct import or runtime use anywhere in the workspace and are removed from the project requirements file:

`aiohttp`, `bcrypt`, `build`, `chromadb`, `cloudpickle`, `cryptography`, `google-auth`, `google-genai`, `googleapis-common-protos`, `grpcio`, `httpx-sse`, `httpx2`, `importlib_resources`, `kubernetes`, `langchain`, `langchain-classic`, `langchain-community`, `langchain-core`, `langchain-google-genai`, `langchain-protocol`, `langchain-text-splitters`, `langgraph`, `langgraph-checkpoint`, `langgraph-prebuilt`, `langgraph-sdk`, `langsmith`, `mmh3`, `oauthlib`, `onnxruntime`, `opentelemetry-api`, `opentelemetry-exporter-otlp-common`, `opentelemetry-exporter-otlp-proto-common`, `opentelemetry-exporter-otlp-proto-grpc`, `opentelemetry-proto`, `opentelemetry-sdk`, `opentelemetry-semantic-conventions`, `orjson`, `ormsgpack`, `overrides`, `pypdf`, `PyPika`, `requests-oauthlib`, `requests-toolbelt`, `SQLAlchemy`, `uuid_utils`, `xxhash`, and `zstandard`.

The remaining packages from the old freeze that are dependencies of required packages are classified below as transitive rather than retained directly.

## 4. Missing Packages

| Package | Evidence | Action |
| --- | --- | --- |
| `groq==1.7.0` | `llm/response_generator.py` imports `Groq`; no Groq entry exists in the old requirements file. | Add |
| `SpeechRecognition==3.17.0` | `voice/speech_to_text.py` and `voice/test.py` import `speech_recognition`. | Add |
| `PyAudio==0.2.14` | `speech_recognition.Microphone` requires an audio backend; it is installed in the project environment. | Add |
| `beautifulsoup4` | `checker.py` imports `BeautifulSoup` from `bs4`; `pip show` confirms it is not installed. | Add, without inventing a version not present locally |

## 5. Transitive Packages

These packages are installed automatically by the required top-level packages and should normally not be manually listed in this project requirements file:

- Streamlit dependencies: `altair`, `anyio`, `attrs`, `blinker` where applicable, `cachetools`, `click`, `gitpython` where applicable, `httptools`, `itsdangerous`, `packaging`, `pandas`, `pillow`, `protobuf`, `pyarrow`, `pydeck`, `python-dateutil`, `python-multipart`, `pytz`/`tzdata`, `requests`, `starlette`, `tenacity`, `toml`, `tornado` where applicable, `typing-extensions`, `uvicorn`, `watchdog`, `watchfiles`, `websockets`.
- FAISS dependencies: `packaging` and `numpy`.
- Sentence-transformers dependencies: `huggingface-hub`, `scikit-learn`, `scipy`, `tokenizers`, `torch`, `tqdm`, `transformers`, `safetensors`, `joblib`, `threadpoolctl`, `networkx`, `filelock`, `fsspec`, `regex`, `sympy`, and related Hugging Face/runtime packages.
- Groq dependencies: `anyio`, `distro`, `httpx`, `pydantic`, `sniffio`, `typing-extensions`, and their dependencies.
- SpeechRecognition dependencies: `audioop-lts`, `standard-aifc`, and `typing-extensions`.
- Requests dependencies: `certifi`, `charset-normalizer`, `idna`, and `urllib3`.

A package can be both transitive and directly imported by another component. For example, `requests` is a Streamlit dependency in the current environment but is retained as an optional direct project dependency because `checker.py` explicitly uses it.

## 6. Final Dependency List

The cleaned `requirements.txt` should contain exactly these 10 top-level entries:

```text
streamlit==1.64.0
numpy==2.5.3
faiss-cpu==1.15.1
sentence-transformers==6.1.0
python-dotenv==1.2.3
groq==1.7.0
SpeechRecognition==3.17.0
PyAudio==0.2.14
requests==2.34.2
beautifulsoup4
```

`beautifulsoup4` has no local installed version to preserve, so it is intentionally left unpinned. Installation will resolve the current compatible release.

## Notes and Uncertainty

1. `checker.py` is present but currently does not match the current RAG APIs: it imports `get_embedder` and `VectorStore`, while the repository defines `get_embedding_model` and `FAISSVectorStore`. It also calls `chunk_text(..., overlap=150)` while the current helper parameter is `chunk_overlap`. This is a source compatibility issue, not a reason to remove `requests` or `beautifulsoup4`; the source was not changed per task scope.
2. `checker.py` contains an `example.gov.in` placeholder URL for the income notification source. This does not affect package classification.
3. `PyAudio` is required for the current microphone implementation on Windows. It is already installed in the project virtual environment, but fresh Windows setup may require a compatible wheel or PortAudio support.
4. `pip check` currently reports an unrelated environment issue: installed `langchain-google-genai` requires `google-genai`. Those packages are not imported by this project and are removed as unused; this does not affect the Civic Saathi implementation.
5. No `.env` values were read or changed.
