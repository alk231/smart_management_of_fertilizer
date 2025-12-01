from flask import Flask, request, jsonify
import pickle
import re
import numpy as np
import random
from langchain_perplexity import ChatPerplexity
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

    llm = ChatPerplexity()

    system_prompt = """You are a helpful assistant. Provide clear, concise answers. 
For informative questions, structure your response naturally with explanations and examples when relevant and make sure that response is in format.

when ask hi,hello,how are you then do not give explanation give generic response like an assistant"""

    # Pass last 10 messages for context
    last_messages = session["history"][-10:]
    llm_input = [{"role": "system", "content": system_prompt}]
    for msg in last_messages:
        llm_input.append({"role": msg["role"], "content": msg["content"]})

    response = llm.invoke(llm_input)
    llm_text = response.content.strip()

    # Append bot response to history
    session["history"].append({"role": "assistant", "content": llm_text})

    return jsonify({"reply": llm_text})


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

        nitrogen = data.get("Nitrogen", random.randint(12, 22))
        phosphorus = data.get("Phosphorus", random.randint(10, 25))
        potassium = data.get("Potassium", random.randint(4, 8))

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
