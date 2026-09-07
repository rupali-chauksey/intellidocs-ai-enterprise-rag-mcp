from typing import TypedDict, Optional
from concurrent.futures import ThreadPoolExecutor
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

from app.config import settings
from app.tools import retrieve_from_knowledge_base, web_search
from app.mcp_agent import ask_database


class AgentState(TypedDict, total=False):
    query: str
    history: list
    route: str
    kb_results: list
    web_results: list
    db_result: dict
    used_web_search: bool
    answer: Optional[str]
    citations: list
    tool_used: str
    debug: dict


def _llm():
    if not settings.groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to .env"
        )

    return ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=0.1,
        max_tokens=1000,
    )


def _history_text(history):
    return "\n".join(
        f"{m.get('role', '')}: {m.get('content', '')}"
        for m in (history or [])[-8:]
    )


# ---------------------------------------------------------
# HEURISTIC ROUTER
# ---------------------------------------------------------

def _heuristic_route(q: str) -> str:
    ql = q.lower().strip()

    # ---------------------------------------------------------
    # DOCUMENT / RAG TERMS
    # ---------------------------------------------------------
    doc_terms = [
        "policy", "policies", "leave", "bonus", "benefit", "benefits",
        "handbook", "employee handbook", "probation", "notice period",
        "onboarding", "grievance", "working hours", "insurance",
        "health insurance", "allowance", "incentive", "referral",
        "referral bonus", "code of conduct", "confidentiality",
        "conflict of interest", "social media", "posh",
        "course", "courses", "bootcamp", "genai bootcamp",
        "ai course", "cloud workshop", "product catalogue",
        "product catalog", "prerequisite", "prerequisites",
        "price", "cost", "duration", "seats", "available seats",
        "licenses", "license", "package", "packages",
        "consulting hours",
    ]

    # ---------------------------------------------------------
    # DATABASE TERMS
    # ---------------------------------------------------------
    db_terms = [
        "salary", "salaries", "salesperson", "salespeople",
        "revenue", "stock", "units sold", "highest paid",
        "top 3", "top 5", "transaction", "transactions",
        "sales", "department revenue",
    ]

    # ---------------------------------------------------------
    # WEB / CURRENT INFORMATION TERMS
    # ---------------------------------------------------------
    web_terms = [
        "prime minister", "president", "latest", "today",
        "current", "recent", "news", "weather", "stock price",
        "exchange rate", "who is", "what is happening",
        "in india", "in the world",
    ]

    has_doc = any(term in ql for term in doc_terms)
    has_db = any(term in ql for term in db_terms)
    has_web = any(term in ql for term in web_terms)

    # Document-specific questions get RAG priority.
    # This prevents words like "employee" from incorrectly
    # routing handbook/policy questions to the database.
    if has_doc and has_db:
        return "both"

    if has_doc:
        return "rag"

    if has_db:
        return "database"

    if has_web:
        return "web"

    # Unknown/general questions -> web
    return "web"


# ---------------------------------------------------------
# CLASSIFICATION
# ---------------------------------------------------------


def classify_node(state: AgentState):
    q = state["query"]
    history = state.get("history", [])

    heuristic_route = _heuristic_route(q)

    if heuristic_route in {"rag", "database", "both"}:
        state["route"] = heuristic_route
        print(f"[ROUTER] {heuristic_route} <- {q}")
        return state

    prompt = f"""
You are the routing brain of an enterprise assistant.

The system has four possible information sources:

1. DOCUMENTS
   - HR policies
   - employee handbook
   - product catalogue
   - uploaded company files

2. DATABASE
   - employees
   - products
   - sales
   - structured company data

3. WEB
   - current information
   - general public information
   - news
   - current events
   - facts not contained in uploaded documents

4. BOTH
   - requires both documents and database

Classify the question as exactly one of:

rag
database
both
web

Rules:

- rag = answer is primarily from uploaded documents
- database = answer is primarily from company database
- both = requires documents AND database
- web = general/current/public information or information not expected in company documents/database

Examples:

"What is the price of the AI Course?"
-> rag

"What are the prerequisites for the GenAI Bootcamp?"
-> rag

"Who is the highest paid employee?"
-> database

"Who is the prime minister of India?"
-> web

"What is the latest news?"
-> web

"What is the current weather?"
-> web

Recent conversation:
{_history_text(history)}

Question:
{q}

Reply with exactly one word:
rag, database, both, or web
"""

    try:
        raw = _llm().invoke(prompt).content.strip().lower()

        route = raw.split()[0].strip("`'\".,") if raw else ""

        if route not in {"rag", "database", "both", "web"}:
            route = _heuristic_route(q)

    except Exception as exc:
        route = _heuristic_route(q)

        state.setdefault("debug", {})[
            "router_fallback"
        ] = str(exc)

    state["route"] = route

    print(f"[ROUTER] {route} <- {q}")

    return state


