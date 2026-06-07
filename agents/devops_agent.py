from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from pathlib import Path


class DevOpsAgentState(TypedDict):
    files: dict
    code_review: list
    test_suggestions: list
    final_report: str


PROJECT_FILES = [
    "app/main.py",
    "app/crud.py",
    "app/models.py",
    "app/schemas.py",
    "tests/test_items.py",
    "Dockerfile",
    ".github/workflows/ci.yml",
]


def read_project_files(state: DevOpsAgentState):
    files = {}

    for file_path in PROJECT_FILES:
        path = Path(file_path)
        if path.exists():
            files[file_path] = path.read_text(encoding="utf-8")
        else:
            files[file_path] = "FILE NOT FOUND"

    return {"files": files}


def code_reviewer(state: DevOpsAgentState):
    suggestions = []

    main_code = state["files"].get("app/main.py", "")
    schemas_code = state["files"].get("app/schemas.py", "")
    dockerfile = state["files"].get("Dockerfile", "")

    if "HTTPException" in main_code:
        suggestions.append("Good: API handles missing food items using HTTPException.")

    if "price: float" in schemas_code:
        suggestions.append("Improve: Add validation to ensure price is greater than 0.")

    if "EXPOSE 8000" in dockerfile:
        suggestions.append("Good: Dockerfile exposes the FastAPI port correctly.")

    if "CMD" in dockerfile:
        suggestions.append("Good: Dockerfile has a startup command for Uvicorn.")

    return {"code_review": suggestions}


def test_suggestion_agent(state: DevOpsAgentState):
    suggestions = []

    test_code = state["files"].get("tests/test_items.py", "")

    if "test_create_food_item" in test_code:
        suggestions.append("Good: Create food item endpoint is tested.")

    if "test_view_menu" in test_code:
        suggestions.append("Good: View menu endpoint is tested.")

    if "test_delete_food_item" not in test_code:
        suggestions.append("Add: Test case for deleting a food item.")

    if "test_edit_food_item" not in test_code:
        suggestions.append("Add: Test case for editing a food item.")

    return {"test_suggestions": suggestions}


def report_generator(state: DevOpsAgentState):
    report = "# AI DevOps Agent Review Report\n\n"

    report += "## Code Review\n"
    for item in state["code_review"]:
        report += f"- {item}\n"

    report += "\n## Test Suggestions\n"
    for item in state["test_suggestions"]:
        report += f"- {item}\n"

    report += "\n## Summary\n"
    report += "The LangGraph workflow successfully reviewed the FastAPI CRUD app, Dockerfile, and test suite.\n"

    output_path = Path("agents/reports/dev_review.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    return {"final_report": report}


def build_graph():
    graph = StateGraph(DevOpsAgentState)

    graph.add_node("read_project_files", read_project_files)
    graph.add_node("code_reviewer", code_reviewer)
    graph.add_node("test_suggestion_agent", test_suggestion_agent)
    graph.add_node("report_generator", report_generator)

    graph.add_edge(START, "read_project_files")
    graph.add_edge("read_project_files", "code_reviewer")
    graph.add_edge("code_reviewer", "test_suggestion_agent")
    graph.add_edge("test_suggestion_agent", "report_generator")
    graph.add_edge("report_generator", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    result = app.invoke({
        "files": {},
        "code_review": [],
        "test_suggestions": [],
        "final_report": ""
    })

    print(result["final_report"])