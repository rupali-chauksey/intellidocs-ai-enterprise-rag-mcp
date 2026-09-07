# IntelliDocs AI — Enterprise RAG + MCP Assistant

IntelliDocs AI is a multi-source enterprise AI assistant that combines **Retrieval-Augmented Generation (RAG)**, the **Model Context Protocol (MCP)** for structured database access, and **web search** — all orchestrated through a **LangGraph** workflow with intelligent query routing and conversation memory.

> One assistant, multiple knowledge sources, intelligent routing.

---


🎥 **Demo Video:** 

https://github.com/user-attachments/assets/74e28186-4539-4337-a1e2-9add03b54a40


## 📸 Images 

**MCP Database + Web Search+RAG**

<img width="1912" height="1017" alt="test 1" src="https://github.com/user-attachments/assets/72da7124-efb1-49c5-8038-b838e7b21962" />

---

## ✨ Key Features

### 📚 1. Retrieval-Augmented Generation (RAG)

IntelliDocs AI can answer questions from uploaded enterprise documents.

**Supported formats:** PDF · TXT · Markdown · DOCX

**RAG pipeline:**

```
Document Upload → Text Extraction → Chunking → Embedding Generation
      → ChromaDB → User Query → Similarity Search
      → Relevance Filtering → LLM → Final Answer
```

**RAG capabilities**
- Document upload & automatic indexing
- Incremental ChromaDB indexing
- Document re-upload replacement
- Duplicate vector prevention
- Document status & chunk count tracking
- Document deletion (with vector cleanup)
- Relevance threshold filtering
- Source-aware answer generation
- Web fallback when relevant internal context is unavailable

### 🔌 2. Model Context Protocol (MCP)

A real MCP server exposes company database functionality as tools. The AI agent dynamically discovers available MCP tools and selects the appropriate one based on the user's question.

**MCP tools include:**
- Department statistics
- Employee queries
- Top products
- Sales performance
- Company overview
- Safe custom `SELECT` queries

The database agent selects the best available MCP tool and validates arguments before execution.

### 🗄️ 3. Company Database

A local SQLite database powers structured business queries, covering:

- **Employees** — info, department, salary, records
- **Products** — info, revenue, performance
- **Sales** — salesperson info, revenue, performance, transactions

Recreate it anytime with:

```bash
python setup_db.py
```

### 🧠 4. Intelligent Query Routing

The system identifies whether a question belongs to **RAG**, **Database**, **Web**, or **Both**, using deterministic routing rules for known enterprise query patterns.

| Example Question | Route |
|---|---|
| "What is the price of the AI course?" | RAG |
| "Who is the highest paid employee?" | Database → MCP |
| "What is the latest news?" | Web |

### 🔗 5. Hybrid RAG + MCP

IntelliDocs AI can answer questions that require more than one source at once, e.g.:

> "What is the sales incentive policy, and who is the top salesperson?"

```
Company Policy (RAG) ─┐
                       ├──► Response Synthesis ──► Final Answer
Sales Database (MCP) ──┘
```

This combines unstructured enterprise knowledge with structured business data in a single response.

### 🌐 6. Web Search Fallback

Used when a query requires current external information, e.g.:
- "Who is the current Prime Minister of India?"
- "What is the latest news?"
- "What is the current exchange rate?"

Also used as a fallback for RAG-oriented queries when no sufficiently relevant internal information is found.

### 💬 7. Conversation Memory

Recent conversation history is kept available to the workflow so follow-up questions can be interpreted in context. Example:

```
User: Who are the top 3 salespeople?
AI:   [Returns top 3 salespeople]

User: What are their salaries?
AI:   [Uses previous conversation context]

User: What department are they in?
AI:   [Uses conversation context + database information]
```

### 📄 8. Document Management

Full document lifecycle: **Upload → Index → Search → Query**

Documents can also be re-uploaded, re-indexed, replaced, deleted, or removed from the vector store. Document status and chunk counts make indexing issues easy to diagnose.

### 🎯 9. Relevance Filtering

Retrieval results are never blindly passed to the LLM — a configurable relevance threshold decides whether retrieved chunks are used:

```
Query → Vector Search → Retrieved Chunks → Relevance Threshold
   ├── Relevant     → Use RAG Context
   └── Not Relevant → Fallback
```