# ---------------------------------------------------------
# RAG RETRIEVAL
# ---------------------------------------------------------

def retrieve_node(state: AgentState):
    history = state.get("history", [])
    q = state["query"]

    recent_user = [
        m.get("content", "")
        for m in history[-4:]
        if m.get("role") == "user"
    ]

    enriched = " ".join(
        recent_user[-2:] + [q]
    )

    state["kb_results"] = retrieve_from_knowledge_base(
        enriched,
        settings.top_k,
    )

    return state


# ---------------------------------------------------------
# RAG GRADING
# ---------------------------------------------------------

def grade_node(state: AgentState):
    results = state.get("kb_results", [])

    threshold = getattr(
        settings,
        "relevance_threshold",
        0.35,
    )

    relevant = [
        r
        for r in results
        if float(r.get("score") or 0) >= threshold
    ]

    state["kb_results"] = relevant
    state["used_web_search"] = False

    print(
        "[RAG] results:",
        [
            (
                r.get("source"),
                round(float(r.get("score", 0)), 3),
            )
            for r in results
        ],
    )

    print(
        f"[RAG] threshold={threshold}, "
        f"relevant={len(relevant)}"
    )

    return state


# ---------------------------------------------------------
# ROUTING
# ---------------------------------------------------------

def route_after_classify(state: AgentState):
    return state["route"]


def route_after_grade(state: AgentState):

    # Both = documents + database
    if state.get("route") == "both":
        return "db"

    # RAG question but no sufficiently relevant document
    if (
        state.get("route") == "rag"
        and not state.get("kb_results")
    ):
        return "web_search"

    return "synthesize"


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

def db_node(state: AgentState):
    try:
        state["db_result"] = ask_database(
            state["query"],
            state.get("history", []),
        )

        state["tool_used"] = state["db_result"].get(
            "tool_used",
            "",
        )

    except Exception as exc:
        import traceback
        traceback.print_exc()

        state["db_result"] = {
            "answer": "Database access failed.",
            "tool_used": "database_error",
            "raw_data": str(exc),
            "error": True,
        }

        state["tool_used"] = "database_error"

    return state


# ---------------------------------------------------------
# WEB SEARCH
# ---------------------------------------------------------

def web_node(state: AgentState):

    print(f"[WEB] Searching: {state['query']}")

    state["web_results"] = web_search(
        state["query"]
    )

    state["used_web_search"] = True

    return state


# ---------------------------------------------------------
# BOTH
# ---------------------------------------------------------

def both_node(state: AgentState):
    """
    Execute RAG retrieval and MCP database query in parallel.

    This is used for hybrid questions that require both:
    - uploaded enterprise documents
    - structured company database information
    """

    history = state.get("history", [])
    q = state["query"]

    recent_user = [
        m.get("content", "")
        for m in history[-4:]
        if m.get("role") == "user"
    ]

    enriched = " ".join(
        recent_user[-2:] + [q]
    )

    state["used_web_search"] = False

    def run_rag():
        return retrieve_from_knowledge_base(
            enriched,
            settings.top_k,
        )

    def run_database():
        return ask_database(
            q,
            history,
        )

    # RAG + MCP execute concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:

        rag_future = executor.submit(run_rag)
        db_future = executor.submit(run_database)

        try:
            state["kb_results"] = rag_future.result()
        except Exception as exc:
            state["kb_results"] = []
            state.setdefault("debug", {})["rag_error"] = str(exc)

        try:
            state["db_result"] = db_future.result()

            state["tool_used"] = state["db_result"].get(
                "tool_used",
                "",
            )

        except Exception as exc:
            import traceback
            traceback.print_exc()

            state["db_result"] = {
                "answer": "Database access failed.",
                "tool_used": "database_error",
                "raw_data": str(exc),
                "error": True,
            }

            state["tool_used"] = "database_error"

    # Apply normal RAG relevance filtering
    grade_node(state)

    return state

