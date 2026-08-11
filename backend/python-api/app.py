import joblib
import numpy as np
import requests
import pandas as pd
from flask import Flask, request, jsonify

# 1. Load the model (ensure agri_model.joblib is in the same directory)
model = joblib.load('agri_model.joblib')

app = Flask(__name__)

GEN_AI_API_URL = "https://your-gen-ai-service.com/generate-advice"

@app.route('/api/predict_and_advise', methods=['POST'])
def predict_and_advise():
    try:
        data = request.json
        # Extract identity for Gen AI, features for the Model
        farmer_name = data.get('name', 'Farmer')
        phone_number = data.get('phone', 'N/A')
        
        # Prepare features for prediction (dropping name/phone)
        features = {k: v for k, v in data.items() if k not in ['name', 'phone']}
        input_df = pd.DataFrame([features])

        # 2. Run Model Prediction
        log_pred = model.predict(input_df)[0]
        yield_val = round(float(np.expm1(log_pred)), 2)

        # 3. Forward to Gen AI with Name, Phone, and Yield
        gen_ai_payload = {
            "name": farmer_name,
            "phone": phone_number,
            "predicted_yield": yield_val,
            "input_characteristics": features,
            "recommendation_context": "Provide agricultural advice in Kinyarwanda based on this yield."
        }

        response = requests.post(GEN_AI_API_URL, json=gen_ai_payload)
        gen_ai_result = response.json()

        return jsonify({
            "status": "success",
            "sent_to_sms_gateway": True,
            "details": gen_ai_result
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)