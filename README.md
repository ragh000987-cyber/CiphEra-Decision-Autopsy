# CiphEra — Decision Autopsy Agent

An AI agent that learns from the consequences of past decisions using Hindsight memory.

## Core loop

Decision → Expected outcome → Actual outcome → Autopsy → Lesson → Hindsight → Future decision

## Run locally

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your Hindsight API key. Hindsight Cloud currently uses the Python package `hindsight-client` and the API endpoint `https://api.hindsight.vectorize.io`. See the official docs for account/API-key setup.

Then:

```bash
streamlit run app.py
```

## Demo

1. Open the app.
2. Click **Load demo history** in the sidebar.
3. Enter a new decision similar to one of the historical decisions.
4. Click **Analyze Decision**.
5. Review the retrieved experiences and CiphEra analysis.
6. Enter the actual outcome.
7. Click **Run Decision Autopsy**.
8. Click **Save this experience to Hindsight**.
9. Run another similar decision to demonstrate that the newly stored experience can be recalled.

## Security

Never commit `.env` or a real Hindsight API key.
