# 🌌 Interactive ML & Software Engineering Portfolio

Welcome to my portfolio! This project is a modern, high-performance, and interactive portfolio designed to showcase my skills as a **Computer Science Engineering Graduate** specializing in Machine Learning, Data Engineering, and Full-Stack Development.

It has been upgraded from a static webpage into a responsive, full-stack application featuring a **Python FastAPI backend** serving a live machine learning classifier, a data-logging terminal, and premium frontend visual effects.

---

## ✨ Features & Highlights

### 🎨 Visual & Frontend Upgrades
- **Interactive Neural Network Canvas**: A dynamic particle system rendering floating nodes and connected edges in the background, responding fluidly to cursor movement.
- **Global Cursor Glow**: CSS-driven glowing halo effect tracked dynamically using `--mouse-x` and `--mouse-y` variables.
- **Scroll Reveal Animations**: Intersection Observer API integrations that fade and slide sections/cards into view as you scroll.
- **3D Card Hover Tilts**: Interactive project and publication cards that react to mouse hover with an elegant three-dimensional tilt.
- **Interactive Skill Filters**: Categorized skill pills (Languages, ML/Data, Frontend, Databases, etc.) that filter automatically with smooth transitions.

### 🧠 Interactive Machine Learning & Simulation Widgets
- **Live SMS Spam Classifier**: A mock terminal widget within the spam detection project card. It allows you to enter custom messages and uses the backend API to predict spam probability with a Naive Bayes model.
- **ATS Resume Matcher**: An interactive widget showing the relevance score of my resume against different recruiter target titles.
- **Code-Themed Contact Terminal**: A dark-theme interactive python terminal mockup (`contact_form.py`). Type your details as variables, run `send()`, and watch it log your message directly to the backend with real-time feedback.

---

## 🛠️ Tech Stack

- **Frontend**: Vanilla HTML5, Modern CSS3 (Grid, Flexbox, HSL variables, transitions), JavaScript (ES6+, Canvas API, Intersection Observer).
- **Backend**: Python 3.x, FastAPI (High-performance web framework), Uvicorn (ASGI server), Scikit-Learn (TF-IDF & Naive Bayes classification), Pydantic v2 (Data validation & serialization), NumPy.

---

## 📂 Directory Structure

```text
Portfolio/
├── index.html            # Main portfolio webpage (HTML, CSS, JS)
├── README.md             # Project documentation (this file)
├── .gitignore            # Git exclusions
└── backend/
    ├── main.py           # FastAPI application server & ML training logic
    ├── requirements.txt  # Python package dependencies
    └── messages.json     # Local message log database
```

---

## 🚀 Getting Started

To run the backend server and serve the interactive features locally, follow these steps:

### Prerequisites
Make sure you have **Python 3.8+** installed on your system.

### 1. Clone & Navigate to the Repository
```bash
git clone https://github.com/Ranit32/Portfolio.git
cd Portfolio
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Run the Server
Launch the FastAPI development server:
```bash
python backend/main.py
```
*(Alternatively, you can run: `python -m uvicorn backend.main:app --reload`)*

Once started, the backend is active at `http://127.0.0.1:8000/`.

### 5. Access the Portfolio
Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```
The FastAPI backend serves the main `index.html` file at the root, automatically routing all pages correctly and exposing endpoints for the contact form (`/api/contact`) and the NLP spam predictor (`/api/predict-spam`).

---

## 🔬 Machine Learning Model Details

The live SMS Spam Predictor endpoint uses a lightweight Natural Language Processing pipeline:
1. **Feature Extraction**: Text is converted to numerical representations using a TF-IDF (Term Frequency-Inverse Document Frequency) Vectorizer with English stop-words removed.
2. **Classifier**: A **Multinomial Naive Bayes (MultinomialNB)** classifier is trained dynamically on startup using structured spam and non-spam training datasets.
3. **Inference**: High-speed, real-time probability estimates are returned to the client to calculate predictive confidence scores dynamically.