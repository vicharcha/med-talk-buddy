# Healthcare ChatBot API Documentation

## Overview

This documentation provides detailed information about the Healthcare ChatBot API, which serves as the backend for the healthcare application. The API is built with FastAPI and integrates with Firebase for authentication, data storage, and user management.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require Firebase authentication. Include the Firebase ID token in the Authorization header:

```
Authorization: Bearer <firebase-id-token>
```

To obtain a Firebase ID token, use the Firebase Authentication SDK on the client side.

## Endpoints

### User Management

#### Get Current User Profile

```
GET /users/me
```

**Description:** Retrieves the profile information of the currently authenticated user.

**Authentication:** Required

**Response:** 
```json
{
  "uid": "string",
  "email": "string",
  "email_verified": true,
  "display_name": "string",
  "photo_url": "string",
  "disabled": false
}
```

#### Update User Profile

```
PUT /users/me
```

**Description:** Updates the profile information of the currently authenticated user.

**Authentication:** Required

**Request Body:**
```json
{
  "display_name": "string",
  "photo_url": "string"
}
```

**Response:** Updated user profile information similar to GET /users/me

#### Delete User Account

```
DELETE /users/me
```

**Description:** Permanently deletes the current user account and all associated data.

**Authentication:** Required

**Response:**
```json
{
  "message": "User successfully deleted"
}
```

### Chat Functionality

#### Create Message

```
POST /chat/messages
```

**Description:** Sends a healthcare query and receives an AI-generated response.

**Authentication:** Required

**Request Body:**
```json
{
  "message": "string"
}
```

**Response:**
```json
{
  "user_message": {
    "id": "string",
    "user_id": "string",
    "message": "string",
    "is_bot": false,
    "timestamp": "string (ISO format)"
  },
  "bot_message": {
    "id": "string",
    "user_id": "string",
    "message": "string",
    "is_bot": true,
    "timestamp": "string (ISO format)"
  }
}
```

#### Get Message History

```
GET /chat/messages
```

**Description:** Retrieves the chat history for the current user.

**Authentication:** Required

**Query Parameters:**
- `limit` (integer, optional): Maximum number of messages to return. Default: 20

**Response:** Array of message objects ordered by timestamp.

#### Delete All Messages

```
DELETE /chat/messages
```

**Description:** Deletes all chat messages for the current user.

**Authentication:** Required

**Response:**
```json
{
  "message": "All chat messages deleted successfully"
}
```

#### Get Health Recommendations

```
GET /chat/recommendations
```

**Description:** Retrieves personalized health recommendations based on user data.

**Authentication:** Required

**Response:** Array of recommendation objects.
```json
[
  {
    "id": "string",
    "category": "string",
    "title": "string",
    "description": "string",
    "priority": "string"
  }
]
```

### BMI Calculator

#### Calculate BMI

```
POST /bmi/calculate
```

**Description:** Calculates BMI based on height and weight. If user is authenticated, the record is saved.

**Authentication:** Optional

**Request Body:**
```json
{
  "height_cm": 0,
  "weight_kg": 0,
  "notes": "string (optional)"
}
```

**Response:**
```json
{
  "bmi_value": 0,
  "bmi_category": "string",
  "height_cm": 0,
  "weight_kg": 0,
  "notes": "string",
  "saved": true,
  "record_id": "string (only if saved)"
}
```

#### Get BMI History

```
GET /bmi/history
```

**Description:** Retrieves BMI calculation history for the current user.

**Authentication:** Required

**Query Parameters:**
- `limit` (integer, optional): Maximum number of records to return. Default: 10

**Response:** Array of BMI record objects ordered by date (most recent first).

#### Delete BMI Record

```
DELETE /bmi/record/{record_id}
```

**Description:** Deletes a specific BMI record.

**Authentication:** Required

**Path Parameters:**
- `record_id` (string): The ID of the BMI record to delete

**Response:**
```json
{
  "message": "BMI record deleted successfully"
}
```

### Medical Records

#### Create Medical Record

```
POST /medical/records
```

**Description:** Creates a new medical record for the current user.

**Authentication:** Required

**Request Body:**
```json
{
  "record_type": "string (consultation | lab_result | prescription | vital_signs | medical_history)",
  "notes": "string",
  "provider": "string (optional)",
  "metadata": {} (optional)
}
```

