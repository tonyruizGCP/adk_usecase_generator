# Agentic Demo Generation Engine

A multi-agent application powered by Google Agent Development Kit (ADK) and Gemini, designed to automatically generate customized demo assets for customer engagements.

## 🚀 Overview

The **Agentic Demo Generation Engine** uses a team of specialized AI agents to analyze a customer's business, create a tailored narrative, and package a deployable HTML demo. It streamlines the creation of personalized sales assets by automating the research and content generation phases.

## 🤖 Agents & Architecture

The system is orchestrated by a **Coordinator Agent** which manages a workflow across three specialized sub-agents:

1.  **Research Agent** (`ResearchAgent`)
    *   **Role**: Conducts market research on the customer and industry.
    *   **Tools**: `web_research_tool` (Simulates web search to find challenges and trends).
    *   **Model**: `gemini-1.5-flash-latest` (Optimized for speed/tasks).

2.  **Narrative Agent** (`NarrativeAgent`)
    *   **Role**: Creative storyteller. Takes research + use case to write a demo script and generate mock data.
    *   **Output**: HTML script and JSON mock data.
    *   **Model**: `gemini-1.5-pro-latest` (Optimized for creative generation).

3.  **Packaging Agent** (`PackagingAgent`)
    *   **Role**: Asset finalizer. Prepares the final artifacts for download/viewing.
    *   **Tools**: `demo_packaging_tool`.
    *   **Model**: `gemini-1.5-flash-latest`.

## 📂 Project Structure

```
hackathon_adk_gen/
├── adk-demo-engine/
│   ├── agents.py         # Definitions of LlmAgents (Coordinator, Researcher, etc.)
│   ├── tools.py          # Custom ADK tools (web_research_tool, demo_packaging_tool)
│   ├── requirements.txt  # Python dependencies
│   ├── templates/        # HTML templates for the Web UI (index.html, demo_template.html)
│   └── static/           # CSS and static assets
└── README.md
```

## 🛠️ Setup & Installation

### Prerequisites
*   Python 3.8+
*   A Google Cloud Project with Vertex AI API enabled.
*   `GOOGLE_API_KEY` environment variable set.

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

## 🖥️ Usage

1.  **Run the Application**:
    (Ensure you have the main application entry point, e.g., `app.py`, configured to serve the Flask app)
    ```bash
    python adk-demo-engine/app.py
    ```

2.  **Access the Web UI**:
    Open your browser to `http://localhost:5000`.

3.  **Generate a Demo**:
    *   Enter **Customer Name** (e.g., "Acme Corp").
    *   Enter **Industry** (e.g., "Retail").
    *   Enter **Use Case** (e.g., "Predictive Analytics for Inventory").
    *   Click **Generate Demo Assets**.

The system will orchestrate the agents to research the customer, write a script, and provide a link to the generated demo artifacts.

## 🧩 Modifying Agents

*   To change agent instructions or models, edit `adk-demo-engine/agents.py`.
*   To add new capabilities, define new tools in `adk-demo-engine/tools.py` and register them with the appropriate agent.
