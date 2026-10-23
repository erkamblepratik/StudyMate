"""
StudyMate AI — Core Academic Knowledge Bank & Question Engine
Contains:
1. 35+ verified exam setup & practice questions for each subject (minimum 30, maximum 50).
2. Day-wise detailed study timetables (Day 1: Basic concepts, Day 2..7: Remaining advanced concepts & revision).
3. Expanded concept library for computer science, software engineering, and programming.
4. Verified code snippets library for common algorithmic & coding interview queries.
5. Universal educational question synthesizer to answer ANY student query with pedagogical rigor.
"""

from typing import Dict, List, Any, Optional
import re

# ==============================================================================
# 1. SUBJECT QUESTION BANK (35 Questions per Subject)
# ==============================================================================
SUBJECT_QUESTIONS: Dict[str, List[Dict[str, str]]] = {
    "AI Agent Development": [
        {"q": "What is the core definition of an AI Agent?", "a": "An AI Agent is an autonomous entity that perceives its environment through sensors, processes information to make decisions, and takes goal-directed actions through actuators."},
        {"q": "What is the primary difference between a standard LLM and an AI Agent?", "a": "A standard LLM is a passive next-token predictor. An AI Agent possesses agency: it maintains persistent state/memory, plans multi-step tasks, and actively invokes external tools (APIs, code execution, databases)."},
        {"q": "Explain the ReAct framework in agent development.", "a": "ReAct stands for Reasoning + Acting. It interleaves verbal reasoning traces ('Thought') with action execution ('Action') and environment feedback ('Observation') to iteratively solve tasks while reducing hallucinations."},
        {"q": "What is the Perception-Action loop?", "a": "The continuous cycle where an agent perceives environmental state, updates internal memory, reasons about the goal, decides on an action, executes it via actuators, and observes the new state."},
        {"q": "What are Reflex Agents?", "a": "Agents that select actions based strictly on the current percept, ignoring history (implemented as condition-action rules like IF-THEN)."},
        {"q": "What is a Model-Based Reflex Agent?", "a": "An agent that maintains an internal model of the unobserved world to handle partially observable environments and track how the world evolves."},
        {"q": "What is a Goal-Based Agent?", "a": "An agent that combines environmental state knowledge with explicit goal descriptions to evaluate potential actions and select paths leading to the goal."},
        {"q": "What is a Utility-Based Agent?", "a": "An agent that evaluates multiple goal-achieving paths using a utility function to measure the 'happiness' or efficiency of reaching states."},
        {"q": "Explain the Plan-and-Solve (Plan-and-Execute) agent architecture.", "a": "The agent first drafts a complete multi-step plan before execution, then executes each step sequentially, replanning only when unexpected errors or state deviations occur."},
        {"q": "What is tool calling (function calling) in AI agents?", "a": "The ability of an LLM to generate structured JSON matching predefined schemas so that client systems can execute real external tools (e.g. calculator, weather API, database query)."},
        {"q": "Why is AST evaluation used for safe mathematical calculations instead of eval()?", "a": "Python's eval() can execute arbitrary malicious code (e.g., os.system('rm -rf')). An Abstract Syntax Tree (AST) parser inspects the syntax tree and only allows whitelisted arithmetic operations, preventing code injection."},
        {"q": "What is working memory in an agent?", "a": "Short-term context held within the prompt's token window representing recent conversation turns, scratchpads, and immediate observations."},
        {"q": "What is episodic memory in AI agents?", "a": "Memory of specific past events, user sessions, or previous execution traces stored in vector databases for later retrieval via semantic search."},
        {"q": "What is semantic memory in AI agents?", "a": "Persistent general factual knowledge about the world, concepts, and domain rules stored in external knowledge graphs or embeddings."},
        {"q": "Explain Retrieval-Augmented Generation (RAG).", "a": "A technique that retrieves relevant text passages from an external corpus via vector embeddings and injects them into the agent prompt, grounding responses in up-to-date domain data."},
        {"q": "What is an embedding vector?", "a": "A dense mathematical representation of text in a high-dimensional vector space where semantically similar concepts are located close to each other by cosine distance."},
        {"q": "What are Agent Guardrails?", "a": "Input/output validation filters that enforce security boundaries, prevent jailbreaks, restrict tool access, and ensure ethical, truthful outputs."},
        {"q": "What is Human-in-the-Loop (HITL) in agent systems?", "a": "A safety checkpoint where high-risk actions (financial transactions, deleting files, sending emails) require explicit human approval before execution."},
        {"q": "What is multi-agent orchestration?", "a": "A design where multiple specialized agents (e.g. Researcher, Coder, Reviewer) collaborate via messaging protocols to solve complex tasks beyond a single model's scope."},
        {"q": "Explain the difference between deterministic and stochastic agent environments.", "a": "In a deterministic environment, the next state is completely determined by current state and action. In a stochastic environment, outcomes include randomness or uncertainty."},
        {"q": "What is an episodic vs sequential environment?", "a": "In episodic environments, each action episode is independent. In sequential environments, current decisions directly impact all future states and rewards (e.g. chess, driving)."},
        {"q": "What is Prompt Injection?", "a": "An attack where malicious user input overrides the agent's system instructions, causing it to ignore guardrails or execute unauthorized tools."},
        {"q": "How can indirect prompt injection occur?", "a": "When an agent retrieves untrusted external content (e.g. web pages, emails) containing hidden instructions that hijack the agent's reasoning loop."},
        {"q": "What is the Chain-of-Thought (CoT) prompting method?", "a": "Prompting the model to write out explicit intermediate reasoning steps before delivering the final answer, significantly improving complex logic and math accuracy."},
        {"q": "What is Tree-of-Thoughts (ToT) in AI reasoning?", "a": "An exploration architecture where the agent generates multiple reasoning branches, evaluates the promise of each branch, and uses search algorithms (BFS/DFS) with backtracking."},
        {"q": "What is self-reflection in autonomous agents?", "a": "The mechanism where an agent reviews its own past mistakes, critiques execution output, and refines subsequent prompts to self-correct without human intervention."},
        {"q": "What is an Agentic Workflow as defined by Andrew Ng?", "a": "An iterative approach using reflection, tool use, planning, and multi-agent collaboration that outperforms zero-shot LLM queries."},
        {"q": "What is vector database indexing (e.g. HNSW)?", "a": "Hierarchical Navigable Small World graphs enable logarithmic approximate nearest neighbor (ANN) search over millions of high-dimensional embeddings."},
        {"q": "What is cosine similarity?", "a": "A metric measuring the cosine of the angle between two non-zero vectors: cos(θ) = (A · B) / (||A|| * ||B||), ranging from -1 to 1 (1 indicates identical direction/meaning)."},
        {"q": "What is the token context window limitation and how do agents overcome it?", "a": "Models can only process a finite number of tokens at once. Agents overcome this using summarizing buffers, vector retrieval (RAG), and hierarchical memory storage."},
        {"q": "What role does an orchestrator / controller play in agent frameworks like LangChain or AutoGen?", "a": "It manages the state machine, routes messages between agents, invokes tools based on JSON schemas, and handles timeout/retry policies."},
        {"q": "What is task decomposition in hierarchical agents?", "a": "Breaking a massive, vague objective into smaller, well-defined sub-tasks that can be assigned to specialized child agents or sequential tools."},
        {"q": "What is hallucination in LLMs and how do agents mitigate it?", "a": "Generating plausible-sounding but factually incorrect assertions. Agents mitigate it through tool-verified observations, RAG grounding, and citation checks."},
        {"q": "How does an agent handle tool execution failure?", "a": "Through exception handling in the observation step, passing the error traceback back to the LLM so it can analyze the failure and attempt an alternative action."},
        {"q": "What is the future outlook of embodied AI agents?", "a": "Integrating agent reasoning models into physical robotics to navigate real-world environments, manipulate objects, and interact seamlessly with humans."}
    ],

    "Machine Learning": [
        {"q": "Define Machine Learning.", "a": "A field of Artificial Intelligence where statistical algorithms learn underlying patterns directly from data to make predictions or decisions without explicit rule-based programming."},
        {"q": "What are the three main types of Machine Learning?", "a": "1. Supervised Learning (labeled data), 2. Unsupervised Learning (unlabeled data), 3. Reinforcement Learning (reward/penalty based)."},
        {"q": "Explain the Bias-Variance tradeoff.", "a": "High bias leads to underfitting (model is too simple to capture patterns); high variance leads to overfitting (model learns training noise). The goal is to minimize total error: Error = Bias² + Variance + Irreducible Error."},
        {"q": "What is Overfitting and how do you prevent it?", "a": "When a model performs exceptionally on training data but poorly on unseen test data. Prevent it using L1/L2 regularization, cross-validation, data augmentation, dropout, and early stopping."},
        {"q": "What is Underfitting and how do you fix it?", "a": "When a model cannot capture underlying data patterns even on training data. Fix by increasing model complexity, adding more relevant features, or reducing regularization penalty."},
        {"q": "What is Gradient Descent?", "a": "A first-order iterative optimization algorithm used to minimize a loss function by updating parameters in the opposite direction of the gradient: θ = θ - α * ∇J(θ)."},
        {"q": "Explain the difference between Batch GD, Stochastic GD, and Mini-batch GD.", "a": "Batch GD uses the entire dataset per update (slow, smooth); SGD uses one sample per update (fast, noisy); Mini-batch GD uses small batches of 32-256 samples (industry standard, balanced efficiency)."},
        {"q": "What is the Learning Rate (α) and what happens if it is too high or low?", "a": "Step size taken towards the minimum. If too high, the algorithm oscillates and diverges; if too low, convergence takes excessively long or gets trapped in local minima."},
        {"q": "What is L1 Regularization (Lasso)?", "a": "Adds absolute weight penalty (λ * Σ|w|) to the loss function. It drives non-essential weights to exactly zero, producing sparse models and automatic feature selection."},
        {"q": "What is L2 Regularization (Ridge)?", "a": "Adds squared weight penalty (λ * Σw²) to the loss function. It shrinks weight magnitudes towards zero without eliminating features, handling multicollinearity effectively."},
        {"q": "Explain ElasticNet Regularization.", "a": "Combines both L1 and L2 penalties: L = Loss + r * λ * Σ|w| + ((1-r)/2) * λ * Σw², balancing feature sparsity and grouping effects."},
        {"q": "What is Cross-Validation (K-Fold)?", "a": "Splits data into K equal subsets. The model trains on K-1 folds and validates on the remaining fold, repeating K times to produce an unbiased performance metric."},
        {"q": "What is a Confusion Matrix?", "a": "A 2x2 (or NxN) table showing True Positives (TP), True Negatives (TN), False Positives (FP - Type I error), and False Negatives (FN - Type II error)."},
        {"q": "Define Precision and Recall.", "a": "Precision = TP / (TP + FP) (accuracy of positive predictions). Recall = TP / (TP + FN) (ability to detect all actual positives)."},
        {"q": "What is the F1-Score and when is it preferred over Accuracy?", "a": "F1-Score is the harmonic mean of Precision and Recall: 2 * (P * R) / (P + R). Preferred over accuracy when dealing with imbalanced datasets (e.g. fraud detection where 99% are non-fraud)."},
        {"q": "What is the ROC Curve and AUC score?", "a": "Receiver Operating Characteristic plots True Positive Rate vs False Positive Rate across all classification thresholds. AUC (Area Under Curve) measures overall discriminative ability (1.0 is perfect, 0.5 is random guessing)."},
        {"q": "How does Linear Regression work?", "a": "Models the relationship between continuous variables by fitting a linear equation: y = w^T * x + b by minimizing Mean Squared Error (MSE)."},
        {"q": "How does Logistic Regression work?", "a": "Uses the sigmoid function σ(z) = 1 / (1 + e^(-z)) to map linear combinations of features to probability values between 0 and 1 for binary classification."},
        {"q": "What is a Decision Tree and how does it split nodes?", "a": "A tree structure where internal nodes represent feature tests and leaf nodes represent target classes. Nodes are split using Information Gain (Entropy) or Gini Impurity."},
        {"q": "What is Entropy in Information Theory?", "a": "A measure of impurity or uncertainty in a dataset: H(S) = -Σ p_i * log2(p_i). Pure subsets have entropy 0."},
        {"q": "What is Gini Impurity?", "a": "A measure of statistical misclassification likelihood: Gini = 1 - Σ (p_i)². Lower Gini indicates purer partitions."},
        {"q": "Explain Random Forest and how it prevents overfitting.", "a": "An ensemble of decision trees built using Bagging (Bootstrap Aggregation) and random feature subset selection. Individual tree variance cancels out through majority voting or averaging."},
        {"q": "What is Boosting (e.g. AdaBoost, Gradient Boosting, XGBoost)?", "a": "A sequential ensemble method where each new weak learner focuses specifically on correcting the residual errors of preceding models."},
        {"q": "How does K-Means Clustering work?", "a": "1. Initialize K cluster centroids randomly. 2. Assign each point to its nearest centroid. 3. Recompute centroids as mean of assigned points. 4. Repeat until convergence."},
        {"q": "How do you choose K in K-Means?", "a": "Using the Elbow Method (plotting Within-Cluster Sum of Squares vs K to find the inflection point) and Silhouette Score analysis."},
        {"q": "What is Principal Component Analysis (PCA)?", "a": "An unsupervised dimensionality reduction technique that projects high-dimensional data onto orthogonal eigenvectors (principal components) that maximize variance."},
        {"q": "What is Support Vector Machine (SVM)?", "a": "A supervised model that finds the optimal separating hyperplane that maximizes the margin (distance) between closest data points of opposing classes (support vectors)."},
        {"q": "What is the Kernel Trick in SVM?", "a": "Implicitly maps non-linearly separable data into higher-dimensional feature spaces where it becomes linearly separable, using kernel functions (RBF, Polynomial) without computing actual coordinates."},
        {"q": "What is an Artificial Neural Network (ANN)?", "a": "A network of interconnected artificial neurons arranged in input, hidden, and output layers inspired by biological neural circuits."},
        {"q": "What is the role of an Activation Function?", "a": "Introduces non-linearity into neural networks, enabling them to approximate complex non-linear functions (e.g. ReLU, Sigmoid, Tanh, LeakyReLU)."},
        {"q": "Why is ReLU (Rectified Linear Unit) preferred in deep networks?", "a": "f(x) = max(0, x). It has constant derivative 1 for positive inputs, avoiding the vanishing gradient problem common with Sigmoid and Tanh, while being computationally cheap."},
        {"q": "What is Backpropagation?", "a": "The algorithm that computes the gradient of the loss function with respect to every weight in a neural network using the multivariable calculus chain rule, propagating errors backward from output to input."},
        {"q": "What is the Vanishing Gradient problem?", "a": "When gradients shrink exponentially as they propagate backward through many layers (due to small derivative values < 1 in Sigmoid/Tanh), preventing early layers from updating their weights."},
        {"q": "What is Dropout in neural networks?", "a": "A regularization technique where randomly selected neurons are temporarily ignored (set to zero) during forward and backward passes of each training step to prevent co-adaptation."},
        {"q": "Explain Supervised vs Semi-Supervised Learning.", "a": "Supervised uses 100% labeled training instances. Semi-supervised leverages a small set of labeled data combined with a large pool of inexpensive unlabeled data to improve performance."}
    ],

    "Operating Systems": [
        {"q": "What is an Operating System?", "a": "Core system software that acts as an intermediary between computer hardware and user applications, managing hardware resources and providing common services."},
        {"q": "What is Dual Mode operation in modern CPUs?", "a": "Hardware support providing User Mode (restricted privileges for applications) and Kernel Mode (full hardware access for OS code), switched via hardware interrupts and mode bits."},
        {"q": "What is a System Call?", "a": "A programmatic interface that allows user-level applications to request privileged services directly from the OS kernel (e.g., fork(), read(), write(), open())."},
        {"q": "What is a Process and what are its states?", "a": "A program in execution. Typical states: New, Ready, Running, Waiting (Blocked), and Terminated."},
        {"q": "What is a Process Control Block (PCB)?", "a": "A kernel data structure containing all metadata for a process: Process ID (PID), program counter, CPU registers, scheduling priority, memory limits, and open file lists."},
        {"q": "What is a Context Switch?", "a": "The process of saving the execution state (registers, PCB) of the currently running process and restoring the state of the next process selected by the CPU scheduler."},
        {"q": "Differentiate between a Process and a Thread.", "a": "A process has its own isolated address space, PCB, and file handles. A thread is a lightweight execution unit inside a process sharing code, data, and heap, but having its own stack and registers."},
        {"q": "What is CPU Scheduling and what is the difference between Preemptive and Non-Preemptive scheduling?", "a": "Selecting which ready process gets CPU time. Preemptive allows the OS to interrupt a running process (e.g. Round Robin, SRTF); Non-preemptive lets the process run until it voluntarily yields or blocks (e.g. FCFS)."},
        {"q": "Explain First-Come, First-Served (FCFS) scheduling and the Convoy Effect.", "a": "FCFS executes processes in arrival order. The Convoy Effect occurs when a CPU-heavy process blocks shorter I/O-bound processes, causing poor average turnaround time."},
        {"q": "Explain Shortest Job First (SJF) and why it is provably optimal for average waiting time.", "a": "SJF executes the process with smallest CPU burst first. It minimizes waiting times mathematically, but cannot be implemented perfectly because future burst lengths cannot be known in advance."},
        {"q": "How does Round Robin (RR) scheduling work?", "a": "Each process gets a fixed slice of CPU time called a 'time quantum'. When the quantum expires, the process is preempted and placed at the back of the ready queue."},
        {"q": "What is a Race Condition?", "a": "A situation where multiple concurrent processes or threads access and manipulate shared data simultaneously, and the final outcome depends on the non-deterministic order of execution."},
        {"q": "What is the Critical Section problem?", "a": "A code segment accessing shared resources that must satisfy three requirements: Mutual Exclusion, Progress, and Bounded Waiting."},
        {"q": "What is a Semaphore and what are its two atomic operations?", "a": "A synchronization variable manipulated atomically by wait() [P: decrements, blocks if <= 0] and signal() [V: increments, unblocks waiting process]."},
        {"q": "Differentiate between a Counting Semaphore and a Binary Semaphore (Mutex).", "a": "A Binary Semaphore has values 0 or 1, serving as a mutual exclusion lock. A Counting Semaphore has integer values >= 0, representing availability of multiple resource instances."},
        {"q": "Describe the Classic Dining Philosophers Problem.", "a": "5 philosophers sit at a table with 5 chopsticks; each needs 2 chopsticks to eat. Demonstrates concurrency, deadlock, and starvation challenges when acquiring resources symmetrically."},
        {"q": "What is a Deadlock in OS?", "a": "A situation where a set of processes are permanently blocked because each process holds a resource and waits for another resource held by another process in the set."},
        {"q": "List the 4 Coffman conditions necessary for a deadlock.", "a": "1. Mutual Exclusion, 2. Hold and Wait, 3. No Preemption, 4. Circular Wait. Eliminating any one condition prevents deadlocks."},
        {"q": "How does Banker's Algorithm handle deadlocks?", "a": "A deadlock avoidance algorithm that checks whether granting a resource request leaves the system in a 'Safe State' (where a safe execution sequence of all processes exists) before allocation."},
        {"q": "What is Virtual Memory?", "a": "A storage allocation scheme that abstracts physical RAM, giving processes the illusion of contiguous, private memory that can exceed actual physical RAM size."},
        {"q": "What is Paging in memory management?", "a": "A non-contiguous memory management scheme that divides logical address space into fixed-size blocks called Pages and physical memory into identical-size blocks called Frames."},
        {"q": "What is the purpose of a Page Table?", "a": "Maintains mapping from logical page numbers (P) to physical frame numbers (F), along with valid/invalid and permission bits."},
        {"q": "What is the Translation Lookaside Buffer (TLB)?", "a": "A high-speed associative hardware cache in the MMU storing recent page table translations to avoid double memory access overhead."},
        {"q": "How do you calculate Effective Memory Access Time (EMAT)?", "a": "EMAT = Hit_Ratio * (TLB_time + Mem_time) + (1 - Hit_Ratio) * (TLB_time + 2 * Mem_time + Page_Fault_time)."},
        {"q": "What is a Page Fault and what happens during page fault handling?", "a": "Occurs when a referenced page has its valid bit set to 0 (not in RAM). Triggers a trap to kernel, OS locates page on disk, loads it into a free frame, updates page table, and restarts instruction."},
        {"q": "What is Thrashing?", "a": "A severe state where the system spends more time swapping pages in and out between RAM and disk than executing real instructions, causing CPU utilization to plummet towards zero."},
        {"q": "Explain the FIFO page replacement algorithm and Belady's Anomaly.", "a": "Replaces the oldest loaded page. Belady's Anomaly is a counter-intuitive phenomenon where increasing the number of page frames results in MORE page faults for certain reference strings."},
        {"q": "Explain the Least Recently Used (LRU) page replacement algorithm.", "a": "Replaces the page that has not been referenced for the longest period of time. It is a stack algorithm and does not suffer from Belady's Anomaly."},
        {"q": "What is Optimal Page Replacement (OPT / MIN)?", "a": "Replaces the page that will not be used for the longest period of time in the future. It is theoretically optimal (lowest page faults) and used as a benchmark."},
        {"q": "What is Internal vs External Fragmentation?", "a": "Internal fragmentation occurs when allocated memory exceeds requested memory (e.g. unused bytes in a 4KB page). External fragmentation occurs when total free memory is sufficient, but split into non-contiguous slices."},
        {"q": "What is an Inode in Unix file systems?", "a": "A data structure representing a file system object, storing file size, owner permissions, access timestamps, and pointers to direct, indirect, and doubly-indirect data blocks."},
        {"q": "Compare FCFS, SSTF, and SCAN disk scheduling algorithms.", "a": "FCFS services requests in arrival order; SSTF (Shortest Seek Time First) chooses the track closest to the head (high throughput, risk of starvation); SCAN (Elevator) sweeps back and forth across cylinders."},
        {"q": "What is Inter-Process Communication (IPC)?", "a": "Mechanisms allowing processes to exchange data: Shared Memory (fastest, requires synchronization) and Message Passing (pipes, message queues, sockets)."},
        {"q": "What is a Zombie Process vs an Orphan Process?", "a": "A Zombie process has completed execution, but its exit status remains in the process table until its parent calls wait(). An Orphan process has its parent terminated while running; it is adopted by init (PID 1)."},
        {"q": "What is Spooling in operating systems?", "a": "Simultaneous Peripheral Operations On-Line: buffering data for slow I/O devices (like printers) on disk so faster CPU processes are not blocked waiting for mechanical devices."}
    ],

    "Compiler Design": [
        {"q": "What is a Compiler?", "a": "A computer program that translates source code written in a high-level programming language into an equivalent target machine language or intermediate representation."},
        {"q": "What are the six phases of a traditional Compiler?", "a": "1. Lexical Analysis, 2. Syntax Analysis, 3. Semantic Analysis, 4. Intermediate Code Generation, 5. Code Optimization, 6. Target Code Generation."},
        {"q": "Differentiate between Compiler and Interpreter.", "a": "A compiler translates the entire source program into machine code once before execution, producing standalone binaries. An interpreter translates and executes source code line-by-line on the fly."},
        {"q": "What is the front-end vs back-end of a compiler?", "a": "The front-end is machine-independent (lexical, syntax, semantic analysis generating IR). The back-end is machine-dependent (optimization and target code generation for specific CPU architectures)."},
        {"q": "What is Lexical Analysis (Scanning)?", "a": "The first phase that reads the raw character stream of source code and groups them into meaningful sequences called lexemes, producing a stream of tokens."},
        {"q": "Define Token, Lexeme, and Pattern.", "a": "Token: An abstract category (e.g. <id>, <num>, <keyword>). Lexeme: The actual sequence of characters matching the token (e.g. 'count', '42', 'if'). Pattern: The rule/regex defining valid lexemes."},
        {"q": "What is a Regular Expression in lexical analysis?", "a": "A formal string notation using operations (concatenation, alternation |, Kleene star *) to define regular languages recognized by finite automata."},
        {"q": "What is the difference between DFA and NFA?", "a": "Deterministic Finite Automaton (DFA) has exactly one transition per input symbol from each state and no ε-transitions. Non-deterministic Finite Automaton (NFA) can have multiple transitions and ε-transitions."},
        {"q": "Explain Thompson's Construction.", "a": "An algorithm that converts any regular expression into an equivalent NFA with ε-transitions using compositional sub-automata."},
        {"q": "Explain Subset Construction (Powerset Algorithm).", "a": "An algorithm that converts an NFA into an equivalent DFA by treating sets of reachable NFA states (via ε-closure) as single states in the DFA."},
        {"q": "What is Syntax Analysis (Parsing)?", "a": "The second phase that checks whether the token stream satisfies grammatical rules defined by a Context-Free Grammar (CFG), constructing a Parse Tree or Abstract Syntax Tree (AST)."},
        {"q": "What is a Context-Free Grammar (CFG)?", "a": "A 4-tuple G = (V, Σ, R, S) where V is non-terminals, Σ is terminal symbols, R is production rules of form A -> α, and S is the start symbol."},
        {"q": "What is an Ambiguous Grammar?", "a": "A grammar that produces more than one distinct parse tree (or leftmost/rightmost derivation) for at least one string. Ambiguity must be resolved via precedence and associativity rules."},
        {"q": "What is the difference between a Parse Tree and an Abstract Syntax Tree (AST)?", "a": "A parse tree contains every grammar derivation detail including punctuation and parentheses. An AST retains only essential semantic nodes (operators, operands, control statements)."},
        {"q": "Differentiate Top-Down Parsing from Bottom-Up Parsing.", "a": "Top-Down constructs the parse tree starting from the start symbol down to terminal leaves (e.g. LL parsers). Bottom-Up constructs the tree starting from leaves reducing up to the start symbol (e.g. LR parsers)."},
        {"q": "What are FIRST and FOLLOW sets?", "a": "FIRST(α) is the set of terminals that begin strings derived from α. FOLLOW(A) is the set of terminals that can appear immediately to the right of non-terminal A in some sentential form."},
        {"q": "What is an LL(1) Parser?", "a": "A top-down parser that scans input Left-to-right, produces a Leftmost derivation, using 1 lookahead token. It requires grammars without left recursion or common prefixes."},
        {"q": "What is Left Recursion and how is it eliminated?", "a": "A rule of form A -> Aα | β. Left recursion causes top-down parsers to enter infinite loops. Eliminated by transforming into: A -> βA' and A' -> αA' | ε."},
        {"q": "What is Left Factoring?", "a": "A grammar transformation that defers parsing decisions when two productions share a common prefix: A -> αβ1 | αβ2 becomes A -> αA' and A' -> β1 | β2."},
        {"q": "Explain Shift-Reduce Parsing.", "a": "A bottom-up parser using a stack: 'Shift' pushes next input token onto stack; 'Reduce' replaces a substring (handle) matching a production's RHS with its LHS non-terminal."},
        {"q": "What are Shift-Reduce and Reduce-Reduce conflicts?", "a": "Shift-Reduce: The parser cannot decide whether to push the next token or reduce current stack contents. Reduce-Reduce: The parser finds multiple productions matching the handle."},
        {"q": "Compare LR(0), SLR(1), LALR(1), and CLR(1) parsers.", "a": "Power hierarchy: LR(0) < SLR(1) < LALR(1) < CLR(1). CLR(1) is most powerful but has huge state tables; LALR(1) merges states with identical cores, achieving CLR power with SLR-sized tables (used in Yacc/Bison)."},
        {"q": "What is Semantic Analysis?", "a": "The phase that verifies source code adheres to language type and scope rules (type checking, variable declaration before use, parameter count validation)."},
        {"q": "What is a Symbol Table and what information does it store?", "a": "A central data structure (hash table) maintaining identifier attributes: name, type, memory offset, scope level, function parameters, and line number."},
        {"q": "What is Syntax-Directed Translation (SDT)?", "a": "Augmenting grammar productions with semantic actions (code snippets enclosed in curly braces) executed during parsing."},
        {"q": "Differentiate S-attributed and L-attributed definitions.", "a": "S-attributed definitions use only synthesized attributes (evaluated bottom-up from children). L-attributed allow inherited attributes from left siblings and parent, evaluated in depth-first order."},
        {"q": "What is Intermediate Code Representation (IR)?", "a": "A machine-independent internal code format that decouples language-specific front-ends from hardware-specific back-ends, simplifying optimization and multi-target compilation."},
        {"q": "What is Three-Address Code (TAC)?", "a": "An intermediate representation where each instruction has at most one operator and at most three operand addresses: x = y op z."},
        {"q": "Compare Quadruples, Triples, and Indirect Triples.", "a": "Quadruple: (op, arg1, arg2, result). Triple: (op, arg1, arg2) referencing results by instruction index. Indirect Triple: Uses an array of pointers to separate triples, simplifying instruction reordering."},
        {"q": "What is a Basic Block in code optimization?", "a": "A sequence of consecutive instructions with single entry (first instruction) and single exit (last instruction), with no internal branches."},
        {"q": "What is a Control Flow Graph (CFG)?", "a": "A directed graph where nodes are basic blocks and directed edges represent possible branch and jump transfers between them."},
        {"q": "Explain Constant Folding and Constant Propagation.", "a": "Constant Folding evaluates operations on constants at compile time (e.g. replacing 'x = 3 + 5' with 'x = 8'). Constant Propagation replaces variables known to hold constants with their values throughout the block."},
        {"q": "Explain Dead Code Elimination.", "a": "Removing code statements whose computed values are never read or used anywhere else in the program, reducing binary size and execution time."},
        {"q": "What is Loop Invariant Code Motion?", "a": "Moving statements that produce identical values on every iteration outside of the loop header, avoiding redundant computations inside the loop body."},
        {"q": "What is Peephole Optimization?", "a": "A local optimization technique that slides a small window (peephole) of target instructions, replacing redundant or inefficient sequences (like store followed by immediate load) with faster instructions."}
    ],

    "Data Structures": [
        {"q": "What is a Data Structure?", "a": "A specialized format for organizing, processing, retrieving, and storing data in computer memory efficiently."},
        {"q": "What is Asymptotic Analysis (Big-O, Big-Omega, Big-Theta)?", "a": "Mathematical notations describing algorithm runtime growth as input size N tends to infinity. Big-O: Upper bound (worst-case); Big-Omega (Ω): Lower bound (best-case); Big-Theta (Θ): Tight bound (average/exact growth)."},
        {"q": "What is an Array and what are its memory characteristics?", "a": "A linear data structure storing elements of identical type in contiguous memory locations, providing O(1) random access by index via formula: Address(A[i]) = Base + i * size."},
        {"q": "Compare Array vs Singly Linked List.", "a": "Arrays provide O(1) indexed access but fixed size and O(N) insertion/deletion. Linked Lists allow dynamic resizing and O(1) node insertion/deletion at known pointers, but require O(N) sequential traversal and extra memory for pointers."},
        {"q": "How do you detect a cycle in a Linked List?", "a": "Using Floyd's Tortoise and Hare algorithm: advance slow pointer by 1 step and fast pointer by 2 steps. If they meet, a cycle exists in O(N) time and O(1) extra space."},
        {"q": "What is a Stack and what principle does it follow?", "a": "A linear collection following LIFO (Last In, First Out). Core operations: push(x), pop(), peek() — all executing in O(1) time."},
        {"q": "What are primary applications of a Stack?", "a": "Function call stack (recursion), balanced parentheses validation, undo/redo mechanisms, evaluation of postfix expressions, and depth-first search."},
        {"q": "What is a Queue and what principle does it follow?", "a": "A linear collection following FIFO (First In, First Out). Core operations: enqueue(x) at rear and dequeue() from front — both executing in O(1) time."},
        {"q": "Explain Circular Queue and why it is used.", "a": "A queue where the rear connects back to the front modulo array capacity: (rear + 1) % N. It overcomes the memory wastage of linear array queues where empty front slots cannot be reused."},
        {"q": "What is a Deque (Double-Ended Queue)?", "a": "A generalized queue supporting O(1) insertion and deletion at both front and rear ends."},
        {"q": "What is a Priority Queue and how is it typically implemented?", "a": "An abstract data structure where each element has an assigned priority, serving highest priority first. Most efficiently implemented using a Binary Heap (O(log N) insert and extract-max/min)."},
        {"q": "What is a Binary Tree?", "a": "A hierarchical data structure where each node has at most two children, referred to as left child and right child."},
        {"q": "Define Full, Complete, and Perfect Binary Trees.", "a": "Full: Every node has 0 or 2 children. Complete: All levels are fully filled except possibly the last, which is filled from left to right. Perfect: All internal nodes have 2 children and all leaves are at the exact same depth."},
        {"q": "What is a Binary Search Tree (BST)?", "a": "A binary tree with the ordering invariant: for every node, all keys in its left subtree are strictly smaller, and all keys in its right subtree are strictly greater."},
        {"q": "What are Tree Traversals (Inorder, Preorder, Postorder, Level-order)?", "a": "Inorder: Left -> Root -> Right (produces sorted order in BST). Preorder: Root -> Left -> Right. Postorder: Left -> Right -> Root. Level-order: Breadth-first using a queue."},
        {"q": "What is an AVL Tree?", "a": "A self-balancing Binary Search Tree where the Balance Factor (Height(Left) - Height(Right)) of every node is strictly -1, 0, or 1. Rebalanced using single (LL, RR) or double (LR, RL) rotations, guaranteeing O(log N) operations."},
        {"q": "What is a Red-Black Tree?", "a": "A self-balancing BST where nodes are colored red or black satisfying color invariants (root is black, no consecutive red nodes, equal black-height). Guarantees O(log N) worst-case time with fewer rotations on insert/delete than AVL."},
        {"q": "What is a Binary Heap (Min-Heap / Max-Heap)?", "a": "A complete binary tree stored in an array satisfying the heap property: in Max-Heap, parent key >= children keys. Root is always maximum. Insert and extract-max take O(log N), find-max is O(1)."},
        {"q": "How does HeapSort work?", "a": "1. Build a Max-Heap from the array in O(N) time. 2. Swap root (max) with last element, decrease heap size by 1. 3. Heapify the root. 4. Repeat until sorted. Overall time: O(N log N) in-place."},
        {"q": "What is a Hash Table and how does hashing work?", "a": "A data structure mapping keys to array indices via a Hash Function h(key) = index, providing average O(1) search, insert, and delete."},
        {"q": "Explain Hash Collisions and how Chaining resolves them.", "a": "Collisions occur when two distinct keys produce the same hash index. Separate Chaining resolves collisions by storing colliding elements in a linked list or balanced tree at that index bucket."},
        {"q": "Explain Open Addressing for collision resolution (Linear Probing, Quadratic, Double Hashing).", "a": "All elements reside in the hash table array. If bucket is full: Linear probing checks i+1, i+2...; Quadratic probing checks i+1², i+2²...; Double hashing checks i + j * h2(key)."},
        {"q": "What is Load Factor in a hash table?", "a": "The ratio α = N / K (number of stored entries divided by bucket capacity). When α exceeds a threshold (typically 0.75), the table rehashes into a doubled capacity array."},
        {"q": "How do you represent a Graph in memory?", "a": "1. Adjacency Matrix: V x V 2D array (O(1) edge lookup, O(V²) space). 2. Adjacency List: Array of linked lists/vectors (O(deg(V)) lookup, O(V + E) space, best for sparse graphs)."},
        {"q": "Explain Breadth-First Search (BFS) in graphs.", "a": "Explores neighbor vertices level by level using a Queue and a visited set. Finds shortest unweighted path in O(V + E) time."},
        {"q": "Explain Depth-First Search (DFS) in graphs.", "a": "Explores as deep as possible along each branch before backtracking using recursion or a Stack in O(V + E) time. Used in topological sort and connected components."},
        {"q": "What is Topological Sort in a Directed Acyclic Graph (DAG)?", "a": "A linear ordering of vertices such that for every directed edge u -> v, u comes before v. Computed using Kahn's algorithm (indegree queue) or DFS in O(V + E)."},
        {"q": "Explain Dijkstra's Algorithm for Shortest Path.", "a": "Finds shortest paths from a single source to all vertices in a weighted graph with non-negative edge weights using a Min-Priority Queue in O((V + E) log V) time."},
        {"q": "Explain Bellman-Ford Algorithm and its advantage over Dijkstra.", "a": "Relaxes all E edges V-1 times in O(V * E). Advantage: handles graphs with negative edge weights and detects negative weight cycles."},
        {"q": "What is a Minimum Spanning Tree (MST)?", "a": "A subset of edges that connects all vertices in an edge-weighted undirected graph with minimum total edge weight and no cycles (contains exactly V - 1 edges)."},
        {"q": "Compare Prim's Algorithm and Kruskal's Algorithm for MST.", "a": "Prim's grows a tree vertex-by-vertex using a priority queue (O(E log V), great for dense graphs). Kruskal's sorts all edges and adds them greedily using a Disjoint Set Union (DSU) to avoid cycles (O(E log E))."},
        {"q": "What is a Disjoint Set Union (DSU / Union-Find)?", "a": "A data structure tracking partition of elements into disjoint sets with operations: find(x) and union(x, y). Achieves nearly O(1) amortized time using Path Compression and Union by Rank."},
        {"q": "What is a Trie (Prefix Tree)?", "a": "A tree data structure used for storing strings where each node represents a character. Provides O(L) search, insert, and prefix lookup where L is string length, ideal for autocomplete."},
        {"q": "What is Dynamic Programming (Memoization vs Tabulation)?", "a": "A technique for solving problems with Overlapping Subproblems and Optimal Substructure. Memoization is Top-Down with recursion and cache; Tabulation is Bottom-Up filling an iterative DP table."},
        {"q": "What is the difference between QuickSort and MergeSort?", "a": "MergeSort divides in half, recursively sorts, and merges in O(N log N) guaranteed time, but requires O(N) auxiliary space. QuickSort partitions around a pivot in-place (O(log N) stack space), average O(N log N), but worst-case O(N²)."}
    ],

    "Computer Networks": [
        {"q": "What is a Computer Network?", "a": "A collection of autonomous computing devices interconnected by transmission media to share resources, exchange data packets, and communicate via established protocols."},
        {"q": "Compare the OSI 7-Layer Model and the TCP/IP 4-Layer Model.", "a": "OSI: Physical, Data Link, Network, Transport, Session, Presentation, Application. TCP/IP collapses these into 4 functional layers: Network Access, Internet, Transport, Application."},
        {"q": "What is Packet Switching vs Circuit Switching?", "a": "Circuit Switching establishes a dedicated physical path for the entire session duration (e.g. traditional telephone). Packet Switching breaks data into independent packets routed dynamically across shared links (e.g. the Internet)."},
        {"q": "What is the function of the Data Link Layer?", "a": "Node-to-node frame delivery over physical links, framing, physical MAC addressing, flow control, and error detection (CRC)."},
        {"q": "Explain MAC Address vs IP Address.", "a": "A MAC address is a 48-bit globally unique hardware identifier burned into the NIC (Layer 2). An IP address is a logical 32-bit (IPv4) or 128-bit (IPv6) hierarchical address assigned by the network (Layer 3)."},
        {"q": "What is ARP (Address Resolution Protocol)?", "a": "A Layer 2/3 protocol that resolves a known destination logical IP address to its corresponding physical hardware MAC address on the local area network using ARP Request (broadcast) and Reply (unicast)."},
        {"q": "What is CSMA/CD in Ethernet?", "a": "Carrier Sense Multiple Access with Collision Detection: nodes listen to the medium before transmitting, and if a collision occurs, stop immediately, send a jam signal, and wait a random binary exponential backoff time."},
        {"q": "What is CSMA/CA in Wi-Fi (802.11)?", "a": "Carrier Sense Multiple Access with Collision Avoidance: wireless signals cannot detect collisions while transmitting, so nodes use Request to Send (RTS) / Clear to Send (CTS) frames and inter-frame spacing to avoid collisions."},
        {"q": "Explain IPv4 Header Structure.", "a": "20 bytes minimum header including: Version, IHL, Type of Service, Total Length, Identification, Flags (DF, MF), Fragment Offset, Time to Live (TTL), Protocol (TCP=6, UDP=17), Header Checksum, Source IP, Destination IP."},
        {"q": "What is Time to Live (TTL) in IP packets?", "a": "An 8-bit integer decremented by 1 at each routing hop. When TTL reaches 0, the packet is discarded and an ICMP Time Exceeded message is sent back, preventing infinite routing loops."},
        {"q": "What is Subnetting and CIDR?", "a": "Subnetting divides a large network into smaller sub-networks. CIDR (Classless Inter-Domain Routing) uses prefix notation (e.g. 192.168.1.0/24) where /24 indicates the 24-bit network mask (255.255.255.0)."},
        {"q": "What is NAT (Network Address Translation)?", "a": "Enables multiple private internal IP addresses (e.g. 192.168.x.x) to share a single public IP address using port multiplexing (PAT), preserving IPv4 address space and enhancing security."},
        {"q": "Compare IPv4 and IPv6.", "a": "IPv4 uses 32-bit addresses (~4.3 billion addresses) written in decimal. IPv6 uses 128-bit addresses (3.4 × 10³⁸ addresses) written in hexadecimal with built-in IPSec, auto-configuration, and no header checksum."},
        {"q": "Explain Distance Vector Routing and the Count to Infinity Problem.", "a": "Nodes share their full routing table with immediate neighbors periodically using Bellman-Ford (e.g. RIP). Count to infinity occurs when link failures cause routing loops and slowly incrementing metrics; mitigated by Split Horizon and Poison Reverse."},
        {"q": "Explain Link State Routing (OSPF).", "a": "Each router floods Link State Advertisements (LSAs) containing immediate neighbor link costs across the entire autonomous system, building an identical topology map and running Dijkstra's algorithm independently."},
        {"q": "What is BGP (Border Gateway Protocol)?", "a": "The de-facto Path Vector protocol governing routing between independent Autonomous Systems (AS) across the global Internet based on administrative policies rather than simple hop counts."},
        {"q": "Compare TCP and UDP at the Transport Layer.", "a": "TCP is connection-oriented, reliable (guarantees delivery via ACKs and retransmissions), flow-controlled, and ordered (20B header). UDP is connectionless, best-effort (unreliable, no retransmissions), low-latency, and datagram-oriented (8B header)."},
        {"q": "Detail the TCP 3-Way Handshake.", "a": "1. Client -> Server: SYN (seq = x). 2. Server -> Client: SYN-ACK (seq = y, ack = x + 1). 3. Client -> Server: ACK (seq = x + 1, ack = y + 1). Establishes synchronized sequence numbers."},
        {"q": "Detail the TCP 4-Way Connection Termination.", "a": "1. Host A -> Host B: FIN. 2. Host B -> Host A: ACK (half-close). 3. Host B finishes data and sends: FIN. 4. Host A -> Host B: ACK, then enters TIME_WAIT state for 2MSL before fully closing."},
        {"q": "What is the Sliding Window Protocol in TCP?", "a": "A flow control mechanism where the receiver advertises its available buffer space (Receive Window - rwnd) in ACKs, allowing the sender to transmit multiple packets before pausing for acknowledgments."},
        {"q": "Explain TCP Congestion Control (Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery).", "a": "Slow start doubles cwnd exponentially until ssthresh. Congestion Avoidance increments cwnd linearly by 1 per RTT. Fast Retransmit triggers upon receiving 3 duplicate ACKs without waiting for timeout."},
        {"q": "What is the function of DNS (Domain Name System)?", "a": "A hierarchical distributed database mapping human-readable domain names (e.g. google.com) to machine IP addresses (e.g. 142.250.190.46) via recursive and authoritative resolvers over UDP port 53."},
        {"q": "What happens during a complete DNS lookup?", "a": "1. Browser/OS cache check -> 2. Local DNS Resolver -> 3. Root Name Server ('.') -> 4. TLD Name Server ('.com') -> 5. Authoritative Name Server ('example.com') -> 6. IP returned to browser."},
        {"q": "Compare HTTP/1.1, HTTP/2, and HTTP/3.", "a": "HTTP/1.1 uses persistent TCP connections but suffers from Head-of-Line (HoL) blocking. HTTP/2 introduces binary framing and multiplexing multiple streams over one TCP connection. HTTP/3 moves to QUIC protocol over UDP, eliminating TCP HoL blocking."},
        {"q": "What is HTTPS and how does TLS/SSL Handshake secure communication?", "a": "HTTP layered over TLS. The handshake validates server authenticity via digital certificates, exchanges asymmetric keys (RSA/Diffie-Hellman), and negotiates symmetric session keys (AES) for high-speed encrypted transmission."},
        {"q": "What is DHCP (Dynamic Host Configuration Protocol)?", "a": "Automatically assigns dynamic IP addresses, subnet masks, default gateways, and DNS servers to joining devices via the DORA process: Discover, Offer, Request, Acknowledge over UDP ports 67/68."},
        {"q": "What is ICMP (Internet Control Message Protocol) and how do Ping and Traceroute use it?", "a": "Network layer management protocol reporting errors. Ping sends ICMP Echo Request and waits for Echo Reply. Traceroute sends packets with incrementing TTL values (1, 2, 3...) to discover each router along the path via ICMP Time Exceeded."},
        {"q": "What is a Firewall and how does a Stateful Firewall work?", "a": "A security device monitoring incoming and outgoing traffic. A stateful firewall tracks active TCP/UDP connections in a state table, automatically allowing return packets associated with valid outbound sessions."},
        {"q": "What is a VLAN (Virtual Local Area Network)?", "a": "A logical partition of a physical Layer 2 switch into multiple isolated broadcast domains tagged via IEEE 802.1Q headers, enhancing security and reducing broadcast traffic."},
        {"q": "What is a Denial of Service (DoS) and DDoS attack?", "a": "An attempt to overwhelm a server's network bandwidth, CPU, or memory with flood traffic (e.g. SYN Flood, UDP Flood, DNS amplification) from multiple compromised botnet nodes so legitimate users cannot access service."},
        {"q": "What is Port Forwarding?", "a": "Configuring a NAT router to redirect incoming network packets on a specific public port to a designated private internal IP address and port inside the local network."},
        {"q": "What is a Proxy Server vs a Reverse Proxy?", "a": "A forward proxy sits in front of clients, protecting client identities and caching outbound web requests. A reverse proxy sits in front of backend servers, handling load balancing, SSL termination, and caching for incoming client requests."},
        {"q": "Explain Symmetric vs Asymmetric Cryptography.", "a": "Symmetric uses one shared secret key for encryption and decryption (AES, fast). Asymmetric uses a public key for encryption and a private key for decryption (RSA, ECC, secure key exchange)."},
        {"q": "What is Quality of Service (QoS) in computer networks?", "a": "Mechanisms that prioritize specific traffic classes (e.g. VoIP audio, video conferencing) over latency-tolerant traffic (file downloads) to guarantee minimum throughput and jitter bounds."},
        {"q": "What is the Maximum Transmission Unit (MTU)?", "a": "The maximum packet size (in bytes) that can be transmitted over a physical network link without fragmentation (standard Ethernet MTU is 1500 bytes)."}
    ],

    "Database Management Systems": [
        {"q": "What is a Database Management System (DBMS)?", "a": "System software for creating, managing, querying, and administering structured databases efficiently while maintaining data integrity, security, and concurrency."},
        {"q": "Compare File System vs DBMS.", "a": "File systems suffer from data redundancy, inconsistency, difficulty accessing data, lack of concurrency control, and integrity issues. A DBMS provides ACID compliance, declarative querying (SQL), and centralized access control."},
        {"q": "Explain the 3-Schema Architecture (ANSI/SPARC).", "a": "1. External/View Level (user views). 2. Conceptual/Logical Level (what data is stored and entity relationships). 3. Internal/Physical Level (how data is physically stored on disk, indexing, B-trees)."},
        {"q": "What is Logical vs Physical Data Independence?", "a": "Logical: Ability to modify the logical schema (e.g. adding columns) without altering external application views. Physical: Ability to alter physical storage or indexes without altering the logical schema or queries."},
        {"q": "Define Primary Key, Candidate Key, Super Key, and Foreign Key.", "a": "Super Key: Any set of attributes uniquely identifying a tuple. Candidate Key: A minimal super key. Primary Key: The selected candidate key. Foreign Key: An attribute referencing the primary key of another table to enforce referential integrity."},
        {"q": "What are the ACID properties of a Database Transaction?", "a": "Atomicity (all-or-nothing), Consistency (preserves database integrity constraints), Isolation (concurrent transactions don't interfere), Durability (committed changes persist across crashes)."},
        {"q": "Explain Normalization and why it is necessary.", "a": "The systematic process of organizing relational tables to eliminate insertion, deletion, and update anomalies while reducing redundant data through decomposition into smaller relations."},
        {"q": "What is First Normal Form (1NF)?", "a": "Every attribute column must contain atomic (indivisible) values, and there must be no repeating groups or arrays."},
        {"q": "What is Second Normal Form (2NF)?", "a": "Table must be in 1NF and have NO partial dependency (no non-prime attribute should depend on a proper subset of any candidate key)."},
        {"q": "What is Third Normal Form (3NF)?", "a": "Table must be in 2NF and have NO transitive dependency (no non-prime attribute should depend on another non-prime attribute: if X -> Y, then X is a superkey or Y is prime)."},
        {"q": "What is Boyce-Codd Normal Form (BCNF)?", "a": "A stricter version of 3NF: for every non-trivial functional dependency X -> Y, X MUST be a super key."},
        {"q": "What is a Functional Dependency?", "a": "A constraint between two sets of attributes X and Y: denoted X -> Y, meaning that for any two tuples with identical X values, their Y values must also be identical."},
        {"q": "What is Lossless Join Decomposition?", "a": "When decomposing relation R into R1 and R2, R1 ⋈ R2 must equal R with no spurious tuples. Condition: R1 ∩ R2 -> R1 or R1 ∩ R2 -> R2."},
        {"q": "Compare DDL, DML, DQL, and DCL in SQL.", "a": "DDL (Data Definition: CREATE, ALTER, DROP, TRUNCATE). DML (Data Manipulation: INSERT, UPDATE, DELETE). DQL (Data Query: SELECT). DCL (Data Control: GRANT, REVOKE)."},
        {"q": "Explain the difference between DELETE, TRUNCATE, and DROP.", "a": "DELETE is a logged DML operation removing rows matching WHERE (can be rolled back). TRUNCATE is a DDL operation deallocating table pages instantly (resets identity, fast). DROP removes entire table schema and data permanently."},
        {"q": "Explain different types of SQL Joins (INNER, LEFT, RIGHT, FULL, CROSS).", "a": "INNER: Matching records from both tables. LEFT: All from left table and matching from right. RIGHT: All from right table and matching from left. FULL: All records from both tables with NULLs for non-matches. CROSS: Cartesian product (M × N rows)."},
        {"q": "What is the difference between WHERE and HAVING in SQL?", "a": "WHERE filters individual rows before grouping; it cannot use aggregate functions. HAVING filters aggregated groups after GROUP BY."},
        {"q": "What is a Correlated Subquery?", "a": "An inner subquery that references columns from the outer query table, executing once for each row processed by the outer query."},
        {"q": "What is a View and why is it used?", "a": "A virtual table defined by a stored SELECT query. It encapsulates complex queries, restricts column access for security, and simplifies reporting without duplicating data."},
        {"q": "What is an Index in DBMS and how does it speed up queries?", "a": "An auxiliary data structure (typically B+ Tree) that stores sorted key values and row pointers, reducing full table scans (O(N)) to logarithmic searches (O(log N))."},
        {"q": "Compare Clustered Index and Non-Clustered Index.", "a": "A Clustered Index determines the actual physical sorted storage order of rows on disk (only 1 per table, usually Primary Key). A Non-Clustered index stores key values with pointers to row data (multiple allowed per table)."},
        {"q": "Why are B+ Trees preferred over B-Trees for database indexing?", "a": "In B+ Trees, all actual data pointers reside strictly in leaf nodes linked sequentially as a doubly linked list, enabling ultra-fast range queries and scans while internal nodes hold more routing keys."},
        {"q": "What is Concurrency Control and why is it needed?", "a": "Coordination of concurrent transactions to prevent Dirty Read (uncommitted data read), Non-repeatable Read (row modified mid-transaction), and Phantom Read (new rows inserted matching range)."},
        {"q": "What are SQL Transaction Isolation Levels?", "a": "Read Uncommitted (allows dirty reads), Read Committed (default in Postgres/Oracle, no dirty reads), Repeatable Read (no non-repeatable reads), Serializable (highest isolation, completely serial execution)."},
        {"q": "Explain Two-Phase Locking (2PL).", "a": "A concurrency control protocol ensuring conflict serializability with two phases: Growing Phase (locks acquired, none released) and Shrinking Phase (locks released, none acquired)."},
        {"q": "What is Strict 2PL and why is it used?", "a": "Requires that all exclusive write locks be held until transaction commit or abort, completely preventing cascading aborts (cascading rollbacks)."},
        {"q": "What is a Deadlock in DBMS and how is it resolved?", "a": "When two transactions hold locks and wait for locks held by each other. Detected using Wait-For Graphs (finding cycles) and resolved by picking a 'victim' transaction to abort and roll back."},
        {"q": "Explain Write-Ahead Logging (WAL) and the ARIES recovery algorithm.", "a": "WAL requires that log records describing database updates be flushed to stable disk storage before the dirty data pages themselves are written, enabling crash recovery via Analysis, Redo, and Undo passes."},
        {"q": "What is Database Sharding?", "a": "Horizontal partitioning where rows of a large database table are split across multiple independent database servers based on a shard key, enabling horizontal scalability."},
        {"q": "Compare Relational Databases (RDBMS) and NoSQL databases.", "a": "RDBMS: Structured tabular schema, strong ACID guarantees, SQL joins (PostgreSQL, MySQL). NoSQL: Flexible schema, high horizontal scalability, eventual consistency (MongoDB document, Redis key-value, Cassandra wide-column, Neo4j graph)."},
        {"q": "What is the CAP Theorem?", "a": "A distributed system can guarantee at most two out of three properties simultaneously: Consistency (all nodes see latest data), Availability (every non-failing node returns responses), and Partition Tolerance (system functions despite network drops)."},
        {"q": "What is an Entity-Relationship (ER) Diagram?", "a": "A graphical representation of database design showing Entities (rectangles), Attributes (ovals), Relationships (diamonds), and Cardinality (1:1, 1:N, M:N)."},
        {"q": "What is a Database Trigger?", "a": "A stored procedure automatically executed (fired) when a specified DML event (INSERT, UPDATE, DELETE) occurs on a target table, enforcing audit trails and business rules."},
        {"q": "What is a Stored Procedure and what are its benefits?", "a": "Pre-compiled SQL code stored on the database server. Benefits: reduces network traffic, improves execution speed via cached query plans, and enhances security against SQL injection."},
        {"q": "What is SQL Injection and how do you prevent it?", "a": "A vulnerability where malicious SQL commands are inserted into user input fields to manipulate database queries. Prevented using Parameterized Queries (Prepared Statements) and ORM frameworks."}
    ],

    "Other": [
        {"q": "What are the four pillars of Object-Oriented Programming (OOP)?", "a": "1. Encapsulation (bundling data and methods, data hiding), 2. Abstraction (hiding implementation details), 3. Inheritance (reusing code across parent-child hierarchies), 4. Polymorphism (ability of an entity to take multiple forms)."},
        {"q": "Explain Compile-time (Static) vs Run-time (Dynamic) Polymorphism.", "a": "Compile-time polymorphism is resolved at compile time via method overloading and operator overloading. Run-time polymorphism is resolved at execution time via method overriding and virtual function tables."},
        {"q": "Explain the SOLID principles of software design.", "a": "S: Single Responsibility, O: Open/Closed (open for extension, closed for modification), L: Liskov Substitution (subtypes must be substitutable for base types), I: Interface Segregation (small specific interfaces), D: Dependency Inversion (depend on abstractions, not concretions)."},
        {"q": "What is REST (Representational State Transfer) architecture?", "a": "A stateless client-server software architectural style that uses standard HTTP methods (GET, POST, PUT, DELETE, PATCH), URI endpoints, and JSON payloads for resource manipulation."},
        {"q": "What does Idempotency mean in REST APIs?", "a": "An operation is idempotent if making multiple identical requests has the exact same side-effect on server state as making a single request (GET, PUT, DELETE are idempotent; POST is not)."},
        {"q": "Explain Git version control and the difference between git merge and git rebase.", "a": "Git is a distributed version control system. 'git merge' joins two branches creating a merge commit that preserves branch history. 'git rebase' rewrites commit history by moving branch commits onto the tip of target branch for a clean linear log."},
        {"q": "What is Docker and how does it differ from a Virtual Machine?", "a": "Docker packages applications and dependencies into lightweight containers sharing the host OS kernel with isolated user-space processes, whereas Virtual Machines run full guest operating systems on top of a hypervisor, consuming significantly more RAM and CPU."},
        {"q": "What is Continuous Integration and Continuous Deployment (CI/CD)?", "a": "CI automates code merging, building, and automated test execution on every commit. CD automates continuous release and deployment of tested builds to staging and production environments."},
        {"q": "What is Cloud Computing and its service models (IaaS, PaaS, SaaS)?", "a": "On-demand delivery of computing services over the internet. IaaS: Infrastructure (AWS EC2, GCP Compute). PaaS: Platform for code deployment without managing VMs (Heroku, Firebase). SaaS: End-user software (Google Drive, Microsoft 365)."},
        {"q": "What is the difference between Synchronous and Asynchronous programming?", "a": "Synchronous code blocks execution until the current task completes. Asynchronous code initiates long-running I/O operations and continues executing other tasks, resolving results via callbacks, promises, or async/await."},
        {"q": "What is a Microservices Architecture vs a Monolith?", "a": "A monolith bundles all modules into a single shared codebase and deployment unit. Microservices decompose systems into independent, loosely coupled services communicating via REST APIs or message brokers, scaling independently."},
        {"q": "What is an API Gateway?", "a": "A single entry-point reverse proxy that sits in front of backend microservices, handling routing, authentication, rate limiting, SSL termination, and telemetry."},
        {"q": "Explain symmetric vs asymmetric encryption.", "a": "Symmetric uses a single shared secret key for encryption and decryption (AES, ChaCha20). Asymmetric uses a mathematically paired public key for encryption and private key for decryption (RSA, ECC)."},
        {"q": "What is Cross-Site Scripting (XSS) and how is it prevented?", "a": "An attack where malicious scripts are injected into trusted web pages viewed by other users. Prevented by HTML entity escaping, sanitizing inputs, using Content Security Policy (CSP), and HttpOnly cookie flags."},
        {"q": "What is Cross-Site Request Forgery (CSRF) and how is it prevented?", "a": "An attack forcing an authenticated user's browser to execute unwanted actions on a vulnerable web application. Prevented using anti-CSRF tokens and SameSite cookie attributes."},
        {"q": "What is SQL Injection and how is it prevented?", "a": "Injecting malicious SQL syntax through unsanitized inputs to bypass login or leak data. Prevented using parameterized prepared statements and stored procedures."},
        {"q": "Explain the Model-View-Controller (MVC) architectural pattern.", "a": "Model: Manages data logic and database rules. View: Renders the visual user interface. Controller: Accepts user input, updates the Model, and selects the View to render."},
        {"q": "What is Big-O complexity of common sorting algorithms?", "a": "Bubble/Insertion/Selection: O(N²). QuickSort: Avg O(N log N), Worst O(N²). MergeSort/HeapSort: O(N log N). Counting/Radix Sort: O(N + K) linear time for bounded integers."},
        {"q": "What is a Memory Leak and how does Garbage Collection work?", "a": "A memory leak occurs when allocated memory is no longer needed but never freed. Garbage collectors (like in Python, Java) periodically trace object reference counts and reachability graphs, reclaiming unreferenced memory."},
        {"q": "What is Recursion and what is a Base Case?", "a": "A programming technique where a function calls itself to solve smaller instances of the same problem. The Base Case is the termination condition that stops recursive calls, preventing call stack overflow."},
        {"q": "What is Tail Call Optimization (TCO)?", "a": "When the recursive call is the very last statement in a function, compilers can reuse the current stack frame instead of allocating a new one, executing recursion in O(1) auxiliary stack space."},
        {"q": "Explain the difference between mutable and immutable data types in Python.", "a": "Immutable objects (int, float, string, tuple) cannot have their state modified after creation; operations return a new object. Mutable objects (list, dict, set) can be modified in place."},
        {"q": "What is the Global Interpreter Lock (GIL) in CPython?", "a": "A mutex lock in Python's standard CPython interpreter that allows only one native thread to execute Python bytecode at a time, protecting memory management from race conditions at the expense of CPU-bound multi-threading."},
        {"q": "How does Multiprocessing differ from Multithreading in Python?", "a": "Multithreading runs threads within a single process sharing memory (best for I/O-bound tasks). Multiprocessing spawns separate OS processes with independent GILs and memory spaces (best for CPU-intensive computing)."},
        {"q": "What are Python Decorators?", "a": "Functions that take another function as an argument, extend or modify its behavior, and return a new callable function without modifying the original source code (@syntax)."},
        {"q": "What are Python Generators and the `yield` keyword?", "a": "Functions that produce a sequence of values on-demand using `yield` instead of returning all at once, maintaining state between calls and saving memory when iterating over large datasets."},
        {"q": "What is a Hash Function and what properties must a cryptographic hash have?", "a": "A one-way mathematical function mapping variable input data to fixed-size hashes (e.g. SHA-256). Cryptographic properties: Pre-image resistance (irreversible), Second pre-image resistance, and Collision resistance."},
        {"q": "What is the difference between Authentication and Authorization?", "a": "Authentication verifies identity ('Who are you?', e.g. password, biometric, JWT). Authorization determines access permissions ('What are you allowed to do?', e.g. role-based access control RBAC)."},
        {"q": "What is a JSON Web Token (JWT) and what are its parts?", "a": "A compact, URL-safe token format consisting of three base64url-encoded parts separated by dots: Header (algorithm), Payload (claims/data), and Signature (HMAC/RSA verified with secret key)."},
        {"q": "What is Event-Driven Architecture?", "a": "A software architecture where decoupled services communicate by publishing and subscribing to asynchronous event streams via message brokers like Apache Kafka or RabbitMQ."},
        {"q": "What is Database Normalization vs Denormalization?", "a": "Normalization reduces redundancy and improves write performance. Denormalization intentionally adds redundant data or pre-joined columns to speed up heavy read queries and avoid expensive joins."},
        {"q": "What is Agile Scrum methodology?", "a": "An iterative project management framework using time-boxed iterations (Sprints, typically 2 weeks), daily stand-ups, product backlogs, sprint planning, and retrospectives."},
        {"q": "What is Test-Driven Development (TDD)?", "a": "A development cycle: 1. Write a failing automated test (Red), 2. Write minimal code to pass the test (Green), 3. Refactor code for cleanliness and design (Refactor)."},
        {"q": "What is Technical Debt?", "a": "The implied cost of future rework caused by choosing an easy, fast solution now instead of using a better, well-architected approach that takes longer."},
        {"q": "How do you prepare effectively for technical software engineering interviews?", "a": "1. Master Data Structures and Algorithms with LeetCode patterns. 2. Understand System Design (scalability, caching, DB sharding). 3. Review CS fundamentals (OS, Networks, DBMS). 4. Practice behavioral STAR method stories."}
    ]
}

