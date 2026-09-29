# CiphEra

Decision memory, hindsight integration, and autopsy for agentic AI systems.

CiphEra helps engineering teams answer:

- What did we decide?
- Why did we decide it?
- Which assumptions have changed?
- What happened after the decision?

## Architecture

```
ciph-era/
├── backend/          FastAPI API
│   ├── main.py
│   ├── routes/       REST endpoints
│   ├── services/
│   │   ├── hindsight.py   retain / recall / reflect
│   │   ├── llm.py         autopsy LLM calls
│   │   └── autopsy.py     post-mortem analysis
│   └── models/       Pydantic schemas
├── frontend/
│   └── app.py        Streamlit UI
├── data/
│   └── decisions.json
└── demo/
    └── demo_script.md
```

## Quick Start

```bash
cd ciph-era
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # then edit OPENAI_API_KEY
```

**Terminal 1 — API:**

```bash
python -m backend.main
```

**Terminal 2 — UI:**

```bash
streamlit run frontend/app.py
```

Open http://localhost:8501

## Hindsight (optional)

For retain / recall / reflect, run a Hindsight server:

```bash
docker run -it --pull always --name hindsight -p 8888:8888 -p 9999:9999 \
  -e HINDSIGHT_API_LLM_API_KEY=$OPENAI_API_KEY \
  ghcr.io/vectorize-io/hindsight:latest
```

Then use the **Hindsight** tab in the UI to retain decisions and query memory.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/decisions` | List all decisions |
| GET | `/decisions/{id}` | Get one decision |
| POST | `/decisions/{id}/autopsy` | Run LLM autopsy |
| POST | `/decisions/{id}/retain` | Store in Hindsight |
| POST | `/decisions/{id}/reflect` | Reflect via Hindsight |
| POST | `/hindsight/recall` | Recall memories |
| GET | `/hindsight/status` | Hindsight connectivity |

## Demo

See [demo/demo_script.md](demo/demo_script.md) for a 10-minute walkthrough.

## License

MIT
