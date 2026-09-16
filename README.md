# ReviewBot — AI Engine

The analysis engine for **ReviewBot**. Give it a GitHub pull request URL and it fetches the diff, runs it through a multi-agent LLM pipeline, and returns a structured review report.

> **This is 1 of 3 services.**
> [🖥️ Frontend](https://github.com/shubhutf/codereview-ai-frontend) · [⚙️ Backend](https://github.com/shubhutf/codereview-ai-backend) · 🧠 **AI Engine** (you are here)

---

## What this service does

1. Parses a GitHub PR URL into owner / repo / PR number
2. Fetches the changed files and their diffs from the **GitHub REST API**
3. Cleans the raw patches into line-level context the model can reason about
4. Runs them through a **LangGraph** pipeline of specialised agents
5. Returns issues, a risk score, and summaries as JSON

This service is stateless — no database, no auth. It's called by the backend, not by the browser.

---

## The agent pipeline

Built with **LangGraph**, where each node is one focused agent and edges define execution order.

```
                    ┌──────────────────┐
              ┌────▶│    bug_agent     │────┐
              │     └──────────────────┘    │
              │     ┌──────────────────┐    │
  START ──────┼────▶│  security_agent  │────┼───▶ risk_agent ──▶ summary_agent ──▶ END
              │     └──────────────────┘    │
              │     ┌──────────────────┐    │
              └────▶│performance_agent │────┘
                    └──────────────────┘
```

| Agent | Responsibility |
|---|---|
| `bug_agent` | Logic errors, undefined variables, syntax problems |
| `security_agent` | Vulnerabilities introduced by the diff |
| `performance_agent` | Inefficient or expensive patterns |
| `risk_agent` | Aggregates all findings into a single 0–100 risk score |
| `summary_agent` | Writes the final human-readable review |

**Why three agents in parallel?** Each gets a narrow, focused prompt, which produces better results than asking one model to do everything at once — and since the three don't depend on each other, LangGraph runs them concurrently.

Shared data flows between nodes through a typed state object (`state/pr_state.py`) holding the patches, parsed lines, accumulated issues, and summaries.

> `fixes_agent` exists in the codebase but is not currently connected to the graph — a planned feature, not yet wired in.

---

## Tech stack

| | |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn (dev) / Gunicorn (production) |
| Orchestration | LangGraph |
| LLM interface | LangChain (`langchain-openai`) |
| Model provider | Groq (`openai/gpt-oss-120b`) |
| Data source | GitHub REST API |

The LLM is configured through an **OpenAI-compatible** endpoint, so swapping providers (Groq, OpenAI, OpenRouter) is a one-line change in `utils/llm.py`.

---

## API

### `POST /analyze`

**Request**
```json
{ "pr_url": "https://github.com/owner/repo/pull/123" }
```

**Response**
```json
{
  "issues": [
    {
      "file": "packages/next/src/server/dev/turbopack-utils.ts",
      "line": 390,
      "code": "processIssues(currentIssues, key, writtenEndpoint, dev)",
      "issue": "`dev` is referenced without being defined in the current scope.",
      "fix": "Pass `dev` into the surrounding function before using it.",
      "type": "bug",
      "severity": "high"
    }
  ],
  "risk_score": 83,
  "risk_summary": "...",
  "final_summary": "..."
}
```

Errors return `500` with the exception message in `detail`.

---

## Project structure

```
├── main.py                  # FastAPI app, /analyze endpoint
├── services/
│   └── pr_pipeline.py       # Fetches the PR, runs the graph, shapes the report
├── graph/
│   └── pr_graph.py          # LangGraph node + edge definitions
├── agents/                  # One file per agent
├── processing/              # Diff parsing and cleanup
├── state/
│   └── pr_state.py          # Shared pipeline state
└── utils/
    └── llm.py               # LLM client configuration
```

---

## Getting started

### Prerequisites
- Python 3.10+
- A [Groq](https://console.groq.com) API key (free tier)
- A [GitHub personal access token](https://github.com/settings/tokens) with read access to public repositories

### Install

```bash
pip install fastapi uvicorn pydantic requests python-dotenv \
            langchain langchain-core langchain-openai langgraph gunicorn
```

### Configure

Create a `.env` file in the project root:

```dotenv
GROQ_API_KEY=gsk_your_key_here
GITHUB_TOKEN=github_pat_your_token_here
```

| Variable | What it's for |
|---|---|
| `GROQ_API_KEY` | Authenticates LLM calls |
| `GITHUB_TOKEN` | Optional but strongly recommended — without it you'll hit GitHub's unauthenticated rate limit quickly |

### Run

```bash
uvicorn main:app --reload --port 8000
```

### Test it directly

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"pr_url": "https://github.com/vercel/next.js/pull/62234"}'
```

---

## Switching model providers

Everything routes through one client in `utils/llm.py`:

```python
llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
```

To use OpenAI instead, drop the `base_url`, swap the key, and set a model like `gpt-4o-mini`. Groq's model lineup changes over time — list what's currently available on your key with:

```bash
curl https://api.groq.com/openai/v1/models -H "Authorization: Bearer $GROQ_API_KEY"
```

---

## Deployment

Deploys to **Render** or **Railway**. Notes:

- Start command: `gunicorn main:app -k uvicorn.workers.UvicornWorker`
- Large PRs mean long LLM calls — raise your host's request timeout
- Set `GROQ_API_KEY` and `GITHUB_TOKEN` as environment variables in the host dashboard

---

## Roadmap

- [ ] Connect `fixes_agent` to the graph
- [ ] Support private repositories
- [ ] Chunk very large diffs to stay inside the context window
- [ ] Stream progress per agent instead of returning only on completion
- [ ] Trim `requirements.txt` to runtime dependencies only

---

## License

MIT
