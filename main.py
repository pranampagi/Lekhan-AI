import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Document

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="Lekhan-AI",
    description="Administrative Document Assistant — Summarize and classify official documents using AI.",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Basic health check endpoint to verify the API is running."""
    return {"status": "healthy", "service": "Lekhan-AI"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF or text document for processing.

    Saves the file to the uploads/ directory and creates a database record.
    """
    # Validate file type
    allowed_types = [
        "application/pdf",
        "text/plain",
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Only PDF and text files are accepted.",
        )

    # Save file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "size": len(contents),
    }
