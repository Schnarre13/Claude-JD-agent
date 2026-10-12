from langgraph.graph import StateGraph
from state.fit_score_state import FitScoreState
from nodes.fit_scoring import fit_scoring_node
from nodes.placeholders import claude_tailoring, storage_agent

def should_proceed(state: FitScoreState) -> str:
    """
    Routing logic for LangGraph.
    """
    if state.compensation_fit == "Below threshold":
        return "skip"

    if state.fit_score is not None and state.fit_score >= 0.60:
        return "proceed"

    return "skip"

workflow = StateGraph(FitScoreState)

workflow.add_node("fit_scoring", fit_scoring_node)
workflow.add_node("claude_tailoring", claude_tailoring)
workflow.add_node("storage_agent", storage_agent)


workflow.add_conditional_edges(
    "fit_scoring",
    should_proceed,
    {
        "proceed": "claude_tailoring",   # placeholder for next node
        "skip": "storage_agent"          # placeholder for skip node
    }
)

workflow.set_entry_point("fit_scoring")

graph = workflow.compile()
