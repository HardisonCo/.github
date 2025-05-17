# API Reference

Complete reference documentation for the HMS API.

## API Overview

The HMS API is organized into the following categories:

1. Authentication
2. User Management
3. Health Records
4. Analytics
5. Administration

## Authentication

### Login

```text


POST /api/auth/login



```text

Request body:
```json


{
  "username": "user@example.com",
  "password": "your-password"
}


```text

Response:
```json


{
  "token": "jwt-token-here",
  "refreshToken": "refresh-token-here",
  "expiresIn": 3600
}


```text

### Refresh Token

```text


POST /api/auth/refresh



```text

Request body:
```json


{
  "refreshToken": "refresh-token-here"
}


```text

Response:
```json


{
  "token": "new-jwt-token-here",
  "refreshToken": "new-refresh-token-here",
  "expiresIn": 3600
}


```text

## User Management

### Get User Profile

```text


GET /api/users/profile



```text

Headers:
```text


Authorization: Bearer jwt-token-here



```text

Response:
```json


{
  "id": "user-id",
  "username": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "roles": ["admin", "analyst"]
}


```text

### Update User Profile

```text


PUT /api/users/profile



```text

Headers:
```text


Authorization: Bearer jwt-token-here



```text

Request body:
```json


{
  "firstName": "John",
  "lastName": "Smith",
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}


```text

Response:
```json


{
  "id": "user-id",
  "username": "user@example.com",
  "firstName": "John",
  "lastName": "Smith",
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}


```text

## Health Records

### Get Patient Records

```text


GET /api/patients/:patientId/records



```text

Headers:
```text


Authorization: Bearer jwt-token-here



```text

Response:
```json


{
  "patientId": "patient-id",
  "records": [
    {
      "id": "record-id-1",
      "date": "2023-01-15T10:30:00Z",
      "type": "examination",
      "provider": "Dr. Jane Smith",
      "notes": "Patient reports improvement in symptoms..."
    },
    {
      "id": "record-id-2",
      "date": "2023-02-10T14:45:00Z",
      "type": "lab-result",
      "test": "Complete Blood Count",
      "results": {
        "wbc": 7.2,
        "rbc": 4.8,
        "platelets": 250
      }
    }
  ]
}


```text

## Error Handling

All API endpoints follow a standard error response format:

```json


{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional error details if available
    }
  }
}


```text

Common error codes:

- `AUTHENTICATION_REQUIRED`: User is not authenticated
- `INVALID_CREDENTIALS`: Username or password is incorrect
- `PERMISSION_DENIED`: User does not have permission to access the resource
- `RESOURCE_NOT_FOUND`: The requested resource does not exist
- `VALIDATION_ERROR`: The request data failed validation
```text

