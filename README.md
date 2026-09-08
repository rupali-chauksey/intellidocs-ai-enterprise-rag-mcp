# IntelliDocs AI — Enterprise RAG + MCP Assistant

<div align="center">

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/rupali-chouksey/IntelliDocs-AI?style=social)](https://github.com/rupali-chouksey/IntelliDocs-AI)

**One assistant, multiple knowledge sources, intelligent routing.**

[🎥 Demo Video](#-demo-video) • [📖 Features](#-key-features) • [⚡ Quick Start](#-quick-start) • [🛠️ Setup](#-installation-setup)

</div>

---

## 🎯 Overview

IntelliDocs AI is a **production-ready enterprise AI assistant** that combines:

- **Retrieval-Augmented Generation (RAG)** — Answer questions from uploaded enterprise documents
- **Model Context Protocol (MCP)** — Access structured company databases with intelligent tool selection
- **Web Search** — Fetch current external information
- **LangGraph Workflow** — Orchestrate complex multi-source queries with conversation memory

Perfect for organizations needing a **unified AI interface** that connects documents, databases, and real-time information.

---

## 🎥 Demo Video

https://github.com/user-attachments/assets/74e28186-4539-4337-a1e2-9add03b54a40

---

## 📸 Architecture Visualization

**IntelliDocs AI Processing Pipeline:**

<img width="1912" height="1017" alt="IntelliDocs AI Demo" src="https://github.com/user-attachments/assets/72da7124-efb1-49c5-8038-b838e7b21962" />

---

## ⚡ Quick Start (5 Minutes)

### Prerequisites
- **Python 3.9+**
- **GROQ API Key** ([Get free key](https://console.groq.com))
- **Git** (for cloning)

### Installation & Running

```bash
# 1️⃣ Clone the repository
git clone https://github.com/rupali-chouksey/IntelliDocs-AI.git
cd IntelliDocs-AI

# 2️⃣ Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Setup environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5️⃣ Initialize database
python setup_db.py

# 6️⃣ Run the application
python -m uvicorn app.main:app --reload --port 8002

# 7️⃣ Open browser
# Navigate to http://localhost:8002
```

**Done! 🎉** Your IntelliDocs AI instance is now running.

---

## 🔧 Installation & Setup

### System Requirements

| Requirement | Version |
|------------|---------|
| Python | 3.9 or higher |
| pip | Latest |
| Node.js (optional) | 16+ (for frontend dev) |
| Git | 2.0+ |
| RAM | Minimum 2GB, Recommended 4GB+ |
| Disk Space | ~500MB for dependencies |

### Detailed Setup Steps

#### Step 1: Clone Repository
```bash
git clone https://github.com/rupali-chouksey/IntelliDocs-AI.git
cd IntelliDocs-AI
```

#### Step 2: Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Environment Configuration
```bash
# Copy template
cp .env.example .env

# Edit .env file and add your keys:
# GROQ_API_KEY=your_api_key_here
# CHROMA_DB_PATH=./chroma_db
# DATABASE_PATH=./company.db
```

**⚠️ Important:** Never commit `.env` file to Git!

#### Step 5: Database Setup
```bash
# Create and populate SQLite database
python setup_db.py

# Verify database
sqlite3 company.db ".tables"
```

#### Step 6: Run the Application
```bash
# Development mode (with auto-reload)
python -m uvicorn app.main:app --reload --port 8002

# Production mode
python -m uvicorn app.main:app --port 8002 --workers 4
```

#### Step 7: Access the Application
```
📱 Open your browser: http://localhost:8002
```

---

## ✨ Key Features

### 📚 1. Retrieval-Augmented Generation (RAG)

Answer questions from uploaded enterprise documents with source awareness.

**Supported Formats:** 
- 📄 PDF
- 📝 TXT
- 📖 Markdown
- 📋 DOCX

**RAG Pipeline:**
```
Document Upload 
    ↓
Text Extraction & Preprocessing
    ↓
Smart Chunking (Overlap Detection)
    ↓
Embedding Generation (Sentence Transformers)
    ↓
ChromaDB Vector Storage
    ↓
User Query Processing
    ↓
Semantic Similarity Search
    ↓
Relevance Threshold Filtering
    ↓
LLM Answer Generation
    ↓
Source-Aware Response
```

**RAG Capabilities:**
- ✅ Document upload & automatic indexing
- ✅ Incremental ChromaDB indexing
- ✅ Document re-upload with replacement
- ✅ Duplicate vector prevention
- ✅ Document status & chunk count tracking
- ✅ Safe document deletion with vector cleanup
- ✅ Configurable relevance threshold filtering
- ✅ Source-aware answer generation
- ✅ Web fallback when context is unavailable

### 🔌 2. Model Context Protocol (MCP)

A real MCP server exposes company database functionality as intelligent tools. The system dynamically discovers available tools and selects the best one for each query.

**Available MCP Tools:**
| Tool | Purpose |
|------|---------|
| `get_department_stats` | Department statistics & metrics |
| `query_employees` | Employee records & information |
| `get_top_products` | Product revenue rankings |
| `get_sales_performance` | Sales team performance data |
| `get_company_overview` | Company-wide metrics |
| `run_custom_query` | Safe SELECT queries |

**Smart Tool Selection:**
- 🎯 Analyzes query intent
- 🔍 Validates argument types
- 🛡️ Prevents SQL injection
- 📊 Returns structured data

### 🗄️ 3. Company Database

A production-ready SQLite database covering:

**Employees Module:**
- Employee ID, name, email, department
- Salary, hire date, job title
- Performance metrics

**Products Module:**
- Product ID, name, category
- Price, revenue, stock
- Performance metrics

**Sales Module:**
- Salesperson details
- Revenue data, commissions
- Transaction records

**Recreate Database Anytime:**
```bash
python setup_db.py
```

### 🧠 4. Intelligent Query Routing

The system identifies query type and routes to the optimal source using deterministic patterns.

| Query Type | Route | Example |
|---|---|---|
| Document Question | RAG | "What is the AI course content?" |
| Database Query | MCP | "Who is the highest paid employee?" |
| Current Information | Web | "What is latest tech news?" |
| Hybrid Query | RAG + MCP | "What is our policy AND who leads sales?" |

**Routing Decision Tree:**
```
                    User Query
                        ↓
                Pattern Matcher
                        ↓
        ┌───────────────┼────────────┐
        ▼               ▼            ▼
      RAG Only    Database Only    Web Only
        ├               ├             │
        └───────────────┼─────────────┘
                        ▼
            Check for Hybrid Patterns
                        ↓
            Route to Appropriate Handler
```

### 🔗 5. Hybrid RAG + MCP Processing

Answer complex questions requiring multiple sources simultaneously.

**Example Query:** 
> "What is our sales incentive policy, and who are our top 3 salespeople?"

**Processing Flow:**
```
┌─────────────────────────────────┐
│   User Query (Hybrid Pattern)   │
└────────────┬────────────────────┘
             ↓
    ┌────────┴────────┐
    ↓                 ↓
 RAG Retrieval   MCP Database
   (Policy)      (Sales Data)
    │                 │
    └────────┬────────┘
             ↓
    Response Synthesis
    (LLM Combination)
             ↓
    ┌───────────────────┐
    │  Final Answer     │
    │ (Policy + Data)   │
    └───────────────────┘
```

**Benefits:**
- Combines unstructured knowledge with structured data
- Single coherent response
- Reduces user query count
- More complete answers

### 🌐 6. Web Search Fallback

Fetch current external information when needed.

**Used For:**
- Current events & news
- Real-time data (weather, exchange rates)
- External reference information
- Fallback when RAG has no relevant context

**Example Queries:**
- "Who is the current PM of India?"
- "What is latest AI news?"
- "Current USD to INR rate?"

### 💬 7. Conversation Memory

Maintain context across multiple turns for natural conversation flow.

**Example Conversation:**
```
User:  "Who are the top 3 salespeople?"
AI:    "Returns: Alice ($500K), Bob ($450K), Carol ($400K)"

User:  "What are their salaries?"
AI:    [Uses previous context, identifies 'their' = top 3 salespeople]
       "Returns their individual salaries from database"

User:  "What department are they in?"
AI:    [Maintains full conversation context]
       "Returns department info from database"
```

**Memory Features:**
- ✅ Context window management
- ✅ Follow-up question resolution
- ✅ Pronoun disambiguation
- ✅ Multi-turn understanding

### 📄 8. Document Management

Complete document lifecycle with status tracking.

**Operations:**
- ✅ **Upload** — Add new documents to knowledge base
- ✅ **Index** — Automatic chunking & embedding
- ✅ **Search** — Semantic similarity search
- ✅ **Re-upload** — Replace old document versions
- ✅ **Delete** — Remove with vector cleanup
- ✅ **Status Check** — View indexing status & chunk count

**Document Status Values:**
| Status | Meaning |
|--------|---------|
| `pending` | Upload received, waiting to index |
| `indexing` | Currently being processed |
| `indexed` | Ready for queries |
| `error` | Failed indexing, check logs |

### 🎯 9. Relevance Filtering

Never blindly trust retrieval results. Configurable threshold prevents weak context.

**Relevance Checking:**
```
Query Input
    ↓
Vector Similarity Search
    ↓
Retrieved Chunks Scored
    ↓
┌───────────────────────┐
│ Relevance Threshold?  │
└───────────┬───────────┘
    ┌───────┴────────┐
    ▼                ▼
  PASS            FAIL
    │                │
Use RAG        Fallback to
Context        Web Search
```

**Configuration in `.env`:**
```
RELEVANCE_THRESHOLD=0.7
```

### 🧩 10. LangGraph Workflow Orchestration

Sophisticated state machine for complex multi-source queries.

**Workflow Diagram:**
```
                      START
                        │
                  Classify Query
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
      RAG            Database              Web
       │                 │                 │
  Retrieve           MCP Agent         Web Search
       │                 │                 │
Relevance Grade    Database Tool          │
       └────────────┬────┴────────────────┘
                    ▼
            Response Synthesis
            (Combine Results)
                    ▼
              Final Answer
                    │
                    ▼
            Stream to User
```

**Hybrid Query Processing:**
```
Input: RAG + Database Question
  │
  ├─→ [Parallel] RAG Retrieval
  │   │→ Vector Search
  │   └→ Relevance Filter
  │
  ├─→ [Parallel] MCP Database
  │   │→ Tool Selection
  │   └→ Database Query
  │
  └─→ [Merge] Response Synthesis
      │→ Combine contexts
      └→ LLM generates unified answer
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────┐
│          User Interface (Browser)       │
│        (HTML/CSS/JavaScript)            │
└──────────────────┬──────────────────────┘
                   │ HTTP/WebSocket
         ┌─────────▼──────────┐
         │  FastAPI Backend   │
         │  (Uvicorn Server)  │
         └─────────┬──────────┘
                   │
         ┌─────────▼────────────────────┐
         │   LangGraph Router (Agent)   │
         │   • Query Classification     │
         │   • Tool Selection           │
         │   • Response Synthesis       │
         └─┬────────────────────┬───────┘
           │                    │
    ┌──────▼─────┐      ┌──────▼──────┐
    │   RAG      │      │  MCP/DB     │
    │  Pipeline  │      │  Agent      │
    │            │      │             │
    │ ChromaDB ◄─┼─────►│ MCP Server  │
    │ (Vectors)  │      │ SQLite DB   │
    └────────────┘      └─────────────┘
           │                    │
           └────────┬───────────┘
                    │
            ┌───────▼─────────┐
            │  Web Search     │
            │  (Fallback)     │
            └─────────────────┘
                    │
            ┌───────▼──────────────┐
            │ Response Synthesis   │
            │ (LLM Combination)    │
            └───────┬──────────────┘
                    │
            ┌───────▼──────────────┐
            │  Final Response      │
            │  (with Sources)      │
            └──────────────────────┘
```

---

## 🧱 Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.9+ | Core application |
| **Backend Framework** | FastAPI | REST APIs & WebSocket |
| **Workflow Orchestration** | LangGraph | Multi-source routing |
| **Vector Database** | ChromaDB | Semantic search |
| **Structured Data** | SQLite | Company database |
| **LLM** | Groq (LLaMA) | Fast inference |
| **Embeddings** | Sentence Transformers | Local embeddings |
| **Protocol** | MCP | Database tool integration |
| **Frontend** | HTML/CSS/JavaScript | User interface |
| **Server** | Uvicorn | ASGI application server |
| **Containerization** | Docker & Docker Compose | Production deployment |
| **API Documentation** | Swagger/OpenAPI | Auto-generated docs |

---

## 📁 Project Structure

```
IntelliDocs_AI_Enterprise_RAG_MCP/
│
├── 📂 app/
│   ├── __init__.py
│   ├── config.py              # Configuration & settings
│   ├── db_tools.py            # Database tool definitions
│   ├── graph.py               # LangGraph workflow
│   ├── ingestion.py           # Document ingestion pipeline
│   ├── main.py                # FastAPI application
│   ├── mcp_agent.py           # MCP agent logic
│   ├── mcp_server.py          # MCP server implementation
│   ├── tools.py               # Tool definitions
│   │
│   ├── 📂 routes/
│   │   ├── documents.py       # Document management endpoints
│   │   └── upload.py          # Upload handling endpoints
│   │
│   ├── 📂 services/
│   │   ├── chunker.py         # Text chunking logic
│   │   ├── document_loader.py # Format-specific loaders
│   │   ├── embedding.py       # Embedding generation
│   │   ├── uploader.py        # File upload service
│   │   └── vector_store.py    # ChromaDB operations
│   │
│   ├── 📂 static/
│   │   ├── index.html         # Main UI
│   │   └── 📂 assets/
│   │       ├── style.css      # Styling
│   │       └── script.js      # Frontend logic
│   │
│   └── 📂 uploads/            # Uploaded documents
│
├── 📂 data/
│   └── company_policy.txt     # Sample company docs
│
├── 📂 tests/
│   └── test_basic.py          # Unit tests
│
├── 📂 Assets/
│   ├── test_1.png
│   └── test_2.png
│
├── 📂 docs/
│   ├── API.md                 # API documentation
│   ├── ARCHITECTURE.md        # Detailed architecture
│   └── TROUBLESHOOTING.md     # Common issues
│
├── setup_db.py                # Database initialization
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker image
├── docker-compose.yml         # Docker Compose config
├── README.md                  # This file
└── LICENSE                    # MIT License
```

---

## 🛠️ Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

**Required Variables:**
```env
# LLM Configuration
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=mixtral-8x7b-32768

# Database Configuration
DATABASE_PATH=./company.db
CHROMA_DB_PATH=./chroma_db

# Server Configuration
API_PORT=8000
API_HOST=0.0.0.0

# RAG Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
RELEVANCE_THRESHOLD=0.7

# MCP Configuration
MCP_ENABLED=true
MCP_PORT=5678
```

**⚠️ Security:** Never commit `.env` to version control!

---

## 📊 Usage Examples

### Example 1: RAG Query
```
User: "What is the pricing of the AI course?"

System Flow:
1. Classify as RAG query
2. Search documents
3. Find relevant sections
4. Generate answer with sources

Response: "The AI course costs $299..."
```

### Example 2: Database Query
```
User: "Who is the top salesperson this quarter?"

System Flow:
1. Classify as Database query
2. Select MCP tool: get_sales_performance
3. Execute database query
4. Synthesize response

Response: "Alice Johnson leads with $500K revenue..."
```

### Example 3: Hybrid Query
```
User: "What is our sales incentive policy and who qualifies?"

System Flow:
1. Classify as Hybrid (RAG + Database)
2. [Parallel] RAG retrieval → Policy documents
3. [Parallel] MCP query → Top performers
4. Synthesize both contexts
5. Generate unified answer

Response: "Our policy offers 5-15% bonus... Top qualifiers: Alice ($500K), Bob ($450K)..."
```

### Example 4: Web Fallback
```
User: "What is the current USD to INR exchange rate?"

System Flow:
1. Not found in documents or database
2. Trigger web search
3. Fetch current rate
4. Return real-time data

Response: "1 USD = 83.45 INR (as of today)"
```

---

## 🔐 Security Best Practices

### Never Commit to Git

```gitignore
.env                    # API keys & secrets
venv/                   # Virtual environment
chroma_db/              # Vector database
company.db              # Company data
__pycache__/            # Python cache
.pytest_cache/          # Test cache
.vscode/                # IDE settings
*.pyc                   # Compiled Python
.DS_Store               # macOS files
```

### Secrets Management

✅ **Do:**
- Store API keys in `.env` locally
- Use environment variables in production
- Rotate keys regularly
- Use separate keys for dev/prod

❌ **Don't:**
- Commit `.env` to Git
- Hardcode API keys
- Share API keys in chat/email
- Use same key for multiple environments

### If Secret is Accidentally Committed

```bash
# 1. Revoke the compromised key immediately
# 2. Create a new key
# 3. Remove from Git history
git rm --cached .env
git commit --amend --no-edit
git push
```

---

## 🚀 Deployment

### Docker Deployment (Recommended)

```bash
# Build and run with Docker Compose
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Manual Deployment

```bash
# Production setup
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --workers 4

# With logging
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --workers 4 --log-level info
```

### Cloud Deployment (Coming Soon)
- AWS EC2/ECS
- Google Cloud Run
- Azure Container Instances
- Heroku

---

## 🧪 Testing

### Run Unit Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run specific test
pytest tests/test_basic.py

# With coverage
pytest --cov=app tests/
```

### Manual Testing Checklist

- [ ] Document upload
- [ ] Document search
- [ ] Database queries
- [ ] Web search fallback
- [ ] Hybrid queries
- [ ] Conversation memory
- [ ] Error handling

---

## 🐛 Troubleshooting

### Issue: Module Import Error

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt  # Reinstall dependencies
python -m uvicorn app.main:app --reload --port 8002  # Run with correct import path
```

---

### Issue: GROQ API Key Error

**Error:** `GROQ_API_KEY not found or invalid`

**Solution:**
```bash
# Check .env file exists
cat .env

# Update .env with correct key
GROQ_API_KEY=sk_xxxxxxxxxxxxxxxxxxxx

# Restart application
```

---

### Issue: Document Not Searchable

**Error:** Document uploaded but not returning in searches

**Solution:**
```bash
# Check document status
curl http://localhost:8000/api/documents/status

# If status is "error", check logs:
# Look for chunking or embedding errors

# Re-upload document
# Or recreate ChromaDB:
rm -rf chroma_db/
# Restart application
```

---

### Issue: Port Already in Use

**Error:** `Address already in use: ('127.0.0.1', 8002)`

**Solution:**
```bash
# Option 1: Use different port
python -m uvicorn app.main:app --port 8003

# Option 2: Kill process using port (Linux/macOS)
lsof -ti:8002 | xargs kill -9

# Option 3: Find and kill process (Windows)
netstat -ano | findstr :8002
taskkill /PID <PID> /F
```

---

### Issue: Upload Files Interfering with Auto-Reload

**Error:** File size mismatch or incomplete uploads during `--reload`

**Solution:**
```bash
# Don't use --reload when testing uploads
python -m uvicorn app.main:app --port 8002

# Or use production mode:
python -m uvicorn app.main:app --port 8002 --workers 4
```

---

### More Detailed Troubleshooting

See [**TROUBLESHOOTING.md**](docs/TROUBLESHOOTING.md) for:
- Server setup issues
- Database connectivity problems
- Vector store initialization
- Performance optimization
- Advanced debugging

---

## 🩺 Diagnostics & Monitoring

### Health Check Endpoint

```bash
curl http://localhost:8002/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "api": "✓ Running",
    "database": "✓ Connected",
    "vector_store": "✓ Initialized",
    "mcp_server": "✓ Running"
  }
}
```

### Document Diagnostics

```bash
# Get all documents status
curl http://localhost:8002/api/documents/status

# Get specific document details
curl http://localhost:8002/api/documents/<doc_id>
```

### Logs

```bash
# View application logs
tail -f app.log

# Check for errors
grep "ERROR" app.log

# Monitor MCP server
grep "MCP" app.log
```

---

## 🛠️ Development Guide

### Setting Up Development Environment

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run with debug mode
export PYTHONUNBUFFERED=1
python -m uvicorn app.main:app --reload --port 8002 --log-level debug

# Format code
black app/

# Lint
flake8 app/

# Type check
mypy app/
```

### API Documentation

Auto-generated documentation available at:
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

---

## 🧩 MCP Tools Reference

### Tool: `get_department_stats`

**Description:** Get department statistics and metrics

**Query Examples:**
- "Give me statistics for the Engineering department"
- "How many employees in Sales?"
- "Department performance metrics"

---

### Tool: `query_employees`

**Description:** Search and filter employees

**Query Examples:**
- "List all employees in Marketing"
- "Who earns above $100K?"
- "Show me employees hired in 2023"

---

### Tool: `get_top_products`

**Description:** Ranking products by revenue

**Query Examples:**
- "What are our top 5 products by revenue?"
- "Which product has highest revenue?"

---

### Tool: `get_sales_performance`

**Description:** Sales team performance data

**Query Examples:**
- "Who is the top salesperson?"
- "Sales rankings this quarter"
- "Revenue by salesperson"

---

### Tool: `get_company_overview`

**Description:** Company-wide metrics

**Query Examples:**
- "Company overview"
- "Total revenue and employees"
- "Company statistics"

---

### Tool: `run_custom_query`

**Description:** Safe SELECT queries (restricted)

**Allowed Operations:**
- ✅ SELECT statements
- ✅ WHERE clauses
- ✅ JOIN operations
- ❌ INSERT, UPDATE, DELETE
- ❌ DROP, ALTER

---

## 🎯 Performance Optimization

### Query Optimization

```
Time Complexity:
- Vector Search: O(n) → ~100ms for 1M vectors
- Database Query: O(log n) → ~10ms with indexes
- LLM Inference: ~2-3 seconds
- Total Response: ~3-4 seconds
```

### Caching Strategy

- Recently retrieved documents cached in memory
- Embedding results cached in ChromaDB
- MCP tool results cached for 5 minutes

### Scaling Recommendations

- **Small deployments:** Single FastAPI instance
- **Medium deployments:** Load balancer + 2-3 instances
- **Large deployments:** Kubernetes + autoscaling + CDN

---

## 🔮 Future Improvements

- 🔐 User authentication & authorization
- 👥 Multi-user workspaces with role-based access
- 🏢 Organization-level management
- ☁️ Cloud deployment templates
- 🗄️ PostgreSQL & MongoDB support
- 📦 Vector DB options (Pinecone, Weaviate, Milvus)
- ⚡ Streaming responses with Server-Sent Events
- 📊 Advanced analytics & observability
- 🔎 Enhanced citation & source tracking
- 🔑 Enterprise SSO (SAML, OAuth2)
- 🤖 Multi-agent collaboration
- 📈 Production monitoring & alerting
- 🧪 Comprehensive test coverage
- 🌍 Distributed deployment architecture
- 🎨 Advanced UI customization

---

## 🎓 What This Project Demonstrates

This is a **production-grade implementation** of modern AI systems covering:

| Area | Technologies |
|------|--------------|
| **LLM Applications** | Groq, Claude integration |
| **RAG Systems** | ChromaDB, Sentence Transformers |
| **Vector Databases** | Semantic search, embeddings |
| **Agentic Workflows** | Tool calling, agent patterns |
| **Orchestration** | LangGraph state machine |
| **Protocols** | Model Context Protocol (MCP) |
| **Database Integration** | SQLite, custom SQL tools |
| **Web Integration** | Web search APIs |
| **Backend Development** | FastAPI, REST APIs |
| **Document Processing** | PDF/DOCX/TXT parsing |
| **DevOps** | Docker, Docker Compose |
| **Testing** | pytest, integration tests |

---

## 👩‍💻 Author & Maintainer

**Rupali Chouksey**
- 🎯 AI Engineer
- 💼 Enterprise AI Systems
- 🔗 [GitHub](https://github.com/rupali-chouksey)
- 📧 Contact: rupalichauksey@gmail.com

---


## 📄 Final Note

IntelliDocs AI brings together the best of modern AI technologies to create a practical, production-ready system for enterprise knowledge management.

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


