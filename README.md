# Lekhan-AI: Administrative Document Assistant

## Overview
Lekhan-AI is a full-stack application designed to streamline bureaucratic workflows by automatically summarizing and classifying official documents. Built to handle standard state administration paperwork—such as circulars, internal memos, and gazette notifications—it reduces manual reading time by extracting key action items and metadata using local NLP models.

## Tech Stack
*   **Backend:** FastAPI, Python 3.10+
*   **Frontend:** Vue.js 3, Bootstrap 5
*   **Database:** SQLite (using SQLAlchemy ORM)
*   **Machine Learning:** HuggingFace Transformers (`facebook/bart-large-cnn` for summarization), XGBoost (for document classification)

## Features
*   📄 **Document Upload** — Drag-and-drop or browse to upload PDF and text files
*   🤖 **AI Summarization** — Automatic summary generation using BART (facebook/bart-large-cnn)
*   🏷️ **Document Classification** — Categorizes documents as Circular, Memo, or Notification using XGBoost
*   📊 **Dashboard** — Real-time stats on processed documents by category
*   🔍 **Search & Filter** — Filter documents by filename or category
*   📱 **Responsive Design** — Fully responsive UI that works on desktop and mobile

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm 9+

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

## Project Structure
```
Lekhan-AI/
├── main.py              # FastAPI application with upload, list, and detail endpoints
├── models.py            # SQLAlchemy Document model with indexed category column
├── database.py          # Database engine and session configuration
├── utils.py             # PDF and text file parsing utilities
├── ml_service.py        # HuggingFace BART summarization with token chunking
├── classifier.py        # XGBoost document classifier (Circular/Memo/Notification)
├── requirements.txt     # Python dependencies
├── uploads/             # Uploaded document storage (auto-created)
├── frontend/            # Vue.js 3 frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.vue      # Stats cards with loading states
│   │   │   ├── Uploader.vue       # Drag-and-drop file upload
│   │   │   ├── DocumentList.vue   # Searchable, filterable document table
│   │   │   └── DocumentModal.vue  # Summary detail modal
│   │   ├── App.vue                # Root component layout
│   │   └── main.js                # Application entry point
│   └── package.json
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload a PDF or text document |
| `GET` | `/documents` | List all processed documents |
| `GET` | `/documents/{id}` | Get a specific document with summary |

## License
This project is for internal administrative use.
