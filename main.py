from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from dicttoxml import dicttoxml
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import re
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
jwt = JWTManager(app)

DEMO_USER = {"username": "admin", "password": "admin"}
    
# ============ AUTHENTICATION ============

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if username == DEMO_USER["username"] and password == DEMO_USER["password"]:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad credentials"}), 401


# ============ HELPER FUNCTIONS ============

def to_format(data, fmt):
    """Convert response to specified format (JSON or XML)."""
    if fmt and fmt.lower() == 'xml':
        xml = dicttoxml(data, custom_root='response', attr_type=False)
        response = make_response(xml)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        response = make_response(jsonify(data))
        response.headers['Content-Type'] = 'application/json'
        return response

def validate_int(val):
    """Validate if value can be converted to integer."""
    try:
        return int(val)
    except:
        return None

def fetchone(query, args=()):
    """Execute query and return single row."""
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    rv = cur.fetchone()
    cur.close()
    return rv

def fetchall(query, args=()):
    """Execute query and return all rows."""
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv

def validate_product_payload(payload, partial=False):
    """Validate product data."""
    errors = []
    if not partial:
        if "product_name" not in payload:
            errors.append("product_name is required")
        if "category" not in payload:
            errors.append("category is required")
        if "unit" not in payload:
            errors.append("unit is required")
    if "product_name" in payload and (not isinstance(payload["product_name"], str) or not payload["product_name"].strip()):
        errors.append("product_name must be a non-empty string")
    if "category" in payload and (not isinstance(payload["category"], str) or not payload["category"].strip()):
        errors.append("category must be a non-empty string")
    if "unit" in payload and (not isinstance(payload["unit"], str) or not payload["unit"].strip()):
        errors.append("unit must be a non-empty string")
    if "price" in payload:
        try:
            float(payload["price"])
        except (TypeError, ValueError):
            errors.append("price must be a number")
    if "quantity" in payload:
        if validate_int(payload["quantity"]) is None:
            errors.append("quantity must be an integer")
    return errors

def validate_supplier_payload(payload, partial=False):
    """Validate supplier data."""
    errors = []
    if not partial:
        if "supplier_name" not in payload:
            errors.append("supplier_name is required")
        if "contact_number" not in payload:
            errors.append("contact_number is required")
        if "address" not in payload:
            errors.append("address is required")
    if "supplier_name" in payload and (not isinstance(payload["supplier_name"], str) or not payload["supplier_name"].strip()):
        errors.append("supplier_name must be a non-empty string")
    if "contact_number" in payload and (not isinstance(payload["contact_number"], str) or not payload["contact_number"].strip()):
        errors.append("contact_number must be a non-empty string")
    if "address" in payload and (not isinstance(payload["address"], str) or not payload["address"].strip()):
        errors.append("address must be a non-empty string")
    return errors

def validate_icecream_payload(payload, partial=False):
    """Validate ice cream data."""
    errors = []
    if not partial:
        if "flavor" not in payload:
            errors.append("flavor is required")
        if "size" not in payload:
            errors.append("size is required")
        if "price" not in payload:
            errors.append("price is required")
    if "flavor" in payload and (not isinstance(payload["flavor"], str) or not payload["flavor"].strip()):
        errors.append("flavor must be a non-empty string")
    if "size" in payload and (not isinstance(payload["size"], str) or not payload["size"].strip()):
        errors.append("size must be a non-empty string")
    if "price" in payload:
        try:
            float(payload["price"])
        except (TypeError, ValueError):
            errors.append("price must be a number")
    if "stock" in payload:
        if validate_int(payload["stock"]) is None:
            errors.append("stock must be an integer")
    return errors