### 🧩 10. LangGraph Workflow

LangGraph orchestrates the full agent workflow:

```
                         START
                           │
                    Classify Query
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
      RAG               Database              Web
       │                   │                   │
   Retrieve            MCP Agent          Web Search
       │                   │                   │
 Relevance Grade     Database Tool             │
       └──────────────┬────┴───────────────────┘
                       ▼
               Response Synthesis
                       ▼
                  Final Answer
```

For hybrid questions: **RAG Retrieval + MCP Database → Response Synthesis → Final Answer**

---

## 🏗️ System Architecture

```
                           USER
                             │
                      FastAPI Backend
                             │
                      LangGraph Router
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
         RAG               MCP / DB            WEB
          │                  │                  │
      ChromaDB           MCP Server         Web Search
          │                  │                  │
    Relevant Context     SQLite DB              │
          └──────────────────┼──────────────────┘
                             ▼
                     Response Synthesis
                             ▼
                       Final Response
```

---

## 🧱 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| FastAPI | Backend API |
| LangGraph | Agent workflow orchestration |
| MCP | Database tool integration |
| ChromaDB | Vector database |
| SQLite | Structured company database |
| Groq | LLM inference |
| Sentence Transformers | Local embeddings |
| HTML / CSS / JavaScript | Frontend |
| Uvicorn | ASGI application server |
| Docker | Containerization support |

---

## 📁 Project Structure

```
IntelliDocs_AI_Enterprise_RAG_MCP/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db_tools.py
│   ├── graph.py
│   ├── ingestion.py
│   ├── main.py
│   ├── mcp_agent.py
│   ├── mcp_server.py
│   ├── tools.py
│   │
│   ├── routes/
│   │   ├── documents.py
│   │   └── upload.py
│   │
│   ├── services/
│   │   ├── chunker.py
│   │   ├── document_loader.py
│   │   ├── embedding.py
│   │   ├── uploader.py
│   │   └── vector_store.py
│   │
│   ├── static/
│   │   ├── index.html
│   │   └── assets/
│   │       └── style.css
│   │
│   └── uploads/
│
├── data/
│   └── company_policy.txt
│
├── tests/
│   └── test_basic.py
│
├── Assets/
│   ├── test_1.png
│   └── test_2.png
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── TROUBLESHOOTING.md
├── requirements.txt
├── run.py
├── setup_db.py
├── start.bat
└── start.sh
```

---


## ⚙️ Installation & Setup

### 🐍 1. Create Virtual Environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔐 4. Environment Configuration

Create a local `.env` file using `.env.example`:

```
GROQ_API_KEY=your_api_key_here
```

> ⚠️ Never commit API keys, passwords, tokens, or other secrets to GitHub.

### 🗄️ 5. Create the Company Database

```bash
python setup_db.py
```

This creates the local SQLite company database required by the MCP tools.

### ▶️ 6. Start the Application

```bash
python -m uvicorn app.main:app --port 8002
```

or

```bash
python run.py
```

On Windows, you can also use `start.bat`.

Open the application in your browser:

```
http://127.0.0.1:8002
```

### 📚 First Startup

On first run, the application may need to:
- Download the local embedding model
- Process bundled documents
- Generate embeddings
- Create/update the ChromaDB index

The first startup can therefore take longer than subsequent ones.

---

## 🧪 Testing

### RAG Test Questions
- **AI Course** — What is the price of the AI Course?
- **GenAI Bootcamp** — What are the prerequisites for the GenAI Bootcamp?
- **Leave Policy** — How many paid leaves are allowed?
- **Bonus** — What is the bonus for Rating 4?

### 🗄️ MCP / Database Test Questions
- **Sales** — Who are the top 3 salespeople by revenue?
- **Salary** — What is the average salary in Engineering?
- **Products** — Which product generated the most revenue?
- **Department** — How many employees are in Sales?

### 🔗 Hybrid Test

> What is the sales incentive policy, and which salesperson generated the most revenue?

Expected flow: `Sales Incentive Policy (RAG) + Top Salesperson (MCP) → Final Combined Answer`

### 🧠 Memory Test

