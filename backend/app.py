from flask import Flask, request, jsonify, render_template
from flasgger import Swagger
import random

app = Flask(__name__, template_folder="templates")
swagger = Swagger(app)

# Mock disorder list (replace with model predictions later)
classes = [
    "Acne", "Basal cell carcinoma", "Benign Keratosis-like Lesions (BKL)",
    "Atopic dermatitis(Eczema)", "Actinic keratosis(AK)",
    "Melanoma", "Psoriasis", "Tinea(Ringworm)"
]

# Mock treatments (replace with JSON lookup later)
treatment_dict = {
    "Acne": ["Use medicated face wash", "Consult dermatologist"],
    "Eczema": ["Moisturize skin", "Avoid irritants"]
}

@app.route('/')
def home():
    """
    Home page endpoint
    ---
    responses:
      200:
        description: Homepage HTML
    """
    return render_template("index.html")  # You can add a simple HTML file in /templates

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict skin disorder from uploaded image
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Image file (.png, .jpg, .jpeg)
    responses:
      200:
        description: Prediction result with treatments
        examples:
          application/json: {
            "prediction": "Acne",
            "probability": 0.87,
            "treatments": ["Use medicated face wash", "Consult dermatologist"]
          }
      400:
        description: Error message
    """
    if 'file' not in request.files:
        return jsonify({"error": "Only image files are allowed"}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400

    # Mock prediction
    pred_class = random.choice(classes)
    prob = round(random.uniform(0.6, 0.95), 2)
    treatments = treatment_dict.get(pred_class, ["Consult dermatologist"])

    return jsonify({
        "prediction": pred_class,
        "probability": prob,
        "treatments": treatments
    })

if __name__ == '__main__':
    app.run(debug=True)