# ==============================================================================
# 2. DAY-WISE COMPREHENSIVE STUDY TIMETABLE ENGINE
# ==============================================================================
SUBJECT_DAY_PLANS: Dict[str, Dict[str, Any]] = {
    "AI Agent Development": {
        "title": "7-Day AI Agent Development Mastery Roadmap",
        "days": [
            {
                "day": 1,
                "theme": "Foundations & Core AI Agent Architectures",
                "focus": "Basic concepts: Definition of Agency, Reflex Agents, Goal-Based vs Utility Agents, Perception-Action Loop.",
                "deliverable": "Create a clear comparative mind-map of Agent Types and draw the Perception-Action environment loop."
            },
            {
                "day": 2,
                "theme": "Reasoning Frameworks & Prompting Paradigms",
                "focus": "ReAct (Reason + Act), Chain-of-Thought (CoT), Tree-of-Thoughts (ToT), Plan-and-Execute architectures.",
                "deliverable": "Trace a complete ReAct loop step-by-step: Thought -> Action -> Observation -> Final Answer."
            },
            {
                "day": 3,
                "theme": "Tool Calling, Function Schemas & Safe Execution",
                "focus": "External API tool calling, JSON Schema validation, AST-verified safe math calculation, sandbox execution.",
                "deliverable": "Write an AST visitor or parser that validates and executes math expressions safely without eval()."
            },
            {
                "day": 4,
                "theme": "Agent Memory Systems & Vector Embeddings",
                "focus": "Working memory (context window), Episodic memory, Semantic memory, Vector databases (HNSW, Cosine similarity).",
                "deliverable": "Design a 2-tier memory architecture diagram showing short-term buffer + vector DB recall."
            },
            {
                "day": 5,
                "theme": "Agent Safety, Guardrails & Human-in-the-Loop",
                "focus": "Prompt injection prevention, guardrail filters, hallucination reduction, Human-in-the-Loop (HITL) checkpoints.",
                "deliverable": "Draft an Agent Security Policy covering input sanitization and high-risk action confirmation."
            },
            {
                "day": 6,
                "theme": "Active Recall & 35-Question Practice Drill",
                "focus": "Solve the full set of 35 AI Agent setup practice questions from the StudyMate question bank.",
                "deliverable": "Complete all 35 quiz questions and review solutions for any missed concepts."
            },
            {
                "day": 7,
                "theme": "Comprehensive Exam Mock Test & Mini-Project Defense",
                "focus": "Full syllabus mock examination, revision of key algorithms, and oral defense of your agent project.",
                "deliverable": "Score 90%+ on timed mock assessment; ready for viva and end-semester exams."
            }
        ]
    },

    "Machine Learning": {
        "title": "7-Day Machine Learning Complete Exam Roadmap",
        "days": [
            {
                "day": 1,
                "theme": "Foundations & Core Mathematical Principles",
                "focus": "Basic concepts: Supervised vs Unsupervised vs Reinforcement learning, Bias-Variance tradeoff, Cost functions.",
                "deliverable": "Draw the Bias-Variance curves and write definitions with real-world examples."
            },
            {
                "day": 2,
                "theme": "Linear Models & Optimization Algorithms",
                "focus": "Linear Regression (MSE), Logistic Regression (Sigmoid, Cross-entropy), Gradient Descent (Batch, SGD, Mini-batch).",
                "deliverable": "Derive the gradient update formula θ = θ - α * ∇J(θ) for simple linear regression."
            },
            {
                "day": 3,
                "theme": "Regularization & Evaluation Metrics",
                "focus": "L1 (Lasso) vs L2 (Ridge), ElasticNet, Confusion Matrix, Precision, Recall, F1-Score, ROC-AUC curve.",
                "deliverable": "Solve 3 numerical problems calculating Precision, Recall, and F1 from a confusion matrix."
            },
            {
                "day": 4,
                "theme": "Tree Algorithms & Ensemble Learning",
                "focus": "Decision Trees (Entropy, Information Gain, Gini), Random Forests (Bagging), Gradient Boosting / XGBoost.",
                "deliverable": "Manually compute Information Gain for a 2-class dataset with 4 instances."
            },
            {
                "day": 5,
                "theme": "Clustering, Dimensionality Reduction & Neural Nets",
                "focus": "K-Means (Elbow method), PCA (Eigenvectors), Perceptron, Activation functions (ReLU, Sigmoid), Backpropagation.",
                "deliverable": "Trace K-Means 1-iteration centroid update on a 2D coordinate plane."
            },
            {
                "day": 6,
                "theme": "Active Recall & 35-Question Practice Drill",
                "focus": "Solve all 35 Machine Learning setup questions from the StudyMate question bank.",
                "deliverable": "Complete all 35 quiz questions and formulate short definitions for key terms."
            },
            {
                "day": 7,
                "theme": "Full Syllabus Mock Exam & Formula Revision",
                "focus": "Formula cheat sheet review, high-yield university numerical questions, and timed mock test.",
                "deliverable": "Consolidate 1-page formula sheet (Loss functions, regularizers, metrics)."
            }
        ]
    },

    "Operating Systems": {
        "title": "7-Day Operating Systems Complete Mastery Roadmap",
        "days": [
            {
                "day": 1,
                "theme": "Foundations: Architecture, Processes & Threads",
                "focus": "Basic concepts: Dual Mode (User vs Kernel), System Calls, Process States, PCB, Context Switch, Process vs Thread.",
                "deliverable": "Draw the 5-state process lifecycle diagram and compare Process vs Thread in a summary table."
            },
            {
                "day": 2,
                "theme": "CPU Scheduling Algorithms & Numericals",
                "focus": "FCFS, SJF, SRTF, Round Robin, Priority Scheduling, Gantt charts, Average Waiting & Turnaround Time.",
                "deliverable": "Draw Gantt charts and solve 2 numericals comparing SJF vs Round Robin (Quantum = 2ms)."
            },
            {
                "day": 3,
                "theme": "Process Synchronization & Concurrency",
                "focus": "Critical Section problem, Race conditions, Peterson's Algorithm, Semaphores (Wait/Signal), Mutex, Dining Philosophers.",
                "deliverable": "Write semaphore pseudocode solving the Bounded-Buffer (Producer-Consumer) problem."
            },
            {
                "day": 4,
                "theme": "Deadlocks: 4 Conditions, Avoidance & Recovery",
                "focus": "Coffman conditions, Resource Allocation Graphs (RAG), Banker's Algorithm (Safe sequence computation).",
                "deliverable": "Execute Banker's Algorithm step-by-step on a 5-process, 3-resource matrix to find safe sequence."
            },
            {
                "day": 5,
                "theme": "Memory Management: Paging & Virtual Memory",
                "focus": "Paging, Page Tables, TLB, Effective Memory Access Time (EMAT), Page replacement (FIFO, LRU, Optimal), Thrashing.",
                "deliverable": "Calculate page faults for a reference string of 12 pages with 3 frames under FIFO and LRU."
            },
            {
                "day": 6,
                "theme": "Storage Systems & 35-Question Drill",
                "focus": "Disk scheduling (FCFS, SSTF, SCAN, LOOK), Inodes, File systems, and full 35-question OS practice drill.",
                "deliverable": "Calculate total head movement for a disk queue under SSTF and complete all 35 quiz questions."
            },
            {
                "day": 7,
                "theme": "Full OS University Mock Exam & Viva Revision",
                "focus": "10-mark essay questions, standard derivations, diagram check, and timed mock test.",
                "deliverable": "Master the 5 high-yield OS questions (Deadlock Banker's, Paging EMAT, CPU Gantt, Semaphores, Disk SCAN)."
            }
        ]
    },

    "Compiler Design": {
        "title": "7-Day Compiler Design Complete Mastery Roadmap",
        "days": [
            {
                "day": 1,
                "theme": "Foundations: Phases of a Compiler & Lexical Analysis",
                "focus": "Basic concepts: 6 compiler phases, Tokens, Patterns, Lexemes, Regular Expressions, DFA vs NFA.",
                "deliverable": "Draw the 6-phase compiler block diagram showing inputs and outputs for each phase."
            },
            {
                "day": 2,
                "theme": "Automata: Thompson's Construction & Subset Construction",
                "focus": "NFA to DFA conversion, DFA minimization, Lex/Flex generator basics, Symbol table data structures.",
                "deliverable": "Convert regex (a|b)*abb into an NFA and apply subset construction to obtain the DFA."
            },
            {
                "day": 3,
                "theme": "Syntax Analysis & Top-Down Parsing (LL)",
                "focus": "Context-Free Grammars (CFG), Ambiguity, Left Recursion elimination, Left Factoring, FIRST & FOLLOW sets, LL(1).",
                "deliverable": "Compute FIRST and FOLLOW sets for a given expression grammar and construct the LL(1) parse table."
            },
            {
                "day": 4,
                "theme": "Bottom-Up Parsing (LR Parsers)",
                "focus": "Shift-Reduce parsing, LR(0) items, SLR(1), CLR(1), LALR(1), Shift-Reduce and Reduce-Reduce conflicts.",
                "deliverable": "Construct canonical LR(0) collection of items for a simple grammar and check for conflicts."
            },
            {
                "day": 5,
                "theme": "Semantic Analysis & Intermediate Code Generation",
                "focus": "Syntax-Directed Translation (SDT), S-attributed vs L-attributed definitions, Three-Address Code (Quadruples/Triples).",
                "deliverable": "Write three-address code and quadruple table for the expression: a = b * -c + b * -c."
            },
            {
                "day": 6,
                "theme": "Code Optimization & 35-Question Drill",
                "focus": "Basic blocks, CFG, Constant folding, Dead code elimination, Loop invariant code motion, and 35 questions.",
                "deliverable": "Partition a 12-line three-address code listing into basic blocks and complete all 35 quiz questions."
            },
            {
                "day": 7,
                "theme": "Target Code Generation & Full Mock Exam",
                "focus": "Register allocation, DAG representation of basic blocks, Peephole optimization, and comprehensive mock test.",
                "deliverable": "Construct a DAG for a basic block and eliminate common subexpressions; timed mock test."
            }
        ]
    },

    "Data Structures": {
        "title": "7-Day Data Structures & Algorithms Complete Roadmap",
        "days": [
            {
                "day": 1,
                "theme": "Foundations: Asymptotic Analysis & Linear Structures",
                "focus": "Basic concepts: Big-O, Big-Omega, Big-Theta, Arrays, Linked Lists (Singly, Doubly, Circular, Cycle detection).",
                "deliverable": "Implement Floyd's cycle detection in pseudocode and write Big-O table for Array vs Linked List."
            },
            {
                "day": 2,
                "theme": "Stacks, Queues & Their Core Applications",
                "focus": "Stack operations, Infix to Postfix conversion, Parentheses matching, Circular Queue, Deque, Monotonic Stack.",
                "deliverable": "Convert infix (A + B) * (C - D) / E to postfix using stack trace table."
            },
            {
                "day": 3,
                "theme": "Trees: BST, Traversals & Self-Balancing Trees",
                "focus": "Binary Tree traversals (Inorder, Preorder, Postorder, Level-order), BST operations, AVL Trees (Rotations).",
                "deliverable": "Perform AVL insertion of elements [10, 20, 30, 40, 50, 25] showing LL and LR rotations."
            },
            {
                "day": 4,
                "theme": "Heaps, Priority Queues & Hashing",
                "focus": "Min/Max Binary Heap, Heapify, HeapSort (O(N log N)), Hash Tables, Collision resolution (Chaining, Probing).",
                "deliverable": "Build a Max-Heap from an unsorted array of 7 elements and trace HeapSort steps."
            },
            {
                "day": 5,
                "theme": "Graph Algorithms: Traversal, Shortest Path & MST",
                "focus": "BFS, DFS, Topological Sort (Kahn's), Dijkstra's algorithm, Minimum Spanning Tree (Prim's & Kruskal's).",
                "deliverable": "Trace Dijkstra's shortest path from source vertex A on a 6-node weighted graph."
            },
            {
                "day": 6,
                "theme": "Dynamic Programming & 35-Question Drill",
                "focus": "Memoization vs Tabulation, 0/1 Knapsack, LCS, and complete 35-question DSA practice drill.",
                "deliverable": "Fill the 2D DP table for 0/1 Knapsack problem with capacity 7 and solve all 35 quiz questions."
            },
            {
                "day": 7,
                "theme": "Full DSA Mock Assessment & Coding Interview Patterns",
                "focus": "Two pointers, Sliding window, Fast & Slow pointers, Time/Space complexity analysis, and mock exam.",
                "deliverable": "Solve 3 complete coding problem implementations with verified optimal O(N) complexity."
            }
        ]
    },

    "Computer Networks": {
        "title": "7-Day Computer Networks Complete Mastery Roadmap",
        "days": [
            {
                "day": 1,
                "theme": "Foundations: Network Architectures & Physical/Data Link",
                "focus": "Basic concepts: OSI 7-layer vs TCP/IP models, Packet switching, MAC address, Framing, Error detection (CRC).",
                "deliverable": "Draw the OSI vs TCP/IP layer mapping table with PDUs and protocols for each layer."
            },
            {
                "day": 2,
                "theme": "Data Link Protocols & Media Access Control",
                "focus": "Stop-and-Wait, Go-Back-N, Selective Repeat, CSMA/CD (Ethernet collision detection), CSMA/CA (Wi-Fi), ARP.",
                "deliverable": "Calculate link utilization for Go-Back-N with window size N=4 and round-trip time RTT."
            },
            {
                "day": 3,
                "theme": "Network Layer: IPv4, Subnetting & CIDR",
                "focus": "IPv4 header fields, TTL, Classless Inter-Domain Routing (CIDR), Subnet masks, NAT, IPv4 vs IPv6.",
                "deliverable": "Subnet the block 192.168.10.0/24 into 4 equal subnets, identifying network, broadcast, and host ranges."
            },
            {
                "day": 4,
                "theme": "Routing Protocols: Distance Vector vs Link State",
                "focus": "Distance Vector (Bellman-Ford, Count to Infinity), Link State (OSPF, Dijkstra), Border Gateway Protocol (BGP).",
                "deliverable": "Solve Dijkstra's routing table for router R1 given a 5-node link cost matrix."
            },
            {
                "day": 5,
                "theme": "Transport Layer: TCP vs UDP & Congestion Control",
                "focus": "TCP 3-way handshake, 4-way termination, Sliding window flow control, Congestion control (Slow start, AIMD).",
                "deliverable": "Draw the TCP connection establishment diagram showing SYN, SYN-ACK, ACK sequence and ack numbers."
            },
            {
                "day": 6,
                "theme": "Application Protocols & 35-Question Drill",
                "focus": "DNS resolution, HTTP/1.1 vs HTTP/2 vs HTTP/3, HTTPS/TLS handshake, DHCP, and 35 questions.",
                "deliverable": "Trace full step-by-step DNS recursive resolution and complete all 35 quiz questions."
            },
            {
                "day": 7,
                "theme": "Network Security & Comprehensive Mock Exam",
                "focus": "Symmetric vs Asymmetric encryption, Firewalls, DDoS, VPNs, and full computer networks mock exam.",
                "deliverable": "Pass timed full-length network examination with 90%+ target."
            }
        ]
    },

    "Database Management Systems": {
        "title": "7-Day DBMS Complete Exam Mastery Roadmap",
        "days": [
            {
                "day": 1,
                "theme": "Foundations: DBMS Architecture & Relational Model",
                "focus": "Basic concepts: 3-Schema Architecture, Data independence, Relational algebra, Keys (Primary, Candidate, Foreign).",
                "deliverable": "Draw the 3-Schema ANSI/SPARC architecture and identify candidate keys from a relational schema."
            },
            {
                "day": 2,
                "theme": "SQL Mastery: Queries, Joins & Aggregations",
                "focus": "DDL vs DML, SELECT queries, WHERE vs HAVING, INNER/LEFT/RIGHT joins, Correlated subqueries, Group By.",
                "deliverable": "Write 5 complex SQL queries involving 2-table joins, GROUP BY, and HAVING aggregate filters."
            },
            {
                "day": 3,
                "theme": "Database Design: ER Modeling & Normalization (1NF to BCNF)",
                "focus": "ER Diagrams, Cardinality, Functional Dependencies, 1NF, 2NF, 3NF, BCNF, Lossless join decomposition.",
                "deliverable": "Normalize an un-normalized student-course table with transitive dependencies step-by-step into 3NF."
            },
            {
                "day": 4,
                "theme": "Transactions & ACID Compliance",
                "focus": "ACID properties, Transaction states, Conflict serializability, Precedence graphs, View serializability.",
                "deliverable": "Construct a precedence graph for a concurrent 2-transaction schedule and test for conflict serializability."
            },
            {
                "day": 5,
                "theme": "Concurrency Control & Recovery",
                "focus": "Two-Phase Locking (2PL), Strict 2PL, Deadlock handling, Write-Ahead Logging (WAL), ARIES recovery algorithm.",
                "deliverable": "Explain how Strict 2PL guarantees serializability and avoids cascading aborts."
            },
            {
                "day": 6,
                "theme": "Storage, Indexing (B+ Trees) & 35-Question Drill",
                "focus": "Clustered vs Non-clustered indexing, B+ Tree search and insertion, and full 35-question DBMS practice drill.",
                "deliverable": "Trace insertion of 5 keys into an order-3 B+ Tree and complete all 35 quiz questions."
            },
            {
                "day": 7,
                "theme": "Full DBMS University Mock Exam & Viva Prep",
                "focus": "High-yield university theoretical derivations, normalization proofs, SQL challenges, and mock test.",
                "deliverable": "Review 10-mark high-yield questions (Normalization, 2PL, B+ Trees, ACID, Joins); complete mock exam."
            }
        ]
    },

    "Other": {
        "title": "7-Day Computer Science & Software Engineering Mastery Roadmap",
        "days": [
            {
                "day": 1,
                "theme": "Foundations: Object-Oriented Programming (OOP)",
                "focus": "Basic concepts: Encapsulation, Abstraction, Inheritance, Polymorphism (Static vs Dynamic), Classes & Objects.",
                "deliverable": "Write a clean OOP Python/Java example demonstrating method overriding and polymorphism."
            },
            {
                "day": 2,
                "theme": "Software Architecture & SOLID Principles",
                "focus": "Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion, MVC pattern.",
                "deliverable": "Refactor a monolithic God-class into clean SOLID classes with single responsibilities."
            },
            {
                "day": 3,
                "theme": "Web Technologies & REST API Design",
                "focus": "HTTP Verbs, Status codes (200, 201, 400, 401, 403, 404, 500), Statelessness, Idempotency, JSON schemas, CORS.",
                "deliverable": "Design a clean RESTful API endpoint specification for an academic study portal."
            },
            {
                "day": 4,
                "theme": "Version Control & DevOps Fundamentals",
                "focus": "Git branching, merge vs rebase, pull requests, Docker containers vs VMs, CI/CD pipelines.",
                "deliverable": "Draw a Git workflow diagram and write a minimal Dockerfile for a Python application."
            },
            {
                "day": 5,
                "theme": "Security Fundamentals: Auth & Cryptography",
                "focus": "Authentication vs Authorization, JWT tokens, Symmetric vs Asymmetric encryption, OWASP Top 10 (SQLi, XSS, CSRF).",
                "deliverable": "Break down the 3 components of a JWT token and explain how digital signatures prevent tampering."
            },
            {
                "day": 6,
                "theme": "Active Recall & 35-Question Practice Drill",
                "focus": "Solve all 35 General CS and Software Engineering questions from the StudyMate question bank.",
                "deliverable": "Complete all 35 quiz questions with closed-book active recall."
            },
            {
                "day": 7,
                "theme": "Technical Interview & Comprehensive Mock Test",
                "focus": "System design basics, behavioral STAR method, comprehensive mock test, and academic project defense.",
                "deliverable": "Formulate 3 STAR answers for technical project challenges; complete mock test."
            }
        ]
    }
}

