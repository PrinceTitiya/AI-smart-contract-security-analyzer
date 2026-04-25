def match_issue_to_category(issue, category):
    issue = issue.lower()
    category = category.lower()
    return issue in category or category in issue

def filter_rag_results(rag_results, slither_issues):
    filtered_results = []

    for item in rag_results:
        func = item["function"]
        results = item["results"]

        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        best_matches = {}

        for i in range(len(metas)):
            vuln = metas[i]["vulnerability"]
            distance=distances[i]

            # Distance filter(remove weak matches)
            if distance > 0.4:
                continue

            # match with slither issues
            if not any(match_issue_to_category(issue,vuln) for issue in slither_issues):
                continue

            # Deduplication(keep best match only)
            key = vuln.lower()
            if key not in best_matches or distance<best_matches[key]["distance"]:
                best_matches[key] = {
                    "metadata": metas[i],
                    "distance": distance
                }

        filtered_results.append({
            "function":func,
            "matches":list(best_matches.values())
        })

    return filtered_results
        
        