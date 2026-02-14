# Lekhan-AI: Administrative Document Assistant

## Overview
Lekhan-AI is a full-stack application designed to streamline bureaucratic workflows by automatically summarizing and classifying official documents. Built to handle standard state administration paperwork—such as circulars, internal memos, and gazette notifications—it reduces manual reading time by extracting key action items and metadata using local NLP models.

## Tech Stack
*   **Backend:** FastAPI, Python 3.10+
*   **Frontend:** Vue.js 3, Bootstrap 5
*   **Database:** SQLite (using SQLAlchemy ORM)
*   **Machine Learning:** HuggingFace Transformers (`facebook/bart-large-cnn` for summarization), XGBoost (for robust document classification)

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm 9+

### Installation

**Backend:**
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure
```
Lekhan-AI/
├── main.py              # FastAPI application entry point
├── models.py            # SQLAlchemy database models
├── requirements.txt     # Python dependencies
├── uploads/             # Uploaded document storage
├── frontend/            # Vue.js 3 frontend application
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── App.vue      # Root component
│   │   └── main.js      # Application entry point
│   └── package.json
└── README.md
```

## License
This project is for internal administrative use.
