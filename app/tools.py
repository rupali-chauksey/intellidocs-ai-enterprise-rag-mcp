from ddgs import DDGS
from app.config import settings
from app.ingestion import get_vectorstore


def retrieve_from_knowledge_base(query: str, k: int | None = None):
    k = k or settings.top_k
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_relevance_scores(query, k=k)
    items = []
    for doc, score in results:
        try:
            score = float(score)
        except Exception:
            score = 0.0
        items.append({
            "text": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "score": score,
        })
    return items


def web_search(query: str, max_results: int | None = None):
    max_results = max_results or settings.web_max_results
    with DDGS() as ddgs:
        hits = list(ddgs.text(query, max_results=max_results))
    return [
        {"text": h.get("body", ""), "source": h.get("href", ""), "score": None}
        for h in hits
    ]
