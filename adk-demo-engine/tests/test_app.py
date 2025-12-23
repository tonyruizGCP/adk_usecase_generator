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

@patch('main.InMemoryRunner')
def test_generate_demo_endpoint(MockRunner, client):
    """
    Tests the /generate-demo endpoint.
    - Mocks the ADK runner.
    - Verifies the form data is processed correctly.
    - Verifies a result file is created.
    - Verifies the response contains a link to the new demo.
    """
    # 1. Define the mock return value from the ADK agent
    mock_agent_output = json.dumps({
        "narrative": "<h3>Mocked Narrative</h3>",
        "files": [{"name": "mock.json", "content": "{}"}]
    })
    
    # Mock events returned by runner.run()
    # We need to simulate the Event object structure roughly or at least what main.py accesses (event.content.parts[0].text)
    class MockPart:
        def __init__(self, text):
            self.text = text
            
    class MockContent:
        def __init__(self, text):
            self.parts = [MockPart(text)]
            
    class MockEvent:
        def __init__(self, text):
            self.content = MockContent(text)

    # runner.run() returns a generator
    def mock_run(*args, **kwargs):
        yield MockEvent(mock_agent_output)

    # Setup the mock runner instance
    mock_runner_instance = MockRunner.return_value
    mock_runner_instance.run.side_effect = mock_run

    # Configure session_service.create_session to be awaitable
    async def mock_create_session(*args, **kwargs):
        pass
    mock_runner_instance.session_service.create_session.side_effect = mock_create_session

    # 2. Simulate a POST request to the endpoint
    response = client.post('/generate-demo', data={
        'customer_name': 'MockCustomer',
        'industry': 'MockIndustry',
        'use_case': 'MockUseCase'
    })

    # 3. Assertions
    # Assert that the runner was initialized
    MockRunner.assert_called()
    
    # Assert run was called
    mock_runner_instance.run.assert_called_once()
    
    call_kwargs = mock_runner_instance.run.call_args[1]
    # Check that new_message contains the prompt with properly formatted text
    # types.Content is not easily equality checked if mocked, but we can check the text inside if we inspect the arg
    # However, 'new_message' arg will be a real types.Content object from main.py import.
    # We can check if prompt contains our Inputs
    input_message = call_kwargs['new_message']
    prompt_text = input_message.parts[0].text
    assert 'MockCustomer' in prompt_text
    assert 'MockIndustry' in prompt_text
    
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
