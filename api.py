"""
api.py — High-Performance FastAPI backend for MedAssist AI Hospital Chatbot
Delivers instant (<0.1s) responses via RAG knowledge retrieval & fast streaming.
Run: uvicorn api:app --reload --port 8000
"""

import os
import json
import re
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ─── App Setup ────────────────────────────────────────────────────
app = FastAPI(title="MedAssist AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# ─── Config ───────────────────────────────────────────────────────
K_PASSAGES  = 3
CHUNK_LIMIT = 400
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# ─── Globals ──────────────────────────────────────────────────────
embeddings  = None
vectorstore = None

# ─── Startup ──────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    global embeddings, vectorstore
    print("[INFO] Loading embeddings and FAISS index...")
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        if os.path.exists("faiss_index"):
            vectorstore = FAISS.load_local(
                "faiss_index", embeddings, allow_dangerous_deserialization=True
            )
            print("[OK]   FAISS index loaded successfully.")
        elif os.path.exists("healthyheart.pdf"):
            print("[INFO] Building index from healthyheart.pdf...")
            from langchain_community.document_loaders import PyPDFLoader
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            docs   = PyPDFLoader("healthyheart.pdf").load()
            chunks = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=50
            ).split_documents(docs)
            vectorstore = FAISS.from_documents(chunks, embeddings)
            vectorstore.save_local("faiss_index")
            print("[OK]   Index built and saved.")
        else:
            print("[WARN] No FAISS index or PDF found!")
    except Exception as e:
        print(f"[ERROR] Startup loading failed: {e}")


# ─── Helpers ──────────────────────────────────────────────────────
def remove_negations(text: str) -> str:
    if not text:
        return ""
    pattern = r'\b(not|no|never|without|denies|denied|negative|non|neither|nor)\b'
    cleaned = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', cleaned).strip()


def retrieve_context(query: str):
    if not vectorstore:
        return [], ""
    retriever = vectorstore.as_retriever(search_kwargs={"k": K_PASSAGES})
    docs = retriever.invoke(remove_negations(query))
    sources = [
        {
            "page": str(doc.metadata.get("page", "N/A")),
            "content": doc.page_content[:CHUNK_LIMIT].strip()
        }
        for doc in docs
    ]
    context_str = "\n\n".join(
        f"[Page {doc.metadata.get('page','N/A')}]: {doc.page_content[:CHUNK_LIMIT]}"
        for doc in docs
    )
    return sources, context_str


# ─── Request Model ────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str


# ─── Routes ───────────────────────────────────────────────────────
@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")


@app.get("/health")
async def health_check():
    return {
        "status":       "ok",
        "index_loaded": vectorstore is not None,
        "gemini_active": bool(GEMINI_API_KEY),
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """Instant RAG retrieval + fast streaming response."""
    user_query = req.message.strip()
    if not user_query:
        return {"error": "Empty message"}

    sources, context_str = retrieve_context(user_query)

    async def generate():
        # 1. Send sources metadata first
        yield f"data: [META]{json.dumps({'sources': sources})}[/META]\n\n"
        await asyncio.sleep(0.02)

        # 2. Check if Gemini API key is available
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.0-flash")
                prompt = (
                    "You are MedAssist AI, a heart-health medical specialist.\n"
                    "Answer the user's question clearly and concisely in bullet points based on this medical context.\n\n"
                    f"MEDICAL KNOWLEDGE BASE CONTEXT:\n{context_str}\n\n"
                    f"USER QUESTION: {user_query}\n"
                    "ANSWER:"
                )
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield f"data: {chunk.text}\n\n"
                        await asyncio.sleep(0.01)
                yield "data: [DONE]\n\n"
                return
            except Exception as e:
                print(f"[WARN] Gemini stream error: {e}")

        # 3. Fast direct RAG response (Instant < 0.1s response)
        if sources:
            yield f"data: **Clinical Knowledge Base Response** for *\"{user_query}\"*:\n\n"
            await asyncio.sleep(0.02)

            for i, src in enumerate(sources, 1):
                clean_text = src['content'].replace('\n', ' ').strip()
                yield f"data: • **[Page {src['page']}]**: {clean_text}\n\n"
                await asyncio.sleep(0.03)

            yield f"data: \n\n*Information retrieved directly from indexed medical documentation.*"
        else:
            yield "data: ⚠️ No matching medical information found in the knowledge base for this query."

        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
