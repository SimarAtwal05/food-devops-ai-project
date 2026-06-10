from langgraph.graph import (
    StateGraph,
    START,
    END
)

from maintenance.state import MaintenanceState

from agents.log_analyzer import (
    log_analyzer
)

from agents.root_cause import (
    root_cause_agent
)

from agents.fix_generator import (
    fix_generator
)

from agents.human_review import (
    human_review
)

def review_router(state):

    if state["approved"]:
        return "approved"

    return "rejected"


def build_graph():

    graph = StateGraph(
        MaintenanceState
    )

    graph.add_node(
        "analyze",
        log_analyzer
    )

    graph.add_node(
        "root_cause",
        root_cause_agent
    )

    graph.add_node(
        "fix",
        fix_generator
    )

    graph.add_node(
        "review",
        human_review
    )

    graph.add_edge(
        START,
        "analyze"
    )

    graph.add_edge(
        "analyze",
        "root_cause"
    )

    graph.add_edge(
        "root_cause",
        "fix"
    )

    graph.add_edge(
        "fix",
        "review"
    )

    graph.add_conditional_edges(
        "review",
        review_router,
        {
            "approved": END,
            "rejected": END,
        }
    )

    return graph.compile()