**Response:** The created medical record object.

#### Get Medical Records

```
GET /medical/records
```

**Description:** Retrieves medical records for the current user.

**Authentication:** Required

**Query Parameters:**
- `record_type` (string, optional): Filter by record type
- `limit` (integer, optional): Maximum number of records to return. Default: 20

**Response:** Array of medical record objects.

#### Get Medical Record

```
GET /medical/records/{record_id}
```

**Description:** Retrieves a specific medical record.

**Authentication:** Required

**Path Parameters:**
- `record_id` (string): The ID of the medical record to retrieve

**Response:** The medical record object.

#### Update Medical Record

```
PUT /medical/records/{record_id}
```

**Description:** Updates a specific medical record.

**Authentication:** Required

**Path Parameters:**
- `record_id` (string): The ID of the medical record to update

**Request Body:**
```json
{
  "notes": "string (optional)",
  "provider": "string (optional)",
  "metadata": {} (optional)
}
```

**Response:** The updated medical record object.

#### Delete Medical Record

```
DELETE /medical/records/{record_id}
```

**Description:** Deletes a specific medical record.

**Authentication:** Required

**Path Parameters:**
- `record_id` (string): The ID of the medical record to delete

**Response:**
```json
{
  "message": "Medical record deleted successfully"
}
```

#### Upload Attachment

```
POST /medical/records/{record_id}/attachments
```

**Description:** Uploads an attachment to a medical record.

**Authentication:** Required

**Path Parameters:**
- `record_id` (string): The ID of the medical record to add the attachment to

**Request Body:** Multipart form data with a file field

**Response:**
```json
{
  "message": "Attachment uploaded successfully",
  "attachment_path": "string",
  "filename": "string"
}
```

## Data Models

### User

```json
{
  "uid": "string",
  "email": "string",
  "email_verified": "boolean",
  "display_name": "string (optional)",
  "photo_url": "string (optional)",
  "disabled": "boolean"
}
```

### Chat Message

```json
{
  "id": "string",
  "user_id": "string",
  "message": "string",
  "is_bot": "boolean",
  "timestamp": "string (ISO format)"
}
```

### BMI Record

```json
{
  "id": "string",
  "user_id": "string",
  "height_cm": "number",
  "weight_kg": "number",
  "bmi_value": "number",
  "bmi_category": "string",
  "date": "string (ISO format)",
  "notes": "string (optional)"
}
```

### Medical Record

```json
{
  "id": "string",
  "user_id": "string",
  "record_type": "string",
  "record_date": "string (ISO format)",
  "provider": "string (optional)",
  "notes": "string",
  "attachments": ["string"],
  "metadata": {},
  "created_at": "string (ISO format)",
  "updated_at": "string (ISO format)"
}
```

### Health Recommendation

```json
{
  "id": "string",
  "category": "string",
  "title": "string",
  "description": "string",
  "priority": "string"
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200 OK`: The request was successful
- `201 Created`: A new resource was successfully created
- `400 Bad Request`: The request was invalid or cannot be otherwise served
- `401 Unauthorized`: Authentication is required or has failed
- `403 Forbidden`: The authenticated user doesn't have permission to access the requested resource
- `404 Not Found`: The requested resource doesn't exist
- `500 Internal Server Error`: An error occurred on the server

Error responses include a JSON object with details:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Firebase Integration

The API integrates with Firebase using the Firebase Admin SDK for server-side operations:

- **Authentication**: Verifies Firebase ID tokens for authenticating API requests
- **Firestore**: Stores and retrieves data, including chat messages, BMI records, and medical records
- **Storage**: Handles file uploads for medical record attachments

## Rate Limiting

To prevent abuse, the API implements rate limiting as follows:

- Basic endpoints: 100 requests per minute
- Upload endpoints: 20 requests per minute

Exceeding these limits results in a `429 Too Many Requests` response.

## CORS Configuration

Cross-Origin Resource Sharing is configured to allow requests from:

- `http://localhost:5173` (Vite dev server)
- `http://localhost:5174`
- `http://localhost:3000`
- `https://healthcare-77135.web.app`
- `https://healthcare-77135.firebaseapp.com`

To modify these settings, update the `BACKEND_CORS_ORIGINS` list in the application settings.
