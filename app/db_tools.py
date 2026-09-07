import sqlite3
from pathlib import Path
from app.config import DB_PATH


def _connect():
    return sqlite3.connect(DB_PATH)


def get_department_stats():
    with _connect() as conn:
        rows = conn.execute("""
            SELECT department, COUNT(*), AVG(salary), MIN(salary), MAX(salary)
            FROM employees GROUP BY department ORDER BY AVG(salary) DESC
        """).fetchall()
    return "\n".join(
        ["Department Statistics:"] + [
            f"{r[0]}: {r[1]} employees | Avg Rs {int(r[2]):,} | Min Rs {r[3]:,} | Max Rs {r[4]:,}"
            for r in rows
        ]
    )


def query_employees(department: str | None = None, city: str | None = None):
    sql = "SELECT name, department, salary, city FROM employees WHERE 1=1"
    params = []
    if department:
        sql += " AND LOWER(department)=LOWER(?)"
        params.append(department)
    if city:
        sql += " AND LOWER(city)=LOWER(?)"
        params.append(city)
    sql += " ORDER BY name"
    with _connect() as conn:
        rows = conn.execute(sql, params).fetchall()
    if not rows:
        return "No employees found matching the criteria."
    return "\n".join(f"{r[0]} | {r[1]} | Rs {r[2]:,} | {r[3]}" for r in rows)


def get_top_products(limit: int = 5):
    limit = max(1, min(int(limit), 20))
    with _connect() as conn:
        rows = conn.execute("""
            SELECT p.name, p.category, SUM(s.quantity), SUM(s.total_amount)
            FROM sales s JOIN products p ON s.product_id=p.id
            GROUP BY p.id ORDER BY SUM(s.total_amount) DESC LIMIT ?
        """, (limit,)).fetchall()
    lines = [f"Top {limit} Products by Revenue:"]
    for i, r in enumerate(rows, 1):
        lines.append(f"{i}. {r[0]} ({r[1]}) | Units sold: {r[2]} | Revenue: Rs {int(r[3]):,}")
    return "\n".join(lines)


def get_sales_performance():
    with _connect() as conn:
        rows = conn.execute("""
            SELECT e.name, e.department, COUNT(s.id), SUM(s.total_amount)
            FROM sales s JOIN employees e ON s.employee_id=e.id
            GROUP BY e.id ORDER BY SUM(s.total_amount) DESC
        """).fetchall()
    return "\n".join(
        ["Sales Performance by Employee:"] + [
            f"{r[0]} ({r[1]}) | Transactions: {r[2]} | Revenue: Rs {int(r[3]):,}"
            for r in rows
        ]
    )


def get_company_overview():
    with _connect() as conn:
        emp = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
        prod = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        sales, revenue = conn.execute("SELECT COUNT(*), SUM(total_amount) FROM sales").fetchone()
    return f"TechVision India Company Overview:\nTotal employees: {emp}\nTotal products: {prod}\nTotal sales transactions: {sales}\nTotal revenue generated: Rs {int(revenue or 0):,}"


def run_custom_query(sql: str):
    cleaned = sql.strip().rstrip(";")
    upper = cleaned.upper()
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "ATTACH", "DETACH", "PRAGMA", "REPLACE", "CREATE"]
    if not upper.startswith("SELECT") or any(word in upper for word in forbidden):
        return "Error: Only read-only SELECT queries are allowed."
    try:
        with _connect() as conn:
            conn.execute("PRAGMA query_only = ON")
            cursor = conn.execute(cleaned)
            rows = cursor.fetchall()
            cols = [d[0] for d in cursor.description or []]
        if not rows:
            return "Query returned no results."
        lines = [" | ".join(cols), "-" * 60]
        lines += [" | ".join(str(v) for v in row) for row in rows]
        return "\n".join(lines)
    except Exception as exc:
        return f"Query error: {exc}"
