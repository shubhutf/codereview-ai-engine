from utils.llm import llm
import json
import re

def bug_agent(state):

    lines = state["parsed_lines"]

    prompt = f"""
You are a code reviewer.

You will be given code lines with file name and line number.

Your task:
- Detect bugs
- Ignore lines without issues

Return ONLY a valid JSON array. No markdown, no explanation.

Each object must contain:
- file
- line
- code
- issue
- fix
- type ("bug")
- severity ("low", "medium", "high")

Input:
{lines}

Example Output:
[
  {{
    "file": "app.js",
    "line": 12,
    "code": "const x = y + 1;",
    "issue": "y is undefined",
    "fix": "Define y before using it",
    "type": "bug",
    "severity": "high"
  }}
]
"""

    result = llm.invoke(prompt)
    content = result.content.strip()
    content = re.sub(r"```json|```", "", content).strip()

    try:
        issues = json.loads(content)
    except:
        issues = []

    return {
        "issues": issues 
    }