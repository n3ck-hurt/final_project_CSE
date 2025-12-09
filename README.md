Flask Students API

This project is a REST API built with Flask and MySQL for managing student records. It provides features for creating, reading, updating, and deleting students in the database.

Setup Instructions

Clone the repository:
git clone <your-repo-url>
cd final_project_CSE

Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate

Install the required packages:
pip install -r requirements.txt

(Optional) Configure your MySQL connection by creating a .env file with the following content:
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=cse_final_project
DB_PORT=3306

Start the development server:
flask --app app run --debug
The server will run at: http://localhost:5000

API Endpoints

GET /health – Verifies that the server is operational

GET /api/students – Retrieves all students

GET /api/students/<id> – Retrieves a single student by ID

POST /api/students – Creates a new student (expects JSON with name, email, major, gpa)

PUT /api/students/<id> – Updates an existing student

DELETE /api/students/<id> – Deletes a student

To receive XML output instead of JSON, append ?format=xml to the request URL.

Testing

To run the tests, ensure the virtual environment is active, then execute:
python -m pytest tests/test_students_api.py -v

The tests use a mock in-memory database and do not require a real MySQL instance.

Notes
