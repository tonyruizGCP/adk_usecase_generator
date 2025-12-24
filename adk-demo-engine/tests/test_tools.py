import json
from tools import web_research_tool, demo_packaging_tool

def test_web_research_tool():
    """Tests that the research tool returns a non-empty string containing key info."""
    customer = "ACME Corp"
    industry = "Logistics"
    result = web_research_tool.func(customer_name=customer, industry=industry)
    assert isinstance(result, str)
    assert customer in result
    assert industry in result
    assert "Challenge" in result

def test_demo_packaging_tool():
    """Tests that the packaging tool correctly structures the final JSON output."""
    narrative = "<h3>Hello World</h3>"
    mock_data_str = '{"analysis_results": [{"finding": "Test finding"}]}'
    customer = "Test Customer"
    
    result_json_str = demo_packaging_tool.func(
        narrative_context=narrative,
        mock_data_json_string=mock_data_str,
        customer_name=customer
    )
    
    # Validate the output is a valid JSON string with the correct structure
    # Validate the output is a valid JSON string with the correct structure
    result_data = json.loads(result_json_str)
    assert "files" in result_data
    
    # Check that we have the expected files for an agent
    filenames = [f['name'] for f in result_data['files']]
    assert "my_agent/agent.py" in filenames
    assert "my_agent/mock_data.json" in filenames
    assert "my_agent/README.md" in filenames
    
    # Verify content of specific files
    for file_info in result_data['files']:
        if file_info['name'] == "my_agent/mock_data.json":
            content = json.loads(file_info['content'])
            assert "analysis_results" in content
        if file_info['name'] == "my_agent/agent.py":
            assert "LlmAgent" in file_info['content']
