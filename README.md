# CiphEra — Decision Autopsy Agent

> **An AI agent that learns from the consequences of past decisions — not just from instructions.**

CiphEra is a **Decision Autopsy Agent** that analyzes decisions after their outcomes are known, extracts lessons from what actually happened, and stores those lessons in **Hindsight memory**.

When a similar decision appears in the future, CiphEra retrieves relevant past experiences and uses them to provide context for the new decision.

---

## 🧠 The Core Idea

Most AI systems focus on making the **next decision**.

CiphEra focuses on understanding the **previous decision first**.

```text
┌──────────────┐
│   Decision   │
└──────┬───────┘
       ↓
┌──────────────────┐
│ Expected Outcome │
└────────┬─────────┘
         ↓
┌────────────────┐
│ Actual Outcome │
└───────┬────────┘
        ↓
┌────────────────┐
│ Decision       │
│ Autopsy        │
└───────┬────────┘
        ↓
┌────────────────┐
│ Extract Lesson │
└───────┬────────┘
        ↓
┌────────────────┐
│ Hindsight      │
│ Memory         │
└───────┬────────┘
        ↓
┌─────────────────────┐
│ Future Decision     │
│ + Past Experience   │
└─────────────────────┘
```

### Core Loop

**Decision → Expected Outcome → Actual Outcome → Autopsy → Lesson → Hindsight → Future Decision**

---

## ✨ Key Features

### 🔍 Decision Analysis

CiphEra analyzes a new decision and retrieves relevant experiences from previous decisions.

### 🧪 Decision Autopsy

Once the actual outcome is known, CiphEra compares:

* What was expected
* What actually happened
* What went wrong
* What went well
* Why the outcome differed
* What should be remembered

### 🧠 Hindsight Memory

Lessons from previous decisions are stored using Hindsight so they can be retrieved when similar situations occur.

### 🔄 Continuous Learning

Every completed decision can become an experience that influences future decisions.

### 🎯 Similar-Decision Retrieval

CiphEra can retrieve relevant historical experiences instead of treating every decision as completely new.

---

## 🏗️ Architecture

```text
                    ┌─────────────────┐
                    │   User Decision │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Decision Agent  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Hindsight       │
                    │ Memory Retrieval│
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ LLM Analysis    │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Decision Result │
                    └────────┬────────┘
                             ↓
                       Actual Outcome
                             ↓
                    ┌─────────────────┐
                    │    Autopsy      │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Lesson / Memory │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Hindsight Store │
                    └─────────────────┘
                             │
                             └──────→ Future Decisions
```

---

## 📁 Project Structure

```text
ciph-era/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   │   ├── hindsight.py
│   │   ├── llm.py
│   │   └── autopsy.py
│   └── models/
│
├── frontend/
│   └── app.py
│
├── data/
│   └── decisions.json
│
├── demo/
│   └── demo_script.md
│
├── README.md
├── requirements.txt
└── .env.example
```

---

## 🛠️ Tech Stack

| Component     | Technology    |
| ------------- | ------------- |
| Frontend      | Streamlit     |
| Backend       | FastAPI       |
| Language      | Python        |
| LLM           | OpenAI API    |
| Memory        | Hindsight     |
| API Server    | Uvicorn       |
| Configuration | python-dotenv |
| Data          | JSON          |

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ciph-era
```

### 2. Create a virtual environment

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from `.env.example`.

Add your required API credentials, including your Hindsight API key.

Hindsight Cloud uses the following API endpoint:

```text
https://api.hindsight.vectorize.io
```

The Python client package used for Hindsight is:

```text
hindsight-client
```

### 5. Start the application

```bash
streamlit run frontend/app.py
```

If the backend is required separately, start it with:

```bash
uvicorn backend.main:app --reload
```

---

## 🎬 Demo

The recommended demo flow is:

### Step 1 — Load historical decisions

Open the application and click:

**Load demo history**

This provides CiphEra with previous decision experiences.

### Step 2 — Make a new decision

Enter a decision that is similar to one of the historical decisions.

Click:

**Analyze Decision**

CiphEra retrieves relevant experiences and uses them during analysis.

### Step 3 — Observe the decision analysis

Review:

* Retrieved experiences
* Relevant historical context
* CiphEra's analysis
* Expected outcome

### Step 4 — Enter the actual outcome

After the decision has been made, provide what actually happened.

### Step 5 — Run the Decision Autopsy

Click:

**Run Decision Autopsy**

CiphEra compares the expected and actual outcomes and extracts a lesson from the experience.

### Step 6 — Save the experience

Click:

**Save this experience to Hindsight**

The new experience becomes part of CiphEra's memory.

### Step 7 — Demonstrate learning

Run another decision similar to the previous one.

CiphEra can now retrieve the newly stored experience and use it as historical context.

This demonstrates the complete learning loop:

```text
Past Decision
     ↓
Outcome
     ↓
Autopsy
     ↓
Lesson
     ↓
Memory
     ↓
Future Decision
     ↓
Better Context
```

---

## 💡 Why CiphEra?

Traditional decision systems often focus on:

> **"What should I do?"**

CiphEra adds another question:

> **"What happened the last time I did something similar?"**

The goal is to make previous experiences useful for future decisions by turning outcomes into structured, retrievable memory.

---

## 🔐 Security

Never commit secrets to the repository.

Do **not** commit:

```text
.env
```

or any real API keys.

Use `.env.example` to document the required environment variables without exposing their values.

Example:

```text
HINDSIGHT_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
```

---

## 🔮 Future Scope

Potential extensions include:

* More sophisticated decision similarity retrieval
* Confidence tracking for decisions
* Long-term decision trends
* Automatic detection of recurring mistakes
* Decision pattern visualization
* Multi-agent decision analysis
* Richer structured memory
* Human feedback on generated autopsies
* Analytics across large decision histories

---

## 🎯 Vision

**CiphEra turns experience into memory and memory into better context for future decisions.**

Instead of simply asking an AI to make a decision, CiphEra gives it the ability to look back, understand what happened, and carry those lessons forward.
