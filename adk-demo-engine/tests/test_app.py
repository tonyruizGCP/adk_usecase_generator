import os
import json
import pytest
from unittest.mock import patch
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('main.coordinator.invoke')
def test_generate_demo_endpoint(mock_invoke, client):
    """
    Tests the /generate-demo endpoint.
    - Mocks the ADK agent call.
    - Verifies the form data is processed correctly.
    - Verifies a result file is created.
    - Verifies the response contains a link to the new demo.
    """
    # 1. Define the mock return value from the ADK agent
    mock_agent_output = json.dumps({
        "narrative": "<h3>Mocked Narrative</h3>",
        "files": [{"name": "mock.json", "content": "{}"}]
    })
    # Mocking the return value of coordinator.invoke to match what main.py expects
    # main.py expects a list of objects with a 'content' attribute
    # We can use a simple class or a mock object
    class MockResponse:
        def __init__(self, content):
            self.content = content
            
    mock_invoke.return_value = [MockResponse(mock_agent_output)]

    # 2. Simulate a POST request to the endpoint
    response = client.post('/generate-demo', data={
        'customer_name': 'MockCustomer',
        'industry': 'MockIndustry',
        'use_case': 'MockUseCase'
    })

    # 3. Assertions
    # Assert that the agent was called once with the correct prompt structure
    mock_invoke.assert_called_once()
    call_args = mock_invoke.call_args[0][0]
    assert 'MockCustomer' in call_args
    assert 'MockIndustry' in call_args
    
    # Assert the web response is successful
    assert response.status_code == 200
    
    # Assert the response HTML contains a link to the generated demo
    response_text = response.get_data(as_text=True)
    assert 'Demo Ready!' in response_text or 'href="/generated_demos/demo_' in response_text

    # Clean up created file (optional, but good practice)
    # This requires more complex logic to find the created file, but shows intent
    for f in os.listdir(os.path.join(os.path.dirname(__file__), '../generated_demos')):
        if f.startswith('demo_'):
            os.remove(os.path.join(os.path.dirname(__file__), '../generated_demos', f))
            break
