from fastapi import FastAPI

app = FastAPI(
    title="Lekhan-AI",
    description="Administrative Document Assistant — Summarize and classify official documents using AI.",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Basic health check endpoint to verify the API is running."""
    return {"status": "healthy", "service": "Lekhan-AI"}
