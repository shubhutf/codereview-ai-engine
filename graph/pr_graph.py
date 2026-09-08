from langgraph.graph import StateGraph, START, END
from state.pr_state import PRState

from agents.bug_agent import bug_agent
from agents.performance_agent import performance_agent
from agents.security_agent import security_agent
from agents.summary_agent import summary_agent
from agents.fixes_agent import fixes_agent
from agents.risk_agent import risk_agent


builder = StateGraph(PRState)

builder.add_node("bug_agent", bug_agent)
builder.add_node("security_agent", security_agent)
builder.add_node("performance_agent", performance_agent)

builder.add_node("fixes_agent", fixes_agent)
builder.add_node("risk_agent", risk_agent)
builder.add_node("summary_agent", summary_agent)

builder.add_edge(START, "bug_agent")
builder.add_edge(START, "security_agent")
builder.add_edge(START, "performance_agent")

builder.add_edge("bug_agent", "risk_agent")
builder.add_edge("security_agent", "risk_agent")
builder.add_edge("performance_agent", "risk_agent")

builder.add_edge("risk_agent", "summary_agent")
builder.add_edge("summary_agent", END)

graph = builder.compile()