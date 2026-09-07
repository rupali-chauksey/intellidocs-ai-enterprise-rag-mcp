from mcp.server import MCPServer

from app.db_tools import (
    get_department_stats,
    query_employees,
    get_top_products,
    get_sales_performance,
    get_company_overview,
    run_custom_query,
)


mcp = MCPServer("intellidocs-company-db")


mcp.tool()(get_department_stats)
mcp.tool()(query_employees)
mcp.tool()(get_top_products)
mcp.tool()(get_sales_performance)
mcp.tool()(get_company_overview)
mcp.tool()(run_custom_query)


if __name__ == "__main__":
    mcp.run()