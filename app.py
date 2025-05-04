from flask import Flask, request, jsonify
import os
from travel_planning_agent import agent  # Imports the 'agent' module (agent.py)
from dotenv import load_dotenv

load_dotenv('travel_planning_agent/.env')

app = Flask(__name__)

google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

travel_agent = agent.root_agent  # Access the 'root_agent' from the imported 'agent' module

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
        return jsonify({"error": f"Error processing message: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=False, port=os.environ.get("PORT", 5000))