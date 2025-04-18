from flask import Flask, render_template, request
import lightgbm as lgb
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
        features = [
            float(request.form["Pregnancies"]),
            float(request.form["PlasmaGlucose"]),
            float(request.form["DiastolicBloodPressure"]),
            float(request.form["TricepsThickness"]),
            float(request.form["SerumInsulin"]),
            float(request.form["BMI"]),
            float(request.form["DiabetesPedigree"]),
            float(request.form["Age"]),
        ]
        # Load model
        model_path = os.path.join(os.path.dirname(__file__), "lgbm_model.pkl")
        model = lgb.Booster(model_file=model_path)
        # Predict
        prediction = model.predict([features])[0]
        result = "Diabetic" if prediction > 0.5 else "Not Diabetic"
        return render_template("output.html", prediction=result)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
