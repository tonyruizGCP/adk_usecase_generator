from flask import Flask, render_template, request, url_for, send_from_directory
from agents import coordinator
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

    prompt = f"Create a complete demo asset for customer '{customer_name}', who is in the '{industry}' industry. The demo should focus on the use case: '{use_case}'."

    # Invoke the ADK agent
    # The coordinator returns a list of GenerationResponse objects (or dicts if mocked)
    # We assume standard ADK invoke return structure
    try:
        response = coordinator.invoke(prompt)
        # response[0].content should contain the JSON string from the packaging tool
        agent_output_str = response[0].content
        
        # Parse the JSON output from the agent
        agent_output = json.loads(agent_output_str)
        
        narrative = agent_output.get('narrative', '')
        mock_data_files = agent_output.get('files', [])

        # Render the full demo HTML using the template
        # We need to manually render the template string here to save it to a file
        # But Flask's render_template returns the full response. 
        # We can use render_template_string or app.jinja_env.get_template
        
        # Use app.jinja_env to retrieve the template and render it
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
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
