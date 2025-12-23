import json
from tools import demo_packaging_tool

narrative = "The customer Acme Corp needs to predict inventory levels."
mock_data = json.dumps({"inventory": [{"item": "widget", "quantity": 100}]})
customer_name = "Acme Corp"

result = demo_packaging_tool(narrative, mock_data, customer_name)
print(result)

parsed = json.loads(result)
files = parsed.get("files", [])
print(f"\nFound {len(files)} files.")
for f in files:
    print(f"- {f['name']}")

# Check if agent.py is present and has expected content
agent_file = next((f for f in files if f['name'] == 'my_agent/agent.py'), None)
if agent_file:
    print("\nVerified my_agent/agent.py exists.")
    if "class DemoAgent" or "name=\"DemoAgent\"" in agent_file['content']:
        print("Verified agent definition in agent.py")
else:
    print("\nFAILED: my_agent/agent.py not found.")