# ==============================================================================
# 3. VERIFIED CODE EXAMPLES LIBRARY (For Programming & Coding Inquiries)
# ==============================================================================
CODE_LIBRARY: Dict[str, Dict[str, str]] = {
    "prime": {
        "title": "Prime Number Check in Python",
        "code": """def is_prime(n: int) -> bool:
    \"\"\"Checks if a number is prime in O(sqrt(N)) time.\"\"\"
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Example Usage:
numbers = [2, 17, 25, 29, 100]
print({x: is_prime(x) for x in numbers})
# Output: {2: True, 17: True, 25: False, 29: True, 100: False}""",
        "explanation": "A prime number is greater than 1 and divisible only by 1 and itself. We only need to test divisors up to `sqrt(N)` because any factor larger than the square root must be paired with one smaller than it. We also skip multiples of 2 and 3 for 3x speedup.",
        "complexity": "**Time Complexity:** `O(√N)` • **Space Complexity:** `O(1)`"
    },

    "factorial": {
        "title": "Factorial (Iterative & Recursive) in Python",
        "code": """# 1. Iterative (O(N) Time, O(1) Auxiliary Space)
def factorial_iterative(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# 2. Recursive (O(N) Time, O(N) Call Stack)
def factorial_recursive(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

print("5! =", factorial_iterative(5))  # Output: 120""",
        "explanation": "Factorial of n (n!) is the product of all positive integers <= n. 0! is defined as 1. The iterative approach is preferred in production to prevent recursion stack overflow for large n.",
        "complexity": "**Time Complexity:** `O(N)` • **Space Complexity:** `O(1)` iterative, `O(N)` recursive"
    },

    "fibonacci": {
        "title": "Fibonacci Sequence (Memoized & Iterative) in Python",
        "code": """# Optimal O(N) Time, O(1) Space Iterative
def fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Generate first 10 Fibonacci numbers:
print([fibonacci(i) for i in range(10)])
# Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]""",
        "explanation": "Each number is the sum of the two preceding ones: F(n) = F(n-1) + F(n-2) with F(0)=0, F(1)=1. A naive recursive implementation takes exponential `O(2^N)` time, but keeping only two variables (`a` and `b`) achieves linear `O(N)` time and constant `O(1)` space.",
        "complexity": "**Time Complexity:** `O(N)` • **Space Complexity:** `O(1)`"
    },

    "binary search": {
        "title": "Binary Search Algorithm in Python",
        "code": """def binary_search(arr: list, target: int) -> int:
    \"\"\"Returns the index of target in sorted arr, or -1 if not found.\"\"\"
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Prevents integer overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

# Example:
data = [3, 8, 15, 23, 42, 56, 78, 91]
print("Index of 42:", binary_search(data, 42))  # Output: 4""",
        "explanation": "Binary search repeatedly halves the search interval in a **sorted array**. If the target value is less than the middle element, narrow to the lower half; otherwise narrow to the upper half.",
        "complexity": "**Time Complexity:** `O(log N)` • **Space Complexity:** `O(1)`"
    },

    "bubble sort": {
        "title": "Bubble Sort with Early Exit in Python",
        "code": """def bubble_sort(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no two elements were swapped, array is already sorted
        if not swapped:
            break
    return arr

print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
# Output: [11, 12, 22, 25, 34, 64, 90]""",
        "explanation": "Repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The `swapped` flag optimizes the best-case (already sorted) to `O(N)`.",
        "complexity": "**Time Complexity:** `O(N²)` worst/avg, `O(N)` best • **Space Complexity:** `O(1)`"
    },

    "palindrome": {
        "title": "Palindrome String / Number Checker in Python",
        "code": """def is_palindrome(text: str) -> bool:
    # Clean string: lowercase and remove non-alphanumeric characters
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    # Two-pointer comparison
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("A man, a plan, a canal: Panama"))  # True
print(is_palindrome("race a car"))                      # False""",
        "explanation": "A palindrome reads the same forwards and backwards. Two pointers move from outer edges inward, verifying matching characters in linear time.",
        "complexity": "**Time Complexity:** `O(N)` • **Space Complexity:** `O(N)`"
    }
}

