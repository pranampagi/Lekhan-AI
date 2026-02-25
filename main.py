import os

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db, SessionLocal
from models import Document
from utils import extract_text
from ml_service import generate_summary
from classifier import classify_document

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


def process_document(document_id: int, file_path: str):
    """Background task to extract text and generate a summary.

    Runs after the upload response is sent so the API doesn't block
    during heavy ML inference.

    Args:
        document_id: The database ID of the uploaded document.
        file_path: Path to the saved file on disk.
    """
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return

        # Extract text from the uploaded file
        raw_text = extract_text(file_path)
        document.original_text = raw_text

        # Generate summary using the BART model
        summary = generate_summary(raw_text)
        document.summary = summary

        # Classify the document using XGBoost
        classification = classify_document(raw_text)
        document.category = classification["category"]

        db.commit()
    except Exception as e:
        print(f"Error processing document {document_id}: {e}")
        db.rollback()
    finally:
        db.close()


@app.get("/health")
async def health_check():
    """Basic health check endpoint to verify the API is running."""
    return {"status": "healthy", "service": "Lekhan-AI"}


@app.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a PDF or text document for processing.

    Saves the file to the uploads/ directory, creates a database record,
    and kicks off background ML processing.
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

    # Create database record
    document = Document(filename=file.filename)
    db.add(document)
    db.commit()
    db.refresh(document)

    # Schedule ML processing as a background task
    background_tasks.add_task(process_document, document.id, file_path)

    return {
        "message": "File uploaded successfully. Processing started in background.",
        "filename": file.filename,
        "document_id": document.id,
        "size": len(contents),
    }


@app.get("/documents/{document_id}")
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Retrieve a processed document by its ID.

    Returns the document record including summary if processing is complete.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": document.id,
        "filename": document.filename,
        "summary": document.summary,
        "category": document.category,
        "upload_date": document.upload_date,
        "has_text": document.original_text is not None,
    }
