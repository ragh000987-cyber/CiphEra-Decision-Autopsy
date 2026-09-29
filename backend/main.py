import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import decisions_router, hindsight_router

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(
    title="CiphEra API",
    description="Decision memory, hindsight integration, and autopsy for agentic systems",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(decisions_router)
app.include_router(hindsight_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "ciph-era"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=True,
    )
