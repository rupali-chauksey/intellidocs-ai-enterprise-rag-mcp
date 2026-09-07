# IntelliDocs AI — Enterprise RAG + MCP Assistant

> An enterprise-grade AI assistant that combines Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP), LangGraph, FastAPI, ChromaDB, SQLite, and Web Search to intelligently answer questions from documents, databases, and the web.

---

## 🚀 Overview

**IntelliDocs AI** is an enterprise-style AI assistant designed to intelligently route user queries to the right knowledge source.

Instead of relying only on an LLM, the system can determine whether a question should be answered using:

- 📚 Enterprise documents through RAG
- 🗄️ Company databases through MCP
- 🌐 Web search for current information
- 🔗 Multiple sources when a query requires both documents and database information

The application uses **LangGraph** for agentic routing and workflow orchestration, **ChromaDB** for vector-based document retrieval, and a real **MCP server** for structured database interaction.

---

## 🎥 Project Demo

### Video Demo

<!-- Add your demo video link here -->

[▶️ Watch IntelliDocs AI Demo](YOUR_VIDEO_LINK_HERE)

---

## 🖼️ Application Screenshots

### Main Dashboard

![IntelliDocs AI Dashboard](screenshots/dashboard.png)

### RAG — Knowledge Base Query

![RAG Query](screenshots/rag-query.png)

### MCP Database Query

![MCP Database Query](screenshots/mcp-query.png)

### Hybrid RAG + MCP Query

![Hybrid Query](screenshots/hybrid-query.png)

> Replace the image paths above with your actual screenshots.

---

# ✨ Key Features

## 📚 1. Enterprise RAG

The system supports document-based question answering using Retrieval-Augmented Generation.

Supported document formats:

- PDF
- TXT
- Markdown
- DOCX

The ingestion pipeline:

1. Upload document
2. Extract document text
3. Split text into chunks
4. Generate embeddings
5. Store vectors in ChromaDB
6. Retrieve relevant chunks for user queries
7. Generate an answer using the LLM

### RAG Capabilities

- Incremental document indexing
- Vector similarity search
- Re-upload replacement
- Document status tracking
- Chunk count tracking
- Document deletion
- Vector deletion
- Relevance threshold filtering
- Web fallback when relevant knowledge is unavailable

---

# 🧠 2. Intelligent Query Routing

IntelliDocs AI does not send every question to the same tool.

The query router determines the appropriate execution path.

### Supported Routes

```text
                    User Query
                         |
                         v
                ┌─────────────────┐
                │  Query Router   │
                └────────┬────────┘
                         |
          ┌──────────────┼──────────────┐
          |              |              |
          v              v              v
        RAG           Database         Web
          |              |              |
          v              v              v
     ChromaDB          MCP          Web Search
          |              |              |
          └──────────────┼──────────────┘
                         |
                         v
                  Final Response
