import json
import re
from dataclasses import dataclass
from pathlib import Path
import requests


# ----------------------------
# Mini-RAG: naive keyword search
# ----------------------------

def load_config(path: str = "config.json") -> dict:
    if not Path(path).exists():
        raise RuntimeError(
            "config.json not found.\n"
            "Create it with api_key, base_url, and model."
        )
    return json.loads(Path(path).read_text())

def _tokenize(text: str) -> set[str]:
    # Lowercase, keep simple words/numbers
    return set(re.findall(r"[a-z0-9']+", text.lower()))

def load_doc_chunks(docs_dir: str = "docs") -> list[dict]:
    """
    Loads .txt files and splits them into small chunks.
    Each chunk is:
      { "source": "filename.txt", "text": "...", "tokens": set(...) }
    """
    chunks = []
    docs_path = Path(docs_dir)
    for file in docs_path.glob("*.txt"):
        raw = file.read_text(encoding="utf-8", errors="ignore")
        # Split by blank lines to get paragraph-ish chunks
        parts = [p.strip() for p in raw.split("\n\n") if p.strip()]
        for p in parts:
            chunks.append({
                "source": file.name,
                "text": p,
                "tokens": _tokenize(p),
            })
    return chunks

def search_docs(query: str, chunks: list[dict], top_k: int = 3) -> str:
    """
    Returns top_k chunks scored by keyword overlap.
    Output is formatted text (so it's easy to show in console).
    """
    q_tokens = _tokenize(query)
    scored = []
    for ch in chunks:
        score = len(q_tokens & ch["tokens"])  # overlap count
        if score > 0:
            scored.append((score, ch))

    scored.sort(key=lambda x: x[0], reverse=True)
    best = scored[:top_k]

    if not best:
        return "NO_RESULTS"

    lines = []
    for score, ch in best:
        lines.append(f"[source={ch['source']} score={score}] {ch['text']}")
    return "\n".join(lines)


# ----------------------------
# LLM Client (OpenAI-compatible)
# ----------------------------

def chat(messages: list[dict], config: dict) -> str:
    api_key = config["api_key"]
    base_url = config.get("base_url", "https://api.openai.com/v1")
    model = config.get("model", "gpt-4o-mini")

    url = base_url.rstrip("/") + "/chat/completions"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


# ----------------------------
# Router Decision Structure
# ----------------------------

@dataclass
class RouterDecision:
    action: str          # "SEARCH_DOCS" or "NO_SEARCH"
    query: str | None    # Search query (if action is SEARCH_DOCS)
    answer: str | None   # Direct answer (if action is NO_SEARCH)


def parse_router_response(raw: str) -> RouterDecision:
    """
    Extracts JSON from LLM response and returns a typed RouterDecision.
    Raises ValueError if parsing fails.
    """
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in response:\n{raw}")

    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}\nRaw output:\n{raw}")

    return RouterDecision(
        action=data.get("action", ""),
        query=data.get("query"),
        answer=data.get("answer"),
    )


# ----------------------------
# Agent Prompts
# ----------------------------

ROUTER_SYSTEM_PROMPT = """
You are a router for a tiny agent.
You can do ONE tool call: SEARCH_DOCS.

Important context:
- The local documents contain ONLY the user's personal travel journal
  (cities visited, dates, places, activities).
- The model itself does NOT know this information unless it searches.

Routing rules (must follow):

1) If the question is about the user’s personal life or past
   (travel, cities, places, dates, activities, where they have been),
   you MUST choose SEARCH_DOCS.

2) Only choose NO_SEARCH for general world knowledge
   that does NOT depend on the user's personal history.

Output exactly ONE line of JSON:
- {"action":"SEARCH_DOCS","query":"..."}
- {"action":"NO_SEARCH","answer":"..."}

Do not explain your reasoning.
"""

ANSWER_SYSTEM_PROMPT = """
You are a helpful assistant answering questions about the user's personal travel journal.

Rules:
- Use ONLY the retrieved snippets as facts.
- If snippets are provided:
  - Answer in 2–5 sentences.
  - Summarize naturally (do not copy text verbatim).
  - Cite the journal source file at the end of sentences that use it,
    e.g. (travel_journal.txt).

- If the tool result is NO_RESULTS:
  - Say clearly that this information is not found in the travel journal.

- Do NOT invent places, dates, or activities.
- If unsure, say you don't know based on the journal.
"""

def agent_once(user_text: str, chunks: list[dict], config: dict) -> str:
    # TODO: Ask router LLM → parse decision → execute tool if needed → answer
    pass


def main():
    print("Loading config...")
    config = load_config()

    print("Loading docs from ./docs ...")
    chunks = load_doc_chunks("docs")
    print(f"Loaded {len(chunks)} chunks.\n")

    print("Mini Agent Demo: Ask a question. Type 'exit' to quit.\n")

    while True:
        user_text = input("You: ").strip()
        if user_text.lower() in {"exit", "quit"}:
            break

        try:
            answer = agent_once(user_text, chunks, config)
            print(f"\nAgent: {answer}\n")
        except Exception as e:
            print(f"\nERROR: {e}\n")


if __name__ == "__main__":
    main()