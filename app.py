from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from travel_planning_agent.agent import root_agent
from dotenv import load_dotenv

# Load environment variables from travel_planning_agent/.env
load_dotenv('travel_planning_agent/.env')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend to talk to backend

# Get Google API key from environment variables
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# Set up the travel agent
travel_agent = root_agent

# Define the /chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = travel_agent.converse(user_message)
        return jsonify({"response": response.reply})
    except Exception as e:
        return jsonify({"error": f"Error processing message: {str(e)}"}), 500

# Root route to test if API is live
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Traveler Agent API is running."})

# This GET route for /chat is not necessary for your main functionality
# as the frontend sends POST requests. You can remove it if you want.

# Run the app
if __name__ == '__main__':
    app.run(debug=False, port=os.environ.get("PORT", 5000))