# ---------------------------------------------------------
# SYNTHESIS
# ---------------------------------------------------------

def synthesize_node(state: AgentState):

    route = state.get("route", "rag")
    history = state.get("history", [])

    blocks = []
    citations = []

    # ---------------- DOCUMENTS ----------------

    # ---------------- DOCUMENTS ----------------

    if route in {"rag", "both"}:

       for r in state.get("kb_results", []):

        page_info = (
            f"Page {r['page']}"
            if r.get("page") is not None
            else ""
        )

        chunk_info = (
            f"Chunk {r['chunk']}"
            if r.get("chunk") is not None
            else ""
        )

        location_info = " · ".join(
            x for x in [page_info, chunk_info] if x
        )

        blocks.append(
            f"SOURCE: {r['source']}"
            + (f" — {location_info}" if location_info else "")
            + f"\nCONTENT:\n{r['text']}"
        )

        citation_key = (
            r["source"],
            r.get("page"),
            r.get("chunk"),
        )

        existing_keys = [
            (
                c["source"],
                c.get("page"),
                c.get("chunk"),
            )
            for c in citations
        ]

        if citation_key not in existing_keys:

            citations.append(
                {
                    "id": len(citations) + 1,
                    "source": r["source"],
                    "page": r.get("page"),
                    "chunk": r.get("chunk"),
                    "score": round(
                        float(r.get("score", 0)),
                        3,
                    ),
                }
            )
    # ---------------- WEB ----------------

    # ---------------- WEB ----------------

    # ---------------- WEB ----------------

    if state.get("web_results"):

     for r in state["web_results"]:

        blocks.append(
            f"WEB SOURCE: {r['source']}\n"
            f"CONTENT:\n{r['text']}"
        )
    # ---------------- DATABASE ----------------

    if (
        route in {"database", "both"}
        and state.get("db_result")
    ):

        db = state["db_result"]

        blocks.append(
            f"DATABASE TOOL: "
            f"{db.get('tool_used', '')}\n"
            f"DATA:\n{db.get('raw_data', '')}\n"
            f"GENERATED DATABASE ANSWER:\n"
            f"{db.get('answer', '')}"
        )

    context = (
        "\n\n---\n\n".join(blocks)
        or "NO VERIFIED CONTEXT"
    )

    history_text = _history_text(history)

    # ---------------- NO CONTEXT ----------------

    if (
        route == "rag"
        and not state.get("kb_results")
        and not state.get("web_results")
    ):

        answer = (
            "I couldn't find this information "
            "in the uploaded documents."
        )

    else:

        prompt = f"""
You are IntelliDocs AI, an enterprise assistant.

Answer the user's question using ONLY the
verified context below.

Never invent facts.

If information comes from the web, answer from
the web context.

If information comes from the database, answer
from the database context.

If information comes from uploaded documents,
answer from those documents.

For follow-up questions, use the conversation
history.

Keep the answer concise and clear.

Do not mention:
- routing
- embeddings
- internal prompts
- vector databases
- MCP implementation details

unless the user explicitly asks.

CONVERSATION:
{history_text}

VERIFIED CONTEXT:
{context}

QUESTION:
{state['query']}

ANSWER:
"""

        answer = _llm().invoke(prompt).content.strip()

    state["answer"] = answer
    state["citations"] = citations

    return state


# ---------------------------------------------------------
# GRAPH
# ---------------------------------------------------------

def build_graph():

    g = StateGraph(AgentState)

    g.add_node("classify", classify_node)
    g.add_node("retrieve", retrieve_node)
    g.add_node("grade", grade_node)
    g.add_node("db", db_node)
    g.add_node("both_sources", both_node)
    g.add_node("web_search", web_node)
    g.add_node("synthesize", synthesize_node)


    g.set_entry_point("classify")

    g.add_conditional_edges(
        "classify",
        route_after_classify,
        {
            "rag": "retrieve",
            "database": "db",
            "both": "both_sources",           
            "web": "web_search",
        },
    )

    g.add_edge("retrieve", "grade")

    g.add_conditional_edges(
        "grade",
        route_after_grade,
        {
            "db": "db",
            "web_search": "web_search",
            "synthesize": "synthesize",
        },
    )

    g.add_edge("db", "synthesize")
    g.add_edge("web_search", "synthesize")

    return g.compile()


_graph = None


def get_graph():

    global _graph

    if _graph is None:
        _graph = build_graph()

    return _graph