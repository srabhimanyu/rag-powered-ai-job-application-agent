from pathlib import Path
import json
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

APP_NAME = os.getenv("APP_NAME", "RAG-Powered AI Job Application Agent")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.2:3b")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
CHROMA_PATH = Path(os.getenv("CHROMA_PATH", str(ROOT / "chroma_db")))
MIN_MATCH_SCORE = int(os.getenv("MIN_MATCH_SCORE", "50"))
REQUIRE_APPROVAL = os.getenv("REQUIRE_APPROVAL", "true").lower() == "true"
DB_PATH = ROOT / "data" / "jobs.db"
PROFILE_PATH = ROOT / "config" / "profile.json"

def load_profile():
    with PROFILE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
