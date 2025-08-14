API Contract – Derma AI

This document defines the agreed contract between the frontend and backend for the Derma AI application.
It will be the single source of truth for all API communication.

------------------------------------------------------------
1. User Authentication
------------------------------------------------------------

1.1 Register User
Feature: Create a new account
HTTP Method: POST
Endpoint Path: /api/auth/register
Description: Creates a new user with email, username, and password.

Request Body (JSON):
{
  "username": "string",
  "email": "string",
  "password": "string"
}

Success Response (201 Created):
{
  "message": "User registered successfully",
  "user_id": "uuid"
}

Error Response (400 Bad Request):
{
  "error": "Email already registered"
}

------------------------------------------------------------
1.2 Login
Feature: Authenticate and retrieve a token
HTTP Method: POST
Endpoint Path: /api/auth/login
Description: Validates credentials and returns a JWT token.

Request Body (JSON):
{
  "email": "string",
  "password": "string"
}

Success Response (200 OK):
{
  "token": "jwt_token_string",
  "user": {
    "id": "uuid",
    "username": "string",
    "email": "string"
  }
}

Error Response (401 Unauthorized):
{
  "error": "Invalid email or password"
}

------------------------------------------------------------
1.3 Logout
Feature: Invalidate the current session
HTTP Method: POST
Endpoint Path: /api/auth/logout
Description: Logs the user out by invalidating the token.

Success Response (200 OK):
{
  "message": "Logged out successfully"
}

------------------------------------------------------------
2. Diagnosis Module
------------------------------------------------------------

2.1 Upload Image for Analysis
Feature: Upload a skin image for AI diagnosis
HTTP Method: POST
Endpoint Path: /api/diagnosis/upload
Description: Accepts an image, runs AI model, and returns results.

Request Body (multipart/form-data):
- image: binary file

Success Response (200 OK):
{
  "diagnosis_id": "uuid",
  "diagnosis_result": "Eczema",
  "confidence": 0.95,
  "image_url": "string",
  "created_at": "2025-08-13T10:15:30Z"
}

Error Response (400 Bad Request):
{
  "error": "Invalid or missing image file"
}

------------------------------------------------------------
2.2 Get Diagnosis History
Feature: View all past diagnosis results
HTTP Method: GET
Endpoint Path: /api/diagnosis/history
Description: Returns list of all diagnosis records for logged-in user.

Success Response (200 OK):
[
  {
    "diagnosis_id": "uuid",
    "diagnosis_result": "Psoriasis",
    "confidence": 0.87,
    "image_url": "string",
    "created_at": "2025-08-12T14:20:00Z"
  }
]

Error Response (401 Unauthorized):
{
  "error": "Authentication required"
}

------------------------------------------------------------
2.3 Get Single Diagnosis Detail
Feature: View details of a specific diagnosis
HTTP Method: GET
Endpoint Path: /api/diagnosis/{diagnosis_id}
Description: Fetches detailed info for a given diagnosis.

Success Response (200 OK):
{
  "diagnosis_id": "uuid",
  "diagnosis_result": "Melanoma",
  "confidence": 0.98,
  "image_url": "string",
  "recommendations": [
    "Consult a dermatologist",
    "Schedule a follow-up test"
  ],
  "created_at": "2025-08-10T09:45:00Z"
}

Error Response (404 Not Found):
{
  "error": "Diagnosis record not found"
}

------------------------------------------------------------
3. User Profile Management
------------------------------------------------------------

3.1 Get Profile
Feature: Retrieve logged-in user's profile
HTTP Method: GET
Endpoint Path: /api/user/profile

Success Response (200 OK):
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "joined_date": "2025-07-25T12:00:00Z"
}

------------------------------------------------------------
3.2 Update Profile
Feature: Update username/email
HTTP Method: PUT
Endpoint Path: /api/user/profile

Request Body (JSON):
{
  "username": "string",
  "email": "string"
}

Success Response (200 OK):
{
  "message": "Profile updated successfully"
}

Error Response (400 Bad Request):
{
  "error": "Invalid email format"
}

------------------------------------------------------------
4. Error Response Standard
------------------------------------------------------------
All error responses will follow this structure:
{
  "error": "Description of the error"
}

------------------------------------------------------------
Notes:
- All authenticated endpoints require Authorization: Bearer <token> header.
- Dates/times are in ISO 8601 UTC format.
- Image URLs are returned as public links to files stored in cloud storage.

