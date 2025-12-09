# PDF Assistant - End-to-End Project

A conversational AI assistant that reads and answers questions about PDF documents. Built with **phidata**, **Streamlit**, and **PostgreSQL** for vector storage and conversation history.

## Project Overview

### What It Does
- Loads a PDF from a URL (Thai Recipes PDF in this example)
- Converts PDF content into vector embeddings (semantic search)
- Stores conversation history in PostgreSQL
- Provides an interactive interface to ask questions about the PDF
- Two ways to interact: **CLI** or **Streamlit Web UI**

### Key Features
- ✅ PDF knowledge base with semantic search (PgVector)
- ✅ Conversation history persistence (PostgreSQL)
- ✅ CLI and Streamlit web interfaces
- ✅ Show tool calls and reasoning
- ✅ Multi-user support with session management
- ✅ Markdown-formatted responses

---

## Project Structure

```
pdfassistent/
├── pdf_assistent.py      # CLI version (command-line interface)
├── streamlit.py          # Streamlit web UI version
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys, DB config)
└── README.md            # This file
```

### File Details

**pdf_assistent.py** - CLI Version
- Uses `typer` for command-line interface
- Loads PDF into vector database (PgVector2)
- Stores conversations in PostgreSQL
- Interactive terminal-based chat

**streamlit.py** - Streamlit Web UI Version (Recommended)
- Modern, user-friendly web interface
- Real-time response display
- Session management
- Start new conversations with one click
- Better for end-users

---

## Prerequisites

- **Python 3.8+** installed
- **Docker** installed (for PostgreSQL)
- **API Keys**: GROQ_API_KEY and/or OPENAI_API_KEY
- Internet connection (for downloading the PDF from URL)

---

## Setup Instructions

### Step 1: Install Python Dependencies

From the project root directory (`c:\Users\Admin\Documents\AgenticAI`):

```cmd
pip install -r pdfassistent/requirements.txt
```

This installs:
- phidata (AI agent framework)
- streamlit (web UI)
- psycopg, pgvector (PostgreSQL support)
- groq, openai (LLM providers)
- python-dotenv (environment variables)
- And others...

### Step 2: Set Up PostgreSQL Database

You have two options:

#### Option A: Using Docker (Recommended - Easiest)

Start PostgreSQL container on port 5433:

```cmd
docker run --name pdf-pg -e POSTGRES_PASSWORD=ai -e POSTGRES_USER=ai -e POSTGRES_DB=ai -p 5433:5432 -d postgres:15
```

Verify it's running:
```cmd
docker ps
```

You should see `pdf-pg` in the list.

#### Option B: Using Local PostgreSQL Installation

If you have PostgreSQL installed locally, make sure:
- Database name: `ai`
- Username: `ai`
- Password: `ai`
- Port: `5433` (or update the connection string)

### Step 3: Configure Environment Variables

Create a `.env` file in the `pdfassistent/` folder:

```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Get API keys from:
- **Groq**: https://console.groq.com
- **OpenAI**: https://platform.openai.com/api-keys

### Step 4: Update Database URL (if needed)

Open `streamlit.py` (line 20) and verify the database URL:

```python
DB_URL = "postgresql+psycopg://ai:ai@localhost:5433/ai"
```

If you used a different port, update accordingly.

---

## Running the Project

### Option 1: Streamlit Web UI (Recommended for End-Users)

```cmd
cd c:\Users\Admin\Documents\AgenticAI
streamlit run pdfassistent/streamlit.py
```

Then open your browser to: **http://localhost:8501**

**How to use:**
1. Type your question in the text input box
2. Press Enter
3. The assistant will search the PDF and respond
4. Click "Start New Session" to begin a fresh conversation

**Example questions:**
- "What are Thai recipes?"
- "Tell me about green curry"
- "List all ingredients for pad thai"
- "How do you make mango sticky rice?"

### Option 2: CLI Version (Terminal-Based)

```cmd
cd c:\Users\Admin\Documents\AgenticAI
python pdfassistent/pdf_assistent.py
```

**How to use:**
- Type your questions at the prompt
- Press Enter to get responses
- Type `exit` or `quit` to close

**CLI Options:**
```cmd
# Start a new conversation
python pdfassistent/pdf_assistent.py --new

# Use a specific username
python pdfassistent/pdf_assistent.py --user "john_doe"
```

---

## How It Works (Technical Overview)

### Architecture Flow

```
PDF URL 
  ↓
PDFUrlKnowledgeBase (loads & chunks PDF)
  ↓
PgVector2 (creates embeddings, stores in PostgreSQL)
  ↓
Assistant (Groq/OpenAI LLM for reasoning)
  ↓
