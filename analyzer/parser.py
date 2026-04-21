def extract_vulnerabilities(slither_json):
    issues = []

    if not slither_json:
        return issues

    detectors = slither_json.get("results", {}).get("detectors", [])

    print(f"Found {len(detectors)} detectors")

    for d in detectors:
        print("DETECTOR:", d.get("check"))

        issues.append({
            "check": d.get("check", "unknown"),
            "impact": d.get("impact", "unknown"),
            "description": d.get("description", "no description")
        })

    print(f"DEBUG: Issues collected = {len(issues)}")

    return issues