from google.adk.agents import LlmAgent
from tools import web_research_tool, demo_packaging_tool

# Using a more capable model is better for orchestration
ORCHESTRATION_MODEL = "gemini-3-pro-preview" 
# A faster model can be used for more specific tasks
TASK_MODEL = "gemini-3-flash-preview"

# 1. Define the Research Agent
researcher = LlmAgent(
    name="ResearchAgent",
    model=TASK_MODEL,
    instruction="You are an expert market researcher. Your job is to use the provided tools to find information about a customer.",
    description="This agent researches a customer and their industry to find relevant business challenges and news.",
    tools=[web_research_tool]
)

# 2. Define the Narrative Agent
narrative_creator = LlmAgent(
    name="NarrativeAgent",
    model=TASK_MODEL, # Use a more capable model for creative generation
    instruction="""You are a creative storyteller and a technical expert.
    Your task is to take research findings and a use case, and do two things:
    1. Create a compelling demo script in HTML format that a CE can present.
    2. Generate a realistic-looking JSON object with mock data that supports the narrative.
    The final output must be ONLY the HTML script and the mock data JSON, nothing else.
    """,
    description="This agent writes the demo script and creates the mock data."
    # This agent uses no external tools; its tool is its own creative generation capability.
)

# 3. Define the Packaging Agent
packager = LlmAgent(
    name="PackagingAgent",
    model=TASK_MODEL,
    instruction="You are a packaging agent. Your job is to take the final narrative and mock data and prepare them for final output using the demo_packaging_tool.",
    description="This agent takes the generated content and packages it into a final set of artifacts.",
    tools=[demo_packaging_tool]
)

# 4. Define the Coordinator Agent
# This is the "parent" agent that directs the sub-agents.
coordinator = LlmAgent(
    name="DemoCoordinator",
    model=ORCHESTRATION_MODEL,
    instruction="""You are the coordinator of a team of agents that build customer demos.
    Your job is to manage the entire workflow step-by-step:
    1.  First, delegate to the `ResearchAgent` to get information about the customer.
    2.  Second, take the research findings and the original use case and delegate to the `NarrativeAgent` to create the demo script and mock data.
    3.  Finally, take the output from the `NarrativeAgent` and delegate to the `PackagingAgent` to create the final demo assets.
    Your final response MUST be the JSON output from the `PackagingAgent`.
    """,
    description="I am a master coordinator that builds demos by directing my team of agents.",
    sub_agents=[
        researcher,
        narrative_creator,
        packager
    ]
)
