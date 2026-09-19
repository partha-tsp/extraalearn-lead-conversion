
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load("extraalearn_final_model.pkl")

FEATURE_COLUMNS = [
    "age",
    "current_occupation",
    "first_interaction",
    "profile_completed",
    "website_visits",
    "time_spent_on_website",
    "page_views_per_visit",
    "last_activity",
    "print_media_type1",
    "print_media_type2",
    "digital_media",
    "educational_channels",
    "referral"
]


def prepare_input(data):
    """Prepare incoming JSON data for model prediction."""
    return pd.DataFrame([{
        feature: data[feature]
        for feature in FEATURE_COLUMNS
    }])


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "ExtraaLearn Lead Conversion API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400

        missing_features = [
            feature for feature in FEATURE_COLUMNS
            if feature not in data
        ]

        if missing_features:
            return jsonify({
                "error": "Missing required features",
                "missing_features": missing_features
            }), 400

        input_df = prepare_input(data)

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        return jsonify({
            "prediction": int(prediction),
            "prediction_label": (
                "Converted" if prediction == 1 else "Not Converted"
            ),
            "conversion_probability": round(float(probability), 4)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    try:
        data = request.get_json()

        if not isinstance(data, list) or len(data) == 0:
            return jsonify({
                "error": "Expected a non-empty JSON list"
            }), 400

        missing_features = []

        for index, record in enumerate(data):
            record_missing = [
                feature for feature in FEATURE_COLUMNS
                if feature not in record
            ]

            if record_missing:
                missing_features.append({
                    "record": index,
                    "missing_features": record_missing
                })

        if missing_features:
            return jsonify({
                "error": "Some records are missing required features",
                "details": missing_features
            }), 400

        input_df = pd.DataFrame(data)[FEATURE_COLUMNS]

        predictions = model.predict(input_df)
        probabilities = model.predict_proba(input_df)[:, 1]

        results = []

        for prediction, probability in zip(predictions, probabilities):
            results.append({
                "prediction": int(prediction),
                "prediction_label": (
                    "Converted"
                    if prediction == 1
                    else "Not Converted"
                ),
                "conversion_probability": round(
                    float(probability), 4
                )
            })

        return jsonify({
            "count": len(results),
            "predictions": results
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
