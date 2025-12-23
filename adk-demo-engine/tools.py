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
def demo_packaging_tool(narrative_html: str, mock_data_json_string: str, customer_name: str) -> str:
    """
    Takes a generated narrative and a JSON string of mock data,
    and creates the final demo artifacts.
    Returns a JSON string containing the final narrative and a list of mock data files.
    """
    print(f"TOOL: Executing demo_packaging_tool for {customer_name}")
    
    mock_data = json.loads(mock_data_json_string)
    
    # Generate a mock text report based on the JSON
    report_text = f"Analysis Report for: {customer_name}\n-------------------------------------\n"
    for item in mock_data.get("analysis_results", []):
        report_text += f"- {item['finding']}\n"

    final_artifacts = {
        "narrative": narrative_html,
        "files": [
            {"name": "simulated_api_response.json", "content": mock_data_json_string},
            {"name": "summary_report.txt", "content": report_text}
        ]
    }
    return json.dumps(final_artifacts, indent=2)
