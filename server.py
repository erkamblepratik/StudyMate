import os
import re
import ast
import operator
import json
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import knowledge_bank

load_dotenv()

app = FastAPI(
    title="StudyMate AI API",
    description="Backend API and web server for StudyMate AI Study Assistant Agent",
    version="2.1.0"
)

# Global tracker for quota status to avoid repeated 429 errors
OPENAI_QUOTA_EXHAUSTED = False

# Safe Calculator Implementation
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_calculate(expression: str):
    """Safely evaluates an arithmetic expression using AST parsing."""
    cleaned = expression.strip()
    cleaned = cleaned.replace("×", "*").replace("÷", "/").replace("^", "**")
    
    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Only numbers and arithmetic operators (+, -, *, /, %, **, parentheses) are supported.")

    if len(cleaned) > 120:
        raise ValueError("Expression is too long (maximum 120 characters).")
    
    try:
        parsed = ast.parse(cleaned, mode="eval").body
        res = _eval(parsed)
        if isinstance(res, float) and res.is_integer():
            return int(res)
        elif isinstance(res, float):
            return round(res, 6)
        return res
    except Exception as exc:
        raise ValueError(f"{exc}")

def looks_like_arithmetic(text: str) -> bool:
    """Detects if a user input looks like a raw math expression (e.g. '12 + 8 * 3')."""
    t = text.strip()
    if len(t) < 3 or len(t) > 60:
        return False
    # Check if string consists primarily of digits, operators, parentheses, and spaces
    math_chars = set("0123456789+-*/%^(). ×÷")
    has_operator = any(op in t for op in ["+", "-", "*", "/", "%", "^", "×", "÷"])
    has_digit = any(c.isdigit() for c in t)
    return has_operator and has_digit and all(c in math_chars for c in t)

