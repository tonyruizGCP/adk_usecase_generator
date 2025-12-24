import json
from google.adk.tools import FunctionTool as tool

@tool
def web_research_tool(customer_name: str, industry: str) -> str:
    """
    Performs web research on a given customer and industry to find key
    challenges, priorities, and recent news.
    For this demo, this tool returns a simulated search result.
    """
    print(f"TOOL: Executing web_research_tool for {customer_name}")
    # In a real application, this would use an actual search API.
    simulated_findings = f"""
    Research Summary for {customer_name} ({industry}):
    - Key Industry Challenge: Reducing operational overhead in supply chain logistics.
    - {customer_name}'s Stated Priority: A recent press release highlights a new corporate initiative focused on 'digitizing the customer journey'.
    - Market Trend: There is a growing demand in the {industry} sector for AI-driven predictive analytics to forecast inventory needs.
    """
    return simulated_findings.strip()

@tool
def demo_packaging_tool(narrative_context: str, mock_data_json_string: str, customer_name: str) -> str:
    """
    Takes a generated narrative context and a JSON string of mock data,
    and creates the final demo agent artifacts.
    Returns a JSON string containing the file structure for the new agent.
    """
    print(f"TOOL: Executing demo_packaging_tool for {customer_name}")
    
    # Validate and re-format JSON to ensure it's valid
    try:
        mock_data = json.loads(mock_data_json_string)
        formatted_mock_data = json.dumps(mock_data, indent=4)
    except json.JSONDecodeError:
        # Fallback if raw string/invalid json
        formatted_mock_data = mock_data_json_string

    # Clean up narrative context (escape quotes for python string)
    safe_narrative = narrative_context.replace('"""', "'''").replace('"', '\\"')
    
    # Template for the generated agent.py
    agent_code = f'''
import json
import os
from google.adk.agents import LlmAgent
from google.adk.tools import tool

# Load Mock Data
# We expect mock_data.json to be in the same directory
current_dir = os.path.dirname(os.path.abspath(__file__))
mock_data_path = os.path.join(current_dir, 'mock_data.json')

try:
    with open(mock_data_path, 'r') as f:
        MOCK_DATA = json.load(f)
except FileNotFoundError:
    print(f"Warning: {{mock_data_path}} not found. Using empty data.")
    MOCK_DATA = {{}}

@tool
def get_customer_data() -> str:
    """Returns the mock data for the customer."""
    return json.dumps(MOCK_DATA)

@tool
def get_demo_context() -> str:
    """Returns the narrative context for the demo."""
    return """{safe_narrative}"""

# Define the Agent
agent = LlmAgent(
    name="DemoAgent",
    model="gemini-2.0-flash-exp",
    instruction="""You are a demo agent for {customer_name}. 
    You have access to specific customer data and narrative context via your tools.
    ALWAYS use `get_demo_context` first to understand the scenario.
    Then use `get_customer_data` to answer specific questions about the customer's challenges and solutions.
    """,
    tools=[get_customer_data, get_demo_context]
)
'''

    readme_content = f"""# {customer_name} Demo Agent

This is a generated ADK agent for the {customer_name} demo.

## Prerequisites

- Python 3.10+
- `google-adk` package installed
- `GOOGLE_API_KEY` set in your environment

## Setup

1.  Install dependencies:
    ```bash
    pip install google-adk
    ```

2.  Set your API key:
    ```bash
    export GOOGLE_API_KEY=your_api_key_here
    ```

## Running the Agent

You can run this agent using the ADK CLI or by running the python file directly if you add a runner block.

### Using ADK CLI (Recommended)

Navigate to the parent directory of `my_agent` and run:

```bash
adk run my_agent.agent:agent
```

### Exploring the Demo

The agent defines the following tools:
- `get_customer_data()`: Returns the simulated data for the customer.
- `get_demo_context()`: Returns the narrative backstory for this demo.

Ask questions like:
- "What is the situation at {customer_name}?"
- "What problems are they facing?"
- "Show me the data."
"""

    final_artifacts = {
        "files": [
            {"name": "my_agent/agent.py", "content": agent_code},
            {"name": "my_agent/__init__.py", "content": ""},
            {"name": "my_agent/.env", "content": "GOOGLE_API_KEY=\n"},
            {"name": "my_agent/mock_data.json", "content": formatted_mock_data},
            {"name": "my_agent/README.md", "content": readme_content}
        ]
    }
    return json.dumps(final_artifacts, indent=2)
