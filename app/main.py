from fastapi import FastAPI
from pydantic import BaseModel
from .orchestrator import create_graph

app = FastAPI(
    title="AI Tutor Orchestrator",
    description="The intelligent middleware for an AI Tutoring System."
)

# Create the graph instance
graph = create_graph()

# --- API Request Models ---
class OrchestratorRequest(BaseModel):
    message: str
    user_id: str

# --- API Endpoints ---
@app.get("/", tags=["Status"])
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"status": "API is running"}

@app.post("/orchestrate", tags=["Orchestrator"])
async def orchestrate(request: OrchestratorRequest):
    """
    Main endpoint to process a user's message and orchestrate the AI tools.
    """
    # For this hackathon, we'll use a mock user profile.
    # In a real application, you would fetch this from a database using request.user_id.
    mock_user_profile = {
        "user_id": request.user_id,
        "name": "Alex",
        "grade_level": "10",
        "learning_style_summary": "Prefers visual examples and structured notes.",
        "emotional_state_summary": "Focused and motivated.",
        "mastery_level_summary": "Level 5: Developing competence with guided practice."
    }

    # Prepare the initial state for the graph
    initial_state = {
        "keys": {
            "message": request.message,
            "user_info": mock_user_profile,
            # In a real app, you'd also include chat_history here
        }
    }

    # Invoke the graph with the initial state
    final_state = graph.invoke(initial_state)

    # Return the final result from the tool
    return {"response": final_state['keys'].get('tool_result')}