# Core Subject Knowledge Bank
SUBJECT_KNOWLEDGE = {
    "AI Agent Development": {
        "summary": "AI Agents are autonomous computational systems that perceive environmental context, reason using models or heuristics, and execute goal-directed actions using external tools.",
        "key_concepts": [
            "Perception-Action Loop (Sensors & Actuators)",
            "Reasoning Architectures (ReAct, Chain-of-Thought, Tool Use)",
            "Memory Systems (Short-term working context vs Long-term vector stores)",
            "Agent Safety Guardrails & Human-in-the-loop Controls"
        ],
        "quiz": [
            {"q": "What is the primary difference between a passive LLM and an AI Agent?", "a": "An AI Agent has agency to use external tools, maintain persistent state/memory, and autonomously perform multi-step planning to accomplish goals."},
            {"q": "What does the ReAct framework stand for?", "a": "Reasoning and Acting — interleaving thought generation ('Thought') with tool execution ('Action') and environment feedback ('Observation')."},
            {"q": "Why is tool calling essential for AI agents?", "a": "It enables LLMs to overcome model knowledge cutoffs, perform exact mathematical calculations, and interact with external databases or APIs."}
        ]
    },
    "Machine Learning": {
        "summary": "Machine Learning focuses on algorithms that learn statistical patterns from data to make predictions or decisions without explicit rule-based programming.",
        "key_concepts": [
            "Supervised vs Unsupervised vs Reinforcement Learning",
            "Bias-Variance Tradeoff & Overfitting Prevention",
            "Loss Functions & Gradient Descent Optimization",
            "Evaluation Metrics: Precision, Recall, F1-Score, ROC-AUC"
        ],
        "quiz": [
            {"q": "What causes high variance (overfitting) in a model?", "a": "The model fits training data noise too closely and fails to generalize to unseen test data."},
            {"q": "What is the role of the learning rate in Gradient Descent?", "a": "It controls the step size taken towards the minimum of the loss function in each iteration."},
            {"q": "When is F1-score preferred over accuracy?", "a": "When dealing with imbalanced datasets where predicting the majority class yields deceptively high accuracy."}
        ]
    },
    "Operating Systems": {
        "summary": "An Operating System manages computer hardware, allocates system resources, and provides common services for application programs.",
        "key_concepts": [
            "Process Management, Threads, and CPU Scheduling (FCFS, SJF, Round Robin)",
            "Concurrency, Race Conditions, Semaphores & Mutexes",
            "Deadlock Conditions (Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait)",
            "Memory Management: Virtual Memory, Paging, TLB, Page Replacement (LRU, FIFO)"
        ],
        "quiz": [
            {"q": "Name the 4 Coffman conditions required for a deadlock to occur.", "a": "1. Mutual Exclusion, 2. Hold and Wait, 3. No Preemption, 4. Circular Wait."},
            {"q": "What is thrashing in virtual memory?", "a": "A condition where the CPU spends more time swapping pages in and out of secondary storage than executing actual processes."},
            {"q": "What is the key difference between a process and a thread?", "a": "A process has an isolated address space and file descriptors; threads within the same process share code and heap data but maintain private registers and stacks."}
        ]
    },
    "Compiler Design": {
        "summary": "Compiler Design encompasses the phases and algorithms that translate human-readable source code into efficient target machine code.",
        "key_concepts": [
            "Lexical Analysis (Tokenization, Regular Expressions, Finite Automata)",
            "Syntax Analysis (Context-Free Grammars, LL/LR Parsers, Abstract Syntax Trees)",
            "Semantic Analysis (Type Checking, Symbol Tables, Scope Verification)",
            "Intermediate Code Generation (3-Address Code) & Target Code Optimization"
        ],
        "quiz": [
            {"q": "What is the output of the Lexical Analyzer (Scanner)?", "a": "A stream of tokens with token identifiers and corresponding attribute values."},
            {"q": "What is the difference between LL and LR parsers?", "a": "LL parsers are top-down (Left-to-right, Leftmost derivation); LR parsers are bottom-up (Left-to-right, Rightmost derivation in reverse)."},
            {"q": "Why is an Intermediate Representation (IR) used?", "a": "It decouples the front-end (source language) from the back-end (target architecture) and enables reusable architecture-independent code optimizations."}
        ]
    },
    "Data Structures": {
        "summary": "Data Structures are specialized formats for organizing, processing, retrieving, and storing data efficiently in memory.",
        "key_concepts": [
            "Linear Structures: Arrays, Linked Lists, Stacks, and Queues",
            "Hierarchical Structures: Binary Search Trees, AVL Trees, Red-Black Trees, Heaps",
            "Graphs: Representations (Adjacency Matrix/List), Traversal (BFS, DFS), Shortest Path",
            "Asymptotic Analysis: Big-O, Big-Omega, Big-Theta notation"
        ],
        "quiz": [
            {"q": "What is the worst-case search time in an unbalanced BST vs an AVL tree?", "a": "O(N) in a skewed BST; O(log N) in an AVL tree because it maintains height balance."},
            {"q": "Which data structure is used to implement Breadth-First Search (BFS)?", "a": "A Queue (FIFO order)."},
            {"q": "What is the average and worst-case time complexity of QuickSort?", "a": "Average case is O(N log N); worst case is O(N²) when pivot selection is poor (e.g., sorted array with last element as pivot)."}
        ]
    },
    "Computer Networks": {
        "summary": "Computer Networks study interconnected computing devices exchanging data using established protocol suites like OSI and TCP/IP.",
        "key_concepts": [
            "OSI 7-Layer Reference Model vs TCP/IP 4-Layer Architecture",
            "IP Addressing, Subnetting, CIDR, and Routing Protocols (OSPF, BGP)",
            "Transport Layer: TCP (Reliable, Flow & Congestion Control) vs UDP (Datagram, Low Latency)",
            "Application Protocols: HTTP/HTTPS, DNS, TLS/SSL Cryptography"
        ],
        "quiz": [
            {"q": "Explain the TCP 3-way handshake process.", "a": "1. Client sends SYN, 2. Server replies with SYN-ACK, 3. Client sends ACK to establish the connection."},
            {"q": "What is the purpose of the ARP (Address Resolution Protocol)?", "a": "It resolves a known logical IP network address to a physical hardware MAC address on the local link."},
            {"q": "Why is UDP preferred over TCP for live audio/video streaming?", "a": "UDP has minimal header overhead and avoids retransmission delays and flow control stalls, making it ideal for real-time traffic."}
        ]
    },
    "Database Management Systems": {
        "summary": "Database Management Systems (DBMS) organize, manage, and query structured data with ACID guarantees, relational schemas, and indexing.",
        "key_concepts": [
            "3-Schema Architecture & Data Independence",
            "Relational Algebra & SQL (DDL, DML, Joins, Aggregation)",
            "Normalization: 1NF, 2NF, 3NF, BCNF & Functional Dependencies",
            "Transactions & ACID Guarantees (2PL, Serializability, WAL)",
            "Indexing: B-Trees, B+ Trees, Clustered vs Non-Clustered"
        ],
        "quiz": [
            {"q": "What are the ACID properties?", "a": "Atomicity, Consistency, Isolation, and Durability."},
            {"q": "Explain 3NF vs BCNF.", "a": "3NF allows X -> Y if X is a superkey OR Y is a prime attribute. BCNF strictly requires X to be a superkey for every functional dependency."}
        ]
    },
    "Other": {
        "summary": "General Computer Science, Software Engineering, Database Systems, and Academic Problem Solving.",
        "key_concepts": [
            "Database Systems: Relational SQL, ACID Transactions, Normalization (1NF to BCNF)",
            "Software Architecture: Object-Oriented Design, SOLID Principles, Design Patterns",
            "Web Technologies: REST APIs, HTTP Verbs, State Management, Authentication (JWT/OAuth)",
            "Algorithms: Divide & Conquer, Dynamic Programming, Greedy Heuristics"
        ],
        "quiz": [
            {"q": "What do the ACID properties stand for in database management?", "a": "Atomicity, Consistency, Isolation, and Durability."},
            {"q": "What is the difference between synchronous and asynchronous operations?", "a": "Synchronous operations block execution until the task finishes; asynchronous operations run in the background and notify via callbacks or promises without blocking."},
            {"q": "What is the Single Responsibility Principle (SRP) in SOLID?", "a": "A module or class should have only one reason to change, meaning it should perform only one cohesive responsibility."}
        ]
    }
}

