# Personal Memory Agent

A minimal AI agent implementation for learning purposes. No frameworks, no magic — just pure Python showing what's under the hood of tools like LangChain, ADK, Koog, etc.

The agent combines LLM's general knowledge with your personal documents (travel journal). It decides when to answer directly vs. when to search your private data.

---

## 🚀 Quick Start

### Prerequisites

<details>
<summary><strong>macOS</strong></summary>

#### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Python 3.10+
```bash
brew install python@3.13
```

#### 3. Install uv (fast Python package manager)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

</details>

<details>
<summary><strong>Windows</strong></summary>

#### 1. Install Python 3.10+
Download and install from [python.org](https://www.python.org/downloads/)

> ✅ During installation, check **"Add Python to PATH"**

#### 2. Install uv (fast Python package manager)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

</details>

<details>
<summary><strong>Linux</strong></summary>

#### 1. Install Python 3.10+ (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### 2. Install uv (fast Python package manager)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

</details>

---

### Setup (using uv)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager written in Rust. It's 10-100x faster than pip.

#### Step 1: Create and activate virtual environment

```bash
# Navigate to project folder
cd ai-agent-lesson-1

# Create virtual environment
uv venv .venv

# Activate it
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

> ✅ You should see `(.venv)` at the beginning of your terminal prompt

#### Step 2: Install dependencies

```bash
uv pip install -r requirements.txt
```

#### Step 3: Configure API credentials

```bash
cp config.example.json config.json   # macOS/Linux
copy config.example.json config.json # Windows
```

Edit `config.json` and add your API key:

```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-4o-mini"
}
```

**Where to get an API key:**
- **OpenAI:** https://platform.openai.com/api-keys
- **OpenRouter** (free models available): https://openrouter.ai/keys

> 💡 Works with any OpenAI-compatible API (OpenAI, OpenRouter, Ollama, etc.)

---

<details>
<summary><strong>📦 Setup without uv (using pip)</strong></summary>

If you prefer using the standard Python tools instead of uv:

#### Step 1: Create and activate virtual environment

```bash
# Navigate to project folder
cd ai-agent-lesson-1

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

> ✅ You should see `(.venv)` at the beginning of your terminal prompt

#### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure API credentials

```bash
cp config.example.json config.json   # macOS/Linux
copy config.example.json config.json # Windows
```

Edit `config.json` and add your API key:

```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-4o-mini"
}
```

</details>

---

### Run the Agent

```bash
python agent.py
```

## Example Questions

Try asking:

- **Personal (triggers search):** "What cities have I visited?" or "When did I go to Lisbon?"
- **General (no search):** "What is the capital of France?" or "How do airplanes fly?"

## Sample Output

```
You: When did I visit Helsinki?

[router decision] {'action': 'SEARCH_DOCS', 'query': 'Helsinki visit date'}
[tool call] search_docs(query='Helsinki visit date')
[tool result]
[source=travel_journal.txt score=2] In September 2024 I found a small coffee shop...

Agent: You visited Helsinki in September 2024, where you discovered a cozy 
coffee shop called Kaffa Roasters (travel_journal.txt).
```

## Key Concepts Demonstrated

| Concept | Where in Code |
|---------|---------------|
| **Agent Loop** | `agent_once()` function |
| **Tool Routing** | `ROUTER_SYSTEM_PROMPT` |
| **Tool Execution** | `search_docs()` |
| **RAG (basic)** | `load_doc_chunks()` + keyword matching |
| **LLM Abstraction** | `chat()` function |

## Limitations (By Design)

This is a **learning project**, intentionally simple:

- ❌ No conversation memory (each question is independent)
- ❌ No embeddings (uses keyword matching, not semantic search)
- ❌ Single tool only (real agents have multiple tools)
- ❌ No streaming (waits for full response)
- ❌ No retry logic (fails on first API error)

---

## 📝 License

MIT — use freely for learning!
