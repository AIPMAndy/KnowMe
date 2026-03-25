#!/usr/bin/env python3
"""
KnowMe Authorization Handler
Processes OAuth callbacks and triggers analysis on approval.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def on_authorization_approved(user_id: str, scope: str, token: str):
    """Called when user approves authorization."""
    
    print(f"Authorization approved for user {user_id}")
    print(f"Scope: {scope}")
    
    # 1. Re-run collection (now should succeed)
    collect_result = subprocess.run(
        [sys.executable, "auto_collect.py"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    if collect_result.returncode != 0:
        print("Failed to collect data after authorization")
        return {"status": "error", "message": "Collection failed"}
    
    result = json.loads(collect_result.stdout)
    
    if result["action"] != "collected":
        print(f"Unexpected result: {result}")
        return {"status": "error", "message": "Unexpected collection result"}
    
    data_path = result["output_path"]
    
    # 2. Run analysis
    report_path = "/tmp/knowme_report.md"
    analyze_result = subprocess.run(
        [sys.executable, "analyze.py", "--input", data_path, "--output", report_path],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    if analyze_result.returncode != 0:
        print("Analysis failed")
        return {"status": "error", "message": "Analysis failed"}
    
    # 3. Generate advice
    advice_path = "/tmp/knowme_advice.md"
    advise_result = subprocess.run(
        [sys.executable, "advise.py", "--report", report_path, "--output", advice_path],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    # 4. Generate portrait prompt
    portrait_path = "/tmp/knowme_portrait.txt"
    portrait_result = subprocess.run(
        [sys.executable, "generate_portrait.py", "--report", report_path, "--output", portrait_path],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    return {
        "status": "success",
        "report_path": report_path,
        "advice_path": advice_path,
        "portrait_path": portrait_path if portrait_result.returncode == 0 else None,
        "stats": result.get("stats", {})
    }

def main():
    """CLI entry point for OAuth callback."""
    if len(sys.argv) < 4:
        print("Usage: handle_auth.py <user_id> <scope> <token>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    scope = sys.argv[2]
    token = sys.argv[3]
    
    result = on_authorization_approved(user_id, scope, token)
    print(json.dumps(result))

if __name__ == "__main__":
    main()
