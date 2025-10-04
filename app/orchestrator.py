import os
from typing import TypedDict, Annotated, List
# CHANGE 1: Import the Google Gemini model instead of OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from . import schemas
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from . import tools

# Load environment variables from .env file
load_dotenv()

# Define the state for our graph
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        keys: A dictionary to store the user's message and other details.
    """
    keys: dict

# --- Nodes ---

class ToolRouter(BaseModel):
    """Route the user to the appropriate tool."""
    tool: str

def get_tool_router():
    """Create the tool router chain."""
    # CHANGE 2: Use the Google Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
    
    structured_llm_router = llm.with_structured_output(ToolRouter)
    
    system_prompt = """You are an expert at routing a user's request to the appropriate tool.
    Based on the user's request, route them to the one of the following tools:
    
    Note Maker: Use this tool when the user wants to create notes, summaries, or outlines on a specific topic.
    
    Flashcard Generator: Use this tool when the user wants to create flashcards for studying, testing their knowledge, or memorization.
    
    Concept Explainer: Use this tool when the user is asking for an explanation of a concept, idea, or topic.
    
    If the user's request is ambiguous, irrelevant, or if you're not sure which tool to use, route them to 'no_tool'.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    return prompt | structured_llm_router

def route_to_tool(state: GraphState):
    """
    This is the first node in our graph. It routes the user's request to the appropriate tool.
    """
    print("--- NODE: route_to_tool ---")
    
    user_message = state['keys']['message']
    
    tool_router = get_tool_router()
    tool_choice = tool_router.invoke({"input": user_message})
    
    print(f"Tool choice: {tool_choice.tool}")

    state['keys']['tool'] = tool_choice.tool
    
    return {"keys": state['keys']}


# --- Edges ---

def decide_next_node(state: GraphState):
    """
    Determines the next node to visit based on the tool choice.
    """
    print("--- EDGE: decide_next_node ---")
    
    tool_choice = state['keys'].get('tool')
    
    if tool_choice == 'Note Maker':
        return 'note_maker'
    elif tool_choice == 'Flashcard Generator':
        return 'flashcard_generator'
    elif tool_choice == 'Concept Explainer':
        return 'concept_explainer'
    else:
        return 'end'


# --- Parameter Extraction Nodes ---

