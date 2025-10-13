from flask import Flask, request, jsonify
import pickle
import numpy as np
import random

app = Flask(_name_)

# ---------- Load Models ----------
model = pickle.load(open("xgb_pipeline.pkl", "rb"))
fertname_dict = pickle.load(open("fertname_dict.pkl", "rb"))
croptype_dict = pickle.load(open("croptype_dict.pkl", "rb"))
soiltype_dict = pickle.load(open("soiltype_dict.pkl", "rb"))

# Reverse mapping for encoding
crop_to_int = {v: k for k, v in croptype_dict.items()}
soil_to_int = {v: k for k, v in soiltype_dict.items()}


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        # Handle environmental data or sensor failure
        temperature = data.get("Temperature", 28)
        humidity = data.get("Humidity", 65)
        moisture = data.get("Moisture", data.get("SoilMoisture", 18))

        # Crop type and soil type from frontend (required)
        crop_type = int(data['cropType'])
        soil_type = int(data['soilType'])

        # If NPK sensor fails, assign dummy values
        nitrogen = data.get("Nitrogen", random.randint(30, 60))
        phosphorus = data.get("Phosphorus", random.randint(15, 40))
        potassium = data.get("Potassium", random.randint(10, 35))

        # Encode categorical inputs
        soil_val = soil_type if isinstance(soil_type, int) else soil_to_int.get(soil_type, 0)
        crop_val = crop_type if isinstance(crop_type, int) else crop_to_int.get(crop_type, 0)

        # Prepare features in correct order for the model
        features = np.array([[temperature, humidity, moisture,
                              soil_val, crop_val, nitrogen, phosphorus, potassium]])

        # Predict fertilizer
        pred_label = int(model.predict(features)[0])
        fertilizer = fertname_dict[pred_label]

        # Return JSON with all details for frontend graph/UI
        return jsonify({
            "Temperature": temperature,
            "Humidity": humidity,
            "Moisture": moisture,
            "Soil Type": soil_type,
            "Crop Type": crop_type,
            "Nitrogen": nitrogen,
            "Phosphorus": phosphorus,
            "Potassium": potassium,
            "predicted_fertilizer": fertilizer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return jsonify({
        "message": "Smart Fertilizer Recommendation API (Test Mode)",
        "note": "If NPK sensor fails, random dummy values are used for Nitrogen, Phosphorus, Potassium"
    })


if _name_ == '_main_':
    app.run(debug=True)
