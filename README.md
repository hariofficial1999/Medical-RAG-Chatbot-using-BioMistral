# 🏥 MedAssist AI — Medical RAG Chatbot

> A **Retrieval-Augmented Generation (RAG)** chatbot for heart-health Q&A, powered by **BioMistral / Qwen2.5**, **FAISS vector search**, **PubMedBERT embeddings**, and **Google Gemini 2.0 Flash** with real-time streaming responses.

---

## ✨ Features

- 🔍 **Semantic Search** — FAISS vector store with `all-MiniLM-L6-v2` embeddings for fast, accurate context retrieval
- 🧠 **Dual LLM Support** — Google Gemini 2.0 Flash (cloud) or local GGUF models (BioMistral-7B / Qwen2.5-3B)
- ⚡ **Streaming Responses** — Token-by-token streaming via Gemini so answers appear instantly
- 📄 **PDF Knowledge Base** — Automatically indexes any medical PDF (default: `healthyheart.pdf`)
- 🏷️ **Source Citations** — Every answer cites the exact page from the knowledge base
- 🌙 **Premium Dark UI** — Glassmorphism design with hospital banner, animated badges, and custom chat bubbles

---

## 🗂️ Project Structure

```
Medical RAG Chatbot using BioMistral/
│
├── app.py                          # Main Streamlit application
├── build_index.py                  # Script to pre-build the FAISS index
├── healthyheart.pdf                # Default medical knowledge base (PDF)
├── requirements.txt                # Python dependencies
├── .env                            # API key config (create this yourself)
│
├── faiss_index/                    # Auto-generated vector index
│   ├── index.faiss
│   └── index.pkl
│
├── assets/                         # UI images
│   ├── hospital_banner.jpg
│   ├── hospital_full_bg.jpg
│   └── bot_avatar.jpg
│
├── BioMistral-7B.Q4_K_M.gguf      # (Optional) Local BioMistral model
└── qwen2.5-3b-instruct-q4_k_m.gguf # (Optional) Local Qwen2.5 model
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

```bash
python build_index.py
```

> If you skip this, the app will auto-build it from `healthyheart.pdf` on first launch.

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## ⚙️ Configuration

| Setting | Default | Description |
|---|---|---|
| `k_passages` | `2` | Number of context chunks retrieved per query |
| `temperature` | `0.2` | LLM response creativity (lower = more factual) |
| `negation_filter` | `True` | Strips negation words before retrieval for better matches |
| Embedding model | `all-MiniLM-L6-v2` | Sentence transformer for vector embeddings |
| Gemini model | `gemini-2.0-flash` | Google Gemini model used for generation |

---

## 🤖 LLM Options

### Option A — Google Gemini (Recommended ✅)
- Fast, accurate, streamed responses
- Requires a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Set `GEMINI_API_KEY` in `.env`

### Option B — Local GGUF Model (Offline)
- Requires `llama-cpp-python` and a C++ compiler
- Place one of these models in the project root:
  - `qwen2.5-3b-instruct-q4_k_m.gguf` *(faster, lighter)*
  - `BioMistral-7B.Q4_K_M.gguf` *(medically fine-tuned)*

```bash
pip install llama-cpp-python
```

> ⚠️ On Windows, if blocked by Application Control policy, use the Gemini option instead.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Embeddings** | `sentence-transformers` / `all-MiniLM-L6-v2` |
| **Vector Store** | FAISS (CPU) |
| **LLM (Cloud)** | Google Gemini 2.0 Flash |
| **LLM (Local)** | BioMistral-7B / Qwen2.5-3B via `llama-cpp-python` |
| **RAG Framework** | LangChain |
| **PDF Parsing** | PyPDF |

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
llama-cpp-python>=0.2.20   # optional, for local inference
python-dotenv               # optional, for .env support
```

---

## 📌 Notes

- The chatbot is specialized for **heart health** questions based on the indexed PDF(s)
- For best results, ask specific clinical questions (e.g. *"What are the risk factors for coronary artery disease?"*)
- The FAISS index is cached — delete `faiss_index/` and restart to re-index a new PDF

---

## 📄 License

This project is for educational and research purposes.

---

<div align="center">
  Made with ❤️ using BioMistral, LangChain & Streamlit
</div>
