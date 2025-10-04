# AI Tutor Orchestrator

This project is an intelligent middleware orchestrator built for the Yophoria Innovation Challenge. It acts as the "brain" for an AI tutoring system, capable of understanding a student's natural language requests and routing them to the appropriate educational tool with the correct parameters.

## 📜 Overview

The core of this project is a FastAPI server powered by a LangGraph agent. When a user sends a message (e.g., "make me some flashcards about biology"), the orchestrator performs the following steps:

1.  **Tool Routing**: An LLM (Google Gemini) analyzes the message to decide which tool is most appropriate (e.g., Flashcard Generator).
2.  **Parameter Extraction**: A second LLM call parses the message and a mock user profile to intelligently fill in the required parameters for that tool (e.g., topic: "biology", difficulty: "easy").
3.  **Tool Execution**: The orchestrator calls the chosen (mock) tool with the extracted parameters.
4.  **Response**: The result from the tool is returned to the user.

This architecture is designed to be highly scalable, making it easy to add dozens of new tools by following the same pattern.

## ✨ Key Features

* **Intelligent Tool Routing**: Automatically selects the correct educational tool (Note Maker, Flashcard Generator, Concept Explainer) based on the user's intent.
* **Dynamic Parameter Extraction**: Uses an LLM to parse natural language and populate detailed tool schemas.
* **Context-Aware Personalization**: Leverages mock user profile data (mastery level, emotional state) to influence tool choices (e.g., inferring 'easy' difficulty for a 'struggling' user).
* **Scalable Architecture**: Built with a modular node-and-edge system (LangGraph) that simplifies the process of adding new tools.
* **API-First Design**: Exposes all functionality through a clean FastAPI endpoint with automatic interactive documentation.

## 🛠 Technology Stack

* **Backend**: Python, FastAPI
* **AI Frameworks**: LangChain, LangGraph
* **LLM**: Google Gemini
* **Core Libraries**: Pydantic, Uvicorn, python-dotenv

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

* Python 3.10 or higher
* pip (Python's package installer)

### Step-by-Step Setup

**1. Clone the Repository**
First, clone the project repository to your local machine.
```bash
git clone <your-repository-url-here>
```

**2. Navigate to the Project Directory**
Change your current directory to the newly cloned project folder.
```bash
cd ai_tutor_orchestrator
```

**3. Create and Activate the Virtual Environment**
This project uses a virtual environment to manage its dependencies.

* **Create the environment:**
    ```bash
    python -m venv venv
    ```

* **Activate the environment:**
    * On **Windows (PowerShell)**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    * On **macOS / Linux**:
        ```bash
        source venv/bin/activate
        ```

**4. Install Dependencies**
Install all the required Python libraries using the requirements.txt file.
```bash
pip install -r requirements.txt
```

**5. Set Up Environment Variables**
The application requires a Google AI API Key to function.

* In the project's root directory, create a new file named .env.
* Open the .env file and add your Google AI API Key. It should look like this:
    ```env
    GOOGLE_API_KEY="your_actual_api_key_here"
    ```

**6. Run the Server**
With the setup complete, you can run the FastAPI server using Uvicorn.
```bash
uvicorn app.main:app --reload
```
The server will be running on http://127.0.0.1:8000.

## 🧪 Usage and Testing

Once the server is running, you can test the application using the interactive documentation provided by FastAPI.

1.  Open your web browser and navigate to:
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

2.  Expand the POST /orchestrate endpoint and click "Try it out".

3.  Use the "Request body" to send different messages and test the various tool routes.

### Example Requests

**To trigger the Note Maker:**
```json
{
  "message": "I need to make a structured outline for my essay on the causes of World War II.",
  "user_id": "user123"
}
```

**To trigger the Flashcard Generator:**
```json
{
  "message": "Make me 10 medium-difficulty flashcards about the periodic table.",
  "user_id": "user456"
}
```

**To trigger the Concept Explainer:**
```json
{
  "message": "Can you give me an advanced explanation of quantum entanglement?",
  "user_id": "user789"
}
```
