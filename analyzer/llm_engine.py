import ollama

def generate_explanation(contract_code, vulnerabilities, rag_context):
    prompt = f"""
You are a smart contract security auditor.

Analyze the Solidity contract and explain vulnerabilities clearly.

Contract:
{contract_code}

Detected Issues:
{vulnerabilities}

Similar Known Patterns:
{rag_context}

Tasks:
1. Explain each vulnerability in simple terms
2. Explain how it can be exploited
3. Suggest a fix

Keep it concise and structured.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']