import sys
from analyzer.loader import load_contract
from analyzer.slither_runner import run_slither
from analyzer.parser import extract_vulnerabilities
from analyzer.rag_engine import process_contract
from analyzer.data_loader import load_dataset
from analyzer.llm_engine import generate_explanation

def calculate_score(issues):

    impact_weights = {
        "High": 25,
        "Medium": 15,
        "Low": 10,
        "Informational": 5
    }

    score = 100

    for issue in issues:
        impact = issue.get("impact", "Low")
        score -= impact_weights.get(impact, 10)

    return max(score, 0)


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <contract.sol>")
        return

    file_path = sys.argv[1]

    print('\n[+] Loading contract...')
    code = load_contract(file_path)

    print("[+] Running slither analysis...")
    result = run_slither(file_path)

    print("[+] Extracting vulnerabilities...")
    issues = extract_vulnerabilities(result)

    if not issues:
        print("No vulnerabilities found")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue['check']} ({issue['impact']})")
            print(f"   {issue['description']}....\n")

    score = calculate_score(issues)

    print("\n===== SECURITY REPORT =====")
    print(f"Score: {score}/100\n")

    print("[+] Loading vulnerability dataset...")
    try:
        load_dataset()
    except:
        pass

    print("[+] Running RAG analysis...")
    rag_results = process_contract(code)

    # ✅ Improved vuln_summary (with description)
    vuln_summary = "\n".join(
        [
            f"{i+1}. {issue['check']} ({issue['impact']}) - {issue['description'][:120]}"
            for i, issue in enumerate(issues)
        ]
    )

    rag_summary = ""
    docs = rag_results.get("documents", [[]])[0]
    metas = rag_results.get("metadatas", [[]])[0]

    for i in range(len(metas)):
        rag_summary += f"""
Match {i+1}:
Vulnerability: {metas[i].get('vulnerability')}
Explanation: {metas[i].get('description')}
"""

    print("\n[+] Generating AI Explanation...\n")

    llm_output = generate_explanation(
        contract_code=code,
        vulnerabilities=vuln_summary,
        rag_context=rag_summary
    )

    print("\n===== AI SECURITY ANALYSIS =====\n")
    print(llm_output)


if __name__ == "__main__":
    main()