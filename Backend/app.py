from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# ---------- Load Models ----------
model = pickle.load(open("xgb_pipeline.pkl", "rb"))
fertname_dict = pickle.load(open("fertname_dict.pkl", "rb"))
croptype_dict = pickle.load(open("croptype_dict.pkl", "rb"))
soiltype_dict = pickle.load(open("soiltype_dict.pkl", "rb"))

# Reverse mapping for encoding
crop_to_int = {v: k for k, v in croptype_dict.items()}
soil_to_int = {v: k for k, v in soiltype_dict.items()}

# ---------- Prediction Route ----------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        # expected keys
        required = ["Temperature", "Humidity", "Moisture",
                    "Soil Type", "Crop Type", "Nitrogen", "Phosphorus", "Potassium"]
        if not all(k in data for k in required):
            return jsonify({"error": f"Missing one of: {required}"}), 400

        # Encode categorical inputs
        soil_val = soil_to_int.get(data["Soil Type"], 0)
        crop_val = crop_to_int.get(data["Crop Type"], 0)

        # Prepare features in correct order
        features = np.array([[
            data["Temperature"],
            data["Humidity"],
            data["Moisture"],
            soil_val,
            crop_val,
            data["Nitrogen"],
            data["Phosphorus"],
            data["Potassium"]
        ]])

        # Predict
        pred_label = int(model.predict(features)[0])
        fertilizer = fertname_dict[pred_label]

        return jsonify({
            "prediction_label": pred_label,
            "fertilizer_name": fertilizer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return jsonify({
        "message": "Smart Fertilizer Recommendation API",
        "usage": "POST JSON to /predict with Temperature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Phosphorus, Potassium"
    })


if __name__ == '__main__':
    app.run(debug=True)