# Dedicated Concept Explanations Library
CONCEPT_LIBRARY = {
    "deadlock": {
        "title": "Deadlock in Operating Systems",
        "definition": "A deadlock is a situation where a set of processes are blocked because each process is holding a resource and waiting for another resource acquired by some other process.",
        "coffman_conditions": [
            "**Mutual Exclusion:** Only one process can use the resource at a time.",
            "**Hold and Wait:** A process is holding at least one resource and waiting for others.",
            "**No Preemption:** Resources cannot be forcibly taken from a process.",
            "**Circular Wait:** A circular chain of processes exists where each waits for a resource held by the next."
        ],
        "handling": "Deadlock prevention (eliminating one of the 4 conditions), Avoidance (Banker's Algorithm), or Detection & Recovery (process termination / resource preemption).",
        "exam_tip": "In exams, always draw a Resource Allocation Graph (RAG) with cycles to illustrate Circular Wait!"
    },
    "virtual memory": {
        "title": "Virtual Memory and Paging",
        "definition": "Virtual memory is a memory management technique that provides an idealized abstraction of the storage resources that are actually available on a given machine, allowing processes larger than physical RAM to execute.",
        "key_points": [
            "**Paging:** Logical address space is divided into fixed-size blocks called *Pages*; physical memory is divided into *Frames*.",
            "**Page Table:** Maps logical page numbers to physical frame numbers.",
            "**TLB (Translation Lookaside Buffer):** High-speed hardware associative cache that stores recent page translations to reduce memory access latency.",
            "**Page Fault:** Occurs when a referenced page is not present in RAM, triggering OS interrupt to fetch it from disk."
        ],
        "exam_tip": "Be prepared to calculate Effective Memory Access Time (EMAT): `EMAT = Hit_Ratio * (TLB_time + Mem_time) + (1 - Hit_Ratio) * (TLB_time + 2*Mem_time + Page_fault_time)`."
    },
    "process vs thread": {
        "title": "Process vs Thread Comparison",
        "definition": "A process is an executing instance of a program with its own memory space, while a thread is a lightweight execution unit within a process.",
        "comparison_table": """| Feature | Process | Thread |
| :--- | :--- | :--- |
| **Address Space** | Isolated private address space | Shares address space with parent process |
| **Creation Overhead** | High (heavyweight context switch) | Low (lightweight creation) |
| **Communication** | IPC (Pipes, Sockets, Shared Memory) | Direct memory access (global variables) |
| **Termination Impact** | Crash of one doesn't affect others | Unhandled crash can terminate whole process |
| **Resources** | Separate PCB, memory, file handles | Private stack and registers; shared code/heap |"""
    },
    "overfitting": {
        "title": "Overfitting vs Underfitting (Bias-Variance Tradeoff)",
        "definition": "Overfitting occurs when a machine learning model learns the training data and its noise too closely, failing to generalize to new, unseen test data.",
        "solutions": [
            "**Regularization:** L1 (Lasso) and L2 (Ridge) penalty on large weights.",
            "**Cross-Validation:** K-Fold cross-validation to evaluate generalization.",
            "**Data Augmentation:** Increasing dataset variety and volume.",
            "**Early Stopping & Dropout:** Halting training when validation loss degrades; dropping neurons randomly."
        ],
        "exam_tip": "High variance = Overfitting (fits train well, fails test). High bias = Underfitting (model too simplistic)."
    },
    "gradient descent": {
        "title": "Gradient Descent Optimization",
        "definition": "Gradient Descent is a first-order iterative optimization algorithm used to find a local minimum of a differentiable cost function.",
        "update_rule": "`θ = θ - α * ∇J(θ)` where `θ` is parameters, `α` is the learning rate, and `∇J(θ)` is the gradient.",
        "variants": [
            "**Batch Gradient Descent:** Uses entire dataset per step (slow, smooth convergence).",
            "**Stochastic Gradient Descent (SGD):** Uses 1 sample per step (fast, noisy convergence).",
            "**Mini-batch Gradient Descent:** Uses batches of 32/64/128 samples (standard in deep learning)."
        ]
    },
    "react framework": {
        "title": "ReAct Framework (Reasoning + Acting) in AI Agents",
        "definition": "ReAct is an agent architecture that combines verbal reasoning traces ('Thoughts') with task-specific actions ('Actions') and observations ('Observations') in an interleaved execution loop.",
        "loop": "1. **Thought:** The agent reasons about current state and determines what information is missing.\n2. **Action:** The agent calls a tool (e.g. `calculate:`, `web_search`, `query_db`).\n3. **Observation:** The tool executes and returns real-world output.\n4. **Repeat:** The agent synthesizes the observation into the next reasoning step until the goal is solved.",
        "exam_tip": "ReAct prevents hallucinations because tool observations ground the agent's thoughts in verified external facts."
    },
    "quicksort": {
        "title": "QuickSort Algorithm",
        "definition": "QuickSort is a divide-and-conquer sorting algorithm that selects a 'pivot' element and partitions array elements into two sub-arrays according to whether they are less than or greater than the pivot.",
        "complexity": "- **Best Case:** `O(N log N)`\n- **Average Case:** `O(N log N)`\n- **Worst Case:** `O(N²)` (occurs when pivot is smallest/largest element consistently, e.g. already sorted array with naive pivot)\n- **Space Complexity:** `O(log N)` auxiliary stack space.",
        "exam_tip": "Use Randomized Pivot selection or Median-of-Three to practically avoid the O(N²) worst-case scenario."
    },
    "tcp vs udp": {
        "title": "TCP vs UDP Protocol Comparison",
        "definition": "TCP and UDP are the two primary Transport Layer protocols in the Internet protocol suite.",
        "comparison_table": """| Attribute | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Connection** | Connection-oriented (3-way handshake) | Connectionless (no handshake) |
| **Reliability** | Guaranteed delivery (retransmits lost packets) | Best-effort (packets may drop or arrive out of order) |
| **Flow/Congestion Control** | Yes (Sliding Window, Congestion Avoidance) | No |
| **Header Size** | 20 to 60 bytes | 8 bytes fixed |
| **Use Cases** | Web (HTTP/HTTPS), File Transfer (FTP), Email (SMTP) | DNS, VoIP, Online Gaming, Live Video Streaming |"""
    },
    "ai agent": {
        "title": "AI Agent Development",
        "simple_analogy": (
            "Think of a traditional AI (like a search bar or basic chatbot) as a **consultant behind a glass window** — it can only answer with words, but cannot touch the keyboard or do work for you.\n\n"
            "An **AI Agent**, on the other hand, is like a **proactive personal assistant with hands**: you give it a goal, and it:\n"
            "1. **Perceives (Sees):** Takes in your prompt and environment.\n"
            "2. **Reasons (Thinks):** Breaks the problem down into a step-by-step plan.\n"
            "3. **Acts (Uses Tools):** Calls external tools (calculator, database, code execution, web APIs).\n"
            "4. **Remembers (Memory):** Keeps track of past actions, errors, and progress across the session."
        ),
        "definition": "An AI Agent is an autonomous system that uses an LLM or reasoning engine to perceive its environment, formulate multi-step plans, and execute actions using external tools to achieve specific goals.",
        "key_points": [
            "**The Brain (Reasoning):** Uses LLM planning or ReAct (Reason + Act) loop to decide what to do next.",
            "**The Hands (Tools):** External tools like Safe Calculator (`calculate:`), databases, or API integrations.",
            "**Memory (Context):** Short-term working session memory + Long-term knowledge base.",
            "**Guardrails (Safety):** Security boundaries, like AST parsing to prevent code injection."
        ],
        "example": "In StudyMate: When you type `calculate: (15 * 8) + 2^4`, a passive chatbot might hallucinate the math. StudyMate as an **AI Agent** detects the math, routes it to its Safe Calculator tool, computes `136` safely, and returns the verified result!",
        "exam_tip": "In an exam, always draw the **Perception → Reasoning (LLM) → Tool Action → Environment Feedback** loop!"
    },
    "machine learning": {
        "title": "Machine Learning",
        "simple_analogy": (
            "Imagine teaching a child to recognize a cat: you don't write down 10,000 rules about whiskers and tail angles. Instead, you show them hundreds of pictures of cats until their brain naturally learns the patterns.\n\n"
            "That is **Machine Learning**: instead of hand-coding every rule, we give algorithms large datasets, and the algorithm automatically discovers the underlying mathematical patterns to make predictions."
        ),
        "definition": "Machine Learning is a subset of Artificial Intelligence where statistical algorithms learn patterns directly from training data to make predictions or decisions on unseen test data without being explicitly programmed.",
        "key_points": [
            "**Supervised Learning:** Learns from labeled data (Input X → Known Label Y). E.g. Spam detection, house price prediction.",
            "**Unsupervised Learning:** Finds hidden structure in unlabeled data. E.g. Customer segmentation, K-Means clustering.",
            "**Reinforcement Learning:** Learns through trial-and-error rewards and penalties. E.g. Chess engines, self-driving agents.",
            "**Overfitting:** When a model memorizes training noise and fails on new real-world data."
        ],
        "example": "Predicting exam scores based on hours studied: Model fits a regression line `Score = m * Hours + c` by minimizing the mean squared error loss function using Gradient Descent.",
        "exam_tip": "Focus on the **Bias-Variance Tradeoff**: High Bias = Underfitting (too simple), High Variance = Overfitting (too complex)."
    },
    "operating systems": {
        "title": "Operating Systems",
        "simple_analogy": (
            "Think of your computer hardware (CPU, RAM, Hard Disk) as a busy **restaurant kitchen**, and application programs (Chrome, Spotify, Code Editor) as the **customers**.\n\n"
            "The **Operating System** is the **Head Chef / Restaurant Manager**: it decides which order gets cooked first on the stove (CPU scheduling), who gets which table (RAM allocation), and makes sure two orders don't ruin each other's ingredients (process isolation and memory protection)."
        ),
        "definition": "An Operating System (OS) is core system software that acts as an intermediary between computer hardware and user applications, managing CPU scheduling, memory, files, and I/O devices.",
        "key_points": [
            "**Process Management:** Creating, scheduling, and synchronizing processes and threads.",
            "**Memory Management:** Virtual memory, paging, and frame allocation to isolate application address spaces.",
            "**File Systems:** Organizing files hierarchically with metadata and security permissions.",
            "**Device Drivers:** Translating standard OS commands into specific hardware signals."
        ],
        "example": "When you switch tabs from your browser to VS Code, the OS performs a **Context Switch**: saving CPU registers of the browser process and loading the state of VS Code in milliseconds.",
        "exam_tip": "High-yield exam topics: Process vs Thread, 4 Coffman Deadlock conditions, and Paging with TLB calculation."
    },
    "compiler design": {
        "title": "Compiler Design",
        "simple_analogy": (
            "Imagine a Shakespearean play written in old English that needs to be performed by actors who only speak binary morse code.\n\n"
            "A **Compiler** is the master translator: it reads your high-level human code (Python, C++, Java), checks every sentence for grammar mistakes, removes redundant words (optimization), and converts it into pure, high-speed machine instructions (0s and 1s) that the CPU can execute."
        ),
        "definition": "A Compiler is a specialized software program that translates human-readable source code into equivalent machine code or bytecode through multiple systematic phases.",
        "key_points": [
            "**Phase 1 - Lexical Analysis (Scanner):** Converts raw characters into a stream of tokens.",
            "**Phase 2 - Syntax Analysis (Parser):** Validates tokens against grammar rules and builds an Abstract Syntax Tree (AST).",
            "**Phase 3 - Semantic Analysis:** Type checking, variable declaration verification, and symbol tables.",
            "**Phase 4 - Optimization & Code Generation:** Converts to 3-address intermediate representation and emits target machine instructions."
        ],
        "example": "StudyMate's Safe Calculator uses **Python's `ast.parse`** (the same syntax analysis phase a compiler uses) to inspect your math expression and reject dangerous system calls!",
        "exam_tip": "Always remember the difference between LL (Top-down) and LR (Bottom-up) parsers!"
    }
}


