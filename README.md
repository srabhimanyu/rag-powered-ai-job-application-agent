# RAG + LLM AI Job Application Agent (Local-first)

A local-first starter project for a Senior Java Developer job search in India. It combines:
- **RAG:** chunks resume text, creates embeddings with Ollama, stores vectors in ChromaDB, and retrieves relevant resume evidence for a vacancy.
- **LLM:** uses a locally running Ollama chat model to analyse job fit and draft cover letters grounded in retrieved resume content.
- **Workflow:** Python CLI, SQLite tracking, Streamlit dashboard, and human approval before application preparation.

No paid API key is required when using local Ollama models. You need enough disk space/RAM for the models.

## What is included / not included
Included: local RAG pipeline, LLM analysis, Chroma vector store, PDF text extraction, job-fit analysis, cover-letter drafting, approval tracking, dashboard and Naukri/LinkedIn search links.

Not included: unrestricted Naukri/LinkedIn scraping, CAPTCHA bypass, automatic portal login, or application submission. Their platform access rules and protections must be respected. The sample jobs are fake demo records, not live vacancies. The scoring and LLM analysis are decision-support only, not guarantees.

## 1. Install Python
Use Python 3.10+ (3.11 recommended).

## 2. Install Ollama
Download and install Ollama from https://ollama.com/download .
Start Ollama, then pull these models in a terminal:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

The first model is the local chat LLM; the second creates embedding vectors for RAG. Model names can be changed in `.env`.

Check Ollama:
```bash
ollama list
```

## 3. Set up this project

### Windows PowerShell
```powershell
cd ai_job_application_agent_rag
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS / Linux
```bash
cd ai_job_application_agent_rag
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `config/profile.json` with your accurate experience, skills and contact details. Do not list skills you cannot substantiate.

## 4. Index your resume (RAG ingestion)
Put your PDF resume somewhere on your computer, then run:

```bash
python main.py init
python main.py index-resume "/path/to/your_resume.pdf"
```

Windows example:
```powershell
python main.py index-resume "C:\Users\YourName\Documents\resume.pdf"
```

The program extracts text, splits it into overlapping chunks, creates embeddings with Ollama, and stores them in the local Chroma database. The source PDF is not uploaded to a cloud API.

Scanned image-only PDFs need OCR; this version supports selectable text PDFs.

## 5. Run RAG + LLM job analysis
```bash
python main.py discover
```

This loads sample jobs, retrieves relevant resume chunks for each vacancy, sends only the relevant evidence plus the job details to the local LLM, and stores the analysis and score in SQLite.

The first run can take longer while the model loads. Sample jobs are not live vacancies.

## 6. Open the dashboard
```bash
streamlit run dashboard.py
```
Open the local URL shown in the terminal, normally http://localhost:8501.

Tabs:
- Discover & match: run LLM analysis and inspect retrieved resume evidence.
- Resume RAG: upload and index your PDF.
- Application tracker: approve preparation, skip, and draft a cover letter.

## 7. Other CLI commands
```bash
python main.py links
python main.py list
python main.py review
python main.py history
python main.py cover-letter DEMO001
```

## 8. Add real job descriptions
For this starter, add a job object to `data/sample_jobs.json` using the same fields as the examples. Give it a unique ID, accurate description, source and legitimate public job URL. Then run `python main.py discover` again. For production, add permitted job-board APIs or user-authorized imports.

## 9. How RAG works in this project
1. **Ingestion:** PDF text is extracted.
2. **Chunking:** text is split into overlapping pieces.
3. **Embedding:** `nomic-embed-text` converts chunks into vectors.
4. **Indexing:** ChromaDB persists vectors and metadata locally.
5. **Retrieval:** the job's title, requirements and description become a query; top relevant resume chunks are retrieved.
6. **Generation:** `llama3.2:3b` receives the job plus retrieved evidence and returns a structured analysis.
7. **Grounding:** prompt instructs the model not to invent experience. Always verify outputs; LLMs can still make mistakes.

## 10. Troubleshooting
- **Connection refused / Ollama unavailable:** open Ollama or run `ollama serve` in a separate terminal.
- **Model not found:** run `ollama pull llama3.2:3b` and `ollama pull nomic-embed-text`.
- **Slow responses / out of memory:** use a smaller supported chat model and update `OLLAMA_CHAT_MODEL` in `.env`; close memory-heavy applications.
- **No text from resume:** it may be scanned; OCR support is a future enhancement.
- **Windows PowerShell activation blocked:** run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` if allowed by your device policy, or use Command Prompt and `venv\\Scripts\\activate.bat`.

## Privacy
The LLM and embedding calls go to your local Ollama server. Keep `.env`, your resume, profile and local database private. Do not publish them in a public repository. This app never asks for Naukri or LinkedIn passwords.
