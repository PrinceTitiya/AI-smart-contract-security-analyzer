import ollama

def generate_explanation(contract_code, vulnerabilities, rag_context):
    prompt = f"""
You are a smart contract security auditor.

STRICT RULES:
- Use ONLY the vulnerabilities provided in "Detected Issues"
- Do NOT invent new vulnerabilities
- Respect severity exactly (High, Medium, Low, Informational)
- Use "Similar Real-World Cases" to support reasoning
- Do NOT exaggerate or misclassify severity

Contract:
{contract_code[:1500]}

Detected Issues:
{vulnerabilities}

Similar Patterns in Solidity:
{rag_context}

TASK:
For each detected issue:
1. Explain the vulnerability clearly
2. Describe how it can be exploited (accurately)
3. Reference similar real-world patterns if relevant
4. Suggest a precise fix

Be concise, technical, and accurate.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']