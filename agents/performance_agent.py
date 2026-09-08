from utils.llm import llm
import json
import re

def performance_agent(state):

    lines = state["parsed_lines"]

    prompt = f"""
You are a performance optimization expert.

You will be given code lines with file name and line number.

Your task:
- Detect performance issues
- Ignore lines without issues

Return ONLY a valid JSON array. No markdown, no explanation.

Each object must contain:
- file
- line
- code
- issue
- fix (keep short)
- type ("performance")
- severity ("low", "medium", "high")

Input:
{lines}

Example Output:
[
  {{
    "file": "app.js",
    "line": 45,
    "code": "for (let i = 0; i < arr.length; i++)",
    "issue": "Inefficient loop, can be optimized",
    "fix": "Use map or cache length",
    "type": "performance",
    "severity": "medium"
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