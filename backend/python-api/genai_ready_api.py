import os
from pathlib import Path

import requests
from flask import Flask, jsonify

app = Flask(__name__)

MODEL_API_URL = os.environ.get(
    "MODEL_API_URL",
    "https://ai-model.onrender.com/api/predict",
)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/farmer-recommendation/<farmer_id>")
def farmer_recommendation(farmer_id):
    """Return a clean, GenAI-friendly prediction payload for one farmer."""
    try:
        response = requests.post(
            f"{MODEL_API_URL}/{farmer_id}",
            timeout=60,
        )
        response.raise_for_status()
        model_payload = response.json()
    except requests.RequestException as exc:
        return jsonify({
            "status": "error",
            "message": f"Could not fetch model prediction: {exc}",
        }), 502

    if model_payload.get("status") != "success":
        return jsonify({
            "status": "error",
            "message": model_payload.get("message", "Prediction failed"),
        }), 400

    result = model_payload.get("result", {})

    return jsonify({
        "status": "success",
        "farmer_id": result.get("farmer_id"),
        "crop_type": result.get("crop_type_received"),
        "prediction": {
            "match_mode": result.get("match_mode"),
            "n_neighbors": result.get("n_neighbors"),
            "median_harvest_kg": result.get("median_harvest_kg"),
            "fertilizer_rate": result.get("fertilizer_rate"),
            "inorganic_fertilizer_rate": result.get("inorganic_fertilizer_rate"),
            "pesticide_rate": result.get("pesticide_rate"),
            "irrigation_rate": result.get("irrigation_rate"),
            "generated_at": result.get("generated_at"),
        },
    })


@app.post("/api/genai/advice")
def genai_advice():
    """Example wrapper that converts prediction data into a prompt for a GenAI model."""
    data = requests.get_json(silent=True) or {}
    farmer_id = data.get("farmer_id")

    if not farmer_id:
        return jsonify({
            "status": "error",
            "message": "farmer_id is required",
        }), 400

    recommendation_response = requests.get(
        f"http://127.0.0.1:5000/api/farmer-recommendation/{farmer_id}",
        timeout=60,
    )
    recommendation_response.raise_for_status()
    recommendation = recommendation_response.json()

    if recommendation.get("status") != "success":
        return jsonify({
            "status": "error",
            "message": recommendation.get("message", "Unable to build recommendation payload"),
        }), 400

    prediction = recommendation.get("prediction", {})

    prompt = (
        "You are an agricultural advisor. "
        f"Farmer ID: {recommendation.get('farmer_id')}. "
        f"Crop: {recommendation.get('crop_type')}. "
        f"Prediction summary: similar records used={prediction.get('n_neighbors')}, "
        f"median harvest={prediction.get('median_harvest_kg')} kg, "
        f"fertilizer rate={prediction.get('fertilizer_rate')}, "
        f"inorganic fertilizer rate={prediction.get('inorganic_fertilizer_rate')}, "
        f"pesticide rate={prediction.get('pesticide_rate')}, "
        f"irrigation rate={prediction.get('irrigation_rate')}. "
        "Give a short, practical recommendation in simple language."
    )

    return jsonify({
        "status": "success",
        "farmer_id": farmer_id,
        "prompt": prompt,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