Run sequentially:
1. Who are the top 3 salespeople?
2. What are their salaries?
3. What department are they in?

Each follow-up should be interpreted using the conversation context.

---

## 🔌 MCP Tool Selection

The database agent dynamically receives available MCP tools and selects the most appropriate one:

| Need | Tool |
|---|---|
| Department statistics | `get_department_stats` |
| Employee records | `query_employees` |
| Product revenue | `get_top_products` |
| Sales rankings | `get_sales_performance` |
| Company overview | `get_company_overview` |
| Other safe SELECT queries | `run_custom_query` |

The database tool layer validates and constrains arguments before execution.

---

## 🩺 Health & Diagnostics

Built-in diagnostics help identify problems with:
- Application startup
- Document indexing
- Vector store
- Database
- MCP connectivity

Document status and chunk counts can be used to verify whether a document was successfully indexed.

---

## 🛠️ Challenges Faced During Development

### Challenge 1 — Correct Query Routing
**Problem:** Not every question should go to the same source (e.g., employee salary → database, leave policy → documents). A generic LLM classifier could sometimes choose an incorrect route.
**Solution:** A deterministic routing layer was added for known enterprise document and database patterns, explicitly distinguishing RAG, Database, Both, and Web.

### Challenge 2 — RAG Retrieval Relevance
**Problem:** A document could be retrieved by vector similarity but still not be sufficiently relevant to the question, risking weak or incorrect context.
**Solution:** A configurable relevance threshold was introduced so weak retrieval results never automatically become trusted context.

### Challenge 3 — RAG Fallback
**Problem:** Some questions look like document questions but lack sufficient matching information internally.
**Solution:** The application falls back to web search when a RAG-only query doesn't produce usable internal context.

### Challenge 4 — MCP Database Integration
**Problem:** The application needs to communicate with a separate MCP server and dynamically select database tools.
**Solution:** The MCP agent starts the MCP server, initializes the session, discovers tools, provides tool descriptions to the routing logic, selects the best tool, validates arguments, executes it, and returns structured data for synthesis.

### Challenge 5 — Safe Custom Database Queries
**Problem:** A general database assistant should not execute arbitrary destructive SQL.
**Solution:** Custom database access is restricted to safe SELECT-style operations through a dedicated tool layer.

### Challenge 6 — Document Re-upload & Duplicate Vectors
**Problem:** Uploading the same document multiple times can create duplicate vectors.
**Solution:** The ingestion workflow supports replacement behavior so old vectors are removed/replaced instead of accumulating duplicates.

### Challenge 7 — MCP / Python Environment Compatibility
**Problem:** MCP SDK versions can change module paths and server APIs.
**Solution:** The project was aligned to the MCP server API available in the working environment, and the MCP server is launched as a Python module to avoid import-path issues.

### Challenge 8 — Port Conflicts During Development
**Problem:** FastAPI can fail to start if another process is using the configured port (e.g., `WinError 10048`).
**Solution:** Stop the conflicting process, or start on another port: `python -m uvicorn app.main:app --port 8003`

### Challenge 9 — Environment Variables & API Security
**Problem:** API keys must never be committed to a public GitHub repository.
**Solution:** Sensitive files are excluded via `.gitignore`; the repo keeps `.env.example` with placeholders while the real `.env` stays local.

---

## 🔒 Security

The following are intentionally excluded from Git:

```
.env
venv/
chroma_db/
company.db
__pycache__/
.pytest_cache/
.vscode/
```

**Never commit:** API keys · Passwords · Access tokens · Database credentials · Private certificates · Personal credentials

If a secret is accidentally committed, revoke/rotate it and remove it from Git history before publishing the repository.

---

## 📊 Example End-to-End Query

**Query:** "What is the sales incentive policy and who is the top salesperson?"

1. **Classification** → Hybrid
2. **RAG Retrieval** → Company Policy Documents → Relevant Chunks
3. **MCP Execution** → Sales Database → Sales Performance Tool → Top Salesperson
4. **Synthesis** → Policy Context + Sales Result → Final Enterprise Answer

---

## 📈 Why This Architecture?

A simple LLM chatbot can generate natural-language responses, but enterprise applications often need:

