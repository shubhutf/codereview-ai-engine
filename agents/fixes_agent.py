from utils.llm import llm
import json
import re

def fixes_agent(state):

    issues = state.get("issues", [])

    if not issues:
        return {"issues": []}

    prompt = f"""
You are an expert software engineer.

You will be given a list of code issues.

Each issue already contains:
- file
- line
- code
- issue
- type
- severity

Your task:
- Add a "fix" field for EACH issue
- Keep fixes short, actionable, and code-focused
- Maintain exact same structure

Return ONLY valid JSON array.

Input:
{issues}

Output format:
[
  {{
    "file": "...",
    "line": 12,
    "code": "...",
    "issue": "...",
    "fix": "...",
    "type": "...",
    "severity": "..."
  }}
]
"""

    result = llm.invoke(prompt)
    content = result.content.strip()
    content = re.sub(r"```json|```", "", content).strip()

    try:
        updated_issues = json.loads(content)
    except:
        updated_issues = issues 

    return {
        "issues": updated_issues
    }