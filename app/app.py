import os
import pickle
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, render_template_string, request


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "regmodel.pkl"


def load_model(model_path: Path) -> Any:
	if not model_path.exists():
		raise FileNotFoundError(f"Model file not found at: {model_path}")
	with open(model_path, "rb") as f:
		return pickle.load(f)


def create_app() -> Flask:
	app = Flask(__name__)

	# Load model once at startup
	app.config["MODEL"] = load_model(MODEL_PATH)

	@app.get("/health")
	def health() -> Dict[str, str]:
		return {"status": "ok"}

	@app.get("/")
	def index():
		# Minimal form for quick manual testing
		html = """
		<!doctype html>
		<title>House Price Prediction</title>
		<h1>Predict</h1>
		<form method="post" action="/predict">
		  <input name="feature1" placeholder="feature1" required />
		  <input name="feature2" placeholder="feature2" required />
		  <button type="submit">Predict</button>
		</form>
		"""
		return render_template_string(html)

	@app.post("/predict")
	def predict():
		model = app.config.get("MODEL")
		if model is None:
			return jsonify({"error": "Model not loaded"}), 500

		# Accept JSON or form data
		if request.is_json:
			data = request.get_json(silent=True) or {}
		else:
			data = request.form.to_dict()

		try:
			# Example expects two numeric features. Adjust to your model inputs.
			feature1 = float(data.get("feature1"))
			feature2 = float(data.get("feature2"))
		except (TypeError, ValueError):
			return jsonify({"error": "Invalid or missing features"}), 400

		# Build input shape expected by scikit-learn: [[f1, f2, ...]]
		features = [[feature1, feature2]]
		try:
			prediction = model.predict(features)
		except Exception as exc:
			return jsonify({"error": f"Prediction failed: {exc}"}), 500

		# Convert numpy types to Python native
		pred_value = prediction[0] if isinstance(prediction, (list, tuple)) else prediction
		try:
			pred_value = float(pred_value)
		except Exception:
			pred_value = str(pred_value)

		return jsonify({"prediction": pred_value})

	return app


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app = create_app()
	app.run(host="0.0.0.0", port=port, debug=True)
