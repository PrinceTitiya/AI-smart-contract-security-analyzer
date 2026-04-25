
# AI Smart Contract Security Analyzer (AISCSA)
---

# Overview

**AISSCA (AI Smart Contract Security Analyzer)** is an intelligent security analysis system that combines:

* Static analysis (rule-based detection)
* Retrieval-Augmented Generation (RAG)
* Large Language Models (LLMs)

to analyze Solidity smart contracts, identify vulnerabilities, and generate human-readable security reports.

---

#  Objective

Traditional tools like Slither detect vulnerabilities but lack:

* Context
* Real-world pattern matching
* Explanation clarity

AISCA solves this by building a **multi-stage AI pipeline**:

```text
Detect → Retrieve → Filter → Explain
```

---

# 🧠Core Architecture

```text
User Contract (.sol)
        ↓
[ Slither Analysis Engine ]
        ↓
[ Function Extraction Layer ]
        ↓
[ Embedding Engine ]
        ↓
[ Vector Database (SCV Dataset) ]
        ↓
[ RAG Retrieval Engine ]
        ↓
[ Filtering & Ranking Layer ]
        ↓
[ LLM Explanation Engine ]
        ↓
Final Security Report
```

---

# 🔍 System Components (Deep Explanation)

---

## 1. Static Analysis Layer

**Tool Used:** Slither

### Role:

* Detect known vulnerability patterns
* Provide deterministic analysis

### Output Example:

```text
reentrancy-eth (High)
timestamp (Low)
low-level-calls (Info)
```

### Key Insight:

```text
Slither = Ground Truth Engine
```

---

## 2. Function Extraction Layer

### Problem Solved:

Whole-contract analysis is noisy.

### Solution:

Extract **function-level code blocks** using Slither’s internal parsing:

```python
function.source_mapping.content
```

### Result:

```text
deposit()
withdraw()
getContractBalance()
```

### Why Important:

```text
Vulnerabilities exist at function level, not contract level
```

---

## 3. Embedding Engine

### Role:

Convert Solidity code into vector representations.

```text
function withdraw() → vector embedding
```

### Properties Captured:

* Code structure
* Logical patterns
* Semantic meaning

---

## 4. Vector Database (RAG Memory)

### Dataset Used:

**Smart Contract Vulnerability Dataset (SCV)**

### Each Entry:

```json
{
  "category": "Reentrancy",
  "code_snippet": "...",
  "description": "...",
  "severity": "High"
}
```

### Stored As:

```text
Embedding → vector
Metadata → vulnerability info
```

---

## 5. RAG (Retrieval Engine)

### Process:

For each function:

```text
Function → embedding → similarity search → top matches
```

### Output Example:

```text
withdraw():
  → Reentrancy (0.05)
  → Reentrancy (0.07)
```

### Important:

```text
RAG = similarity engine (NOT truth engine)
```

---

## 6. Filtering & Ranking Layer (Phase 4)

### Purpose:

Remove noise and improve precision.

### Filters Applied:

---

### 1. Distance Threshold

```text
distance > 0.4 → discard
```

Removes weak matches.

---

### 2. Slither Alignment

```text
Only keep matches related to Slither-detected issues
```

Example:

```text
Slither: reentrancy
RAG: overflow → removed ❌
RAG: reentrancy → kept ✅
```

---

### 3. Deduplication

```text
Keep best match per vulnerability
```

---

### 4. Function-Level Filtering

```text
Safe functions → no matches
Vulnerable functions → focused matches
```

---

### Result:

```text
deposit() → No relevant matches
withdraw() → Reentrancy (0.05)
```

---

## 7. LLM Explanation Engine

**Model:** Local LLM via Ollama (e.g., Llama)

### Input:

* Slither vulnerabilities
* Filtered RAG context

### Output:

```text
- Vulnerability explanation
- Exploitation method
- Real-world analogy
- Suggested fix
```

---

# 🔄 Full System Flow

---

## Step-by-Step Execution

---

### 1. Input

User provides:

```bash
python analyze.py contract.sol
```

---

### 2. Slither Analysis

```text
Detect vulnerabilities
```

---

### 3. Function Extraction

```text
Split contract → functions
```

---

### 4. Embedding

```text
Each function → vector
```

---

### 5. RAG Retrieval

```text
Find similar vulnerabilities from dataset
```

---

### 6. Filtering

```text
Remove noise using:
- Distance
- Slither alignment
- Deduplication
```

---

### 7. Context Building

```text
Create structured RAG summary
```

---

### 8. LLM Explanation

```text
Generate final human-readable report
```

---

#  Example Output Behavior

---

## Input Contract

```solidity
withdraw() uses msg.sender.call before state update
```

---

## Output

```text
Function: withdraw()
→ Reentrancy (0.05)

Explanation:
- External call before state update
- Allows recursive withdrawal
- Similar to DAO hack
- Fix: Checks-Effects-Interactions pattern
```

---

#  Known Limitations

---

## 1. Dataset Coverage

```text
RAG only works if dataset contains relevant patterns
```

Example:

* Reentrancy → strong detection ✅
* Timestamp dependency → weak detection ❌

---

## 2. String-Based Matching

```text
Current matching uses substring logic
```

Future improvement:

```text
Embedding-based alignment
```

---

## 3. Fixed Threshold

```text
distance threshold = 0.4
```

Future:

```text
Adaptive thresholding
```

---

#  Key Design Principles

---

## 1. Hybrid Intelligence

```text
Static + Retrieval + Generative AI
```

---

## 2. Separation of Concerns

```text
Detection ≠ Retrieval ≠ Explanation
```

---

## 3. Precision over Noise

```text
Better to show nothing than wrong results
```

---

## 4. Data-Driven Intelligence

```text
System quality depends on dataset quality
```

---

# 📈 Evolution of the System

---

## Phase 1

```text
Slither only → basic detection
```

---

## Phase 2

```text
RAG added → weak influence
```

---

## Phase 3

```text
Function-level RAG → strong similarity
```

---

## Phase 4 (Current)

```text
Filtering layer → precision + reliability
```

---

#  Future Improvements

---

## Phase 5 (Planned)

* Embedding-based vulnerability alignment
* Exploit (PoC) generation
* Multi-function reasoning
* Cross-contract analysis
* Dynamic threshold tuning

---

#  How to Run

---

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Run analyzer

```bash
python analyze.py test.sol
```

---

## 3. Output includes:

* Vulnerability list
* Security score
* Filtered RAG matches
* AI-generated explanation

---

#  Final System Identity

---

AISCA is not just:

```text
❌ A static analyzer
❌ A chatbot
```

---

It is:

```text
 An AI-powered smart contract auditing system
```

---

*~ Author: Prince Titiya ~*


