from flask import Flask, request, jsonify
import pickle
import re
import numpy as np
import random
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------- Load Models ----------
model = pickle.load(open("xgb_pipeline.pkl", "rb"))
fertname_dict = pickle.load(open("fertname_dict.pkl", "rb"))
croptype_dict = pickle.load(open("croptype_dict.pkl", "rb"))
soiltype_dict = pickle.load(open("soiltype_dict.pkl", "rb"))

# Reverse mapping for encoding
crop_to_int = {v: k for k, v in croptype_dict.items()}
soil_to_int = {v: k for k, v in soiltype_dict.items()}

# Store the latest crop & soil selected
latest_selection = {}
# Store latest sensor readings for /live_data
latest_sensor_data = {
    "Temperature": 0,
    "Humidity": 0,
    "Moisture": 0,
    "Nitrogen": 0,
    "Phosphorus": 0,
    "Potassium": 0,
}


def format_points(text):
    """
    Splits numbered points and ensures each point is on a separate line.
    Returns a list of points for frontend <ul> rendering.
    """
    if not text:
        return ["N/A"]

    # Match numbered points like "1. something", "2. something"
    points = re.findall(r"\d+\.\s*[^0-9]+", text)
    formatted = [pt.strip() for pt in points if pt.strip()]
    return formatted if formatted else ["N/A"]


from flask import session

# Make sure you enable sessions
app.secret_key = "your_secret_key"


@app.route("/groq-chat", methods=["POST"])
def groq_chat():
    user_input = request.json.get("message")

    # Initialize conversation history in session
    if "history" not in session:
        session["history"] = []

    # Append the new user message
    session["history"].append({"role": "user", "content": user_input})

    llm = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
    )

    system_prompt = """
You are an assistant that always responds in a clear, structured format for informative questions. Use the following sections only if they make sense:

**Answer:**
- Main points in numbered format.

**Explanation:**
- Explain the answer in numbered points if applicable. Skip if the question is trivial or conversational.

**Example:**
- Give an example in numbered points if relevant. Otherwise, write "N/A".

Include line breaks between sections. Keep answers concise, easy to read, and in points. For casual talk, respond naturally without forcing Explanation or Example.
"""

    # Pass last N messages for context (e.g., last 10)
    last_messages = session["history"][-10:]
    llm_input = [{"role": "system", "content": system_prompt}]
    for msg in last_messages:
        llm_input.append({"role": msg["role"], "content": msg["content"]})

    response = llm.invoke(llm_input)
    llm_text = response.content.strip()

    # Append bot response to history
    session["history"].append({"role": "bot", "content": llm_text})

    # Plain text for greetings/casual messages
    if "**Answer:**" not in llm_text:
        return jsonify({"reply": llm_text})

    # Extract structured sections
    answer_match = re.search(
        r"\*\*Answer:\*\*\s*(.*?)\s*(\*\*Explanation:\*\*|$)", llm_text, re.DOTALL
    )
    explanation_match = re.search(
        r"\*\*Explanation:\*\*\s*(.*?)\s*(\*\*Example:\*\*|$)", llm_text, re.DOTALL
    )
    example_match = re.search(r"\*\*Example:\*\*\s*(.*)", llm_text, re.DOTALL)

    response_json = {
        "answer": format_points(answer_match.group(1)) if answer_match else ["N/A"],
        "explanation": (
            format_points(explanation_match.group(1)) if explanation_match else ["N/A"]
        ),
        "example": format_points(example_match.group(1)) if example_match else ["N/A"],
    }

    return jsonify(response_json)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        global latest_selection, latest_sensor_data

        # Read incoming data
        data = request.get_json(force=True)
        latest_selection = data
        print("Received /predict data:", latest_selection, flush=True)

        # Environmental and sensor data
        temperature = data.get("Temperature", latest_sensor_data["Temperature"])
        humidity = data.get("Humidity", latest_sensor_data["Humidity"])
        moisture = data.get(
            "Moisture", data.get("SoilMoisture", latest_sensor_data["Moisture"])
        )

        # Crop and soil type
        crop_type = data.get("cropType", 0)
        soil_type = data.get("soilType", 0)

        soil_val = (
            soil_type if isinstance(soil_type, int) else soil_to_int.get(soil_type, 0)
        )
        crop_val = (
            crop_type if isinstance(crop_type, int) else crop_to_int.get(crop_type, 0)
        )

        nitrogen = data.get("Nitrogen", random.randint(35, 45))
        phosphorus = data.get("Phosphorus", random.randint(15, 25))
        potassium = data.get("Potassium", random.randint(20, 35))

        # Update latest sensor data
        latest_sensor_data.update(
            {
                "Temperature": temperature,
                "Humidity": humidity,
                "Moisture": moisture,
                "Nitrogen": nitrogen,
                "Phosphorus": phosphorus,
                "Potassium": potassium,
            }
        )

        # Prepare features for model
        features = np.array(
            [
                [
                    temperature,
                    humidity,
                    moisture,
                    soil_val,
                    crop_val,
                    nitrogen,
                    phosphorus,
                    potassium,
                ]
            ]
        )

        pred_label = int(model.predict(features)[0])
        fertilizer = fertname_dict.get(pred_label, "Unknown")
        print("Predicted Fertilizer:", fertilizer)

        return jsonify(
            {
                "Temperature": temperature,
                "Humidity": humidity,
                "Moisture": moisture,
                "Soil Type": soil_type,
                "Crop Type": crop_type,
                "Nitrogen": nitrogen,
                "Phosphorus": phosphorus,
                "Potassium": potassium,
                "predicted_fertilizer": fertilizer,
            }
        )

    except Exception as e:
        print("Error in /predict:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/live_data", methods=["GET"])
def live_data():
    # Return the latest sensor readings
    return jsonify(latest_sensor_data)


@app.route("/")
def home():
    return jsonify(
        {
            "message": "Smart Fertilizer Recommendation API (Test Mode)",
            "note": "If NPK sensor fails, random dummy values are used for Nitrogen, Phosphorus, Potassium",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
