import google.generativeai as genai
import json
import uuid
from dotenv import load_dotenv
import os

# Load variables from .env file into the environment
load_dotenv()


genai.configure(api_key=os.getenv("gemini_key"))
def build_conversation_context(chat_history):
    """
    Takes a list of chat entries (each with user_input and response.response_to_user)
    and returns a formatted conversation string.
    """
    convo_lines = []

    for chat in chat_history:
        user_input = chat.get("user_input", "").strip()
        bot_response = chat.get("response", {}).get("response_to_user", "").strip()

        if user_input:
            convo_lines.append(f"User: {user_input}")
        if bot_response:
            convo_lines.append(f"Amica: {bot_response}")

    return "\n".join(convo_lines)

def parse_gemini_response(response):
    parsed = {
        "response_to_user": "",
        "emotion": "",
        "suicidal_cues": "",
        "summary": "",
        "urgency": ""
    }

    for line in response.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip().lower().replace(" ", "_")
            value = value.strip().strip('"')
            if key in parsed:
                parsed[key] = value

    return parsed
CHATS_FILE = "chats.json"
def save_chat(entry):
    with open(CHATS_FILE, "r+") as f:
        chats = json.load(f)
        chats.append(entry)
        f.seek(0)
        json.dump(chats, f, indent=2)
def get_gemini_response(user_id,input):
    coversation = ""
    # Load the conversation history for the user
    with open(CHATS_FILE, "r") as f:
        chats = json.load(f)
    chats = [chat for chat in chats if chat.get("user_id") == user_id]
    conversation= build_conversation_context(chats)
    conversation += f"\nUser: {input}"
    
    prompt = f"""
        You are an expert mental health assistant.
You are Amica, a kind and expert mental health assistant.

Here is the ongoing conversation:
{conversation}

Now, respond empathetically to the latest user message and analyze it :
be short and like a friend
Format your output exactly like this:
response_to_user: ...
Emotion: ...
Suicidal Cues: ...
Summary: ...
Urgency: ...
"""


    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    
    parsed_response= parse_gemini_response(response.text)
    entry = {"id": str(uuid.uuid4()), "user_id":user_id,"user_input": input, "response": parsed_response}
    save_chat(entry)
    return parsed_response
