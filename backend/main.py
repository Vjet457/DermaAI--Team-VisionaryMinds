from keras.models import load_model
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import json
from PIL import Image
import cv2
from flasgger import Swagger, swag_from

# Creating the app
app = Flask(__name__)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)

# Loading the model
model = load_model("skin_disorder_classifier_EfficientNetB2.h5")

# Loading the json file with the skin disorders
def get_treatment(path):
    with open(path) as f:
        return json.load(f)
treatment_dict = get_treatment("skin_disorder.json")

# function to check if the file is an allowed image type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

# function to detect skin color
def is_skin(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    skin_pixels = np.sum(mask > 0)
    skin_percent = skin_pixels / (img.shape[0] * img.shape[1]) * 100
    return skin_percent > 5

@app.route('/')
def home():
    """
    Home page endpoint
    ---
    responses:
      200:
        description: Home page HTML
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@swag_from({
    'tags': ['Prediction'],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Image file of the skin disorder'
        }
    ],
    'responses': {
        200: {
            'description': 'Prediction result with probability and treatments',
            'examples': {
                'application/json': {
                    'prediction': 'Acne',
                    'probability': 0.87,
                    'treatments': ['Use medicated face wash', 'Consult dermatologist']
                }
            }
        },
        400: {'description': 'Invalid file or processing error'}
    }
})
def predict():
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Only image files are allowed"}), 400

    image = Image.open(file)
    if not is_skin(np.array(image)):
        return jsonify({"error": "Image does not contain skin"}), 400

    img = image.resize((300, 300))
    img_array = img_to_array(img) / 255.0
    image_exp = np.expand_dims(img_array, axis=0)

    pred = model.predict(image_exp)
    class_idx = np.argmax(pred)

    classes = ["Acne", "Basal cell carcinoma", "Benign Keratosis-like Lesions (BKL)", "Atopic dermatitis(Eczema)",
               "Actinic keratosis(AK)", "Melanoma", "Psoriasis", "Tinea(Ringworm)"]

    pred_class = classes[class_idx]
    prob = float(pred[0][class_idx])
    threshold = 0.6

    if prob < threshold:
        return jsonify({"error": "Inconclusive result. Please consult a healthcare professional."}), 400

    treatments = treatment_dict.get(pred_class, [])
    return jsonify({"prediction": pred_class, "probability": prob, "treatments": treatments})

if __name__ == '__main__':
    app.run(debug=True)