def generate_study_plan(subject: str, level: str) -> str:
    """Generates a proper day-wise revision timetable starting from Day 1 foundations."""
    return knowledge_bank.format_day_wise_timetable(subject, level)

def generate_quiz(subject: str, level: str, count: int = 35) -> str:
    """Generates 30 to 50 setup & practice questions with revealable solutions."""
    return knowledge_bank.format_quiz_output(subject, level, count=count)


def clean_topic_query(text: str):
    """Cleans user query prefixes and detects if a simple explanation was requested."""
    t = text.strip()
    is_simple = False
    prefixes = [
        "explain in simple words:",
        "explain in simple words",
        "explain in simple terms:",
        "explain in simple terms",
        "explain in plain english:",
        "explain in plain english",
        "simple explanation of:",
        "simple explanation of",
        "explain simply:",
        "explain simply",
        "explain:",
        "explain",
        "what is:",
        "what is",
        "what are:",
        "what are",
        "meaning of:",
        "meaning of",
        "define:",
        "define",
        "tell me about:",
        "tell me about"
    ]
    t_lower = t.lower()
    for p in prefixes:
        if t_lower.startswith(p):
            if "simple" in p or "plain" in p or "simply" in p:
                is_simple = True
            t = t[len(p):].strip()
            t_lower = t.lower()
            break
    t = t.lstrip(":- ").strip()
    if "simple words" in text.lower() or "simple terms" in text.lower() or "beginner" in text.lower():
        is_simple = True
    return (t if t else text, is_simple)

