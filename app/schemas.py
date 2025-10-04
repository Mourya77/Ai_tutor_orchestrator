from pydantic import BaseModel, Field
from typing import List, Literal

# --- Common Reusable Schemas ---

class UserInfo(BaseModel):
    """Consistent user information object required by all tools."""
    user_id: str
    name: str
    grade_level: str
    learning_style_summary: str
    emotional_state_summary: str
    mastery_level_summary: str

class ChatMessage(BaseModel):
    """Represents a single message in the conversation history."""
    role: Literal['user', 'assistant']
    content: str


# --- Tool-Specific Input Schemas ---

class NoteMakerInput(BaseModel):
    """Input schema for the Note Maker Tool."""
    user_info: UserInfo
    chat_history: List[ChatMessage]
    topic: str
    subject: str
    note_taking_style: Literal['outline', 'bullet_points', 'narrative', 'structured']
    include_examples: bool = True
    include_analogies: bool = False

class FlashcardGeneratorInput(BaseModel):
    """Input schema for the Flashcard Generator Tool."""
    user_info: UserInfo
    topic: str
    count: int = Field(..., ge=1, le=20) # Ensures count is between 1 and 20
    difficulty: Literal['easy', 'medium', 'hard']
    subject: str
    include_examples: bool = True

class ConceptExplainerInput(BaseModel):
    """Input schema for the Concept Explainer Tool."""
    user_info: UserInfo
    chat_history: List[ChatMessage]
    concept_to_explain: str
    current_topic: str
    desired_depth: Literal['basic', 'intermediate', 'advanced', 'comprehensive']