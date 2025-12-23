# Agentic Demo Generation Engine

A multi-agent application powered by Google Agent Development Kit (ADK) and Gemini, designed to automatically generate customized demo assets for customer engagements.

## 🚀 Overview

The **Agentic Demo Generation Engine** uses a team of specialized AI agents to analyze a customer's business, create a tailored narrative, and package a deployable HTML demo. It streamlines the creation of personalized sales assets by automating the research and content generation phases.

## 🤖 Agents & Architecture

The system is orchestrated by a **Coordinator Agent** which manages a workflow across three specialized sub-agents:

1.  **Research Agent** (`ResearchAgent`)
    *   **Role**: Conducts market research on the customer and industry.
    *   **Tools**: `web_research_tool` (Simulates web search to find challenges and trends).
    *   **Model**: `gemini-3-flash-preview` (Optimized for speed/tasks).

2.  **Narrative Agent** (`NarrativeAgent`)
    *   **Role**: Creative storyteller. Takes research + use case to write a demo script and generate mock data.
    *   **Output**: HTML script and JSON mock data.
    *   **Model**: `gemini-3-flash-preview` (Optimized for creative generation).

3.  **Packaging Agent** (`PackagingAgent`)
    *   **Role**: Asset finalizer. Prepares the final artifacts for download/viewing.
    *   **Tools**: `demo_packaging_tool`.
    *   **Model**: `gemini-3-flash-preview`.

## 📂 Project Structure

```
hackathon_adk_gen/
└── adk-demo-engine/
    ├── main.py              # Flask web server and ADK execution logic
    ├── agents.py            # Definitions of LlmAgents (Coordinator, Researcher, etc.)
    ├── tools.py             # Custom ADK tools (web_research_tool, demo_packaging_tool)
    ├── requirements.txt     # Python dependencies
    ├── tests/               # Unit and integration tests
    │   ├── test_tools.py    # Tests for custom tools
    │   └── test_app.py      # Tests for Flask app (mocks ADK)
    ├── eval_sets/           # ADK evaluation sets
    │   ├── researcher_eval.json      # Eval set for ResearchAgent
    │   └── coordinator_e2e_eval.json # E2E eval set for Coordinator
    ├── templates/           # HTML templates for the Web UI
    ├── static/              # CSS and static assets
    └── generated_demos/     # Directory where final HTML demos are stored
```

## 🛠️ Setup & Installation

### Prerequisites
*   Python 3.8+
*   A Google Cloud Project with Vertex AI API enabled.
*   `GOOGLE_API_KEY` environment variable set.
*   `pip` installed.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd hackathon_adk_gen
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r adk-demo-engine/requirements.txt
    ```

3.  **Set your API Key**:
    ```bash
    export GOOGLE_API_KEY="your_actual_api_key_here"
    ```

## 🧪 Testing & Evaluation

This project includes a comprehensive testing strategy covering unit tests, integration tests, and agent evaluations.

All commands should be run from inside the `adk-demo-engine` directory.

```bash
cd adk-demo-engine
```

### 1. Component Testing (Unit Tests)
Validates the logic of individual tools.
```bash
PYTHONPATH=. pytest tests/test_tools.py
```

### 2. Application Testing (Integration Tests)
Validates the Flask web application logic, mocking the ADK agent calls to ensure fast and reliable testing of the web layer.
```bash
PYTHONPATH=. pytest tests/test_app.py
```

### 3. Agent Evaluation (ADK Evals)
Uses the `adk eval` command to test the behavior of the agents against defined golden datasets.

**Evaluate the Research Agent:**
```bash
adk eval agents.researcher eval_sets/researcher_eval.json
```

**Evaluate the Full E2E Workflow (Coordinator):**
```bash
adk eval agents.coordinator eval_sets/coordinator_e2e_eval.json
```

## 🖥️ Usage

1.  **Run the Application**:
    ```bash
    python adk-demo-engine/main.py
    ```
    *Note: If you are already inside `adk-demo-engine`, run `python main.py`.*

2.  **Access the Web UI**:
    Open your browser to `http://localhost:5000`.

3.  **Generate a Demo**:
    *   Enter **Customer Name** (e.g., "Acme Corp").
    *   Enter **Industry** (e.g., "Retail").
    *   Enter **Use Case** (e.g., "Predictive Analytics for Inventory").
    *   Click **Generate Demo Assets**.

The system will orchestrate the agents to research the customer, write a script, and provide a link to the generated demo artifacts.
