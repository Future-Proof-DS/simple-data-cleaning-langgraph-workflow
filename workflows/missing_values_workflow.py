from typing_extensions import TypedDict
import pandas as pd
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# ---------------------------
# 1. Shared State Definition
# ---------------------------

class DataState(TypedDict):
    csv_path: str
    df: pd.DataFrame
    has_missing: bool
    summary: str


# ---------------------------
# 2. Initialize LLM (for reasoning)
# ---------------------------

llm = ChatOpenAI(model="gpt-4o-mini")


# ---------------------------
# 3. Nodes
# ---------------------------

def load_data(state: DataState) -> DataState:
    """Load CSV into a DataFrame."""
    df = pd.read_csv(state["csv_path"])
    state["df"] = df
    return state


def inspect_data(state: DataState) -> DataState:
    """Inspect data to check for missing values."""
    df = state["df"]
    state["has_missing"] = df.isna().any().any()
    
    if state["has_missing"]:
        missing_count = df.isna().sum().sum()
        print(f"⚠️  Found {missing_count} missing value(s) - routing to cleaning step")
    else:
        print("✓ No missing values detected - skipping cleaning step")
    
    return state


def handle_missing_values(state: DataState) -> DataState:
    """Simple cleaning step: fill missing numeric values with mean."""
    print("🧹 Cleaning data: filling missing numeric values with column means...")
    df = state["df"].copy()
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].mean())
    state["df"] = df
    print("✓ Data cleaning completed")
    return state


def describe_data(state: DataState) -> DataState:
    """Summarize numeric columns."""
    summary = state["df"].describe().to_string()
    state["summary"] = summary
    return state


def output_results(state: DataState):
    """Print summary result."""
    print("\nData Summary:\n", state["summary"])


# ---------------------------
# 4. Conditional Router
# ---------------------------

def route_missing(state: DataState) -> str:
    """Route depending on whether data has missing values."""
    return "Handle" if state["has_missing"] else "Skip"


# ---------------------------
# 5. Build the Graph
# ---------------------------

workflow = StateGraph(DataState)

# Add nodes
workflow.add_node("load_data", load_data)
workflow.add_node("inspect_data", inspect_data)
workflow.add_node("handle_missing_values", handle_missing_values)
workflow.add_node("describe_data", describe_data)
workflow.add_node("output_results", output_results)

# Add edges
workflow.add_edge(START, "load_data")
workflow.add_edge("load_data", "inspect_data")
workflow.add_conditional_edges(
    "inspect_data",
    route_missing,
    {
        "Handle": "handle_missing_values",
        "Skip": "describe_data"
    }
)
workflow.add_edge("handle_missing_values", "describe_data")
workflow.add_edge("describe_data", "output_results")
workflow.add_edge("output_results", END)

# Compile
graph = workflow.compile()

# ---------------------------
# 6. Visualize the Graph
# ---------------------------

def visualize_graph():
    """Save the workflow graph as a PNG image."""
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        output_path = PROJECT_ROOT / "outputs" / "missing_values_workflow.png"
        with open(output_path, "wb") as f:
            f.write(png_data)
        print("✓ Workflow graph saved to outputs/missing_values_workflow.png")
    except Exception as e:
        print(f"Could not generate graph visualization: {e}")


# ---------------------------
# 7. Run Example
# ---------------------------

if __name__ == "__main__":
    # Visualize the workflow structure
    visualize_graph()
    
    # Run the workflow
    print("Running workflow...\n")
    csv_path = str(PROJECT_ROOT / "data" / "example.csv")
    init_state: DataState = {"csv_path": csv_path, "df": None,
                             "has_missing": False, "summary": ""}
    graph.invoke(init_state)
