import os
import ast
import operator
import re
import streamlit as st
from dotenv import load_dotenv
import knowledge_bank

load_dotenv()

st.set_page_config(page_title="StudyMate AI", page_icon="🎓", layout="wide")

# Global tracker for quota
OPENAI_QUOTA_EXHAUSTED = False

# Safe calculator: only numeric constants and basic arithmetic operators are accepted.
_ALLOWED_OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}

def safe_calculate(expression: str):
    cleaned = expression.strip().replace("×", "*").replace("÷", "/").replace("^", "**")
    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Use only numbers and +, -, *, /, %, **, and parentheses.")
    if len(cleaned) > 100:
        raise ValueError("Expression is too long.")
    parsed = ast.parse(cleaned, mode="eval").body
    res = _eval(parsed)
    if isinstance(res, float) and res.is_integer():
        return int(res)
    elif isinstance(res, float):
        return round(res, 6)
    return res

def offline_reply(question: str, subject: str, level: str, student_name: str = "Student") -> str:
    q = question.strip()
    q_lower = q.lower()

    # 1. Greetings
    greeting_triggers = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "how are you", "who are you"]
    if any(q_lower == g or q_lower.startswith(g + " ") for g in greeting_triggers):
        return (
            f"### 👋 Hello, {student_name}!\n\n"
            f"Welcome to **StudyMate AI**! I'm your academic study assistant for **{subject}** at the **{level}** level.\n\n"
            f"- 📅 Ask for a **Day-Wise Timetable** (starting from Day 1 basic concepts).\n"
            f"- 📝 Ask for **Setup Questions (30-50 questions)** with hidden exam answers.\n"
            f"- 🧮 Type `calculate: <math>` for safe AST arithmetic.\n"
            f"- 💡 Ask me to explain **any** question, code problem, or concept!\n\n"
            f"What would you like to learn today?"
        )

    # 2. Calculator
    if q_lower.startswith("calculate:") or q_lower.startswith("calc:"):
        expr = q.split(":", 1)[1].strip()
        try:
            result = safe_calculate(expr)
            return f"### 🧮 Safe Calculator Result\n\n`{expr}` = **`{result}`**"
        except Exception as exc:
            return f"⚠️ I couldn't calculate that expression: {exc}"

    # 3. Day-Wise Study Timetable
    if any(k in q_lower for k in ["study plan", "timetable", "time table", "schedule", "routine", "revision plan", "day wise", "day-wise", "day 1", "days plan"]):
        return knowledge_bank.format_day_wise_timetable(subject, level)

    # 4. Practice Quiz & Setup Questions (30 - 50 questions)
    if any(k in q_lower for k in ["quiz", "practice", "mcq", "test me", "question", "questions", "mock test", "setup question", "setup questions"]):
        count = 35
        m = re.search(r'(\d+)\s*(?:questions?|mcqs?|q\b)', q_lower)
        if m:
            try:
                count = max(1, min(50, int(m.group(1))))
            except ValueError:
                count = 35
        return knowledge_bank.format_quiz_output(subject, level, count=count)

    # 5. Answer ANY Question (Universal Academic Engine)
    return knowledge_bank.answer_any_question(question, subject, level, student_name)

def llm_reply(question: str, subject: str, level: str, history: list, student_name: str = "Student") -> str:
    global OPENAI_QUOTA_EXHAUSTED
    q_stripped = question.strip().lower()

    # Route direct tools to internal verified engine immediately
    if (q_stripped.startswith("calculate:") or
        any(k in q_stripped for k in ["timetable", "time table", "study plan", "day wise", "day 1", "quiz", "setup question", "practice question"])):
        return offline_reply(question, subject, level, student_name)

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or OPENAI_QUOTA_EXHAUSTED or not api_key.startswith("sk-"):
        return offline_reply(question, subject, level, student_name)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        system_prompt = (
            f"You are StudyMate, a supportive and clear academic tutor for college student {student_name}. "
            f"Subject: {subject}. Target Level: {level}. "
            f"Explain clearly with structured markdown, bullet points, intuition, and examples."
        )
        messages = [{"role": "system", "content": system_prompt}]
        for item in history[-6:]:
            messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})
        messages.append({"role": "user", "content": question})

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=900
        )
        return completion.choices[0].message.content
    except Exception as exc:
        err = str(exc)
        if "insufficient_quota" in err or "credit_balance_exhausted" in err or "429" in err:
            OPENAI_QUOTA_EXHAUSTED = True
        return offline_reply(question, subject, level, student_name)

# ==============================================================================
# STREAMLIT UI
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = []

st.title("🎓 StudyMate AI")
st.caption("AI Study Assistant Agent • Day-Wise Timetables • 35-50 Setup Questions • Universal Concept Answering")

with st.sidebar:
    st.header("👤 Student Profile")
    student_name = st.text_input("Student Name", value="Pratik Kamble")
    
    subject = st.selectbox(
        "Selected Subject",
        [
            "AI Agent Development",
            "Machine Learning",
            "Operating Systems",
            "Compiler Design",
            "Data Structures",
            "Computer Networks",
            "Database Management Systems",
            "Other"
        ]
    )
    
    level = st.select_slider("Target Level", options=["Beginner", "Intermediate", "Exam-ready"], value="Exam-ready")
    st.divider()

    st.subheader("⚡ Quick Launch Tools")
    if st.button("📅 Day-Wise Timetable (Day 1-7)", use_container_width=True):
        plan_text = knowledge_bank.format_day_wise_timetable(subject, level)
        st.session_state.messages.append({"role": "assistant", "content": plan_text})
        st.rerun()

    if st.button("📝 Setup Questions (35 Qs Bank)", use_container_width=True):
        quiz_text = knowledge_bank.format_quiz_output(subject, level, count=35)
        st.session_state.messages.append({"role": "assistant", "content": quiz_text})
        st.rerun()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.memory = []
        st.rerun()

    st.caption("Session privacy: Memory is kept in the current session.")

st.write(f"Welcome, **{student_name or 'Student'}**! You are studying **{subject}** at **{level}** level.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

prompt = st.chat_input("Ask ANY study question, request day-wise timetable, quiz 35 questions, or calculate: 12 * 5")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.memory.append(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("StudyMate is thinking..."):
            answer = llm_reply(prompt, subject, level, st.session_state.messages[:-1], student_name)
            st.markdown(answer, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.memory.append(answer)

with st.expander("📚 View Session Memory & Notes"):
    if st.session_state.memory:
        for idx, entry in enumerate(st.session_state.memory, start=1):
            st.write(f"{idx}. {entry}")
    else:
        st.write("No messages yet. Ask a question to build session memory.")

st.divider()
st.caption("Mini Project • AI Agent Development • FastAPI / Streamlit • Comprehensive Knowledge & Question Engine")
