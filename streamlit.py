# pdfassistent/streamlit_app.py
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

# Fix/ensure GROQ key present in env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY is None:
    st.warning("GROQ_API_KEY not set in environment. Set it in pdfassistent/.env or your environment variables.")

# Import phi components (must be installed)
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2

# Database URL (adjust as needed)
DB_URL = "postgresql+psycopg://ai:ai@localhost:5532/ai"

@st.cache_resource
def init_knowledge_base():
    kb = PDFUrlKnowledgeBase(
        urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
        vector_db=PgVector2(collection="recipes", db_url=DB_URL),
    )
    kb.load()
    return kb

@st.cache_resource
def init_storage():
    return PgAssistantStorage(table_name="pdf_assistant", db_url=DB_URL)

def get_assistant(run_id=None, user="streamlit_user"):
    kb = init_knowledge_base()
    storage = init_storage()
    assistant = Assistant(
        run_id=run_id,
        user_id=user,
        knowledge_base=kb,
        storage=storage,
        show_tool_calls=True,
        search_knowledge=True,
        read_chat_history=True,
    )
    return assistant

# Streamlit UI
st.title("PDF Assistant (Streamlit)")

# Session-based run id to keep conversation
if "run_id" not in st.session_state:
    st.session_state["run_id"] = None

col1, col2 = st.columns([4,1])
with col1:
    user_input = st.text_input("Ask about the PDF:", key="user_input")
with col2:
    new_run = st.button("Start New Session")

if new_run:
    st.session_state["run_id"] = None
    st.experimental_rerun()

assistant = get_assistant(run_id=st.session_state.get("run_id"))

# When user submits
if user_input:
    try:
        # Use whatever programmatic API is available on Assistant:
        # try run/ask/respond depending on the phi version. We'll try 'run' first.
        if hasattr(assistant, "run"):
            resp = assistant.run(user_input)
        elif hasattr(assistant, "respond"):
            resp = assistant.respond(user_input)
        elif hasattr(assistant, "ask"):
            resp = assistant.ask(user_input)
        else:
            raise RuntimeError("Assistant object has no run/respond/ask method.")
    except Exception as e:
        st.error(f"Agent call failed: {e}")
    else:
        # Save run_id to session for subsequent calls (if assistant exposes it)
        try:
            st.session_state["run_id"] = assistant.run_id
        except Exception:
            pass

        st.subheader("Assistant response")
        st.markdown(str(resp))