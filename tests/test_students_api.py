import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from app import create_app


class FakeCursor:
    def __init__(self, db):
        self.db = db
        self.result = []
        self.rowcount = 0
        self.lastrowid = None

    def execute(self, query, params=None):
        params = params or tuple()
        if query.strip().startswith("SELECT") and "WHERE id =" in query:
            target_id = params[0]
            self.result = [row for row in self.db.rows if row["id"] == target_id]
            self.rowcount = len(self.result)
        elif query.strip().startswith("SELECT"):
            self.result = list(self.db.rows)
            self.rowcount = len(self.result)
        elif query.strip().startswith("INSERT"):
            next_id = max(row["id"] for row in self.db.rows) + 1 if self.db.rows else 1
            new_row = {
                "id": next_id,
                "name": params[0],
                "email": params[1],
                "major": params[2],
                "gpa": float(params[3]),
            }
            self.db.rows.append(new_row)
            self.lastrowid = next_id
            self.rowcount = 1
            self.result = []
        elif query.strip().startswith("UPDATE"):
            set_clause = query.split("SET ")[1].split(" WHERE")[0]
            fields = [part.split("=")[0].strip() for part in set_clause.split(",")]
            target_id = params[-1]
            target = next((row for row in self.db.rows if row["id"] == target_id), None)
            if not target:
                self.rowcount = 0
                self.result = []
                return
            for field, value in zip(fields, params[:-1]):
                target[field] = value
            self.rowcount = 1
            self.result = []
        elif query.strip().startswith("DELETE"):
            target_id = params[0]
            before = len(self.db.rows)
            self.db.rows = [row for row in self.db.rows if row["id"] != target_id]
            self.rowcount = 1 if len(self.db.rows) != before else 0
            self.result = []
        else:
            raise ValueError(f"Unhandled query: {query}")

    def fetchall(self):
        return list(self.result)

    def fetchone(self):
        return self.result[0] if self.result else None

    def close(self):
        return None


class FakeConnection:
    def __init__(self, rows):
        self.rows = rows
        self.closed = False

    def cursor(self, dictionary=True):
        return FakeCursor(self)

    def commit(self):
        return None

    def rollback(self):
        return None

    def close(self):
        self.closed = True


@pytest.fixture()
def client():
    seed_rows = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "major": "CS", "gpa": 3.8},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "major": "IT", "gpa": 3.5},
    ]
    db = FakeConnection(seed_rows)
    app = create_app(lambda: db)
    app.config["TESTING"] = True
    return app.test_client()


def test_list_students(client):
    res = client.get("/api/students")
    assert res.status_code == 200
    payload = res.get_json()
    assert "students" in payload
    assert len(payload["students"]) == 2


def test_get_student(client):
    res = client.get("/api/students/1")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["name"] == "Alice"


def test_create_student(client):
    new_student = {
        "name": "Cathy",
        "email": "cathy@example.com",
        "major": "DS",
        "gpa": 3.9,
    }
    res = client.post("/api/students", json=new_student)
    assert res.status_code == 201
    payload = res.get_json()
    assert payload["email"] == new_student["email"]
    # Ensure it is returned by list endpoint
    listing = client.get("/api/students").get_json()
    assert any(s["email"] == new_student["email"] for s in listing["students"])


def test_update_student(client):
    res = client.put("/api/students/2", json={"major": "Networking", "gpa": 3.6})
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["major"] == "Networking"
    assert payload["gpa"] == 3.6


def test_delete_student(client):
    res = client.delete("/api/students/1")
    assert res.status_code == 200
    not_found = client.get("/api/students/1")
    assert not_found.status_code == 404


def test_xml_formatting(client):
    res = client.get("/api/students?format=xml")
    assert res.status_code == 200
    assert "application/xml" in res.headers["Content-Type"]
    assert b"<response>" in res.data


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["status"] == "ok"


def test_create_student_missing_field(client):
    # Missing email field
    new_student = {
        "name": "Incomplete",
        "major": "CS",
        "gpa": 3.5,
    }
    res = client.post("/api/students", json=new_student)
    assert res.status_code == 400
    payload = res.get_json()
    assert "error" in payload


def test_create_student_invalid_gpa(client):
    new_student = {
        "name": "Invalid GPA",
        "email": "invalid@example.com",
        "major": "CS",
        "gpa": "not_a_number",
    }
    res = client.post("/api/students", json=new_student)
    assert res.status_code == 400
    payload = res.get_json()
    assert "gpa must be a number" in payload["error"]


def test_get_nonexistent_student(client):
    res = client.get("/api/students/999")
    assert res.status_code == 404
    payload = res.get_json()
    assert "error" in payload


def test_update_nonexistent_student(client):
    res = client.put("/api/students/999", json={"major": "NewMajor"})
    assert res.status_code == 404
    payload = res.get_json()
    assert "error" in payload


def test_update_no_valid_fields(client):
    res = client.put("/api/students/1", json={"invalid_field": "value"})
    assert res.status_code == 400
    payload = res.get_json()
    assert "No valid fields provided" in payload["error"]


def test_update_invalid_gpa(client):
    res = client.put("/api/students/1", json={"gpa": "invalid"})
    assert res.status_code == 400
    payload = res.get_json()
    assert "gpa must be a number" in payload["error"]


def test_delete_nonexistent_student(client):
    res = client.delete("/api/students/999")
    assert res.status_code == 404
    payload = res.get_json()
    assert "error" in payload


def test_create_returns_location_header(client):
    new_student = {
        "name": "Location Test",
        "email": "location@example.com",
        "major": "CS",
        "gpa": 3.7,
    }
    res = client.post("/api/students", json=new_student)
    assert res.status_code == 201
    assert "Location" in res.headers
    assert "/api/students/" in res.headers["Location"]


def test_json_response_format(client):
    res = client.get("/api/students")
    assert res.status_code == 200
    assert "application/json" in res.headers["Content-Type"]


def test_update_single_field(client):
    res = client.put("/api/students/1", json={"name": "UpdatedAlice"})
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["name"] == "UpdatedAlice"
    assert payload["email"] == "alice@example.com"  # unchanged


def test_update_multiple_fields(client):
    res = client.put(
        "/api/students/2",
        json={"name": "Robert", "major": "Engineering", "gpa": 3.9}
    )
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["name"] == "Robert"
    assert payload["major"] == "Engineering"
    assert payload["gpa"] == 3.9


def test_create_with_decimal_gpa(client):
    new_student = {
        "name": "Decimal Test",
        "email": "decimal@example.com",
        "major": "CS",
        "gpa": 3.14159,
    }
    res = client.post("/api/students", json=new_student)
    assert res.status_code == 201
    payload = res.get_json()
    assert payload["gpa"] == 3.14159


def test_list_empty_after_delete_all(client):
    # Delete both students
    client.delete("/api/students/1")
    client.delete("/api/students/2")
    
    res = client.get("/api/students")
    assert res.status_code == 200
    payload = res.get_json()
    assert len(payload["students"]) == 0