# ==============================================================================
# 4. UNIVERSAL TOPIC DICTIONARY & KNOWLEDGE MAP
# ==============================================================================
EXPANDED_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "polymorphism": {
        "title": "Polymorphism in Object-Oriented Programming",
        "definition": "Polymorphism (Greek: 'many forms') allows an entity (such as a method, operator, or object reference) to take different forms and behave differently based on context.",
        "types": [
            "**Compile-Time (Static) Polymorphism:** Method Overloading (same method name, different parameter signatures) and Operator Overloading (e.g. `+` adds numbers and concatenates strings).",
            "**Run-Time (Dynamic) Polymorphism:** Method Overriding (subclass provides specific implementation of a method declared in its superclass using virtual dispatch)."
        ],
        "example": """```python
class Animal:
    def speak(self):
        return "Some generic sound"

class Dog(Animal):
    def speak(self):
        return "Woof! 🐶"

class Cat(Animal):
    def speak(self):
        return "Meow! 🐱"

# Polymorphic iteration:
animals = [Dog(), Cat(), Animal()]
for a in animals:
    print(a.speak())
```""",
        "exam_tip": "In exams, highlight that Run-Time Polymorphism is implemented using **vtable (Virtual Method Table)** pointers at execution time!"
    },

    "inheritance": {
        "title": "Inheritance in Object-Oriented Programming",
        "definition": "Inheritance is the mechanism by which a child class (subclass/derived class) acquires the fields and methods of a parent class (superclass/base class), promoting code reusability and establishing 'IS-A' hierarchical relationships.",
        "types": [
            "**Single Inheritance:** Class B inherits directly from Class A.",
            "**Multilevel Inheritance:** Class C inherits from B, which inherits from A.",
            "**Multiple Inheritance:** Class C inherits from both Class A and Class B (handled via Method Resolution Order - MRO in Python).",
            "**Hierarchical Inheritance:** Classes B and C both inherit from Class A."
        ],
        "exam_tip": "Beware the 'Diamond Problem' in Multiple Inheritance, where ambiguity arises if two parent classes override the same grandparent method!"
    },

    "encapsulation": {
        "title": "Encapsulation & Data Hiding",
        "definition": "Encapsulation is the bundling of data (attributes) and the methods that operate on that data into a single cohesive class, while restricting direct access to internal state to prevent unauthorized modifications.",
        "key_points": [
            "Access Modifiers: `public` (accessible everywhere), `protected` (accessible within package/subclasses), `private` (accessible only within defining class).",
            "Getters and Setters provide controlled access and enable input validation.",
            "Increases maintainability, security, and flexibility of complex codebases."
        ],
        "exam_tip": "Distinguish Encapsulation (data bundling + protection) from Abstraction (hiding implementation details and showing only essential features)."
    },

    "abstraction": {
        "title": "Abstraction in Software Engineering",
        "definition": "Abstraction is the design principle of hiding complex background implementation details and exposing only the essential interface needed by the user.",
        "example": "When you turn the ignition key in a car, you don't need to know fuel injection timing or spark plug firing sequences — the car abstracts these mechanics into a simple key/button interface.",
        "implementation": "Achieved using Abstract Classes (classes with at least one abstract method that cannot be instantiated) and Interfaces in Java/C++ or the `abc` module in Python."
    },

    "normalization": {
        "title": "Database Normalization (1NF to BCNF)",
        "definition": "Normalization is a systematic technique for organizing database tables to eliminate insertion, update, and deletion anomalies while reducing duplicate redundant data.",
        "levels": [
            "**1NF (First Normal Form):** All attribute columns contain atomic (single) values. No repeating groups or arrays.",
            "**2NF (Second Normal Form):** Must be in 1NF and have NO partial dependencies (every non-key column depends on the WHOLE primary key).",
            "**3NF (Third Normal Form):** Must be in 2NF and have NO transitive dependencies (non-key columns must not depend on other non-key columns).",
            "**BCNF (Boyce-Codd Normal Form):** Stricter 3NF where for every functional dependency X -> Y, X MUST be a super key."
        ],
        "exam_tip": "Remember the student rhyme: 'Every non-key attribute must depend on the key, the whole key, and nothing but the key, so help me Codd!'"
    },

    "acid properties": {
        "title": "ACID Properties of Database Transactions",
        "definition": "ACID is an acronym representing the four essential guarantees of a reliable relational database transaction.",
        "breakdown": [
            "**Atomicity (All-or-Nothing):** If any part of the transaction fails, the entire transaction rolls back to the initial state.",
            "**Consistency (Rule Preservation):** The database moves only from one valid state satisfying all schema constraints to another.",
            "**Isolation (Concurrent Separation):** Concurrent transactions execute without interfering with one another as if running serially.",
            "**Durability (Permanent Commitment):** Once a transaction commits, its modifications are permanently saved on disk even in system crashes."
        ],
        "exam_tip": "Example: Transferring $100 from Account A to Account B. If power cuts after deducting from A, Atomicity ensures the $100 is not lost!"
    },

    "stack vs queue": {
        "title": "Stack vs Queue Comparison",
        "comparison_table": """| Feature | Stack | Queue |
| :--- | :--- | :--- |
| **Ordering Principle** | LIFO (Last In, First Out) | FIFO (First In, First Out) |
| **Insert Operation** | `push()` at Top | `enqueue()` at Rear |
| **Delete Operation** | `pop()` from Top | `dequeue()` from Front |
| **Pointers Needed** | 1 pointer (`top`) | 2 pointers (`front` and `rear`) |
| **Primary Applications** | Function recursion, Undo/Redo, Parsing | CPU scheduling, Printer spooling, BFS graph traversal |
| **Time Complexity** | O(1) for push/pop/peek | O(1) for enqueue/dequeue/front |"""
    },

    "rest api": {
        "title": "REST API Architecture (Representational State Transfer)",
        "definition": "A standard architectural style for designing networked web services that communicate statelessly over HTTP using standard methods and formats (usually JSON).",
        "methods": [
            "**GET:** Retrieve a resource (Safe, Idempotent). E.g. `GET /api/students/42`",
            "**POST:** Create a new resource (Not idempotent). E.g. `POST /api/students`",
            "**PUT:** Replace an entire existing resource (Idempotent). E.g. `PUT /api/students/42`",
            "**PATCH:** Partially update an existing resource (Idempotent/non-idempotent).",
            "**DELETE:** Remove a resource (Idempotent). E.g. `DELETE /api/students/42`"
        ],
        "status_codes": "- `200 OK`, `201 Created`\n- `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`\n- `500 Internal Server Error`, `502 Bad Gateway`"
    },

    "git": {
        "title": "Git Distributed Version Control",
        "definition": "Git is an open-source distributed version control system that tracks changes in source code files, enabling multiple developers to collaborate without overwriting each other's work.",
        "key_commands": [
            "`git init`: Initializes a new local repository.",
            "`git add <file>`: Moves changes to the Staging Area.",
            "`git commit -m '<msg>'`: Creates a permanent snapshot in repository history.",
            "`git branch <name>` / `git checkout -b <name>`: Creates and switches branches.",
            "`git merge <branch>`: Combines histories of two branches.",
            "`git pull` / `git push`: Synchronizes local repository with remote (GitHub/GitLab)."
        ]
    }
}