def generate_concept_explanation(topic: str, subject: str, level: str) -> str:
    cleaned_topic, is_simple_requested = clean_topic_query(topic)
    cleaned_lower = cleaned_topic.lower()
    
    # Check concept library
    for key, c in CONCEPT_LIBRARY.items():
        if key in cleaned_lower or cleaned_lower in key or (key in subject.lower() and len(cleaned_topic) < 4):
            title = c['title']
            out = [f"### 💡 {title}\n"]
            out.append(f"**Academic Subject:** `{subject}` • **Target Level:** `{level}`\n")
            
            # Simple Analogy First if available
            if "simple_analogy" in c:
                out.append(f"#### 🌟 Intuition in Simple Words\n{c['simple_analogy']}\n")
            elif "definition" in c:
                out.append(f"#### 📖 Definition\n{c['definition']}\n")
                
            if "comparison_table" in c:
                out.append(f"#### ⚖️ Detailed Comparison Table\n{c['comparison_table']}\n")
            if "coffman_conditions" in c:
                out.append("#### 🔒 Required Conditions\n" + "\n".join(f"- {cond}" for cond in c['coffman_conditions']) + "\n")
            if "key_points" in c:
                out.append("#### 🏗️ Core Architectural Blocks\n" + "\n".join(f"- {p}" for p in c['key_points']) + "\n")
            if "example" in c:
                out.append(f"#### 🔍 Practical Example\n{c['example']}\n")
            if "solutions" in c:
                out.append("#### 🛡️ Prevention & Solutions\n" + "\n".join(f"- {s}" for s in c['solutions']) + "\n")
            if "loop" in c:
                out.append(f"#### 🔄 Execution Loop\n{c['loop']}\n")
            if "complexity" in c:
                out.append(f"#### ⏱️ Complexity Analysis\n{c['complexity']}\n")
            if "exam_tip" in c:
                out.append(f"> 🎯 **University Exam Tip:**\n> {c['exam_tip']}\n")
            return "\n".join(out)

    info = SUBJECT_KNOWLEDGE.get(subject, SUBJECT_KNOWLEDGE["Other"])
    summary_text = info.get("summary", f"Fundamental principles of {subject}.")
    
    return f"""### 💡 {cleaned_topic.title()} — Concept Breakdown
**Subject:** `{subject}` • **Level:** `{level}`

#### 🌟 Intuition in Simple Words
{summary_text}
Think of **{cleaned_topic.title()}** as a structured solution to a specific computer science challenge: it defines what inputs are required, the rules of transformation, and the verified outcome.

#### 🏗️ Key Pillars & Workflow
- **The Core Function:** Understand what problem statement it addresses before memorizing syntax.
- **The Trade-off:** Balance execution time complexity against RAM usage and engineering simplicity.
- **Real-World Application:** Used extensively in scalable software systems to ensure reliability, correctness, and performance.

#### 🎯 University Exam Checklist
- [x] Clear formal technical definition with standard notation.
- [x] Labeled block diagram or step-by-step trace table.
- [x] Time & Space complexity bounds where applicable.
- [x] Practical engineering use-case.

*(💡 Want practice questions on this? Ask "quiz on {cleaned_topic}" or request a study timetable!)*"""


