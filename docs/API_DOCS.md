# API Documentation

The Medical Chatbot provides a RESTful API for chat interaction and system health monitoring.

## 1. Chat Interface
**Endpoint**: `/`
- **Method**: `GET`
- **Description**: Returns the HTML chat interface.

## 2. Get Response
**Endpoint**: `/get`
- **Method**: `POST`
- **Payload**:
  - `msg`: (string) The user's query.
- **Response**: (string) The LLM's response.

## 3. Health Check
**Endpoint**: `/health`
- **Method**: `GET`
- **Description**: Returns the operational status of the service.
- **Response**: `{"status": "healthy"}`

## 4. Environment Variables
The API requires the following environment variables:
- `OPENAI_API_KEY`: For LLM access.
- `PINECONE_API_KEY`: For vector database access.
- `PORT`: (Optional) Defaults to 8080.