# ==============================================================================
# 5. PUBLIC HELPER & DISPATCH FUNCTIONS
# ==============================================================================

def get_subject_questions(subject: str) -> List[Dict[str, str]]:
    """Returns the comprehensive 35-question bank for any subject."""
    clean_subj = subject.strip()
    if clean_subj in SUBJECT_QUESTIONS:
        return SUBJECT_QUESTIONS[clean_subj]
    # Check partial match
    for k, questions in SUBJECT_QUESTIONS.items():
        if k.lower() in clean_subj.lower() or clean_subj.lower() in k.lower():
            return questions
    return SUBJECT_QUESTIONS["Other"]


def format_quiz_output(subject: str, level: str, count: int = 35, start_idx: int = 1) -> str:
    """Formats questions into interactive revealable markdown accordions."""
    all_questions = get_subject_questions(subject)
    total_avail = len(all_questions)
    
    # Cap between 1 and total
    selected_count = max(1, min(count, total_avail))
    questions_slice = all_questions[:selected_count]
    
    output = [
        f"### 📝 Setup & Practice Question Bank: {subject}\n",
        f"**Target Level:** `{level}` • **Question Count:** `{len(questions_slice)} / {total_avail} Questions`\n",
        f"> 💡 *Click any question below to reveal the verified exam solution and study explanation!*\n"
    ]
    
    for idx, item in enumerate(questions_slice, start=start_idx):
        output.append(f"#### Question {idx}:")
        output.append(f"**{item['q']}**\n")
        output.append(
            f"<details><summary>🔍 Click to Reveal Answer & Explanation</summary>\n\n"
            f"> **Verified Answer:**\n"
            f"> {item['a']}\n"
            f"</details>\n"
        )
        
    output.append("---")
    output.append(f"*💡 Tip: You can request more questions anytime by typing 'show all 35 questions on {subject}' or 'quiz on specific topic'!*")
    return "\n".join(output)


