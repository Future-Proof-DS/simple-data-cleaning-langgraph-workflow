# LangGraph Workflow Example

A simple example demonstrating how to build workflows with LangGraph for data processing.

## What This Example Does

This workflow demonstrates:
- Loading CSV data
- Using LLM to analyze data quality and decide on actions
- Inspecting data for missing values and outliers
- Conditional routing based on LLM decision
- Cleaning data (filling missing values with mean)
- Removing outliers (using IQR method)
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
│   ├── missing.csv              # Data with only missing values
│   ├── outliers.csv             # Data with only outliers
│   └── missing_and_outliers.csv # Data with both issues
│
├── workflows/
│   └── simple_clean_data_workflow.py   # Main workflow implementation
│
└── outputs/
    └── .gitkeep                 # Generated files (graphs, reports)
```

**Folder Organization:**
- `data/` - Sample CSV files with different data quality issues
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
poetry run python workflows/simple_clean_data_workflow.py
```

The workflow will:
1. Save a workflow graph visualization to `outputs/workflow_graph.png`
2. Load data from `data/missing.csv` (you can change this in the script)
3. Use an LLM to analyze the data and decide which cleaning action to take
4. Execute the appropriate cleaning steps
5. Display the results

## How It Works

The workflow follows these steps:

1. **Load Data** - Reads the CSV file into a pandas DataFrame
2. **Summarize Data** - Generates comprehensive summary including:
   - Statistical description (`.describe()`)
   - Dataset info (`.info()`)
   - Explicit missing value counts
3. **LLM Reasoning** - Uses GPT-4o-mini to analyze the summary and decide which action to take
4. **Conditional Routing** - Routes to appropriate cleaning node based on LLM decision
5. **Data Cleaning** - Can execute:
   - **Handle Missing Values** - Fills numeric missing values with column means
   - **Remove Outliers** - Removes outliers using IQR (Interquartile Range) method
6. **Describe Data** - Generates statistical summary of cleaned data
7. **Output Results** - Prints the action taken and final summary

