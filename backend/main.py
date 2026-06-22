import os
import json
import logging
from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("portfolio-backend")

app = FastAPI(
    title="Ranit Pal Portfolio Backend",
    description="Python FastAPI backend serving contact operations and machine learning predictions",
    version="1.0.0"
)

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to portfolio URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- NLP SPAM MODEL CONFIGURATION -----------------
# We train a lightweight model dynamically on startup for demonstration purposes.
spam_training_data = [
    # Spam samples
    ("Free entry in 2 a weekly competition to win FA Cup final tickets. Text FA to 87121.", 1),
    ("Winner!! Selected to receive a £900 prize reward! Call now to claim your code KL34.", 1),
    ("Urgent! Your account has been locked. Verify details here immediately to unlock.", 1),
    ("Had your mobile 11 months? You are entitled to update to the latest camera phone for free.", 1),
    ("Congratulations! You won a free flight to Paris! Call 0800 now to book.", 1),
    ("Double your cash back! Subscribe now to receive daily tips. SMS STOP to end.", 1),
    ("Get cheap medications online. Buy pills without prescription today.", 1),
    ("Urgent message: your loan of $5000 is approved. Click link to deposit.", 1),
    # Ham samples
    ("Go until jurong point, crazy.. Available only in bugis n great world buffet.", 0),
    ("Ok lar... Joking wif u oni...", 0),
    ("Nah I don't think he goes to usf, he lives around here though.", 0),
    ("Even my brother is not like to speak with me. They treat me like a friend.", 0),
    ("Hey, how are you? Let's meet for lunch tomorrow.", 0),
    ("Are you coming over tonight? Let me know.", 0),
    ("I am home soon. Do you want to watch a movie?", 0),
    ("Thanks for the help, I appreciate your support.", 0),
    ("Sure, we can discuss the project metrics on Monday morning.", 0),
    ("Can you send me the resume PDF? I want to look at your research papers.", 0)
]

texts, labels = zip(*spam_training_data)
vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
X_train = vectorizer.fit_transform(texts)
clf = MultinomialNB()
clf.fit(X_train, labels)
logger.info("Spam classifier model trained successfully on startup.")

# ----------------- PYDANTIC SCHEMAS -----------------
class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class SpamRequest(BaseModel):
    text: str

# ----------------- ENDPOINTS -----------------
@app.get("/")
@app.get("/{path:path}")
def serve_portfolio(path: str = ""):
    if path.startswith("api/") or path == "favicon.ico":
        raise HTTPException(status_code=404, detail="Not Found")
    from fastapi.responses import FileResponse
    html_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    if os.path.exists(html_file):
        return FileResponse(html_file)
    else:
        raise HTTPException(status_code=404, detail="index.html not found")

@app.post("/api/contact")
def receive_contact(payload: ContactRequest):
    logger.info(f"Received contact message from: {payload.name} ({payload.email})")
    
    # Save message locally to a JSON file
    messages_file = os.path.join(os.path.dirname(__file__), "messages.json")
    try:
        if os.path.exists(messages_file):
            with open(messages_file, "r") as f:
                data = json.load(f)
        else:
            data = []
    except Exception as e:
        logger.error(f"Error reading messages file: {e}")
        data = []

    new_message = payload.model_dump()
    import datetime
    new_message["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    data.append(new_message)

    try:
        with open(messages_file, "w") as f:
            json.dump(data, f, indent=4)
        logger.info("Contact message saved locally.")
    except Exception as e:
        logger.error(f"Error saving message: {e}")
        raise HTTPException(status_code=500, detail="Failed to save message on server.")

    return {"message": "Success", "status": 200}

@app.post("/api/predict-spam")
def predict_spam(payload: SpamRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    
    # Vectorize and predict
    vec = vectorizer.transform([payload.text])
    pred = clf.predict(vec)[0]
    prob = clf.predict_proba(vec)[0]
    confidence = float(prob[pred])
    
    return {
        "text": payload.text,
        "is_spam": bool(pred),
        "confidence": confidence
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
