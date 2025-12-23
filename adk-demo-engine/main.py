from flask import Flask, render_template, request, url_for, send_from_directory
from agents import coordinator
from google.adk.runners import InMemoryRunner
from google.genai import types


import asyncio
import json
import os
import uuid

app = Flask(__name__)

# Ensure generated_demos directory exists
GENERATED_DEMOS_DIR = os.path.join(os.path.dirname(__file__), 'generated_demos')
os.makedirs(GENERATED_DEMOS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generated_demos/<path:filename>')
def serve_demo(filename):
    return send_from_directory(GENERATED_DEMOS_DIR, filename)

@app.route('/generate-demo', methods=['POST'])
def generate_demo():
    customer_name = request.form.get('customer_name')
    industry = request.form.get('industry')
    use_case = request.form.get('use_case')

    prompt_text = f"Create a complete demo asset for customer '{customer_name}', who is in the '{industry}' industry. The demo should focus on the use case: '{use_case}'."
    
    try:
        # Create a runner for the session
        # Use a new session ID for each request
        session_id = str(uuid.uuid4())
        runner = InMemoryRunner(agent=coordinator)
        
        # Explicitly create the session
        asyncio.run(
            runner.session_service.create_session(
                app_name="InMemoryRunner",
                user_id="demo_user",
                session_id=session_id
            )
        )
        
        # Execute the agent synchronously
        events = runner.run(
            user_id="demo_user",
            session_id=session_id,
            new_message=types.Content(parts=[types.Part(text=prompt_text)])
        )
        
        # Collect the final response
        # We iterate through events and look for the final response or accumulate content
        # For simplicity, we'll take the text content from the events authored by the coordinator
        # The PackagingAgent output should be the final response.
        
        final_output_text = ""
        for event in events:
            # We are interested in the final response from the system (Coordinator)
            # which wraps the PackagingAgent output.
            # event.content might be None for tool calls etc.
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_output_text += part.text

        # The output is expected to be the JSON string from the packaging tool
        # ADK might return thoughts + JSON. We need to extract the JSON.
        cleaned_output = final_output_text
        if "```json" in cleaned_output:
            cleaned_output = cleaned_output.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_output:
            cleaned_output = cleaned_output.split("```")[1].split("```")[0].strip()

        agent_output = json.loads(cleaned_output)
        
        # New structure: {"files": [{"name": "path/to/file", "content": "..."}]}
        files = agent_output.get('files', [])

        # Create a unique directory for this demo
        demo_id = str(uuid.uuid4())
        demo_dir = os.path.join(GENERATED_DEMOS_DIR, demo_id)
        os.makedirs(demo_dir, exist_ok=True)

        saved_files = []
        for file_info in files:
            file_path = os.path.join(demo_dir, file_info['name'])
            # Ensure parent directories exist (e.g. for my_agent/agent.py)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(file_info['content'])
            saved_files.append(file_info['name'])

        return render_template('index.html', success=True, demo_id=demo_id, files=saved_files)

    except Exception as e:
        print(f"Error generating demo: {e}")
        # import traceback
        # traceback.print_exc()
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
