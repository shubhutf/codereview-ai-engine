from typing import TypedDict, List, Any
from typing_extensions import Annotated

def merge_lists(a, b):
    return a + b

class Issue(TypedDict):
    file: str
    line: int
    code: str
    issue: str
    fix: str
    type: str
    severity: str

class PRState(TypedDict):
    patches: List[Any]
    parsed_lines: List[dict]

    issues: Annotated[List[Issue], merge_lists] 

    risk_score: int
    risk_summary: str
    final_summary: str