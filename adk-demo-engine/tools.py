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
    
    mock_data = json.loads(mock_data_json_string)
    
    # Template for the generated agent.py
    agent_code = f'''
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool as tool
import json

# Mock Data
MOCK_DATA = {json.dumps(mock_data, indent=4)}

@tool
def get_customer_data() -> str:
    """Returns the mock data for the customer."""
    return json.dumps(MOCK_DATA)

@tool
def get_demo_context() -> str:
    """Returns the narrative context for the demo."""
    return """{narrative_context}"""

# Define the Agent
agent = LlmAgent(
    name="DemoAgent",
    model="gemini-3-flash-preview",
    instruction="""You are a demo agent for {customer_name}. 
    You have access to specific customer data and narrative context.
    Answer questions about the customer's challenges and solutions based ONLY on the provided tools.
    """,
    tools=[get_customer_data, get_demo_context]
)
'''

    final_artifacts = {
        "files": [
            {"name": "my_agent/agent.py", "content": agent_code},
            {"name": "my_agent/__init__.py", "content": ""},
            {"name": "my_agent/.env", "content": f"GOOGLE_API_KEY=\nPROJECT_ID=''\n"},
            {"name": "my_agent/mock_data.json", "content": mock_data_json_string}
        ]
    }
    return json.dumps(final_artifacts, indent=2)
