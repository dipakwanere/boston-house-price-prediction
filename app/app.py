import os
import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template


app = Flask(__name__, template_folder="../templates")

# Load model and scaler at startup
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "regmodel.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaling.pkl")

with open(MODEL_PATH, "rb") as f:
	regmodel = pickle.load(f)

with open(SCALER_PATH, "rb") as f:
	scalar = pickle.load(f)

# Fixed feature order to align with training/scaler
FEATURE_ORDER = [
	"CRIM","ZN","INDUS","CHAS","NOX","RM","AGE","DIS",
	"RAD","TAX","PTRATION","B","LSTAT"
]

@app.route("/")
def home():
	return render_template('home.html')


@app.route("/predict", methods=["GET","POST"])
def predict_api():
	if request.method == "GET":
		return jsonify({"message": "POST a JSON body to /predict with key 'data', or submit the HTML form on /"})

	# If the request came from an HTML form submission
	if request.form:
		try:
			data = [float(request.form[name]) for name in FEATURE_ORDER]
		except Exception:
			return render_template('home.html', prediction_text="Invalid input. Please enter numeric values." )
		final_input = scalar.transform(np.array(data).reshape(1,-1))
		output = regmodel.predict(final_input)[0]
		return render_template('home.html', prediction_text=f"The House price prediction is {output}")

	# Fallback: JSON API
	payload = request.get_json(silent=True) or {}
	if 'data' not in payload:
		return jsonify({"error": "Missing 'data' in JSON body"}), 400
	data_dict = payload['data']
	new_data = scalar.transform(np.array([data_dict[name] for name in FEATURE_ORDER]).reshape(1,-1))
	output = regmodel.predict(new_data)
	return jsonify(output[0])

# Alias path if user calls /predict_api directly
@app.route("/predict_api", methods=["POST"])
def predict_api_alias():
	return predict_api()

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
