from flask import Flask, render_template, request, url_for, send_from_directory
from agents import coordinator
from google.adk.runners import InMemoryRunner
from google.genai import types

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
        # However, PackagingAgent is instructed to return *only* the JSON is tricky with LLMs.
        # But let's assume the final output text contains the JSON.
        # We might need to clean markdown code blocks.
        
        cleaned_output = final_output_text
        if "```json" in cleaned_output:
            cleaned_output = cleaned_output.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_output:
            # Maybe just ``` without json
             cleaned_output = cleaned_output.split("```")[1].split("```")[0].strip()

        agent_output = json.loads(cleaned_output)
        
        narrative = agent_output.get('narrative', '')
        mock_data_files = agent_output.get('files', [])

        # Render the full demo HTML using the template
        template = app.jinja_env.get_template('demo_template.html')
        rendered_demo = template.render(
            narrative=narrative,
            mock_data_files=mock_data_files
        )

        # Save to a file
        filename = f"demo_{uuid.uuid4()}.html"
        filepath = os.path.join(GENERATED_DEMOS_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(rendered_demo)

        # Generate URL for the new file
        demo_url = f"/generated_demos/{filename}"

        return render_template('index.html', demo_url=demo_url)

    except Exception as e:
        print(f"Error generating demo: {e}")
        # import traceback
        # traceback.print_exc()
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