def get_parameter_extractor(tool_schema):
    """A helper function to create a parameter extraction chain for a given tool schema."""
    # CHANGE 3: Use the Google Gemini model here as well
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
    structured_llm_extractor = llm.with_structured_output(tool_schema)
    
    system_prompt = """You are an expert at extracting parameters from a user's request to fill a tool's schema.
    Based on the user's message and their profile information, extract the required parameters for the following tool.
    
    User Profile:
    - Grade Level: {grade_level}
    - Learning Style: {learning_style_summary}
    - Emotional State: {emotional_state_summary}
    - Mastery Level: {mastery_level_summary}
    
    Infer any missing parameters based on the context. For example, if a user says they are "struggling", the difficulty should be 'easy' or 'basic'.
    If the user's emotional state is 'anxious' or 'confused', simplify the request (e.g., lower the count, choose 'basic' depth).
    If the user's mastery level is low (1-3), choose 'easy'/'basic' settings. If high (7+), choose 'hard'/'advanced' settings.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{message}")
    ])
    
    return prompt | structured_llm_extractor

def extract_note_maker_params(state: GraphState):
    """Node to extract parameters for the Note Maker tool."""
    print("--- NODE: extract_note_maker_params ---")
    
    keys = state['keys']
    user_info = keys['user_info']
    
    param_extractor = get_parameter_extractor(schemas.NoteMakerInput)
    
    extracted_params = param_extractor.invoke({
        "message": keys['message'],
        "grade_level": user_info['grade_level'],
        "learning_style_summary": user_info['learning_style_summary'],
        "emotional_state_summary": user_info['emotional_state_summary'],
        "mastery_level_summary": user_info['mastery_level_summary'],
    })
    
    keys['tool_parameters'] = extracted_params
    return {"keys": keys}

def extract_flashcard_params(state: GraphState):
    """Node to extract parameters for the Flashcard Generator tool."""
    print("--- NODE: extract_flashcard_params ---")
    
    keys = state['keys']
    user_info = keys['user_info']
    
    param_extractor = get_parameter_extractor(schemas.FlashcardGeneratorInput)
    
    extracted_params = param_extractor.invoke({
        "message": keys['message'],
        "grade_level": user_info['grade_level'],
        "learning_style_summary": user_info['learning_style_summary'],
        "emotional_state_summary": user_info['emotional_state_summary'],
        "mastery_level_summary": user_info['mastery_level_summary'],
    })
    
    keys['tool_parameters'] = extracted_params
    return {"keys": keys}

def extract_concept_explainer_params(state: GraphState):
    """Node to extract parameters for the Concept Explainer tool."""
    print("--- NODE: extract_concept_explainer_params ---")
    
    keys = state['keys']
    user_info = keys['user_info']
    
    param_extractor = get_parameter_extractor(schemas.ConceptExplainerInput)
    
    extracted_params = param_extractor.invoke({
        "message": keys['message'],
        "grade_level": user_info['grade_level'],
        "learning_style_summary": user_info['learning_style_summary'],
        "emotional_state_summary": user_info['emotional_state_summary'],
        "mastery_level_summary": user_info['mastery_level_summary'],
    })
    
    keys['tool_parameters'] = extracted_params
    return {"keys": keys}


# --- Tool Calling Nodes ---

def call_note_maker(state: GraphState):
    """Calls the mock Note Maker tool."""
    print("--- NODE: call_note_maker ---")
    keys = state['keys']
    tool_parameters = keys.get('tool_parameters')
    
    result = tools.note_maker_tool(tool_parameters)
    
    keys['tool_result'] = result
    return {"keys": keys}

def call_flashcard_generator(state: GraphState):
    """Calls the mock Flashcard Generator tool."""
    print("--- NODE: call_flashcard_generator ---")
    keys = state['keys']
    tool_parameters = keys.get('tool_parameters')
    result = tools.flashcard_generator_tool(tool_parameters)
    keys['tool_result'] = result
    return {"keys": keys}

def call_concept_explainer(state: GraphState):
    """Calls the mock Concept Explainer tool."""
    print("--- NODE: call_concept_explainer ---")
    keys = state['keys']
    tool_parameters = keys.get('tool_parameters')
    result = tools.concept_explainer_tool(tool_parameters)
    keys['tool_result'] = result
    return {"keys": keys}


# --- Graph Assembly ---

def create_graph():
    """Creates the LangGraph workflow."""
    workflow = StateGraph(GraphState)

    # Add the nodes
    workflow.add_node("router", route_to_tool)
    workflow.add_node("note_maker_extractor", extract_note_maker_params)
    workflow.add_node("flashcard_generator_extractor", extract_flashcard_params)
    workflow.add_node("concept_explainer_extractor", extract_concept_explainer_params)
    workflow.add_node("note_maker", call_note_maker)
    workflow.add_node("flashcard_generator", call_flashcard_generator)
    workflow.add_node("concept_explainer", call_concept_explainer)

    # Set the entry point
    workflow.set_entry_point("router")

    # Add the conditional edge from the router
    workflow.add_conditional_edges(
        "router",
        decide_next_node,
        {
            "note_maker": "note_maker_extractor",
            "flashcard_generator": "flashcard_generator_extractor",
            "concept_explainer": "concept_explainer_extractor",
            "end": END
        }
    )

    # Add edges from the parameter extractors to the tool callers
    workflow.add_edge("note_maker_extractor", "note_maker")
    workflow.add_edge("flashcard_generator_extractor", "flashcard_generator")
    workflow.add_edge("concept_explainer_extractor", "concept_explainer")

    # Add edges from the tool callers to the end
    workflow.add_edge("note_maker", END)
    workflow.add_edge("flashcard_generator", END)
    workflow.add_edge("concept_explainer", END)

    # Compile the graph
    return workflow.compile()