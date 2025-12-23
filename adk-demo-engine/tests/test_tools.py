import json
from tools import web_research_tool, demo_packaging_tool

def test_web_research_tool():
    """Tests that the research tool returns a non-empty string containing key info."""
    customer = "ACME Corp"
    industry = "Logistics"
    result = web_research_tool(customer_name=customer, industry=industry)
    assert isinstance(result, str)
    assert customer in result
    assert industry in result
    assert "Challenge" in result

def test_demo_packaging_tool():
    """Tests that the packaging tool correctly structures the final JSON output."""
    narrative = "<h3>Hello World</h3>"
    mock_data_str = '{"analysis_results": [{"finding": "Test finding"}]}'
    customer = "Test Customer"
    
    result_json_str = demo_packaging_tool(
        narrative_html=narrative,
        mock_data_json_string=mock_data_str,
        customer_name=customer
    )
    
    # Validate the output is a valid JSON string with the correct structure
    result_data = json.loads(result_json_str)
    assert "narrative" in result_data
    assert "files" in result_data
    assert result_data["narrative"] == narrative
    assert len(result_data["files"]) == 2
    assert result_data["files"][0]["name"] == "simulated_api_response.json"
    assert "Test finding" in result_data["files"][1]["content"]
