from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# === Load trained model ===
with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)

# === Define all feature names ===
numeric_features = [
    "Age", "Weight_kg", "Height_cm", "BMI", "Daily_Caloric_Intake",
    "Cholesterol_mg/dL", "Blood_Pressure_mmHg", "Glucose_mg/dL",
    "Weekly_Exercise_Hours", "Adherence_to_Diet_Plan",
    "Dietary_Nutrient_Imbalance_Score"
]

categorical_features = [
    "Gender", "Disease_Type", "Severity", "Physical_Activity_Level",
    "Dietary_Restrictions", "Allergies", "Preferred_Cuisine"
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # === Get numeric features from form ===
        numeric_values = [float(request.form[f]) for f in numeric_features]

        # === Get categorical features from form ===
        categorical_values = [request.form[f] for f in categorical_features]

        # Combine into a single DataFrame
        input_df = pd.DataFrame([numeric_values + categorical_values],
                                columns=numeric_features + categorical_features)

        # === Predict diet recommendation ===
        prediction = model.predict(input_df)[0]

        return render_template('result.html', prediction=prediction)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