def validate_student_payload(payload, partial=False):
    """Validate student data."""
    errors = []
    if not partial:
        if "student_name" not in payload:
            errors.append("student_name is required")
        if "email" not in payload:
            errors.append("email is required")
    if "student_name" in payload and (not isinstance(payload["student_name"], str) or not payload["student_name"].strip()):
        errors.append("student_name must be a non-empty string")
    if "email" in payload and (not isinstance(payload["email"], str) or not payload["email"].strip()):
        errors.append("email must be a non-empty string")
    if "major" in payload and (not isinstance(payload["major"], str) or not payload["major"].strip()):
        errors.append("major must be a non-empty string")
    if "gpa" in payload:
        try:
            float(payload["gpa"])
        except (TypeError, ValueError):
            errors.append("gpa must be a number")
    return errors


# ============ PAGE ROUTES ============

@app.route('/')
def home():
    """Home route — return JSON overview."""
    return jsonify({
        "service": "sari-sari_store",
        "status": "ok",
        "endpoints": {
            "products": "/api/products",
            "suppliers": "/api/suppliers",
            "icecream": "/api/icecream",
            "students": "/api/students",
            "login": "/login"
        }
    })


# ============ PRODUCTS API ============

@app.route('/api/products', methods=['GET'])
@jwt_required(optional=True)
def get_products():
    """Get all products."""
    fmt = request.args.get('format')
    q = request.args.get('q')
    if q:
        qlike = f'%{q}%'
        rows = fetchall("SELECT * FROM product WHERE product_name LIKE %s OR category LIKE %s", (qlike, qlike))
    else:
        rows = fetchall('SELECT * FROM product')
    return to_format({'products': rows}, fmt)

@app.route('/api/products/<int:item_id>', methods=['GET'])
@jwt_required(optional=True)
def get_product(item_id):
    """Get single product by ID."""
    fmt = request.args.get('format')
    row = fetchone("SELECT * FROM product WHERE id=%s", (item_id,))
    if not row:
        return jsonify({"msg": "Not Found"}), 404
    return to_format({"product": row}, fmt)

@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    """Create new product."""
    payload = request.get_json() or {}
    errors = validate_product_payload(payload, partial=False)
    if errors:
        return jsonify({"errors": errors}), 400
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO product (product_name, category, unit, price, quantity, description) VALUES (%s,%s,%s,%s,%s,%s)",
        (
            payload.get("product_name"),
            payload.get("category"),
            payload.get("unit"),
            payload.get("price", 0.0),
            payload.get("quantity", 0),
            payload.get("description", ""),
        )
    )
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    return jsonify({"msg": "created", "id": new_id}), 201

