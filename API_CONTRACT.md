API Contract
This document defines the contract between the frontend and backend for the Skin Disorder Detection API.
It describes all available endpoints, their inputs, and outputs. This is the single source of truth for API communication.

1. Home Page Endpoint
Feature: Display the homepage.
HTTP Method: GET
Endpoint Path: /
Description: Returns the main HTML page for the web application.

Request Body: None

Success Response (200 OK):

html
Copy
Edit
<!DOCTYPE html>
<html>
  <!-- HTML content of index.html -->
</html>
Error Response(s):
None

2. Prediction Endpoint
Feature: Predict skin disorder from an uploaded image.
HTTP Method: POST
Endpoint Path: /predict
Description: Accepts an image file, checks if it contains skin, runs it through the ML model, and returns the predicted skin disorder with probability and treatment suggestions.

Request Body:

Content Type: multipart/form-data

Fields:

file (file, required) — Image file of the suspected skin disorder (.png, .jpg, .jpeg).

Example Request (cURL):


curl -X POST "http://localhost:5000/predict" \
  -F "file=@acne.jpg"
Success Response (200 OK):

{
  "prediction": "Acne",
  "probability": 0.87,
  "treatments": [
    "Use medicated face wash",
    "Consult dermatologist"
  ]
}
Error Response(s):

400 Bad Request — Invalid File Type


{"error": "Only image files are allowed"}
400 Bad Request — No Skin Detected


{"error": "Image does not contain skin"}
400 Bad Request — Low Confidence


{"error": "Inconclusive result. Please consult a healthcare professional."}
Data Models
Prediction Response Model
Field	                    Type	                                   Description
prediction    	          string	                                   Name of the predicted skin disorder
probability              float	                                      Confidence score (0 to 1)
treatments	             string[]                                   List of suggested treatments

Error Response Model

Field	           Type	              Description
error	           string	              Error message



