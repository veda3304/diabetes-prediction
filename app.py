from flask import Flask, request, render_template
import pickle
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained LightGBM model
model = pickle.load(open("lgbm_model.pkl", "rb"))

# Define feature names
FEATURES = [
    "Pregnancies",
    "PlasmaGlucose",
    "DiastolicBloodPressure",
    "TricepsThickness",
    "SerumInsulin",
    "BMI",
    "DiabetesPedigree",
    "Age",
]


# Home route: Display the input form
@app.route("/")
def home():
    return render_template("index.html")


# Prediction route: Handle form submission and redirect to output page
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from the form
        input_data = [float(request.form[feature]) for feature in FEATURES]

        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data], columns=FEATURES)

        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1] * 100

        # Interpret the prediction
        result = "Diabetic" if prediction == 1 else "Not Diabetic"

        # Redirect to output page with prediction results
        return render_template(
            "output.html",
            prediction_text=f"Prediction: {result}",
            probability_text=f"Probability of being diabetic: {probability:.2f}%",
        )
    except Exception as e:
        return render_template(
            "output.html", prediction_text=f"Error: {str(e)}", probability_text=""
        )


# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Heroku's port or default to 5000
    app.run(host="0.0.0.0", port=port, debug=False)  # Set debug=False for production
