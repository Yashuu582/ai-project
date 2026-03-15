# 🤖 AI Application Tracking System (ATS)

A full-stack **Application Tracking System** powered by a local LLM (via Ollama) that helps you track job applications and analyze your resume against job descriptions using AI.

---

## ✨ Features

- ➕ Add, edit, delete job applications
- 📋 Track status — `Applied` | `Interview` | `Offer` | `Rejected`
- 🧠 AI resume analysis with match score (0–100)
- 💡 AI-generated strengths, gaps & improvement suggestions
- 🔍 Filter applications by status
- 📊 Real-time stats bar

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | SQLite + SQLAlchemy |
| AI / LLM | Ollama (llama3) — runs locally, free |
| Frontend | HTML, CSS, Vanilla JavaScript |

---

## 📁 Project Structure

```
ai-project/
├── backend/
│   ├── main.py          # FastAPI routes (CRUD + AI endpoints)
│   ├── models.py        # SQLAlchemy ORM model (Application table)
│   ├── database.py      # SQLite engine & session setup
│   ├── ai_service.py    # Ollama llama3 integration & response parsing
│   └── schemas.py       # Pydantic schemas for validation
├── frontend/
│   ├── index.html       # Main dashboard UI
│   ├── style.css        # Dark theme styling
│   └── app.js           # API calls & UI logic
├── requirements.txt
├── start.bat
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/download) installed

### 1. Clone the repository

```bash
git clone https://github.com/Yashuu582/ai-project.git
cd ai-project
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

> Dependencies: `fastapi==0.111.0`, `uvicorn==0.29.0`, `sqlalchemy==2.0.30`, `pydantic==2.7.1`, `requests==2.31.0`

### 3. Pull the llama3 model

```bash
ollama pull llama3
```

> ⚠️ Model is ~4GB — wait for the download to complete.

### 4. Start Ollama

```bash
ollama serve
```

### 5. Start the backend

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

> On Windows, you can also double-click `start.bat`

### 6. Open the frontend

Open `frontend/index.html` in your browser (Chrome or Edge recommended).

---

## 🧠 How AI Analysis Works

1. Add a job application with a **job description** and your **resume text**
2. Click the **🧠 Analyze** button
3. The backend sends a structured prompt to Ollama (`http://localhost:11434/api/generate`)
4. llama3 returns a JSON response with:
   - `score` — match percentage (0–100)
   - `strengths` — what aligns well
   - `gaps` — what's missing
   - `suggestions` — how to improve your resume
   - `summary` — 2-sentence overall assessment
5. Score and feedback are saved back to the database

> Use **Quick Analyze** (`POST /analyze`) to test without saving an application.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/applications` | Get all applications (sorted by date) |
| `POST` | `/applications` | Create new application |
| `PUT` | `/applications/{id}` | Update application fields |
| `DELETE` | `/applications/{id}` | Delete application |
| `POST` | `/applications/{id}/analyze` | AI analyze a saved application |
| `POST` | `/analyze` | Quick AI analyze (no save) |
| `GET` | `/stats` | Get total count & counts by status |

### Example Request — Create Application

```json
POST /applications
{
  "company": "Google",
  "role": "Software Engineer",
  "status": "Applied",
  "job_description": "...",
  "resume_text": "...",
  "notes": "Referral from John"
}
```

### Example Response — AI Analyze

```json
{
  "score": 78,
  "strengths": ["Strong Python skills", "Relevant project experience"],
  "gaps": ["No Kubernetes experience", "Missing system design examples"],
  "suggestions": ["Add a distributed systems project", "Mention cloud certifications"],
  "summary": "Good overall match with strong backend skills. Address the infrastructure gaps to improve chances."
}
```

---

## 🗄️ Database Schema

**Table: `applications`**

| Column | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `company` | String | Company name |
| `role` | String | Job role/title |
| `status` | String | Applied / Interview / Offer / Rejected |
| `job_description` | Text | Job posting text |
| `resume_text` | Text | Your resume content |
| `ai_score` | Integer | AI match score (0–100) |
| `ai_feedback` | Text | Full AI response stored as string |
| `notes` | Text | Personal notes |
| `applied_date` | DateTime | Auto-set on creation |

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| Backend won't start | Run from inside the `backend/` folder |
| AI returns "unavailable" | Run `ollama serve` in a separate terminal |
| CORS error in browser | Ensure backend is running on port 8000 |
| `ollama pull llama3` is slow | Normal — model is ~4GB |
| 422 Unprocessable Entity | Check request body matches the schema |
| AI score is 0 | Ollama response parsing failed — check Ollama logs |

---

## 📈 Project Level

**Medium-level** full-stack project with local LLM integration — suitable for portfolios demonstrating AI-powered app development.

---

## 📄 License

MIT License — free to use and modify.
