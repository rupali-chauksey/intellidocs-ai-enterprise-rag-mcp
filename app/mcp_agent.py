import asyncio
import os
import sys
from pathlib import Path
import traceback


from langchain_groq import ChatGroq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from app.config import settings


SERVER = StdioServerParameters(
    command=sys.executable,
    args=["-m", "app.mcp_server"],
    cwd=str(Path(__file__).resolve().parent.parent),
)


def _llm():
    if not settings.groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to .env"
        )

    return ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=0.1,
        max_tokens=700,
    )


def _safe_tool_choice(text: str, names: list[str]) -> str:
    token = (
        text.strip().split()[0].strip("`'\".,")
        if text.strip()
        else ""
    )

    return token if token in names else "run_custom_query"


async def answer_from_database_async(
    question: str,
    history: list[dict] | None = None
):
    try:
        async with stdio_client(SERVER) as (read, write):

            async with ClientSession(read, write) as session:

                # -----------------------------
                # MCP INITIALIZE
                # -----------------------------
                await session.initialize()

                # -----------------------------
                # GET MCP TOOLS
                # -----------------------------
                tools = await session.list_tools()

                names = [
                    t.name
                    for t in tools.tools
                ]

                descriptions = "\n".join(
                    f"- {t.name}: {t.description}"
                    for t in tools.tools
                )

                history_text = "\n".join(
                    f"{m['role']}: {m['content']}"
                    for m in (history or [])[-6:]
                )

                # -----------------------------
                # TOOL ROUTER
                # -----------------------------
                router_prompt = f"""
Choose exactly one database tool
for this question.

TOOLS:
{descriptions}

CONVERSATION:
{history_text}

QUESTION:
{question}

Reply with only the tool name.
If no fixed tool fits,
use run_custom_query.
"""

                choice = _safe_tool_choice(
                    _llm().invoke(router_prompt).content,
                    names
                )

                print(f"[MCP] Tool selected: {choice}")

                # -----------------------------
                # TOOL ARGUMENTS
                # -----------------------------
                args = {}

                if choice == "query_employees":

                    filter_prompt = f"""
Return JSON only with optional
department and city keys for this question:

{question}
"""

                    raw = (
                        _llm()
                        .invoke(filter_prompt)
                        .content
                        .strip()
                        .replace("```json", "")
                        .replace("```", "")
                    )

                    try:
                        import json

                        obj = json.loads(raw)

                        args = {
                            k: v
                            for k, v in obj.items()
                            if k in {
                                "department",
                                "city"
                            }
                            and v
                        }

                    except Exception as e:
                        print(
                            f"[MCP] Filter parsing error: {e}"
                        )
                        args = {}

                elif choice == "get_top_products":

                    args = {
                        "limit": 5
                    }

                elif choice == "run_custom_query":

                    schema = (
                        "employees("
                        "id,name,department,salary,city"
                        "), "
                        "products("
                        "id,name,category,price,stock"
                        "), "
                        "sales("
                        "id,product_id,employee_id,"
                        "quantity,sale_date,total_amount"
                        ")"
                    )

                    sql_prompt = f"""
Write one read-only SQLite SELECT query
for this question.

Tables:
{schema}

Return ONLY SQL.

Question:
{question}
"""

                    sql = (
                        _llm()
                        .invoke(sql_prompt)
                        .content
                        .strip()
                        .replace("```sql", "")
                        .replace("```", "")
                        .strip()
                    )

                    args = {
                        "sql": sql
                    }

                # -----------------------------
                # MCP TOOL CALL
                # -----------------------------
                try:

                    result = await session.call_tool(
                        choice,
                        args
                    )

                except Exception as e:

                    print(
                        f"[MCP] Tool call error "
                        f"'{choice}': {e}"
                    )

                    traceback.print_exc()

                    return {
                        "answer": (
                            "I encountered an error "
                            "while querying the database."
                        ),
                        "tool_used": choice,
                        "raw_data": str(e),
                        "error": True,
                    }

                # -----------------------------
                # MCP RESULT
                # -----------------------------
                raw_data = (
                    result.content[0].text
                    if result.content
                    else "No database data returned."
                )

                print(
                    f"[MCP] Database result: {raw_data}"
                )

                # -----------------------------
                # FINAL ANSWER
                # -----------------------------
                final_prompt = f"""
Answer the user using ONLY the
database data below.

Be concise and factual.

Question:
{question}

Database data:
{raw_data}

Answer:
"""

                try:

                    answer = (
                        _llm()
                        .invoke(final_prompt)
                        .content
                    )

                except Exception as e:

                    print(
                        f"[MCP] Final answer error: {e}"
                    )

                    traceback.print_exc()

                    answer = (
                        f"Database query returned: "
                        f"{raw_data[:500]}"
                    )

                return {
                    "answer": answer,
                    "tool_used": choice,
                    "raw_data": raw_data,
                    "error": False,
                }

    except Exception as e:

        print(
            f"[MCP] Fatal error connecting "
            f"to database server: {e}"
        )

        traceback.print_exc()

        return {
            "answer": (
                "I'm unable to access the database "
                "right now. Please try again."
            ),
            "tool_used": "mcp_connection_error",
            "raw_data": (
                f"Database connection error: {str(e)}"
            ),
            "error": True,
        }


def ask_database(
    question: str,
    history: list[dict] | None = None
):
    try:

        return asyncio.run(
            answer_from_database_async(
                question,
                history
            )
        )

    except Exception as e:

        print(
            f"[MCP] Asyncio error: {e}"
        )

        traceback.print_exc()

        return {
            "answer": (
                "I'm unable to access the database "
                "right now. Please try again."
            ),
            "tool_used": "asyncio_error",
            "raw_data": (
                f"Asyncio error: {str(e)}"
            ),
            "error": True,
        }