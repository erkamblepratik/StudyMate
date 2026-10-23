# StudyMate AI — Student Study Assistant Agent

A B.Tech AI Agent Development mini project built with Python, FastAPI, and a modern web frontend (with optional Streamlit interface). It combines an aesthetic glassmorphic chat interface, AST-verified safe math calculation, subject-tailored study plans, practice quizzes, session memory, and optional OpenAI LLM reasoning.

## Frontend & Features

### 🌟 Modern Web Frontend (Recommended)
- **Aesthetic Glassmorphic UI:** Obsidian dark theme with vibrant indigo/cyan gradients, ambient glow, and light theme toggle.
- **Student Personalization:** Student name profile, subject selector, and 3-stage level tuner (*Beginner*, *Intermediate*, *Exam-ready*).
- **Day-Wise Study Timetable Engine:** Structured Day 1 to Day 7 roadmaps starting from Day 1 foundational concepts to Day 7 mock exams.
- **Setup Question Bank (30-50 Questions per Subject):** 280+ total verified university exam questions across all subjects with interactive answer accordions.
- **Universal Question Answering:** Answers ANY student query (coding problems, OOP concepts, algorithms, comparisons, academic topics) with complete pedagogical explanations.
- **Interactive Safe Calculator:** On-screen keypad + AST expression evaluator that prevents code injection.
- **Session Memory Drawer:** Live memory tracker and notes saver.
- **Session Export:** 1-click export of chat notes to Markdown (`.md`).
- **Sound Effects:** Subtle, pleasant Web Audio API feedback for message send/receive.
- **Zero-Failure Offline & Online Engine:** Works 100% reliably even without API credits or offline, with optional live LLM mode.

---

## Requirements
- Python 3.10+
- Modern Web Browser (Chrome, Edge, Firefox, Brave, Safari)
- Internet connection only for initial setup and optional OpenAI responses

---

## Quick Start

### 1. Setup Environment
Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Modern Web Frontend
```bash
python server.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:8000`**

*(Alternatively run with reload: `uvicorn server:app --reload --port 8000`)*

### 3. Optional: Run Streamlit Interface
If you want to view the original Streamlit interface:
```bash
streamlit run app.py
```
Streamlit will display `http://localhost:8501`.

---

## Optional OpenAI API Setup
1. Copy `.env.example` to `.env`.
2. Add your API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
3. Or configure it directly inside the Web UI via the **Settings (⚙️)** modal.

---

## Example Prompts & Agent Actions
- `Explain Compiler Design in simple words.`
- `Make a study plan for Machine Learning.`
- `Give me a quiz on Operating Systems.`
- `calculate: (15 * 8) + (2**6 / 4)`
- Click any of the **Quick Prompt Chips** at the bottom of the chat interface.

---

## Architecture
```
Student Web Client (HTML5 / Vanilla CSS / ES6 JS)
        │
        ▼  [REST API / JSON]
FastAPI Backend (server.py)
   ├── Safe AST Calculator (_ALLOWED_OPERATORS)
   ├── Academic Knowledge Engine (Offline Fallback)
   ├── Study Plan & Practice Quiz Generators
   └── Optional OpenAI API Client (GPT-4o-mini)
        │
        ▼
   Session Memory & Markdown Formatted Stream
```

---

## Academic Project Information
- **Project:** StudyMate AI: Student Study Assistant Agent
- **Course:** AI Agent Development Mini-Project
- **Author:** Pratik Kamble