- Grounded answers
- Structured database access
- Document retrieval
- Current information
- Tool selection
- Source awareness
- Conversation context
- Controlled data access

IntelliDocs AI combines all of these into a single workflow.

---

## 🧪 Reliability Principles

1. **Don't blindly trust retrieval** — results are evaluated using relevance filtering.
2. **Don't use the database for everything** — only database-oriented questions are routed to MCP.
3. **Don't use RAG for current information** — current/external info uses web search.
4. **Don't expose secrets** — API keys stay outside version control.
5. **Don't execute uncontrolled database operations** — custom access is restricted to safe query patterns.

---

## 🚀 Future Improvements

- 🔐 Authentication
- 👥 Multi-user workspaces
- 🏢 Role-based document access
- ☁️ Cloud deployment
- 🗄️ PostgreSQL support
- 📦 Cloud vector databases
- ⚡ Streaming responses
- 📊 Advanced observability
- 🔎 Better citation rendering
- 🔑 Enterprise SSO
- 🤖 Multi-agent collaboration
- 📈 Production monitoring
- 🧪 Expanded automated test coverage
- 🌍 Scalable deployment architecture

---

## 🐳 Docker Support

The project includes a `Dockerfile` and `docker-compose.yml` for containerized deployment:

```bash
docker compose up --build
```

Verify environment variables and service configuration before using Docker in production.

---

## 🧪 Troubleshooting

**Server Import Error**
```bash
venv\Scripts\activate
python -m uvicorn app.main:app --port 8002
```

**GROQ API Key Error**
Check your local `.env`:
```
GROQ_API_KEY=your_new_key
```
Restart the server after updating the key.

**Product PDF Visible but Not Searchable**
Check the document status — it should show **Indexed** with a chunk count greater than zero. If needed, re-run ingestion or restart the application.

**Port Already in Use**
```bash
python -m uvicorn app.main:app --port 8003
```
Then open `http://127.0.0.1:8003`

**Upload Testing**
Avoid using `--reload` while testing uploads — the upload directory is inside the application directory, and automatic reloads can interfere while files are being written.

> More detail on server setup, Groq key issues, indexing, and port conflicts is available in `TROUBLESHOOTING.md`.

---

## 📌 Project Highlights

**Artificial Intelligence:** Retrieval-Augmented Generation · LLM-based response generation · Local embedding generation · Conversation memory · Multi-source answer synthesis

**Agentic AI:** LangGraph workflow · Intelligent query routing · MCP tool selection · Hybrid RAG + MCP execution · Web fallback

**Enterprise Knowledge:** PDF/TXT/Markdown/DOCX ingestion · Incremental indexing · Re-upload replacement · Relevance filtering

**Enterprise Data:** SQLite database · Employee, product, sales data · Department statistics · MCP database tools

**Backend:** FastAPI · Uvicorn · REST APIs

**Deployment:** Dockerfile · Docker Compose · Windows/Linux/macOS startup scripts

---

## 🎓 What This Project Demonstrates

Practical implementation of: **LLM Applications + RAG + Vector Databases + Agentic Workflows + LangGraph + Model Context Protocol + Database Tool Calling + Web Search + FastAPI + Document Processing**

Rather than building only a chatbot, IntelliDocs AI focuses on building a multi-source enterprise AI system capable of connecting unstructured documents, structured business data, and external information.

---

## 👩‍💻 Author

**Rupali Chouksey**
AI Engineer 

---

## ⭐ Support the Project

If you found this project interesting or useful:
- ⭐ Star the repository
- 🍴 Fork the project
- 💬 Share feedback
- 🚀 Explore the implementation

---


## 📄Final Note

IntelliDocs AI brings enterprise documents, structured company data, and external web intelligence together through an intelligent AI workflow.

```
              INTELLIDOCS AI

       ┌──────────┬──────────┬──────────┐
       │          │          │          │
     RAG         MCP        WEB      MEMORY
       │          │          │          │
       ▼          ▼          ▼          ▼
   Documents   Database   Internet   Context
       │          │          │          │
       └──────────┴──────────┴──────────┘
                    │
                    ▼
             LangGraph Router
                    │
                    ▼
             Intelligent Answer
```

**Enterprise Knowledge + Business Data + Web Intelligence = IntelliDocs AI**
