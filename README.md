# 🤖 RAG-Powered AI Job Application Agent

An AI-powered job application assistant built using **Python, Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), ChromaDB and Ollama**.

The system analyses candidate resumes against job descriptions, retrieves relevant professional experience using semantic search, evaluates job compatibility using an LLM, and assists in preparing personalized job applications.

The project currently targets **Senior Java Developer opportunities across India**, with a human-in-the-loop approval workflow.

---

## 🚀 Project Overview

Finding relevant job opportunities and applying to them consistently can be time-consuming.

This project aims to simplify the job search process using Generative AI and intelligent retrieval techniques.

The AI agent combines resume intelligence, semantic search and LLM-based reasoning to:

- Analyse candidate resumes.
- Extract relevant skills and professional experience.
- Retrieve relevant resume information using RAG.
- Analyse job descriptions using an LLM.
- Evaluate candidate-job compatibility.
- Identify matching and missing skills.
- Generate personalized cover letters.
- Maintain an application approval and tracking workflow.

**Important:** The current version uses sample job listings and manually accessible job descriptions. Naukri and LinkedIn automated discovery and application submission are not implemented.

## 🏗️ System Architecture

```text
              Candidate Resume (PDF)
                       |
                       v
                Resume Parser
                       |
                       v
                 Text Chunking
                       |
                       v
             Embedding Generation
               (Nomic Embeddings)
                       |
                       v
                ChromaDB
              (Vector Database)
                       |
                       |
Job Description ------+
                       |
                       v
                RAG Retrieval
                       |
                       v
             Relevant Resume Context
                       |
                       v
              Local LLM (Ollama)
                 Llama 3.2
                       |
                       v
             Job Compatibility Analysis
                       |
              +--------+--------+
              |                 |
              v                 v
         Skill Matching    Skill Gap Analysis
              |                 |
              +--------+--------+
                       |
                       v
             Application Preparation
                       |
                       v
               Human Approval
                       |
                       v
             Application Tracking
```

## 🧠 RAG Implementation

The project implements a Retrieval-Augmented Generation pipeline to provide context-aware job matching.

### RAG Workflow

**1. Document Ingestion**

The candidate uploads a PDF resume.

**2. Text Extraction**

PDF content is extracted using PyPDF.

**3. Text Chunking**

The extracted content is divided into smaller overlapping chunks to improve retrieval relevance.

**4. Embedding Generation**

The Nomic embedding model converts text chunks into numerical vector representations.

**5. Vector Storage**

Embeddings and associated metadata are stored in ChromaDB.

**6. Semantic Retrieval**

When a job description is analysed, the retrieval engine searches for relevant resume chunks.

**7. Context Augmentation**

The retrieved resume information is combined with the job description and candidate profile.

**8. LLM Generation**

Llama 3.2 analyses the supplied context and generates a structured job compatibility report.

### RAG Technologies

- ChromaDB
- Nomic Embed Text
- Ollama
- Python

## 🤖 LLM Integration

The project uses locally hosted LLMs through Ollama.

| Model | Purpose |
|---|---|
| Llama 3.2 (3B) | Job analysis and cover-letter generation |
| Nomic Embed Text | Text embeddings and semantic retrieval |

The LLM evaluates:

- Relevant technical skills.
- Professional experience.
- Job requirements.
- Missing or unproven skills.
- Candidate-job compatibility.
- Application recommendations.

The system instructs the LLM to use retrieved resume evidence and avoid inventing candidate experience.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Generative AI | Llama 3.2 |
| LLM Runtime | Ollama |
| RAG Framework | Custom Python RAG pipeline |
| Embedding Model | Nomic Embed Text |
| Vector Database | ChromaDB |
| PDF Processing | PyPDF |
| Database | SQLite |
| Frontend | Streamlit |
| Data Validation | Pydantic |
| Environment Configuration | Python-dotenv |
| API Communication | Python Requests |

## ✨ Key Features

### 1. Resume Intelligence
- Upload PDF resumes.
- Extract resume text.
- Split documents into chunks.
- Generate embeddings.
- Store resume information in ChromaDB.

### 2. Semantic Job Matching
- Retrieve relevant resume sections.
- Analyse job descriptions.
- Identify matching technical skills.
- Identify missing or unproven skills.
- Generate compatibility scores.

### 3. LLM-Based Analysis
- Context-aware job analysis.
- Experience suitability assessment.
- Skill gap identification.
- Application recommendations.

### 4. Cover Letter Generation
- Generate personalized cover-letter drafts.
- Use retrieved resume evidence.
- Tailor content to job requirements.
- Avoid unsupported professional claims.

### 5. Human-in-the-Loop Workflow
- Review job opportunities.
- Approve application preparation.
- Skip irrelevant opportunities.
- Maintain application approval history.

### 6. Interactive Dashboard
- Resume indexing.
- Job matching.
- RAG analysis.
- Application tracking.
- AI model connection status.

## 📁 Project Structure

```text
ai_job_application_agent_rag/
│
├── config/
│   └── profile.json
│
├── data/
│   └── sample_jobs.json
│
├── job_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── database.py
│   ├── llm.py
│   ├── matching.py
│   ├── models.py
│   ├── rag.py
│   ├── resume.py
│   └── sources.py
│
├── output/
│
├── chroma_db/
│
├── .env.example
├── .gitignore
├── dashboard.py
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10+
- VS Code
- Ollama
- Git

### Step 1: Clone Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai_job_application_agent_rag
```

### Step 2: Create Virtual Environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv v
