# 🏥 MedAssist AI — Medical RAG Chatbot

> A **Retrieval-Augmented Generation (RAG)** chatbot specialized in **heart health Q&A**, built with **BioMistral-7B / Qwen2.5-3B** local models, **FAISS semantic vector search**, `all-MiniLM-L6-v2` embeddings, and **Google Gemini 2.0 Flash** with real-time token streaming.

---

## ✨ Features

- 🔍 **Semantic Search** — FAISS vector store with `all-MiniLM-L6-v2` embeddings retrieves the most relevant context passages instantly
- 🧠 **Dual LLM Support** — Google Gemini 2.0 Flash (cloud, streamed) **or** local GGUF models (BioMistral-7B / Qwen2.5-3B, fully offline)
- ⚡ **Token Streaming** — Gemini responses stream word-by-word so answers feel instant, no waiting
- 🚫 **Negation Filter** — Strips negation words (no, not, never…) from queries before retrieval for better semantic matches
- 📄 **Auto PDF Indexing** — Drop any medical PDF in the folder; the app auto-indexes it into FAISS on first launch
- 🏷️ **Page-level Citations** — Every answer cites the exact page number from `healthyheart.pdf`
- 🌙 **Premium Dark UI** — Hospital banner background, glassmorphism cards, animated chat bubbles, custom bot avatar

---

## 🗂️ Project Structure

```
Medical RAG Chatbot using BioMistral/
│
├── app.py                             # Main Streamlit app (UI + RAG pipeline)
├── build_index.py                     # One-time script to pre-build FAISS index
├── healthyheart.pdf                   # Heart health knowledge base (PDF source)
├── requirements.txt                   # Python dependencies
├── .env                               # Set GEMINI_API_KEY here (optional)
│
├── faiss_index/                       # Auto-generated FAISS vector index
│   ├── index.faiss                    # Binary vector index
│   └── index.pkl                      # Document metadata store
│
├── assets/                            # UI image assets
│   ├── hospital_banner.jpg            # Header banner background
│   ├── hospital_full_bg.jpg           # Full page background
│   └── bot_avatar.jpg                 # Chatbot avatar image
│
├── BioMistral-7B.Q4_K_M.gguf         # (Optional) Medically fine-tuned local LLM
└── qwen2.5-3b-instruct-q4_k_m.gguf   # (Optional) Fast lightweight local LLM
```

---

## 🔄 How It Works

```
User Query
    │
    ▼
[Negation Filter]          ← strips "no/not/never" for cleaner retrieval
    │
    ▼
[FAISS Retriever]          ← top-2 semantic chunks from healthyheart.pdf
    │
    ▼
[Prompt Builder]           ← system prompt + context + question
    │
    ▼
[LLM Generation]           ← Gemini 2.0 Flash (streaming) or local GGUF
    │
    ▼
[Response + Citations]     ← answer with page references shown in UI
```

---

## 🚀 Quick Start

### 1. Clone / Download the project

```bash
git clone https://github.com/your-username/medical-rag-chatbot.git
cd "Medical RAG Chatbot using BioMistral"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Pre-build the FAISS index

Run this once to build and save the vector index to disk — the app loads instantly on all future runs:

```bash
python build_index.py
```

```
============================================================
  FAISS Index Builder for Medical RAG Chatbot
============================================================
[1/4] Loading PDF: healthyheart.pdf...
[2/4] Chunking (size=500, overlap=50)...
[3/4] Loading embedding model: all-MiniLM-L6-v2...
[4/4] Building FAISS index and saving to 'faiss_index/'...
  INDEX BUILT SUCCESSFULLY!
============================================================
```

> If you skip this step, the index is auto-built from `healthyheart.pdf` on first launch (takes ~30–60s).

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 💬 Example Questions

Try asking MedAssist AI:

- *"What are the main risk factors for heart disease?"*
- *"How does diet affect cholesterol levels?"*
- *"What exercises are recommended for heart health?"*
- *"What is the difference between HDL and LDL cholesterol?"*
- *"How does high blood pressure damage the heart?"*

---

## ⚙️ Configuration

All settings are in [`app.py`](app.py) under `Fixed Defaults`:

| Setting | Default | Description |
|---|---|---|
| `k_passages` | `2` | Number of context chunks retrieved per query |
| `temperature` | `0.2` | LLM creativity — lower = more factual answers |
| `negation_filter` | `True` | Strips negation words before retrieval |
| `chunk_size` | `500` | Characters per document chunk (in `build_index.py`) |
| `chunk_overlap` | `50` | Overlap between chunks to preserve context |
| Embedding model | `all-MiniLM-L6-v2` | Sentence transformer for vector search |
| LLM (cloud) | `gemini-2.0-flash` | Google Gemini model |

---

## 🤖 LLM Options



###  Local GGUF Models (Offline 🖥️)
Requires `llama-cpp-python` and a C++ compiler:

```bash
pip install llama-cpp-python
```

Place one of these in the project root:

| Model | Size | Notes |
|---|---|---|
| `qwen2.5-3b-instruct-q4_k_m.gguf` | ~1.9 GB | Faster, lighter, general purpose |
| `BioMistral-7B.Q4_K_M.gguf` | ~4.4 GB | Medically fine-tuned on PubMed data |

> ⚠️ On Windows, if blocked by **Application Control policy (WinError 4551)**, the app automatically falls back gracefully — use Gemini instead.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit 1.30+ |
| **Embedding Model** | `all-MiniLM-L6-v2` via `sentence-transformers` |
| **Vector Store** | FAISS (CPU) |
| **LLM — Cloud** | Google Gemini 2.0 Flash (`google-generativeai`) |
| **LLM — Local** | BioMistral-7B / Qwen2.5-3B via `llama-cpp-python` |
| **RAG Framework** | LangChain + LangChain-Community |
| **PDF Parsing** | PyPDF |
| **Env Config** | `python-dotenv` |

---

## 📋 Requirements

```
streamlit>=1.30.0
langchain>=0.1.0
langchain-community>=0.0.20
langchain-text-splitters>=0.0.1
sentence-transformers>=2.2.2
pypdf>=4.0.0
faiss-cpu>=1.7.4
google-generativeai>=0.5.0
llama-cpp-python>=0.2.20   # optional — for local offline inference
python-dotenv               # optional — for .env file support
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 📌 Tips & Notes

- 💡 The chatbot answers based **only** on the indexed PDF — for best results use `healthyheart.pdf` or replace it with your own medical PDF
- 🗑️ To re-index a new PDF: delete the `faiss_index/` folder and restart the app
- 🔁 Embedding model and vector store are **cached** with `@st.cache_resource` — no reload on every query
- 🧹 Negation filter pre-processes queries like *"foods that are not bad for the heart"* → *"foods good heart"* for better semantic matches
- 📖 Source citations are shown per-response in a collapsible **"Retrieved Medical Sources"** expander

---

## 📄 License

This project is for **educational and research purposes** only.  
Not intended as a substitute for professional medical advice.

---

<div align="center">
  Made with ❤️ using BioMistral · LangChain · FAISS · Streamlit
</div>
