from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_utils import get_gemini_response
from dotenv import load_dotenv
import os

# Load variables from .env file into the environment
load_dotenv()
import json

app = Flask(__name__)
CORS(app)

CHATS_FILE = "chats.json"

# Initialize chat storage
if not os.path.exists(CHATS_FILE):
    with open(CHATS_FILE, "w") as f:
        json.dump([], f)


#user params from this
@app.route("/api/chats", methods=["GET"]) 
#user params from request phone number as id
def get_chats():
    with open(CHATS_FILE, "r") as f:
        chats = json.load(f)
    # Filter chats by user ID if provided
    user_id = request.args.get("user_id")
    if user_id:
        chats = [chat for chat in chats if chat.get("user_id") == user_id]
   
    return jsonify(chats)

@app.route("/api/chat", methods=["POST"])
def post_chat():
    #get user_id from request
    if not request.json or "message" not in request.json:
        return jsonify({"error": "Invalid input"}), 400
    # Assuming user_id is passed in the request body
    data = request.json
    user_id = data.get("user_id")

    user_input = data.get("message", "") 
    response = get_gemini_response(user_id,user_input)
    
    return jsonify(response)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)), debug=True)
