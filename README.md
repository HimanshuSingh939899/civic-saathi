# 🏛️ Civic Saathi

Civic Saathi is an AI assistant that helps people understand Indian government services and schemes through simple, conversational questions — 
instead of searching through government websites and PDFs.

It uses Retrieval-Augmented Generation (RAG) to answer questions about eligibility, required documents, and application steps, 
backed by a rule-based eligibility checker for fast, accurate answers.

## ✨Features

Conversational AI assistant for government scheme queries
RAG-based retrieval from official scheme documents
Fast, rule-based eligibility checking (no LLM call, no hallucination risk)
Required document and application step guidance
Voice input support
Streamlit web interface
FAISS-based vector search
Groq-powered LLM responses

## 🔍How It Works

Civic Saathi uses a **Retrieval-Augmented Generation (RAG)** pipeline to provide answers based on the available government-service documents.

### Step-by-Step Flow

```text
👤 User
   │
   │  Text / Voice Question
   ▼
🤖 Civic Saathi
   │
   ▼
🔎 Query Processing
   │
   ▼
📚 RAG Retriever
   │
   │  Searches relevant information
   ▼
🗂️ FAISS Vector Database
   │
   │  Retrieves relevant document chunks
   ▼
📄 Government Documents
   │
   ▼
🧠 Groq LLM
   │
   │  Generates an answer using retrieved context
   ▼
💬 Personalized Response
   │
   ├── ✅ Eligibility Information
   ├── 📄 Required Documents
   ├── 📝 Application Steps
   └── 🔗 Official Information / Sources
      


## 📂 Project Structure

text
civic-saathi/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── data/
│   ├── documents/
│   └── synthetic_data/
|   |__ Dummy_data/
│
├── rag/
│   ├── ingest.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── vector_store.py
│
├── llm/
│   ├── prompts.py
│   └── response_generator.py
│
├── services/
│   ├── application_steps.py
│   ├── document_checker.py
│   └── eligibility.py
│
├── ui/
│   ├── __init__.py
│   ├── components.py
│   ├── services.py
│   ├── chat.py
│   ├── state.py
│   └── styles.py
│
├── voice/
│   └── speech_to_text.py
│
└── utils/
    └── helpers.py

    
## 🏛️ Services Covered

Aadhaar
PAN Card
Voter ID
Passport
Driving License
Ration Card
Income Certificate
PM-Kisan
PM Awas Yojana
PM Jan Dhan Yojana
Atal Pension Yojana
Ayushman Bharat (PM-JAY)
e-Shram Card
PM Fasal Bima Yojana

## 🛠️ Tech Stack

Frontend: Streamlit
Vector Search: FAISS
Embeddings: Sentence Transformers
LLM: Groq (openai/gpt-oss-20b)
Language: Python

## ⚙️Setup

bash
git clone https://github.com/<your-username>/civic-saathi.git
cd civic-saathi
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
cp .env.example .env         # added GROQ_API_KEY here

python -m rag.ingest         # builds the vector index
streamlit run app.py

### 📝 Notes

Eligibility rules are simplified and meant as guidance, not official confirmation. Always verify on the official government portal before applying.
Scheme rules and documents can change over time; the data here is a snapshot and may not reflect the latest updates.
Eligibility rules were tested against 140 synthetic applicant cases across all 14 schemes, with 100% accuracy.


## 🚀 Future Improvements

1. Self-updating knowledge base Right now Civic Saathi can only answer from documents already in its knowledge base. In the future, if a user asks
 about a scheme that isn't covered yet, the system should automatically find the official source, clean and chunk the content,
 add it to the vector database, and answer from it — so the next person asking the same question gets an instant answer instead of starting from scratch.

4. Agent Mode Add an optional mode where Civic Saathi doesn't just explain how to apply for a scheme, but helps fill and submit the
  actual application — collecting the user's details, filling the official form, and asking for confirmation before any final submission or payment.
  The user stays in control at every important step, and the agent never bypasses CAPTCHAs, OTPs, or other security checks.
