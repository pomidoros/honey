Mock API Documentation
This document describes a mock API built with FastAPI that serves image metadata based on a description query. The API returns 3 images with their local paths and descriptions, filtered by an optional description parameter.
Table of Contents

Overview
Project Structure
Prerequisites
Setup and Installation
Running the Application
API Endpoints
Testing the API
Troubleshooting

Overview
The API is designed to handle GET requests to /get with an optional description query parameter. It returns a JSON array of up to 3 image objects, each containing an id, path (local file path), and description. Images are stored locally in the images/ directory, and their metadata is defined in images.json.
Project Structure
project/
├── images/                 # Directory containing image files (e.g., image1.jpg)
├── docs/                   # Documentation files
│   ├── api_documentation.md
├── images.json             # Metadata for images (id, path, description)
├── main.py                 # FastAPI application code
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration

Prerequisites

Docker: Install Docker and Docker Compose (Docker Installation Guide).
Images: Place at least 5 image files (e.g., image1.jpg, image2.jpg, etc.) in the images/ directory. Supported formats include JPG, PNG, etc.
Python 3.7+ (optional): Only required if running without Docker.

Setup and Installation

Clone the project (if applicable) or create the project structure as shown above.
Prepare images:
Place image files in the images/ directory.
Ensure images.json references these files correctly. Example:{
  "images": [
    {
      "id": 1,
      "path": "images/image1.jpg",
      "description": "A beautiful sunset over the mountains"
    },
    ...
  ]
}




Verify files:
Ensure all image files listed in images.json exist in the images/ directory.
Check that main.py, requirements.txt, Dockerfile, and docker-compose.yml are present.



Running the Application
Using Docker

Build and run the container:
docker-compose up --build

This command builds the Docker image and starts the FastAPI server on http://localhost:8000.

Stop the application:Press Ctrl+C or run:
docker-compose down



Without Docker (Optional)

Install dependencies:pip install -r requirements.txt


Run the server:uvicorn main:app --host 0.0.0.0 --port 8000 --reload



API Endpoints
GET /get

Description: Retrieves up to 3 image objects, optionally filtered by a description.
Query Parameter:
description (optional, string): Filters images whose descriptions contain the provided string (case-insensitive).


Response:
Success (200): JSON array of up to 3 image objects.[
  {
    "id": 1,
    "path": "images/image1.jpg",
    "description": "A beautiful sunset over the mountains"
  },
  ...
]


Error (404): If no images match the description.{
  "detail": "No images found matching the description"
}


Error (500): If an image file is missing.{
  "detail": "Image file images/imageX.jpg not found"
}




Example Requests:
All images (random 3):GET http://localhost:8000/get


Filter by "mountain":GET http://localhost:8000/get?description=mountain





Testing the API
Use tools like curl, Postman, or a browser to test the API:

Example with curl:curl http://localhost:8000/get
curl http://localhost:8000/get?description=mountain


Swagger UI: Access http://localhost:8000/docs for an interactive API interface.

Troubleshooting

Image file not found: Ensure all files listed in images.json exist in images/.
Port conflict: If port 8000 is in use, change the port in docker-compose.yml (e.g., ports: ["8080:8000"]) and restart.
Docker issues: Verify Docker is running and you have permissions (sudo may be required).
No images returned: Check that images.json is valid JSON and contains entries.

For further assistance, contact the project maintainer or refer to the FastAPI documentation (https://fastapi.tiangolo.com).