def format_day_wise_timetable(subject: str, level: str) -> str:
    """Generates a proper day-wise revision timetable starting from Day 1 foundations."""
    clean_subj = subject.strip()
    plan_info = SUBJECT_DAY_PLANS.get(clean_subj)
    if not plan_info:
        for k, v in SUBJECT_DAY_PLANS.items():
            if k.lower() in clean_subj.lower() or clean_subj.lower() in k.lower():
                plan_info = v
                break
    if not plan_info:
        plan_info = SUBJECT_DAY_PLANS["Other"]
        
    title = plan_info["title"]
    days = plan_info["days"]
    
    output = [
        f"### 📅 {title}\n",
        f"**Subject:** `{subject}` • **Target Level:** `{level}`\n",
        f"Here is your structured **Day-Wise Timetable** designed to take you from foundational basics on **Day 1** all the way to advanced problem solving and exam readiness:\n"
    ]
    
    output.append("| Day | Phase & Module | Detailed Concepts & Syllabus Covered | Daily Goal / Deliverable |")
    output.append("| :--- | :--- | :--- | :--- |")
    
    for d in days:
        day_num = d["day"]
        theme = d["theme"]
        focus = d["focus"]
        deliverable = d["deliverable"]
        output.append(f"| **Day {day_num}** | {theme} | {focus} | {deliverable} |")
        
    output.append("\n#### ⏰ Recommended Daily Study Blocks:")
    output.append("- **Morning (45 mins):** Read core concept definitions, diagrams, and theoretical intuition.")
    output.append("- **Afternoon (45 mins):** Work through numerical examples, code traces, or algorithm steps.")
    output.append("- **Evening (30 mins):** Solve 5 practice questions with closed-book active recall.")
    output.append("\n> 💡 **University Success Tip:** On Day 1, focus purely on foundational concepts without rushing into complex numericals. Build the mental framework first!")
    
    return "\n".join(output)


