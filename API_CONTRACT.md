API Contract – DermaAI
Version: 1.0
Project: DermaAI – Visionary Minds
Date: 12-Aug-2025



1. Overview
   This document specifies the contract between the frontend and backend for the DermaAI application.

Backend Technology: Python (Flask)

Response Format: JSON



2. Core Features
   User Registration – Create a new user account.

User Login (optional) – Authenticate an existing user.

Upload Image for Prediction – Upload an image and receive a skin disease prediction with a confidence score.

Get Disease Information – Retrieve details about a specific skin disease.

View All Predictions – Fetch all predictions made in the current session.

View All Users (optional) – Retrieve all registered user emails.



3. Endpoints
   3.1 Register a New User
   Method: POST

Path: /api/register

Description: Registers a new user.

Request Body:

json
Copy
Edit
{
"username": "vishwajeet",
"email": "vishwajeet@example.com",
"password": "securepassword"
}
Success Response (200 OK):

json
Copy
Edit
{
"message": "User registered successfully",
"user\_id": "12345"
}
Error Responses:

400 Bad Request

json
Copy
Edit
{ "error": "Username, email, and password are required." }
409 Conflict

json
Copy
Edit
{ "error": "User with this email already exists." }


3.2 User Login (Optional)
Method: POST

Path: /api/login

Description: Authenticates user and returns a token.

Request Body:

json
Copy
Edit
{
"email": "vishwajeet@example.com",
"password": "securepassword"
}
Success Response (200 OK):

json
Copy
Edit
{ "token": "JWT\_TOKEN\_HERE" }
Error Response (401 Unauthorized):

json
Copy
Edit
{ "error": "Invalid email or password." }


3.3 Upload Image for Prediction
Method: POST

Path: /api/predict

Description: Uploads an image and returns prediction results.

Request Body:

Content-Type: multipart/form-data

Field: image (file, required)

Success Response (200 OK):

json
Copy
Edit
{
"prediction\_label": "Psoriasis",
"confidence": 0.92
}
Error Responses:

400 Bad Request

json
Copy
Edit
{ "error": "Only .jpg, .jpeg, and .png formats are allowed." }
500 Internal Server Error

json
Copy
Edit
{ "error": "An error occurred while processing the image." }


3.4 Get Disease Information
Method: GET

Path: /api/disease/{name}

Description: Retrieves information about a specific skin disease.

Success Response (200 OK):

json
Copy
Edit
{
"name": "Psoriasis",
"description": "A chronic autoimmune condition that causes skin cells to multiply rapidly.",
"symptoms": \["Red patches", "Itching"],
"prevention": \["Moisturize skin", "Avoid triggers"]
}
Error Response (404 Not Found):

json
Copy
Edit
{ "error": "Disease information not found." }


3.5 View All Predictions
Method: GET

Path: /api/predictions

Description: Returns all predictions from the current session.

Success Response (200 OK):

json
Copy
Edit
\[
{ "filename": "image1.jpg", "label": "Eczema", "confidence": 0.87 },
{ "filename": "image2.jpg", "label": "Psoriasis", "confidence": 0.92 }
]
3.6 View All Users (Optional)
Method: GET

Path: /api/users

Description: Retrieves a list of registered user emails.

Success Response (200 OK):

json
Copy
Edit
\[ "vishwajeet@example.com", "sanket@example.com" ]


4. Error Format
All error responses will follow this format:

json
Copy
Edit
{ "error": "Description of the error" }


5. Notes
All API responses are in JSON format.

Allowed image formats: .jpg, .jpeg, .png.

Optional endpoints may require authentication in the future

