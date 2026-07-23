# 🏥 MedAssist AI — Medical RAG Chatbot & Hospital Portal

> A **Retrieval-Augmented Generation (RAG)** medical chatbot and hospital portal specialized in **heart health Q&A**, built with **FastAPI**, **Streamlit**, **FAISS semantic vector search**, `all-MiniLM-L6-v2` embeddings, and **Google Gemini 2.0 Flash / BioMistral-7B** with real-time streaming responses.

---

## ✨ Features

- 🏥 **Hospital Web Portal** — Full-featured, modern dark-themed medical web app (`index.html`) with an embedded AI assistant
- ⚡ **FastAPI Backend** — High-performance non-blocking SSE streaming API (`api.py`)
- 🔍 **Semantic Vector Search** — FAISS vector store with `all-MiniLM-L6-v2` embeddings for instant context retrieval (<0.1s)
- 🧠 **RAG Engine** — Retrieves exact page-numbered context from indexed medical documentation (`healthyheart.pdf`)
- 🚫 **Negation Filtering** — Pre-filters query negation words (`no`, `not`, `never`...) for higher semantic accuracy
- 🚨 **Emergency Triage** — Direct 24/7 cardiac emergency hotline integration (**911**)
- 🏷️ **Source Citations** — Every answer includes collapsible citations referencing exact PDF page numbers

---

## 🗂️ Project Structure

```
Medical RAG Chatbot using BioMistral/
│
├── api.py                             # FastAPI backend (SSE streaming + RAG)
├── index.html                         # Hospital web portal & embedded chatbot
├── app.py                             # Streamlit web application
├── build_index.py                     # Script to pre-build FAISS vector index
├── healthyheart.pdf                   # Medical knowledge base PDF
├── requirements.txt                   # Dependencies
├── .env                               # Config (GEMINI_API_KEY optional)
│
├── faiss_index/                       # Pre-built FAISS vector store
│   ├── index.faiss                    # Vector index
│   └── index.pkl                      # Metadata store
│
├── assets/                            # Web & branding assets
│   ├── hospital_banner.jpg
│   ├── hospital_full_bg.jpg
│   └── bot_avatar.jpg
│
├── BioMistral-7B.Q4_K_M.gguf         # (Optional) Medically fine-tuned LLM
└── qwen2.5-3b-instruct-q4_k_m.gguf   # (Optional) Lightweight LLM
```

---

## 🔄 RAG Architecture

```
User Query (e.g. "Heart disease risk factors")
    │
    ▼
[Negation Filter]     ← Cleans query for optimal semantic matching
    │
    ▼
[FAISS Vector Search] ← Retrieves top-3 relevant chunks from healthyheart.pdf (<0.05s)
    │
    ▼
[Context Assembly]    ← Formats medical passages with page numbers
    │
    ▼
[Response Generator]  ← Gemini 2.0 Flash streaming / Instant RAG response
    │
    ▼
[Web UI Output]       ← Streams response + collapsible page citations
```

---

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run FastAPI Hospital Portal (Recommended)

```bash
uvicorn api:app --port 8000
```

Open your browser at: **`http://localhost:8000`**

---

### 4. Alternative: Run Streamlit Interface

```bash
streamlit run app.py
```

Open your browser at: **`http://localhost:8501`**

---

## 💬 Example Questions

- *"What are the main risk factors for heart disease?"*
- *"How does high blood pressure damage the heart?"*
- *"What exercises are recommended for heart health?"*
- *"What is the difference between HDL and LDL cholesterol?"*
- *"How does diet affect cardiac health?"*

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Web Portal** | HTML5, Vanilla CSS3, Modern JS (ES6+) |
| **Backend API** | FastAPI + Uvicorn (ASGI) |
| **Streamlit App** | Streamlit 1.30+ |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| **Vector Database** | FAISS (Facebook AI Similarity Search) |
| **Cloud LLM** | Google Gemini 2.0 Flash (`google-generativeai`) |
| **Local LLM** | BioMistral-7B / Qwen2.5-3B via `llama-cpp-python` |
| **RAG Framework** | LangChain + PyPDF |

---

## 📌 Notes & Customization

- 📄 **Custom Knowledge Base**: Replace `healthyheart.pdf` with any medical document and delete `faiss_index/` to re-index automatically.
- 🚨 **Emergency Contact**: Standardized to **911** in the hospital portal emergency section.
- 🔑 **API Key (Optional)**: Set `GEMINI_API_KEY` in `.env` for AI text synthesis, or run in instant direct RAG mode out-of-the-box.

---

## 📄 License

Educational and research project for medical RAG architecture demonstration.

---

<div align="center">
  Made with ❤️ using BioMistral · LangChain · FAISS · FastAPI · Streamlit
</div>
