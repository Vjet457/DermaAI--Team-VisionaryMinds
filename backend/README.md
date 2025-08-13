# 🖥️ DermaAI Backend

This is the backend API for **DermaAI**, a skin disorder detection application.  
It is built using **Flask** and provides endpoints for predicting skin disorders and managing related data.

---

## 📂 Project Structure

/backend  
│── app.py                  # Main Flask application  
│── requirements.txt        # Python dependencies  
 




## 🚀 Running the Backend Locally

 1. Clone the Repository




  2. Install Dependencies

pip install -r requirements.txt


  3. Start the Server

python app.py


You should see something like:

Running on http://127.0.0.1:5000/




## 📄 API Documentation (Swagger UI)

Once the server is running, you can view the interactive API documentation at:  
**http://127.0.0.1:5000/apidocs/**



## 📌 Endpoints Overview

- `GET /` → Home endpoint  
- `POST /predict` → Upload an image and get a skin disorder prediction  

---

## 🛠 Tech Stack
- **Flask** (Python Web Framework)  
- **Flasgger** (Swagger UI integration)  
- **Keras/TensorFlow** (Machine Learning model handling)  

---

## 👨‍💻 Author
**Team Visionary Minds**