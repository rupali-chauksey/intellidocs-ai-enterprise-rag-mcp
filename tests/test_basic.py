from pathlib import Path

def test_project_files_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "app" / "main.py").exists()
    assert (root / "app" / "mcp_server.py").exists()
    assert (root / "company.db").exists()
