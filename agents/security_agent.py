from utils.llm import llm
import json
import re

def security_agent(state):

    lines = state["parsed_lines"]

    prompt = f"""
You are a security expert reviewing code.

You will be given code lines with file name and line number.

Your task:
- Detect security vulnerabilities
- Ignore safe lines

Return ONLY a valid JSON array. No markdown, no explanation.

Each object must contain:
- file
- line
- code
- issue
- fix (short and actionable)
- type ("security")
- severity ("low", "medium", "high")

Input:
{lines}

Example Output:
[
  {{
    "file": "app.py",
    "line": 30,
    "code": "query = f'SELECT * FROM users WHERE id=user_ID'",
    "issue": "SQL injection vulnerability",
    "fix": "Use parameterized queries",
    "type": "security",
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