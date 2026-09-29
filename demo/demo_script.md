# CiphEra Demo Script

**Duration:** ~10 minutes
**Audience:** Engineers evaluating agent memory and decision audit tooling

---

## Setup (before demo)

1. Copy `.env.example` → `.env` and set `OPENAI_API_KEY`
2. Start Hindsight (optional but recommended):
   ```bash
   docker run -it --pull always --name hindsight -p 8888:8888 -p 9999:9999 \
     -e HINDSIGHT_API_LLM_API_KEY=$OPENAI_API_KEY \
     ghcr.io/vectorize-io/hindsight:latest
   ```
3. Start the API:
   ```bash
   cd ciph-era
   pip install -r requirements.txt
   python -m backend.main
   ```
4. Start the UI:
   ```bash
   streamlit run frontend/app.py
   ```

---

## Act 1 — The Problem (2 min)

> "Every engineering team has been here: a decision made months ago comes back to haunt you, and nobody remembers *why* we did it."

1. Open the Streamlit UI
2. Select **"Remove automated database backups"**
3. Walk through Context → Reasoning → Assumptions
4. Reveal the **failure** outcome and evidence

**Talking point:** Decisions without memory become archaeology.

---

## Act 2 — Autopsy (3 min)

1. Go to the **Autopsy** tab
2. Set focus: `cost vs recovery risk`
3. Click **Run Autopsy**

**Talking point:** The autopsy surfaces root causes and premise drift — assumptions that were wrong at decision time but looked reasonable.

Compare with **"Use vector-only RAG for agent memory"** — another failure with a different failure mode.

---

## Act 3 — Hindsight Integration (3 min)

1. Select **"Adopt Hindsight for decision memory"** (success case)
2. Go to **Hindsight** tab → **Retain in Hindsight**
3. Run **Reflect**: _"What patterns connect our failed memory decisions?"_
4. Run **Recall**: _"decisions about agent memory"_

**Talking point:** Hindsight gives agents outcome-aware memory — not just what was said, but what worked.

---

## Act 4 — The Audit View (2 min)

1. Quickly flip through all four decisions in the sidebar
2. Note the outcome status badges: 2 failures, 1 partial, 1 success
3. Highlight the arc: vector RAG failed → Hindsight succeeded

**Closing line:**

> "CiphEra turns your decision history into an active system: remember the decision, expose the reasoning, detect premise drift, and reconsider when assumptions change."

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| API unreachable | Ensure `python -m backend.main` is running on port 8000 |
| Autopsy returns placeholder | Set `OPENAI_API_KEY` in `.env` |
| Hindsight 503 | Install `hindsight-client` and ensure server is on `:8888` |
| Empty reflect/recall | Retain decisions first to populate the bank |
