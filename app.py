from contextlib import contextmanager

from dicttoxml import dicttoxml
from flask import Flask, current_app, jsonify, make_response, request
from mysql.connector import Error as MySQLError

from config import Config
from db import get_db_connection


def create_app(get_connection=get_db_connection):
    """Application factory for easier testing."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["GET_DB_CONNECTION"] = get_connection

    @contextmanager
    def db_cursor(commit: bool = False):
        """Yield a DB cursor and close/commit safely."""
        conn = current_app.config["GET_DB_CONNECTION"]()
        cursor = conn.cursor(dictionary=True)
        try:
            yield conn, cursor
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def to_xml(body):
        xml_bytes = dicttoxml(
            body,
            custom_root="response",
            attr_type=False,
            item_func=lambda _: "item",
        )
        return xml_bytes.decode()

    def format_response(payload, status_code=200):
        response_format = (request.args.get("format") or "json").lower()
        if response_format == "xml":
            xml_body = to_xml(payload)
            response = make_response(xml_body, status_code)
            response.headers["Content-Type"] = "application/xml"
            return response

        return make_response(jsonify(payload), status_code)

    def format_error(message, status=400):
        return format_response({"error": message}, status)

    @app.route("/health", methods=["GET"])
    def health():
        return format_response({"status": "ok"})

    @app.route("/api/students", methods=["GET"])
    def list_students():
        try:
            with db_cursor() as (_, cursor):
                cursor.execute(
                    """
                    SELECT id, name, email, major, gpa
                    FROM students
                    ORDER BY id
                    """
                )
                students = cursor.fetchall()
            return format_response({"students": students})
        except MySQLError:
            current_app.logger.exception("Database error while listing students")
            return format_error("Database error", 500)

    @app.route("/api/students/<int:student_id>", methods=["GET"])
    def get_student(student_id: int):
        try:
            with db_cursor() as (_, cursor):
                cursor.execute(
                    """
                    SELECT id, name, email, major, gpa
                    FROM students
                    WHERE id = %s
                    """,
                    (student_id,),
                )
                student = cursor.fetchone()
            if not student:
                return format_error("Student not found", 404)
            return format_response(student)
        except MySQLError:
            current_app.logger.exception("Database error while fetching student")
            return format_error("Database error", 500)

    @app.route("/api/students", methods=["POST"])
    def create_student():
        payload = request.get_json(silent=True) or {}
        required_fields = ["name", "email", "major", "gpa"]
        missing = [field for field in required_fields if not payload.get(field)]
        if missing:
            return format_error(f"Missing required fields: {', '.join(missing)}")

        try:
            gpa_value = float(payload["gpa"])
        except (TypeError, ValueError):
            return format_error("gpa must be a number")

        try:
            with db_cursor(commit=True) as (conn, cursor):
                cursor.execute(
                    """
                    INSERT INTO students (name, email, major, gpa)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        payload["name"],
                        payload["email"],
                        payload["major"],
                        gpa_value,
                    ),
                )
                new_id = cursor.lastrowid
                cursor.execute(
                    """
                    SELECT id, name, email, major, gpa
                    FROM students
                    WHERE id = %s
                    """,
                    (new_id,),
                )
                student = cursor.fetchone()
            response = format_response(student, 201)
            response.headers["Location"] = f"/api/students/{new_id}"
            return response
        except MySQLError as exc:
            current_app.logger.exception("Database error while creating student")
            if getattr(exc, "errno", None) == 1062:
                return format_error("Email already exists", 409)
            return format_error("Database error", 500)

    @app.route("/api/students/<int:student_id>", methods=["PUT"])
    def update_student(student_id: int):
        payload = request.get_json(silent=True) or {}
        allowed_fields = ["name", "email", "major", "gpa"]
        updates = {k: v for k, v in payload.items() if k in allowed_fields}

        if "gpa" in updates:
            try:
                updates["gpa"] = float(updates["gpa"])
            except (TypeError, ValueError):
                return format_error("gpa must be a number")

        if not updates:
            return format_error("No valid fields provided for update")

        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
        values = list(updates.values())
        values.append(student_id)

        try:
            with db_cursor(commit=True) as (conn, cursor):
                cursor.execute(
                    """
                    SELECT id FROM students WHERE id = %s
                    """,
                    (student_id,),
                )
                existing = cursor.fetchone()
                if not existing:
                    return format_error("Student not found", 404)

                cursor.execute(
                    f"""
                    UPDATE students
                    SET {set_clause}
                    WHERE id = %s
                    """,
                    values,
                )

                cursor.execute(
                    """
                    SELECT id, name, email, major, gpa
                    FROM students
                    WHERE id = %s
                    """,
                    (student_id,),
                )
                student = cursor.fetchone()
            return format_response(student)
        except MySQLError as exc:
            current_app.logger.exception("Database error while updating student")
            if getattr(exc, "errno", None) == 1062:
                return format_error("Email already exists", 409)
            return format_error("Database error", 500)

    @app.route("/api/students/<int:student_id>", methods=["DELETE"])
    def delete_student(student_id: int):
        try:
            with db_cursor(commit=True) as (conn, cursor):
                cursor.execute(
                    """
                    DELETE FROM students
                    WHERE id = %s
                    """,
                    (student_id,),
                )
                if cursor.rowcount == 0:
                    return format_error("Student not found", 404)
            return format_response({"message": "Student deleted"})
        except MySQLError:
            current_app.logger.exception("Database error while deleting student")
            return format_error("Database error", 500)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)


