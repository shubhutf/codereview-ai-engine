from utils.llm import llm

def risk_agent(state):

    issues = state.get("issues", [])

    issues_sample = issues[:100]

    prompt = f"""
You are a senior code reviewer.

You are given a list of detected issues in a pull request.

Each issue contains:
- type (bug/security/performance)
- severity (low/medium/high)
- code context

Your task:
- Assign a risk score (0–100)
- Provide a short summary

Guidelines:
- Security + high severity → increase risk significantly
- Many issues → increase risk
- Minor issues → lower risk

Issues:
{issues_sample}

Output STRICTLY in this format:

Risk Score: <number>
Summary: <short explanation>
"""

    result = llm.invoke(prompt)
    content = result.content.strip()

    try:
        score_line = [line for line in content.split("\n") if "Risk Score" in line][0]
        summary_line = [line for line in content.split("\n") if "Summary" in line][0]

        score = int(score_line.split(":")[1].strip())
        summary = summary_line.split(":", 1)[1].strip()

    except:
        score = 50
        summary = "Unable to parse risk properly."

    return {
        "risk_score": score,
        "risk_summary": summary
    }