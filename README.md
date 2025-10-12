# LangGraph Workflow Example

A simple example demonstrating how to build workflows with LangGraph for data processing.

## What This Example Does

This workflow demonstrates:
- Loading CSV data
- Inspecting data for missing values
- Conditional routing based on data quality
- Cleaning data (filling missing values)
- Generating summaries

## Project Structure

```
.
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── data/
│   └── example.csv              # Sample data files
│
├── workflows/
│   └── missing_values_workflow.py   # Workflow implementation
│
└── outputs/
    └── .gitkeep                 # Generated files (graphs, reports)
```

**Folder Organization:**
- `data/` - Input data files (CSV, JSON, etc.)
- `workflows/` - LangGraph workflow scripts
- `outputs/` - Generated outputs (visualizations, reports)

## Setup

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Set up your OpenAI API key**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

## Running the Example

From the project root:
```bash
poetry run python workflows/missing_values_workflow.py
```

## How It Works

The workflow follows these steps:

1. **Load Data** - Reads the CSV file into a pandas DataFrame
2. **Inspect Data** - Checks for missing values
3. **Conditional Routing** - If missing values exist, routes to cleaning; otherwise skips to summary
4. **Handle Missing Values** - Fills numeric missing values with column means
5. **Describe Data** - Generates statistical summary
6. **Output Results** - Prints the summary