@app.route('/api/products/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_product(item_id):
    """Update product."""
    payload = request.get_json() or {}
    if not payload:
        return jsonify({"msg": "No payload"}), 400
    errors = validate_product_payload(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    keys = []
    vals = []
    allowed = ["product_name", "category", "unit", "price", "quantity", "description"]
    for k in allowed:
        if k in payload:
            keys.append(f"{k}=%s")
            vals.append(payload[k])
    if not keys:
        return jsonify({"msg": "Nothing to update"}), 400
    vals.append(item_id)
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE product SET {', '.join(keys)} WHERE id=%s", tuple(vals))
    mysql.connection.commit()
    changed = cur.rowcount
    cur.close()
    if changed == 0:
        return jsonify({"msg":"Not found"}), 404
    return jsonify({"msg":"updated"}), 200

@app.route("/api/products/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_product(item_id):
    """Delete product."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM product WHERE id=%s", (item_id,))
    mysql.connection.commit()
    rc = cur.rowcount
    cur.close()
    if rc == 0:
        return jsonify({"msg": "Not found"}), 404
    return jsonify({"msg": "deleted"}), 200


# ============ SUPPLIERS API ============

@app.route('/api/suppliers', methods=['GET'])
@jwt_required(optional=True)
def get_suppliers():
    """Get all suppliers."""
    fmt = request.args.get('format')
    q = request.args.get('q')
    if q:
        qlike = f'%{q}%'
        rows = fetchall("SELECT * FROM supplier WHERE supplier_name LIKE %s OR address LIKE %s", (qlike, qlike))
    else:
        rows = fetchall('SELECT * FROM supplier')
    return to_format({'suppliers': rows}, fmt)

@app.route('/api/suppliers/<int:item_id>', methods=['GET'])
@jwt_required(optional=True)
def get_supplier(item_id):
    """Get single supplier by ID."""
    fmt = request.args.get('format')
    row = fetchone("SELECT * FROM supplier WHERE supplier_id=%s", (item_id,))
    if not row:
        return jsonify({"msg": "Not Found"}), 404
    return to_format({"supplier": row}, fmt)

@app.route('/api/suppliers', methods=['POST'])
@jwt_required()
def create_supplier():
    """Create new supplier."""
    payload = request.get_json() or {}
    errors = validate_supplier_payload(payload, partial=False)
    if errors:
        return jsonify({"errors": errors}), 400
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO supplier (supplier_name, contact_number, address, contact_person, phone, email) VALUES (%s,%s,%s,%s,%s,%s)",
        (
            payload.get("supplier_name"),
            payload.get("contact_number"),
            payload.get("address"),
            payload.get("contact_person", ""),
            payload.get("phone", ""),
            payload.get("email", ""),
        )
    )
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    return jsonify({"msg": "created", "id": new_id}), 201

@app.route('/api/suppliers/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_supplier(item_id):
    """Update supplier."""
    payload = request.get_json() or {}
    if not payload:
        return jsonify({"msg": "No payload"}), 400
    errors = validate_supplier_payload(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    keys = []
    vals = []
    allowed = ["supplier_name", "contact_number", "address", "contact_person", "phone", "email"]
    for k in allowed:
        if k in payload:
            keys.append(f"{k}=%s")
            vals.append(payload[k])
    if not keys:
        return jsonify({"msg": "Nothing to update"}), 400
    vals.append(item_id)
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE supplier SET {', '.join(keys)} WHERE supplier_id=%s", tuple(vals))
    mysql.connection.commit()
    changed = cur.rowcount
    cur.close()
    if changed == 0:
        return jsonify({"msg":"Not found"}), 404
    return jsonify({"msg":"updated"}), 200

@app.route("/api/suppliers/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_supplier(item_id):
    """Delete supplier."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM supplier WHERE supplier_id=%s", (item_id,))
    mysql.connection.commit()
    rc = cur.rowcount
    cur.close()
    if rc == 0:
        return jsonify({"msg": "Not found"}), 404
    return jsonify({"msg": "deleted"}), 200


# ============ ICE CREAM API ============

@app.route('/api/icecream', methods=['GET'])
@jwt_required(optional=True)
def get_icecreams():
    """Get all ice cream items."""
    fmt = request.args.get('format')
    q = request.args.get('q')
    if q:
        qlike = f'%{q}%'
        rows = fetchall("SELECT * FROM icecream WHERE flavor LIKE %s OR size LIKE %s", (qlike, qlike))
    else:
        rows = fetchall('SELECT * FROM icecream')
    return to_format({'icecreams': rows}, fmt)

@app.route('/api/icecream/<int:item_id>', methods=['GET'])
@jwt_required(optional=True)
def get_icecream(item_id):
    """Get single ice cream item by ID."""
    fmt = request.args.get('format')
    row = fetchone("SELECT * FROM icecream WHERE icecream_id=%s", (item_id,))
    if not row:
        return jsonify({"msg": "Not Found"}), 404
    return to_format({"icecream": row}, fmt)

@app.route('/api/icecream', methods=['POST'])
@jwt_required()
def create_icecream():
    """Create new ice cream item."""
    payload = request.get_json() or {}
    errors = validate_icecream_payload(payload, partial=False)
    if errors:
        return jsonify({"errors": errors}), 400
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO icecream (flavor, size, price, stock, description) VALUES (%s,%s,%s,%s,%s)",
        (
            payload.get("flavor"),
            payload.get("size"),
            payload.get("price"),
            payload.get("stock", 0),
            payload.get("description", ""),
        )
    )
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    return jsonify({"msg": "created", "id": new_id}), 201

@app.route('/api/icecream/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_icecream(item_id):
    """Update ice cream item."""
    payload = request.get_json() or {}
    if not payload:
        return jsonify({"msg": "No payload"}), 400
    errors = validate_icecream_payload(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    keys = []
    vals = []
    allowed = ["flavor", "size", "price", "stock", "description"]
    for k in allowed:
        if k in payload:
            keys.append(f"{k}=%s")
            vals.append(payload[k])
    if not keys:
        return jsonify({"msg": "Nothing to update"}), 400
    vals.append(item_id)
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE icecream SET {', '.join(keys)} WHERE icecream_id=%s", tuple(vals))
    mysql.connection.commit()
    changed = cur.rowcount
    cur.close()
    if changed == 0:
        return jsonify({"msg":"Not found"}), 404
    return jsonify({"msg":"updated"}), 200

@app.route("/api/icecream/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_icecream(item_id):
    """Delete ice cream item."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM icecream WHERE icecream_id=%s", (item_id,))
    mysql.connection.commit()
    rc = cur.rowcount
    cur.close()
    if rc == 0:
        return jsonify({"msg": "Not found"}), 404
    return jsonify({"msg": "deleted"}), 200


# ============ STUDENTS API ============

@app.route('/api/students', methods=['GET'])
@jwt_required(optional=True)
def get_students():
    """Get all students."""
    fmt = request.args.get('format')
    q = request.args.get('q')
    if q:
        qlike = f'%{q}%'
        rows = fetchall("SELECT * FROM students WHERE student_name LIKE %s OR email LIKE %s", (qlike, qlike))
    else:
        rows = fetchall('SELECT * FROM students')
    return to_format({'students': rows}, fmt)


@app.route('/api/students/<int:item_id>', methods=['GET'])
@jwt_required(optional=True)
def get_student(item_id):
    """Get single student by ID."""
    fmt = request.args.get('format')
    row = fetchone("SELECT * FROM students WHERE student_id=%s", (item_id,))
    if not row:
        return jsonify({"msg": "Not Found"}), 404
    return to_format({"student": row}, fmt)


@app.route('/api/students', methods=['POST'])
@jwt_required()
def create_student():
    """Create new student."""
    payload = request.get_json() or {}
    errors = validate_student_payload(payload, partial=False)
    if errors:
        return jsonify({"errors": errors}), 400
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO students (student_name, email, major, gpa, enrollment_date) VALUES (%s,%s,%s,%s,%s)",
        (
            payload.get("student_name"),
            payload.get("email"),
            payload.get("major", ""),
            payload.get("gpa", 0.0),
            payload.get("enrollment_date", None),
        )
    )
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    return jsonify({"msg": "created", "id": new_id}), 201


@app.route('/api/students/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_student(item_id):
    """Update student."""
    payload = request.get_json() or {}
    if not payload:
        return jsonify({"msg": "No payload"}), 400
    errors = validate_student_payload(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    keys = []
    vals = []
    allowed = ["student_name", "email", "major", "gpa", "enrollment_date"]
    for k in allowed:
        if k in payload:
            keys.append(f"{k}=%s")
            vals.append(payload[k])
    if not keys:
        return jsonify({"msg": "Nothing to update"}), 400
    vals.append(item_id)
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE students SET {', '.join(keys)} WHERE student_id=%s", tuple(vals))
    mysql.connection.commit()
    changed = cur.rowcount
    cur.close()
    if changed == 0:
        return jsonify({"msg":"Not found"}), 404
    return jsonify({"msg":"updated"}), 200


@app.route("/api/students/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_student(item_id):
    """Delete student."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE student_id=%s", (item_id,))
    mysql.connection.commit()
    rc = cur.rowcount
    cur.close()
    if rc == 0:
        return jsonify({"msg": "Not found"}), 404
    return jsonify({"msg": "deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
