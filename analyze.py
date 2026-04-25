import sys
from analyzer.scv_loader import load_scv_dataset
from analyzer.slither_runner import run_slither
from analyzer.parser import extract_vulnerabilities
from analyzer.rag_engine import process_contract
from analyzer.llm_engine import generate_explanation
from analyzer.loader import load_contract
from analyzer.filter_engine import filter_rag_results  # ✅ 2.1 Import added


# -----------------------------
# SCORING ENGINE
# -----------------------------
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


# -----------------------------
# OUTPUT HELPERS
# -----------------------------
def print_vulnerabilities(issues):
    print("\n===== VULNERABILITIES =====")

    if not issues:
        print("No vulnerabilities found\n")
        return

    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue.get('check', 'Unknown')} ({issue.get('impact', 'Unknown')})")
        print(f"   {issue.get('description', '')[:200]}...\n")


def print_security_score(score):
    print("\n===== SECURITY REPORT =====")
    print(f"Score: {score}/100\n")


def build_vuln_summary(issues):
    summary = ""

    for i, issue in enumerate(issues, 1):
        summary += f"""
Issue {i}:
- Type: {issue.get('check', '')}
- Severity: {issue.get('impact', '')}
- Description: {issue.get('description', '')[:200]}
"""

    return summary


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <contract.sol>")
        return

    file_path = sys.argv[1]

    # Load contract
    print("\n[+] Loading contract...")
    code = load_contract(file_path)

    # Run Slither
    print("[+] Running slither analysis...")
    result = run_slither(file_path)

    # Extract vulnerabilities
    print("[+] Extracting vulnerabilities...")
    issues = extract_vulnerabilities(result)

    #   Extract Slither issue types
    slither_issues = [issue["check"].lower() for issue in issues]
    print("\n[DEBUG] Slither Issues:", slither_issues)

    print_vulnerabilities(issues)

    # Score calculation
    score = calculate_score(issues)
    print_security_score(score)

    # Load dataset
    print("[+] Loading vulnerability dataset...")
    try:
        load_scv_dataset()
    except Exception:
        pass

    # RAG analysis
    print("[+] Running RAG analysis...")
    rag_results = process_contract(file_path)

    # ✅ 2.3 Apply filter
    filtered_results = filter_rag_results(rag_results, slither_issues)

    # -----------------------------
    # ✅ STEP 3 — FILTERED RAG OUTPUT (REPLACED)
    # -----------------------------
    rag_summary = ""

    print("\n===== FILTERED RAG MATCHES =====")

    for idx, item in enumerate(filtered_results):
        func = item["function"]
        matches = item["matches"]

        print(f"\nFunction {idx+1}:")
        print(func[:100], "...")

        if not matches:
            print("  No relevant matches")
            continue

        for match in matches:
            meta = match["metadata"]
            distance = match["distance"]

            print(f"  → {meta['vulnerability']} ({distance:.3f})")

            rag_summary += f"""
Function:
{func[:100]}

- Vulnerability: {meta['vulnerability']}
- Severity: {meta['severity']}
- Description: {meta['description']}
"""

    # Build summaries
    vuln_summary = build_vuln_summary(issues)

    # LLM Explanation
    print("\n[+] Generating AI Explanation...\n")

    llm_output = generate_explanation(
        contract_code=code,
        vulnerabilities=vuln_summary,
        rag_context=rag_summary
    )

    print("\n===== AI SECURITY ANALYSIS =====\n")
    print(llm_output)


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()