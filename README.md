# AI Smart Contract Security Analyzer

An **AI-powered smart contract auditing system** that combines **static analysis (Slither)** with **Retrieval-Augmented Generation (RAG)** and a **local LLM (Llama3 via Ollama)** to detect, analyze, and explain vulnerabilities in Solidity contracts.

---

# 🚀 Overview

This project is designed to simulate how a **real-world smart contract auditor** works:

- **Static tools** detect known vulnerabilities
- **AI retrieves similar exploit patterns**
- **LLM explains issues like a human expert**

---

# 🧠 System Architecture

```
            ┌──────────────┐
            │   Contract   │
            └──────┬───────┘
                   ↓
        ┌──────────────────────────┐
        │Static Analysis (Slither) │
        └──────────┬───────────────┘
                   ↓
            Vulnerabilities (facts)
                   ↓
               Scoring Engine
                   +
        ┌──────────────────────────┐
        │  Embedding Model         │
        └──────────┬───────────────┘
                   ↓
            Vector Database (ChromaDB)
                   ↓
         Similar Contracts Retrieved
                   ↓
              Metadata (context)
                   ↓
        ┌──────────────────────────┐
        │  LLM (Llama3 via Ollama) │
        └──────────┬───────────────┘
                   ↓
        Final Security Report
```

---

# Tech Stack

### 🔹 Static Analysis

- **Slither** → vulnerability detection

### 🔹 AI / RAG

- **SentenceTransformers (MiniLM)** → embeddings
- **ChromaDB** → vector database

### 🔹 LLM

- **Ollama + Llama3 / Mistral** → explanation engine

### 🔹 Language

- Python

---

# 📁 Project Structure

```
ai-smart-contract-analyzer/

├── analyzer/
│   ├── loader.py            # Load contract
│   ├── slither_runner.py    # Run Slither
│   ├── parser.py            # Extract vulnerabilities
│   ├── embedder.py          # Generate embeddings
│   ├── vector_store.py      # ChromaDB interface
│   ├── rag_engine.py        # Similarity search
│   ├── data_loader.py       # Load dataset into DB
│   ├── llm_engine.py        # LLM explanation
│
├── data/
│   ├── vulnerable_contracts/
│   ├── metadata.json
│
├── analyze.py               # Main CLI entry point
└── README.md
```

---

# 🔄 System Flow (Step-by-Step)

---

## 🟢 1. Input Layer

User provides:

```
.sol file
```

Handled by:

```python
loader.py
```

👉 Output: Raw Solidity code (string)

---

## 🟢 2. Static Analysis (Slither)

```python
slither_runner.py
```

Runs:

```
slither contract.sol --json result.json
```

👉 Output:

```json
{
  "check": "reentrancy-eth",
  "impact": "High",
  "description": "..."
}
```

---

## 🟢 3. Parsing Layer

```python
parser.py
```

Extracts structured vulnerabilities:

```json
[
  {
    "check": "reentrancy-eth",
    "impact": "High"
  }
]
```

---

## 🟢 4. Scoring Engine

```python
analyze.py
```

Uses weighted scoring:

| Impact        | Penalty |
| ------------- | ------- |
| High          | -25     |
| Medium        | -15     |
| Low           | -10     |
| Informational | -5      |

👉 Example:

```
Score = 100 - penalties
```

---

## 🟡 5. Embedding Layer (AI)

```python
embedder.py
```

Converts contract into vector:

```
Solidity Code → 384-dim vector
```

👉 Represents **semantic meaning of code**

---

## 🟡 6. Vector Database (Memory)

```python
vector_store.py
```

Stores:

```
[id, contract_code, embedding, metadata]
```

---

## 🟡 7. Dataset (Knowledge Base)

### Why needed?

AI needs **examples to compare against**

---

### 📄 metadata.json

```json
{
  "vulnerability": "reentrancy",
  "description": "External call before state update..."
}
```

👉 Adds **meaning to raw code**

---

### Key Insight

```
Code alone = syntax
Code + metadata = knowledge
```

---

## 🟡 8. RAG Engine (Similarity Search)

```python
rag_engine.py
```

Process:

```
Input contract → embedding → compare with DB → retrieve closest matches
```

---

### Similarity Metric

- Uses **vector distance**
- Lower = more similar

```
0.0 → identical
0.1 → very similar
0.3+ → less similar
```

---

## 🔵 9. LLM Explanation Engine

```python
llm_engine.py
```

Uses:

- Contract code
- Slither output
- RAG insights

---

### Prompt Structure

```
Contract
+
Detected Issues
+
Similar Patterns
↓
LLM Explanation
```

---

### Output

```
- Explanation
- Exploitation scenario
- Fix suggestions
```

---

# 🧠 Core Design Philosophy

---

## 🔹 1. Hybrid Intelligence

```
Slither → factual correctness
RAG → contextual similarity
LLM → human explanation
```

---

## 🔹 2. Grounded AI

LLM is NOT allowed to guess.

```
AI is grounded on:
✔ Slither results
✔ RAG context
```

---

## 🔹 3. Modular Architecture

Each component is independent:

- Can upgrade embeddings
- Can swap LLM
- Can improve dataset

---

# 🧪 Example Output

```
===== SECURITY REPORT =====
Score: 65/100

===== AI SECURITY ANALYSIS =====

1. Reentrancy Vulnerability:
Explanation: External call before state update...
Attack: Recursive withdraw exploit...
Fix: Use Checks-Effects-Interactions pattern

2. Solidity Version Issue:
...

3. Low-Level Call Risk:
...
```

---

# ⚠️ Current Limitations

- LLM runs locally → slow on CPU
- Dataset is small → limited intelligence
- No UI/API (CLI only)
- No AST-level analysis

---

# 🚀 Future Improvements

### 🔹 Performance

- Use smaller models (Mistral)
- GPU acceleration

### 🔹 AI Improvements

- Code-specific embeddings
- AST-based chunking

### 🔹 Productization

- FastAPI backend
- Web dashboard
- Upload GitHub repo

---

# 🎯 Key Learnings

This project demonstrates:

- ✅ Smart contract security fundamentals
- ✅ Static analysis integration
- ✅ RAG system design
- ✅ LLM grounding techniques
- ✅ End-to-end AI system architecture

---

# 🧠 Final Insight

This system is NOT:

```
AI replacing auditors
```

It is:

```
AI assisting auditors
```

---

# 🏁 Conclusion

You have built a:

```
Real AI-powered Smart Contract Security Analyzer
```

with:

- Deterministic detection
- Contextual intelligence
- Human-like explanation
---