def smart_offline_reply(question: str, subject: str, level: str, student_name: str = "Student") -> Dict[str, Any]:
    """Rich conversational academic assistant for offline and zero-quota execution."""
    q = question.strip()
    q_lower = q.lower()
    
    # 1. Greetings & Conversation
    greeting_triggers = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "howdy", "sup", "hola"]
    if any(q_lower == g or q_lower.startswith(g + " ") or q_lower.startswith(g + "!") or q_lower.startswith(g + ",") for g in greeting_triggers):
        reply = (
            f"### 👋 Hello, {student_name}!\n\n"
            f"Welcome to **StudyMate AI**! I'm your academic study assistant, ready to help you with **{subject}** at the **{level}** level.\n\n"
            f"Here are a few ways we can study right now:\n"
            f"- 💡 **Ask a Concept:** Ask me to explain any topic, algorithm, or comparison.\n"
            f"- 🧮 **Safe Calculator:** Type `calculate: (12+8)*3` or raw math expressions.\n"
            f"- 📅 **Study Planner:** Ask for a *study plan* or *revision timetable*.\n"
            f"- 📝 **Practice Quiz:** Ask for a *quiz* with revealable exam answers.\n\n"
            f"What would you like to explore today?"
        )
        return {"reply": reply, "tool_used": "conversational_greeting", "mode": "smart_offline"}

    # 2. Politeness / How are you
    if "how are you" in q_lower or "how're you" in q_lower:
        reply = (
            f"I'm running smoothly and fully prepared to help you study, {student_name}! 🎓\n\n"
            f"We are currently configured for **{subject}** ({level} level). "
            f"What topic, theorem, or question would you like to tackle?"
        )
        return {"reply": reply, "tool_used": "conversational", "mode": "smart_offline"}

    # 3. Who are you / Identity
    if "who are you" in q_lower or "what are you" in q_lower or "what can you do" in q_lower:
        reply = (
            f"### 🎓 About StudyMate AI\n\n"
            f"I am **StudyMate AI**, an intelligent student study assistant agent built for B.Tech AI Agent Development.\n\n"
            f"**My Core Capabilities:**\n"
            f"1. **Concept Explainer:** Deep pedagogical breakdowns with intuition, math, and exam tips.\n"
            f"2. **AST-Verified Safe Calculator:** Safe arithmetic evaluator that prevents code injection.\n"
            f"3. **Study Planner:** Adaptive Pomodoro revision timetables.\n"
            f"4. **Practice Quiz Engine:** Active recall testing with hidden answer accordions.\n"
            f"5. **Session Memory:** Stores and recalls session queries and study notes."
        )
        return {"reply": reply, "tool_used": "conversational_info", "mode": "smart_offline"}

    # 4. Thank you
    if "thank" in q_lower or "thanks" in q_lower:
        reply = f"You're very welcome, {student_name}! Keep up the great focus. Let me know if you need another concept broken down or a practice quiz!"
        return {"reply": reply, "tool_used": "conversational", "mode": "smart_offline"}

    # 5. Help / Assistance
    if q_lower == "help" or q_lower == "/help":
        reply = (
            f"### 🆘 StudyMate Quick Guide\n\n"
            f"- **Math:** `calculate: (25 * 4) + 120 / 4` or enter math expressions in the calculator modal.\n"
            f"- **Timetable:** Type `make a study plan for {subject}`.\n"
            f"- **Quiz:** Type `give me a quiz on {subject}`.\n"
            f"- **Explanations:** Type `explain deadlock`, `explain quicksort`, or `tcp vs udp`.\n"
            f"- **Settings:** Click ⚙️ to configure custom API keys or toggle audio feedback."
        )
        return {"reply": reply, "tool_used": "help", "mode": "smart_offline"}

    # 6. Safe Calculator (explicit or auto-detected)
    if q_lower.startswith("calculate:") or q_lower.startswith("calc:"):
        expr = q.split(":", 1)[1].strip()
        try:
            res = safe_calculate(expr)
            reply = (
                f"### 🧮 Safe Calculator Result\n\n"
                f"**Expression:** `{expr}`\n\n"
                f"**Result:** `{res}`\n\n"
                f"```text\n{expr} = {res}\n```"
            )
            return {"reply": reply, "tool_used": "calculator", "result": res, "mode": "smart_offline"}
        except Exception as exc:
            return {
                "reply": f"⚠️ **Calculator Error:** Could not evaluate expression `{expr}`.\n\n*Reason:* {exc}\n\n*Tip:* Use standard numbers and operators (+, -, *, /, %, **, parentheses).",
                "tool_used": "calculator",
                "error": str(exc),
                "mode": "smart_offline"
            }

    if looks_like_arithmetic(q):
        try:
            res = safe_calculate(q)
            reply = (
                f"### 🧮 Safe Calculation\n\n"
                f"**Input:** `{q}`\n\n"
                f"**Result:** `{res}`\n\n"
                f"```text\n{q} = {res}\n```"
            )
            return {"reply": reply, "tool_used": "calculator", "result": res, "mode": "smart_offline"}
        except Exception:
            pass

    # 7. Study Planner (Day-Wise Timetable starting with Day 1 basics)
    if any(k in q_lower for k in ["study plan", "timetable", "time table", "schedule", "routine", "revision plan", "day wise", "day-wise", "day 1", "days plan"]):
        return {"reply": generate_study_plan(subject, level), "tool_used": "study_planner", "mode": "smart_offline"}

    # 8. Quiz & Setup Questions Generator (30 to 50 questions per subject)
    if any(k in q_lower for k in ["quiz", "practice", "mcq", "test me", "questions", "mock test", "setup question", "setup questions", "question bank"]):
        # Extract requested number of questions if student specified a count
        count = 35
        m = re.search(r'(\d+)\s*(?:questions?|mcqs?|q\b)', q_lower)
        if m:
            try:
                count = max(1, min(50, int(m.group(1))))
            except ValueError:
                count = 35
        return {"reply": generate_quiz(subject, level, count=count), "tool_used": "quiz_generator", "mode": "smart_offline"}

    # 9. Concept Explanation / Comparison (Known library topics)
    for key in CONCEPT_LIBRARY:
        if key in q_lower:
            return {"reply": generate_concept_explanation(key, subject, level), "tool_used": "concept_explainer", "mode": "smart_offline"}

    # 10. Universal Question Answering (Answers ANY question asked by student)
    answered_text = knowledge_bank.answer_any_question(q, subject, level, student_name)
    return {"reply": answered_text, "tool_used": "academic_knowledge_engine", "mode": "smart_offline"}


