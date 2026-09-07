# Troubleshooting

### Server import error
Use the project venv:
`venv\\Scripts\\activate`
then:
`python -m uvicorn app.main:app --port 8002`

### GROQ key error
Edit `.env` and set `GROQ_API_KEY=your_new_key`.
Restart the server.

### Product PDF is visible but not searchable
Check `/documents`: its status should be `Indexed` and chunks should be > 0. If needed, call POST `/ingest` or restart the server.

### Port already in use
Use another port, e.g.:
`python -m uvicorn app.main:app --port 8003`
Then open that port in the browser.

### Do not use --reload while testing uploads
The upload directory is inside `app/`, so reload mode can restart the server while a file is being written.
