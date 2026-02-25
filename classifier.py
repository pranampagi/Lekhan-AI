import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier

# Document category labels
CATEGORIES = ["Circular", "Memo", "Notification"]

# Sample training data representing typical administrative documents.
# In production, this would be replaced with a properly curated dataset.
TRAINING_TEXTS = [
    # Circulars — formal directives issued to multiple departments
    "All department heads are hereby directed to implement the new attendance policy effective immediately.",
    "This circular is to inform all employees about the revised travel reimbursement guidelines.",
    "Circular: The office timings will be changed from next month as per the new government directive.",
    "It is hereby notified that all departments must submit quarterly reports by the 15th of each month.",
    "All staff members are directed to complete the mandatory training program by end of this quarter.",
    "This circular mandates the adoption of digital signatures for all official correspondence.",
    "Department heads are required to ensure compliance with the new data protection regulations.",
    "All employees are informed that the leave policy has been updated as per the latest circular.",
    # Memos — internal communications between specific parties
    "Memo: Please review the attached budget proposal for the upcoming fiscal year and provide feedback.",
    "Internal memo regarding the rescheduling of the weekly team meeting to Thursday afternoons.",
    "Memo to all project leads: Submit your resource allocation plans by Friday.",
    "This memo outlines the proposed changes to the internal review process for document approvals.",
    "Memo: The IT department will be conducting server maintenance this weekend.",
    "Please note the updated meeting agenda attached to this memo for the board review session.",
    "Internal communication: New procurement procedures will take effect starting next month.",
    "Memo from HR: Updated guidelines for remote work arrangements are now available.",
    # Notifications — official announcements and public notices
    "Notification: The office will remain closed on March 15th on account of a public holiday.",
    "Public notification regarding the extension of the deadline for property tax submissions.",
    "Gazette notification: Amendment to Section 42 of the Administrative Services Act, 2024.",
    "Notice: Applications are invited for the post of Senior Administrative Officer.",
    "Notification of scheduled power maintenance in Block B from 10 AM to 4 PM on Saturday.",
    "Public notice: The annual general meeting will be held on April 5th at the main auditorium.",
    "Official notification regarding changes to pension disbursement schedules.",
    "Notice: The examination schedule for the recruitment test has been published.",
]

TRAINING_LABELS = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]

# Train the TF-IDF vectorizer and XGBoost classifier
vectorizer = TfidfVectorizer(max_features=500, stop_words="english")
X_train = vectorizer.fit_transform(TRAINING_TEXTS)

classifier = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    objective="multi:softprob",
    num_class=3,
    eval_metric="mlogloss",
    use_label_encoder=False,
)
classifier.fit(X_train, TRAINING_LABELS)


def classify_document(text: str) -> dict:
    """Classify a document into one of the administrative categories.

    Uses TF-IDF features with an XGBoost classifier to predict whether
    the document is a Circular, Memo, or Notification.

    Args:
        text: The document text to classify.

    Returns:
        A dict with 'category' (predicted label) and 'confidence'
        (probability score for the predicted class).
    """
    if not text or not text.strip():
        return {"category": "Unknown", "confidence": 0.0}

    # Transform the input text using the fitted vectorizer
    X = vectorizer.transform([text])

    # Get prediction probabilities
    probabilities = classifier.predict_proba(X)[0]
    predicted_index = int(np.argmax(probabilities))

    return {
        "category": CATEGORIES[predicted_index],
        "confidence": round(float(probabilities[predicted_index]), 4),
    }
