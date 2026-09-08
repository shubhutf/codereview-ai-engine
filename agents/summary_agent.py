from utils.llm import llm

def summary_agent(state):

    issues = state.get("issues", [])[:100]
    risk_score = state.get("risk_score", 0)
    risk_summary = state.get("risk_summary", "")

    prompt = f"""
You are a senior code reviewer.

Generate a concise and professional summary of this pull request review.

You are given:
- A list of issues (with type and severity)
- A risk score
- A risk summary

Issues:
{issues}

Risk Score:
{risk_score}

Risk Summary:
{risk_summary}

Instructions:
- Highlight critical (high severity) issues first
- Mention security issues explicitly if present
- Comment on performance if relevant
- Clearly mention overall risk level
- Keep it concise and actionable
- Do NOT include fixes
"""

    result = llm.invoke(prompt)

    return {
        "final_summary": result.content.strip()
    }