Response (Streamlit UI or CLI output)
```

### Key Components

1. **PDFUrlKnowledgeBase**
   - Fetches PDF from URL
   - Chunks it into searchable segments
   - Creates semantic embeddings

2. **PgVector2** (Vector Database)
   - Stores embeddings in PostgreSQL with pgvector extension
   - Enables semantic search
   - Collection name: `recipes`

3. **PgAssistantStorage** (Conversation Storage)
   - Saves chat history to PostgreSQL
   - Table: `pdf_assistant`
   - Enables context-aware responses

4. **Assistant** (AI Agent)
   - Uses Groq LLM (fast, free tier available)
   - Searches knowledge base when needed
   - Reads conversation history for context
   - Returns markdown-formatted responses

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:** Install requirements:
```cmd
pip install -r pdfassistent/requirements.txt
```

### Issue: `GROQ_API_KEY not set`
**Solution:** Add your API key to `.env` file in the `pdfassistent/` folder

### Issue: `psycopg2.OperationalError: could not connect to server`
**Solution:** 
- Make sure PostgreSQL container is running: `docker ps`
- Or check local PostgreSQL is accessible on port 5433
- Update DB_URL in `streamlit.py` if using different port

### Issue: `Port 5433 already in use`
**Solution:** Use a different port:
```cmd
docker run --name pdf-pg -e POSTGRES_PASSWORD=ai -e POSTGRES_USER=ai -e POSTGRES_DB=ai -p 5434:5432 -d postgres:15
```
Then update `DB_URL` to `localhost:5434`

### Issue: No responses from the assistant
**Solution:**
- Verify PostgreSQL is running and connected
- Check that Groq/OpenAI API keys are valid
- Check internet connection (needed to download PDF)
- Look at error messages in terminal for details

---

## Customization

### Change the PDF Source

Edit `streamlit.py` or `pdf_assistent.py`, find the `PDFUrlKnowledgeBase` section:

```python
PDFUrlKnowledgeBase(
    urls=["https://your-pdf-url-here.pdf"],  # Change this URL
    vector_db=PgVector2(collection="your_collection_name", db_url=DB_URL),
)
```

### Use Different LLM

Change the model in `streamlit.py`:

```python
# Instead of Groq, use OpenAI (if OPENAI_API_KEY is set)
from phi.model.openai import OpenAIChat
# Then pass it to Assistant: model=OpenAIChat(api_key=...)
```

### Adjust Number of Context Chunks

Modify in `get_assistant()` function:

```python
assistant = Assistant(
    # ... existing params ...
    # Add: top_k=5  # retrieves top 5 chunks (default is usually 5)
)
```

---

## Stopping the Project

### Stop Streamlit
- Press `Ctrl+C` in the terminal where `streamlit run` is running

### Stop PostgreSQL Container
```cmd
docker stop pdf-pg
```

### Remove PostgreSQL Container (Optional)
```cmd
docker rm pdf-pg
```

---

## Next Steps / Enhancements

- [ ] Add support for local PDF files (not just URLs)
- [ ] Multiple PDF sources in one knowledge base
- [ ] Custom PDF upload in Streamlit UI
- [ ] Conversation export (PDF, JSON)
- [ ] User authentication & role-based access
- [ ] Rate limiting & usage analytics
- [ ] Deploy to Streamlit Cloud or Docker
- [ ] Add file persistence for offline use

---

## Dependencies Summary

| Package | Purpose |
|---------|---------|
| phidata | AI agent framework |
| streamlit | Web UI framework |
| psycopg[binary] | PostgreSQL driver |
| pgvector | Vector database extension |
| groq | Groq LLM API client |
| openai | OpenAI LLM API client |
| python-dotenv | Environment variable management |
| typer | CLI framework |

---

## Support & Resources

- **Phidata Docs**: https://docs.phidata.com
- **Streamlit Docs**: https://docs.streamlit.io
- **Groq API**: https://console.groq.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

## License & Notes

- This project uses open-source tools and free-tier APIs (Groq)
- Be mindful of API rate limits if using OpenAI
- Keep your `.env` file with API keys **private** and out of version control
- Add `.env` to `.gitignore` if using Git

---

## Quick Command Reference

```cmd
# Install dependencies
pip install -r pdfassistent/requirements.txt

# Start PostgreSQL (Docker)
docker run --name pdf-pg -e POSTGRES_PASSWORD=ai -e POSTGRES_USER=ai -e POSTGRES_DB=ai -p 5433:5432 -d postgres:15

# Run Streamlit UI
streamlit run pdfassistent/streamlit.py

# Run CLI version
python pdfassistent/pdf_assistent.py

# Check Docker status
docker ps

# Stop PostgreSQL
docker stop pdf-pg
```

---

**Last Updated**: November 11, 2025  
**Project Status**: ✅ Ready to Use