def call_gemini_api(api_key: str, question: str, subject: str, level: str, history: List[Dict[str, str]] = None, student_name: str = "Student") -> Optional[str]:
    """Calls Google Gemini Free API tier (15 requests/min completely free, no credit card needed)."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        system_instruction = (
            f"You are StudyMate, a helpful, encouraging, and clear academic tutor for college student {student_name}.\n"
            f"Subject: {subject}. Target understanding level: {level}.\n"
            f"Format answers with clear markdown headings, bullet points, intuitive explanations, and examples."
        )
        contents = []
        if history:
            for item in history[-6:]:
                role = "user" if item.get("role") == "user" else "model"
                contents.append({"role": role, "parts": [{"text": item.get("content", "")}]})
        
        contents.append({"role": "user", "parts": [{"text": f"[{system_instruction}]\n\n{question}"}]})
        
        payload = {"contents": contents}
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        if res.status_code == 200:
            data = res.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
    except Exception as exc:
        print("Gemini API error:", exc)
    return None

def call_groq_api(api_key: str, question: str, subject: str, level: str, history: List[Dict[str, str]] = None, student_name: str = "Student") -> Optional[str]:
    """Calls Groq Free API endpoint with Llama 3.3 70B (free, ultra fast)."""
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        system_prompt = (
            f"You are StudyMate, an academic study assistant for college student {student_name}. "
            f"Subject: {subject}. Target Level: {level}. Explain clearly with markdown, intuition, and examples."
        )
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            for item in history[-6:]:
                messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})
        messages.append({"role": "user", "content": question})
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        res = requests.post(url, json=payload, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return data["choices"][0]["message"]["content"]
    except Exception as exc:
        print("Groq API error:", exc)
    return None

def llm_reply(question: str, subject: str, level: str, history: List[Dict[str, str]], api_key: Optional[str] = None, student_name: str = "Student") -> Dict[str, Any]:
    global OPENAI_QUOTA_EXHAUSTED
    
    # Check for direct calculations first
    q_stripped = question.strip()
    if q_stripped.lower().startswith("calculate:") or looks_like_arithmetic(q_stripped):
        return smart_offline_reply(question, subject, level, student_name)

    # Check for greetings first before burning API tokens
    greeting_triggers = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "how are you", "who are you", "what can you do"]
    if any(q_stripped.lower() == g or q_stripped.lower().startswith(g + " ") for g in greeting_triggers):
        return smart_offline_reply(question, subject, level, student_name)

    # Route timetable and quiz/question requests directly to dedicated academic engine
    if any(k in q_stripped.lower() for k in ["study plan", "timetable", "time table", "schedule", "routine", "day wise", "day-wise", "quiz", "setup question", "setup questions", "practice question"]):
        return smart_offline_reply(question, subject, level, student_name)

    active_key = (api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY", "")).strip()

    # 1. Google Gemini (Starts with AIza) - Free API
    if active_key.startswith("AIza"):
        gemini_output = call_gemini_api(active_key, question, subject, level, history, student_name)
        if gemini_output:
            return {"reply": gemini_output, "mode": "gemini", "tool_used": "llm_gemini"}

    # 2. Groq (Starts with gsk_) - Free API
    if active_key.startswith("gsk_"):
        groq_output = call_groq_api(active_key, question, subject, level, history, student_name)
        if groq_output:
            return {"reply": groq_output, "mode": "groq", "tool_used": "llm_groq"}

    # 3. Check env-configured Gemini/Groq keys if available
    env_gemini = os.getenv("GEMINI_API_KEY", "").strip()
    if env_gemini and not active_key.startswith("AIza"):
        gemini_output = call_gemini_api(env_gemini, question, subject, level, history, student_name)
        if gemini_output:
            return {"reply": gemini_output, "mode": "gemini", "tool_used": "llm_gemini"}

    # 4. OpenAI Key (Starts with sk-)
    openai_key = (api_key or os.getenv("OPENAI_API_KEY", "")).strip()
    
    # If key is empty or known to have exhausted quota, use smart offline engine directly
    if not openai_key or OPENAI_QUOTA_EXHAUSTED or not openai_key.startswith("sk-"):
        res = smart_offline_reply(question, subject, level, student_name)
        if OPENAI_QUOTA_EXHAUSTED:
            res["quota_note"] = "OpenAI credits exhausted ($0 balance). Answering via built-in smart academic engine."
        return res
        
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        
        system_prompt = (
            f"You are StudyMate, an exceptionally clear, supportive, and pedagogical academic study assistant agent for college students. "
            f"The student's name is {student_name}. The selected subject is: {subject}. Target understanding level: {level}. "
            f"Formatting rules:\n"
            f"- Use structured markdown with clean headers, bullet points, and code/math blocks.\n"
            f"- If the student asks for explanations, provide intuition first, followed by technical rigor, an exam tip, and a brief example.\n"
            f"- If the student asks for practice or quiz questions, provide questions with answers.\n"
            f"- If calculation is needed, show steps clearly.\n"
            f"- Keep tone encouraging, rigorous, and student-focused."
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
        output = completion.choices[0].message.content
        return {"reply": output, "mode": "openai", "tool_used": "llm_chat"}
        
    except Exception as exc:
        err_str = str(exc)
        # Check if error is quota exhaustion (429)
        if "insufficient_quota" in err_str or "credit_balance_exhausted" in err_str or "429" in err_str:
            OPENAI_QUOTA_EXHAUSTED = True
            fallback = smart_offline_reply(question, subject, level, student_name)
            fallback["reply"] = (
                f"> 💡 *Notice: OpenAI API credit balance is $0. StudyMate is answering using its built-in smart academic engine. (Add a free Google Gemini key in Settings for live AI!)*\n\n"
                + fallback["reply"]
            )
            fallback["mode"] = "smart_offline"
            fallback["quota_exhausted"] = True
            return fallback
            
        fallback = smart_offline_reply(question, subject, level, student_name)
        fallback["reply"] = f"> ⚠️ *Notice: Switched to built-in smart assistant engine ({exc}).*\n\n" + fallback["reply"]
        fallback["mode"] = "offline_fallback"
        return fallback


# Pydantic Request Models
class ChatRequest(BaseModel):
    message: str
    subject: str = "AI Agent Development"
    level: str = "Exam-ready"
    student_name: str = "Pratik Kamble"
    history: List[Dict[str, str]] = []
    api_key: Optional[str] = None

class CalculateRequest(BaseModel):
    expression: str

class KeyValidateRequest(BaseModel):
    api_key: str
    provider: Optional[str] = "openai"

# API Endpoints
@app.get("/api/status")
def get_status():
    has_openai = bool(os.getenv("OPENAI_API_KEY", "").strip())
    has_gemini = bool(os.getenv("GEMINI_API_KEY", "").strip())
    return {
        "status": "ready",
        "app_name": "StudyMate AI",
        "version": "2.1.0",
        "has_openai_key": has_openai,
        "has_gemini_key": has_gemini,
        "quota_exhausted": OPENAI_QUOTA_EXHAUSTED,
        "active_mode": "smart_offline" if (OPENAI_QUOTA_EXHAUSTED or not has_openai) else "openai",
        "default_subject": "AI Agent Development",
        "subjects": list(SUBJECT_KNOWLEDGE.keys()),
        "levels": ["Beginner", "Intermediate", "Exam-ready"],
        "tools": [
            {"id": "calculator", "name": "Safe Calculator", "syntax": "calculate: <expression>"},
            {"id": "study_planner", "name": "Day-Wise Timetable", "syntax": "make timetable for <subject>"},
            {"id": "quiz_generator", "name": "Setup Questions (30-50)", "syntax": "give me 35 questions on <subject>"},
            {"id": "concept_explainer", "name": "Universal Concept Explainer", "syntax": "explain <any topic>"}
        ]
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    result = llm_reply(
        question=req.message,
        subject=req.subject,
        level=req.level,
        history=req.history,
        api_key=req.api_key,
        student_name=req.student_name
    )
    return result

@app.post("/api/calculate")
def calculate_endpoint(req: CalculateRequest):
    try:
        res = safe_calculate(req.expression)
        return {"success": True, "expression": req.expression, "result": res}
    except Exception as exc:
        return {"success": False, "expression": req.expression, "error": str(exc)}

@app.post("/api/validate-key")
def validate_key(req: KeyValidateRequest):
    key = req.api_key.strip()
    if not key:
        return {"valid": False, "message": "Key cannot be blank"}
        
    if key.startswith("AIza") or req.provider == "gemini":
        test_res = call_gemini_api(key, "Say hello", "AI", "Beginner")
        if test_res:
            return {"valid": True, "message": "Google Gemini API key verified successfully! Live AI ready."}
        return {"valid": False, "message": "Gemini key validation failed. Check your key at https://aistudio.google.com/app/apikey"}

    if key.startswith("gsk_") or req.provider == "groq":
        test_res = call_groq_api(key, "Say hello", "AI", "Beginner")
        if test_res:
            return {"valid": True, "message": "Groq API key verified successfully! Llama 3.3 live AI ready."}
        return {"valid": False, "message": "Groq key validation failed. Check your key at https://console.groq.com/keys"}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        client.models.list()
        return {"valid": True, "message": "OpenAI API key verified successfully!"}
    except Exception as exc:
        err = str(exc)
        if "credit_balance_exhausted" in err or "insufficient_quota" in err:
            return {"valid": True, "quota_exhausted": True, "message": "Key is valid, but OpenAI credit balance is $0 (quota exhausted). StudyMate will use the built-in smart assistant engine."}
        return {"valid": False, "message": f"Verification failed: {exc}"}

# Mount static files and serve frontend
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Frontend is loading..."})

if __name__ == "__main__":
    import uvicorn
    print("Starting StudyMate AI Server on http://127.0.0.1:8000")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
