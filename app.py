import os
import re
import json
import tempfile
import time
import base64

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import streamlit as st

# ─── Page Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="MedAssist — Medical RAG Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Helper for Base64 Images ──────────────────────────────────────
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"
    return ""

banner_b64 = get_base64_image("assets/hospital_banner.jpg")
bot_avatar_b64 = get_base64_image("assets/bot_avatar.jpg")
bot_avatar_path = "assets/bot_avatar.jpg" if os.path.exists("assets/bot_avatar.jpg") else "🩺"
full_bg_b64 = get_base64_image("assets/hospital_full_bg.jpg")

# ─── Premium Dark Medical Theme CSS ───────────────────────────────
page_bg_css = f"background: linear-gradient(180deg, rgba(15, 23, 42, 0.82) 0%, rgba(15, 23, 42, 0.94) 100%), url('{full_bg_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if full_bg_b64 else "background-color: #0f172a;"
header_bg_css = f"background: linear-gradient(135deg, rgba(15, 23, 42, 0.75) 0%, rgba(14, 116, 144, 0.85) 100%), url('{banner_b64}'); background-size: cover; background-position: center;" if banner_b64 else "background: linear-gradient(135deg, #0f766e 0%, #0e7490 30%, #0369a1 60%, #1d4ed8 100%);"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Force dark background on root & Streamlit chrome */
    html, body, [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], header[data-testid="stHeader"],
    .stApp > header, #root {{
        background-color: #0f172a !important;
        background: #0f172a !important;
    }}

    /* Hide Streamlit top toolbar bar line */
    [data-testid="stHeader"] {{
        background-color: #0f172a !important;
        border-bottom: none !important;
    }}

    /* Global Full Hospital Background */
    .stApp {{
        font-family: 'Inter', sans-serif;
        {page_bg_css}
    }}

    /* Hide Sidebar */
    section[data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}

    /* Header with Hospital Banner */
    .med-header {{
        {header_bg_css}
        padding: 36px 42px;
        border-radius: 24px;
        color: white;
        box-shadow: 0 20px 60px -15px rgba(14, 116, 144, 0.5);
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }}
    .med-header-content {{
        max-width: 75%;
        z-index: 2;
    }}
    .med-title-container {{
        display: flex;
        align-items: center;
        gap: 16px;
    }}
    .med-avatar-img {{
        width: 64px;
        height: 64px;
        border-radius: 50%;
        border: 3px solid #38bdf8;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
        object-fit: cover;
    }}
    .med-title {{
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}
    .med-subtitle {{
        font-size: 1.05rem;
        opacity: 0.95;
        margin-top: 10px;
        font-weight: 400;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 5px rgba(0,0,0,0.3);
    }}
    .med-badges {{
        display: flex;
        gap: 10px;
        margin-top: 16px;
        position: relative;
        z-index: 1;
    }}
    .med-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        padding: 6px 16px;
        border-radius: 24px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    .hospital-badge-img {{
        width: 140px;
        height: 140px;
        border-radius: 20px;
        border: 2px solid rgba(255,255,255,0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        object-fit: cover;
        z-index: 2;
    }}

    /* Chat Bubbles */
    .user-msg {{
        background: linear-gradient(135deg, #0284c7, #2563eb);
        color: #ffffff !important;
        padding: 16px 22px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        font-size: 1rem;
        line-height: 1.6;
    }}
    .user-msg * {{
        color: #ffffff !important;
    }}

    .assistant-msg {{
        background: #ffffff !important;
        color: #0f172a !important;
        padding: 22px 28px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 0;
        max-width: 92%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        border: 1px solid #cbd5e1;
        font-size: 1rem;
        line-height: 1.75;
    }}
    .assistant-msg *, 
    .assistant-msg p, 
    .assistant-msg span, 
    .assistant-msg li, 
    .assistant-msg strong, 
    .assistant-msg b,
    .assistant-msg div {{
        color: #0f172a !important;
    }}

    /* Source Citation Cards */
    .source-card {{
        background: #ffffff !important;
        border-left: 4px solid #0ea5e9;
        padding: 14px 18px;
        border-radius: 0 12px 12px 0;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: transform 0.2s ease;
    }}
    .source-card:hover {{
        transform: translateX(4px);
    }}
    .source-tag {{
        font-size: 0.75rem;
        font-weight: 700;
        color: #0284c7 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }}
    .source-text, .source-text * {{
        font-size: 0.88rem;
        color: #334155 !important;
        line-height: 1.5;
    }}

    /* Bright White Spinner, Status Widget, & Expander Headers Override */
    div[data-testid="stSpinner"] *,
    div[data-testid="stStatusWidget"] *,
    details[data-testid="stStatusWidget"] *,
    div[data-testid="stStatusWidget"] summary,
    div[data-testid="stStatusWidget"] summary *,
    div[data-testid="stExpander"] summary *,
    details summary *,
    summary *,
    .stStatusWidget *,
    .stSpinner * {{
        color: #ffffff !important;
        font-weight: 600 !important;
    }}
</style>
""", unsafe_allow_html=True)

# ─── Header with Hospital & Bot Avatar ─────────────────────────────
avatar_html = f'<img src="{bot_avatar_b64}" class="med-avatar-img" />' if bot_avatar_b64 else '🩺'
hospital_side_html = f'<img src="{bot_avatar_b64}" class="hospital-badge-img" />' if bot_avatar_b64 else ''

st.markdown(f"""
<div class="med-header">
    <div class="med-header-content">
        <div class="med-title-container">
            {avatar_html}
            <div class="med-title">MedAssist AI</div>
        </div>
        <div class="med-subtitle">
            Clinical Knowledge Base QA Powered by BioMistral RAG & Hospital Knowledge Search
        </div>
        <div class="med-badges">
            <span class="med-badge">🏥 Hospital RAG Base</span>
            <span class="med-badge">🔬 PubMedBERT Embeddings</span>
        </div>
    </div>
    {hospital_side_html}
</div>
""", unsafe_allow_html=True)

# ─── Fixed Defaults (No Sidebar) ──────────────────────────────────
k_passages = 2
temperature = 0.2
negation_filter = True
uploaded_pdfs = []

# ─── Helper Functions ──────────────────────────────────────────────
def remove_negations(text: str) -> str:
    if not text:
        return ""
    pattern = r'\b(not|no|never|without|denies|denied|negative|non|neither|nor)\b'
    cleaned = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', cleaned).strip()


# ─── Local GGUF LLM (Optimized for Fast CPU Inference) ───────────
@st.cache_resource(show_spinner=False)
def load_local_llm():
    try:
        from langchain_community.llms import LlamaCpp
    except ImportError:
        return None

    # Check if llama-cpp-python is actually importable
    try:
        import llama_cpp  # noqa: F401
    except (ImportError, OSError):
        return None

    if os.path.exists("qwen2.5-3b-instruct-q4_k_m.gguf"):
        path = "qwen2.5-3b-instruct-q4_k_m.gguf"
    elif os.path.exists("BioMistral-7B.Q4_K_M.gguf"):
        path = "BioMistral-7B.Q4_K_M.gguf"
    else:
        return None

    try:
        cpu_threads = max(1, (os.cpu_count() or 4) - 1)
        return LlamaCpp(
            model_path=path,
            temperature=0.2,
            max_tokens=300,
            n_threads=cpu_threads,
            n_batch=512,
            n_ctx=1024,
            top_p=0.9,
            verbose=False
        )
    except Exception:
        # Handles WinError 4551 (Application Control policy blocked llama.dll)
        # and any other OS/runtime errors during model load
        return None


# ─── Session State ─────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


# ─── Load / Build Vector Store ─────────────────────────────────────
vectorstore = None

with st.status("🚀 Initializing Hospital RAG Pipeline...", expanded=True) as status:
    st.write("🔍 Loading FAISS Medical Index...")
    vectorstore = load_prebuilt_index()

    if not vectorstore and os.path.exists("healthyheart.pdf"):
        st.write("📄 Building index from healthyheart.pdf...")
        vectorstore = build_index_from_pdf("healthyheart.pdf")

    status.update(label="✅ Hospital Knowledge Base Ready!", state="complete", expanded=False)

st.session_state.vectorstore = vectorstore

if not vectorstore:
    st.error("❌ No knowledge base available. Please ensure `healthyheart.pdf` or `faiss_index` is in the folder.")
    st.stop()

retriever = vectorstore.as_retriever(search_kwargs={"k": k_passages})


# ─── Render Chat History ──────────────────────────────────────────
for message in st.session_state.messages:
    avatar_choice = bot_avatar_path if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_choice):
        if message["role"] == "user":
            st.markdown(f'<div class="user-msg">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-msg">{message["content"]}</div>', unsafe_allow_html=True)

        if "sources" in message and message["sources"]:
            with st.expander("📚 Retrieved Medical Sources"):
                for idx, src in enumerate(message["sources"], 1):
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-tag">Source #{idx} · Page {src['page']}</div>
                        <div class="source-text">{src['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ─── Chat Input ────────────────────────────────────────────────────
if user_query := st.chat_input("💬 Ask about heart health, risk factors, diet, exercise..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(f'<div class="user-msg">{user_query}</div>', unsafe_allow_html=True)

    # Negation removal for retrieval
    search_query = remove_negations(user_query) if negation_filter else user_query

    # Retrieve context
    retrieved_docs = retriever.invoke(search_query)
    sources_data = [
        {"page": str(doc.metadata.get("page", "N/A")), "content": doc.page_content}
        for doc in retrieved_docs
    ]
    context_str = "\n\n".join(
        [f"[Page {doc.metadata.get('page', 'N/A')}]: {doc.page_content[:300]}" for doc in retrieved_docs]
    )

    # Build prompt (concise for speed)
    full_prompt = f"""You are MedAssist, a concise heart-health medical assistant.
Answer using ONLY the context below. Use bullet points. Cite page numbers.

CONTEXT:
{context_str}

QUESTION: {user_query}
ANSWER:"""

    # Generate response
    with st.chat_message("assistant", avatar=bot_avatar_path):
        response_text = ""
        try:
            if use_gemini:
                # Stream tokens directly — no waiting for full response
                streamed = st.write_stream(stream_gemini(full_prompt, gemini_api_key))
                response_text = streamed if isinstance(streamed, str) else "".join(streamed)
            else:
                llm = load_local_llm()
                if llm is None:
                    response_text = (
                        "⚠️ **No LLM available.** Set `GEMINI_API_KEY` in the `.env` file to enable responses."
                    )
                    st.markdown(f'<div class="assistant-msg">{response_text}</div>', unsafe_allow_html=True)
                else:
                    with st.spinner("🧠 Thinking..."):
                        response_text = llm.invoke(full_prompt)
                    st.markdown(f'<div class="assistant-msg">{response_text}</div>', unsafe_allow_html=True)
        except Exception as e:
            response_text = f"❌ Error: {str(e)}"
            st.markdown(f'<div class="assistant-msg">{response_text}</div>', unsafe_allow_html=True)

        # Source Citations
        if sources_data:
            with st.expander("📚 Retrieved Medical Sources"):
                for idx, src in enumerate(sources_data, 1):
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-tag">Source #{idx} · Page {src['page']}</div>
                        <div class="source-text">{src['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # Save to session
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "sources": sources_data
    })
