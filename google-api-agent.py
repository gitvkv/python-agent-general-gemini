# This is a simple AI agent that uses the Gemini API to respond to user prompts.
# It's a great starting point for new programmers to understand how AI agents work.

# First, you'll need to install the 'requests' library to make API calls.
# You can do this by opening your terminal and typing:
# pip install requests

import requests
import json
import os
from dotenv import load_dotenv

# Your API key from Google AI Studio.
# You can get one for free at https://aistudio.google.com/app/apikey
# IMPORTANT: Never share your API key with anyone or put it in a public repository.
# For this simple example, we'll store it directly in the code, but in a real app,
# you would use environment variables or a secure vault.

load_dotenv()

def get_api_key():
    """
    Retrieves the API key from the environment variables.

    Returns:
        str: The API key, or None if not found.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key is None:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please create a .env file and add GEMINI_API_KEY='your-api-key-here'")
    return api_key



API_KEY = get_api_key()

print(f"Using API Key: {API_KEY}")  # For debugging purposes only. Remove in production!
if API_KEY is None:
    exit(1)

# The Gemini API endpoint we will use.
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

def get_ai_response(prompt):
    """
    Sends a prompt to the Gemini API and gets a response.
    The 'tools' property with 'google_search' allows the model to search the web
    for current information, making it a powerful agent.
    """
    
    # We define the system instruction and the user prompt.
    # The system instruction tells the model what its role is.
    # The 'tools' property is what turns this into a web-aware agent.
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "tools": [
            {"google_search": {}}
        ],
        "systemInstruction": {
            "parts": [{"text": "You are a helpful and intelligent AI assistant. Use Google Search to find information when needed to provide accurate and up-to-date responses."}]
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Make the POST request to the API.
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        # Raise an exception for bad status codes (4xx or 5xx).
        response.raise_for_status()

        # Parse the JSON response.
        response_data = response.json()
        
        # Check if the response contains a valid candidate.
        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            candidate = response_data["candidates"][0]
            # Extract the text content from the response.
            if "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                return candidate["content"]["parts"][0]["text"]
        
        return "I'm sorry, I couldn't get a response from the AI."
        
    except requests.exceptions.RequestException as e:
        # Handle any network or API-related errors.
        return f"An error occurred: {e}"

# --- Main part of the script ---

if __name__ == "__main__":
    # Introduce the user to the AI agent and provide usage instructions.
    print("Welcome! This is your AI agent powered by Gemini.")
    print("You can ask any question, and I'll search for the latest information to help you.")
    print("Ask me anything, and I'll do my best to provide a response.")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("-" * 50)

    while True:
        # Get user input.
        user_prompt = input("You: ")

        # Check for exit commands.
        if user_prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not user_prompt.strip():
            continue

        # Get the AI's response.
        print("AI Agent: Thinking...")
        ai_response = get_ai_response(user_prompt)

        # Print the response to the console.
        print(f"AI Agent: {ai_response}\n")
        print(f"#####################################################\n")

