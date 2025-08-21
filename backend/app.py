from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import numpy as np
import os
from werkzeug.utils import secure_filename
from PIL import Image
import csv
from datetime import datetime

app = Flask(__name__)

# Load trained model
MODEL_PATH = "skin_disease_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Class labels
CLASS_NAMES = ["Acne", "Actinic_Keratosis", "DrugEruption", "Eczema",
               "Moles", "SkinCancer", "Sun_Sunlight_Damage", "Tinea", "Warts"]

# Remedies / info dictionary
REMEDIES = {
    "Acne": "Wash face twice daily, avoid oily food, use dermatologist-prescribed ointments.",
    "Actinic_Keratosis": "Use sun protection, consult dermatologist, may require cryotherapy.",
    "DrugEruption": "Stop suspected drug, consult a doctor immediately.",
    "Eczema": "Moisturize skin regularly, avoid triggers, use prescribed steroid creams.",
    "Moles": "Usually harmless, but monitor for changes and consult dermatologist.",
    "SkinCancer": "Requires urgent medical consultation and possible biopsy.",
    "Sun_Sunlight_Damage": "Use sunscreen, wear protective clothing, avoid peak sunlight.",
    "Tinea": "Apply antifungal cream, keep area dry and clean.",
    "Warts": "Over-the-counter wart treatments, cryotherapy, or consult dermatologist."
}

# Upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# CSV file for logging predictions
LOG_FILE = "predictions_log.csv"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Filename", "Prediction", "Confidence", "Remedy"])


# ===== Routes =====
@app.route("/")
def intro():
    """Introduction page with logo and button"""
    return render_template("intro.html")


@app.route("/home")
def home():
    """Home page with image upload form"""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Handle image upload and prediction"""
    if "file" not in request.files:
        return redirect(url_for("error"))

    file = request.files["file"]

    if file.filename == "":
        return redirect(url_for("error"))

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Preprocess image
        img = Image.open(filepath).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        # Prediction
        predictions = model.predict(img_array)
        predicted_class = CLASS_NAMES[np.argmax(predictions)]
        confidence = np.max(predictions) * 100
        remedy = REMEDIES[predicted_class]

        # Log prediction to CSV
        with open(LOG_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             filename, predicted_class, f"{confidence:.2f}%", remedy])

        return render_template(
            "results.html",
            image_file=filepath,
            prediction=predicted_class,
            confidence=f"{confidence:.2f}%",
            treatments=[remedy]
        )

    except Exception as e:
        print("Error:", e)
        return redirect(url_for("error"))


@app.route("/error")
def error():
    """Error page"""
    return render_template("error.html")


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
