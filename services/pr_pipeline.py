from graph.pr_graph import graph
from processing.patches import extract_cleaned_patches
from processing.processPatches import process_pr_files
import requests
import os


def pr_pipeline(git_url:str):
    parts = git_url.rstrip("/").split("/")
    owner = parts[3]
    repo = parts[4]
    pr_number = parts[6]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    headers = {}
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR data: {response.status_code} {response.text}")

    files = response.json()

    if not files:
        raise Exception("No files found in PR")

    processed_files = process_pr_files(files)

    if not processed_files:
        raise Exception("No parsed lines extracted from PR files")

    result = graph.invoke({
        "patches": files,
        "parsed_lines": processed_files,
        "issues": [],
        "risk_score": 0,
        "risk_summary": "",
        "final_summary": ""
    })

    report = {
        "issues": result.get("issues", []),
        "risk_score": result.get("risk_score", 0),
        "risk_summary": result.get("risk_summary", ""),
        "final_summary": result.get("final_summary", "")
    }

    return report