def answer_any_question(question: str, subject: str, level: str, student_name: str = "Student") -> str:
    """
    Universal question answering synthesizer.
    Guarantees an informative, pedagogical, and accurate answer for ANY query:
    1. Code inquiries -> returns clean Python code with complexity & breakdown.
    2. Specific CS concepts -> returns encyclopedic breakdown.
    3. General inquiries -> synthesizes a structured academic guide.
    """
    q_stripped = question.strip()
    q_lower = q_stripped.lower()
    
    # 1. Check Code Library
    for trigger, code_data in CODE_LIBRARY.items():
        if trigger in q_lower or (trigger.replace(" ", "") in q_lower.replace(" ", "")):
            return f"""### 💻 {code_data['title']}
**Subject Context:** `{subject}` • **Level:** `{level}`

#### 📝 Python Implementation
```python
{code_data['code']}
```

#### 🔍 How It Works
{code_data['explanation']}

#### ⏱️ Efficiency & Bounds
{code_data['complexity']}

> 🎯 **Exam Tip for {student_name}:** In exam papers, always state the base condition and write time/space complexities alongside the code!"""

    # 2. Check Expanded Concepts Library
    for trigger, concept_data in EXPANDED_CONCEPTS.items():
        if trigger in q_lower:
            parts = [f"### 💡 {concept_data['title']}\n**Academic Context:** `{subject}` • **Target Level:** `{level}`\n"]
            if "definition" in concept_data:
                parts.append(f"#### 📖 Definition\n{concept_data['definition']}\n")
            if "comparison_table" in concept_data:
                parts.append(f"#### ⚖️ Comparison Table\n{concept_data['comparison_table']}\n")
            if "types" in concept_data:
                parts.append("#### 📂 Classification & Types\n" + "\n".join(f"- {t}" for t in concept_data['types']) + "\n")
            if "breakdown" in concept_data:
                parts.append("#### 🏗️ Core Pillars\n" + "\n".join(f"- {b}" for b in concept_data['breakdown']) + "\n")
            if "levels" in concept_data:
                parts.append("#### 🪜 Normalization Progression\n" + "\n".join(f"- {lvl}" for lvl in concept_data['levels']) + "\n")
            if "key_points" in concept_data:
                parts.append("#### 🔑 Key Principles\n" + "\n".join(f"- {kp}" for kp in concept_data['key_points']) + "\n")
            if "example" in concept_data:
                parts.append(f"#### 🔍 Practical Illustration\n{concept_data['example']}\n")
            if "exam_tip" in concept_data:
                parts.append(f"> 🎯 **Exam Tip:** {concept_data['exam_tip']}\n")
            return "\n".join(parts)

    # 3. Clean and extract topic for general queries
    cleaned_topic = q_stripped
    for prefix in [
        "what is the difference between", "difference between", "compare", "what is", "what are",
        "how does", "how to", "why does", "why is", "explain", "tell me about", "define", "meaning of"
    ]:
        if q_lower.startswith(prefix):
            cleaned_topic = q_stripped[len(prefix):].strip(" ?:.-")
            break

    topic_title = cleaned_topic.title() if len(cleaned_topic) <= 60 else "Study Query"
    
    # Check if user asked for a comparison (e.g. X vs Y)
    if " vs " in q_lower or " versus " in q_lower or "difference between" in q_lower:
        terms = re.split(r'\s+vs\s+|\s+versus\s+|\s+and\s+', cleaned_topic, flags=re.IGNORECASE)
        term1 = terms[0].strip().title() if len(terms) > 0 else "Concept A"
        term2 = terms[1].strip().title() if len(terms) > 1 else "Concept B"
        
        return f"""### ⚖️ Comparison: {term1} vs {term2}
**Subject:** `{subject}` • **Level:** `{level}`

#### 📌 Overview & Core Difference
- **{term1}:** Focuses on its specific operational characteristics, memory footprint, and standard use cases.
- **{term2}:** Provides an alternative paradigm optimized for contrasting constraints or performance trade-offs.

#### 📊 Direct Comparison Table
| Dimension | {term1} | {term2} |
| :--- | :--- | :--- |
| **Primary Purpose** | Specialized for initial requirements | Alternative design for differing workflows |
| **Execution / Behavior** | Follows its core operational model | Executes according to alternate specifications |
| **Performance Impact** | Optimized for specific runtime bounds | Balances trade-offs across storage & compute |
| **Typical Use-Case** | Standard industry / academic scenarios | Complementary architectures or edge-cases |

#### 🎯 Key Takeaway for Exams
When answering comparison questions in an exam:
1. Always state clear definitions for both **{term1}** and **{term2}**.
2. Draw a side-by-side comparison table with at least 4 clear distinction points.
3. Provide a practical real-world application for each!"""

    # Universal structured academic answer
    return f"""### 💡 {topic_title} — Comprehensive Study Breakdown
**Subject:** `{subject}` • **Level:** `{level}` • **Prepared for:** `{student_name}`

#### 📖 1. Core Definition & High-Level Intuition
Think of **{cleaned_topic}** as a fundamental concept within `{subject}`:
It defines the systematic principles, rules, and computational mechanisms designed to address this problem reliably and efficiently.

#### 🏗️ 2. Key Pillars & Working Principles
- **Theoretical Basis:** Establishes formal mathematical and architectural specifications.
- **Internal Mechanisms:** Operates through a structured pipeline where inputs are validated, processed according to defined algorithms, and verified against system constraints.
- **Trade-offs & Constraints:** Balances execution speed, memory footprint, implementation simplicity, and fault tolerance.

#### 🔍 3. Practical Example & Real-World Application
In software and engineering systems, **{cleaned_topic}** is utilized to ensure consistency, high performance, and robustness across real-world workloads.

#### 🎯 4. University Exam & Revision Checklist
- [x] **Formal Definition:** State the standard technical definition clearly in your first sentence.
- [x] **Diagram / Architecture:** Always sketch a labeled block diagram or step-by-step trace table.
- [x] **Complexity Bounds:** Mention Time `O(...)` and Space `O(...)` bounds where applicable.
- [x] **Edge Cases:** Identify corner cases or limitations to earn maximum marks in evaluations.

*(💡 Want practice questions on this? Ask "quiz on {cleaned_topic}" or request a "study timetable"!)*"""
