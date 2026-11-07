import requests
from .config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL, OLLAMA_EMBED_MODEL

class OllamaError(RuntimeError):
    pass

def ollama_available():
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=4)
        return r.ok
    except requests.RequestException:
        return False

def chat(prompt, system=None, temperature=0.2):
    payload = {
        "model": OLLAMA_CHAT_MODEL,
        "messages": ([{"role": "system", "content": system}] if system else []) +
                    [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": temperature}
    }
    try:
        r = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=180)
        r.raise_for_status()
        return r.json()["message"]["content"]
    except requests.RequestException as e:
        raise OllamaError(
            f"Could not call Ollama at {OLLAMA_BASE_URL}. "
            f"Start Ollama and pull {OLLAMA_CHAT_MODEL}. Details: {e}"
        ) from e

def embed(texts):
    """Use Ollama's local embedding endpoint; returns one vector per input string."""
    payload = {"model": OLLAMA_EMBED_MODEL, "input": texts}
    try:
        r = requests.post(f"{OLLAMA_BASE_URL}/api/embed", json=payload, timeout=180)
        r.raise_for_status()
        vectors = r.json().get("embeddings", [])
        if len(vectors) != len(texts):
            raise OllamaError("Ollama returned an unexpected number of embeddings.")
        return vectors
    except requests.RequestException as e:
        raise OllamaError(
            f"Could not create embeddings. Ensure Ollama is running and "
            f"`ollama pull {OLLAMA_EMBED_MODEL}` has completed. Details: {e}"
        ) from e
