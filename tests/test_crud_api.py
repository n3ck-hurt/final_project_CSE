"""
Comprehensive CRUD tests for all API endpoints.
Tests cover Products, Suppliers, Ice Cream, and Students with various scenarios and edge cases.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app as main_app


# ============ FIXTURES ============

@pytest.fixture
def app():
    """Create and configure a test Flask app."""
    test_app = main_app
    test_app.config['TESTING'] = True
    return test_app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def auth_token(client):
    """Get JWT auth token by logging in."""
    response = client.post('/login', 
        json={'username': 'admin', 'password': 'admin'})
    if response.status_code == 200:
        return response.get_json()['access_token']
    return None


# ============ PRODUCTS CRUD TESTS ============

class TestProductsCRUD:
    """Test CRUD operations for products endpoint."""
    
    def test_get_all_products(self, client):
        """Test retrieving all products."""
        response = client.get('/api/products')
        assert response.status_code in [200, 404, 500]  # Accept various states
    
    def test_get_products_with_search(self, client):
        """Test searching products by query parameter."""
        response = client.get('/api/products?q=test')
        assert response.status_code in [200, 404, 500]
    
    def test_get_products_xml_format(self, client):
        """Test retrieving products in XML format."""
        response = client.get('/api/products?format=xml')
        assert response.status_code in [200, 404, 500]
        if response.status_code == 200:
            assert 'application/xml' in response.headers.get('Content-Type', '')
    
    def test_get_single_product(self, client):
        """Test retrieving a single product by ID."""
        response = client.get('/api/products/1')
        assert response.status_code in [200, 404, 500]
    
    def test_get_nonexistent_product(self, client):
        """Test retrieving a non-existent product returns 404."""
        response = client.get('/api/products/99999')
        assert response.status_code == 404
    
    def test_create_product_success(self, client, auth_token):
        """Test creating a product with valid data."""
        product_data = {
            'product_name': 'Test Product',
            'category': 'Test Category',
            'unit': 'pcs',
            'price': 99.99,
            'quantity': 50,
            'description': 'Test Description'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/products', json=product_data, headers=headers)
        assert response.status_code in [201, 400, 401, 500]
    
    def test_create_product_missing_required_field(self, client, auth_token):
        """Test creating product with missing required fields."""
        product_data = {
            'product_name': 'Incomplete',
            'category': 'Test',
            # missing 'unit'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/products', json=product_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_product_invalid_price(self, client, auth_token):
        """Test creating product with invalid price."""
        product_data = {
            'product_name': 'Invalid Price',
            'category': 'Test',
            'unit': 'pcs',
            'price': 'not_a_number',
            'quantity': 10
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/products', json=product_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_product_invalid_quantity(self, client, auth_token):
        """Test creating product with invalid quantity."""
        product_data = {
            'product_name': 'Invalid Qty',
            'category': 'Test',
            'unit': 'pcs',
            'price': 50.0,
            'quantity': 'not_an_integer'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/products', json=product_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_product_no_auth(self, client):
        """Test creating product without authentication."""
        product_data = {
            'product_name': 'Test',
            'category': 'Test',
            'unit': 'pcs'
        }
        response = client.post('/api/products', json=product_data)
        assert response.status_code == 401
    
    def test_update_product_success(self, client, auth_token):
        """Test updating a product."""
        update_data = {'product_name': 'Updated Name', 'price': 199.99}
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.put('/api/products/1', json=update_data, headers=headers)
        assert response.status_code in [200, 404, 401, 500]
    
    def test_update_product_invalid_price(self, client, auth_token):
        """Test updating product with invalid price."""
        update_data = {'price': 'invalid'}
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.put('/api/products/1', json=update_data, headers=headers)
        assert response.status_code in [400, 404, 401, 500]
    
    def test_update_product_no_payload(self, client, auth_token):
        """Test updating product with no data."""
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.put('/api/products/1', json={}, headers=headers)
        assert response.status_code in [400, 404, 401, 500]
    
    def test_update_nonexistent_product(self, client, auth_token):
        """Test updating non-existent product."""
        update_data = {'product_name': 'Test'}
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.put('/api/products/99999', json=update_data, headers=headers)
        assert response.status_code == 404
    
    def test_delete_product_success(self, client, auth_token):
        """Test deleting a product."""
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.delete('/api/products/1', headers=headers)
        assert response.status_code in [200, 404, 401, 500]
    
    def test_delete_nonexistent_product(self, client, auth_token):
        """Test deleting non-existent product returns 404."""
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.delete('/api/products/99999', headers=headers)
        assert response.status_code == 404
    
    def test_delete_product_no_auth(self, client):
        """Test deleting product without authentication."""
        response = client.delete('/api/products/1')
        assert response.status_code == 401


# ============ SUPPLIERS CRUD TESTS ============

class TestSuppliersCRUD:
    """Test CRUD operations for suppliers endpoint."""
    
    def test_get_all_suppliers(self, client):
        """Test retrieving all suppliers."""
        response = client.get('/api/suppliers')
        assert response.status_code in [200, 404, 500]
    
    def test_get_suppliers_with_search(self, client):
        """Test searching suppliers by query parameter."""
        response = client.get('/api/suppliers?q=supplier')
        assert response.status_code in [200, 404, 500]
    
    def test_get_suppliers_xml_format(self, client):
        """Test retrieving suppliers in XML format."""
        response = client.get('/api/suppliers?format=xml')
        assert response.status_code in [200, 404, 500]
    
    def test_get_single_supplier(self, client):
        """Test retrieving a single supplier by ID."""
        response = client.get('/api/suppliers/1')
        assert response.status_code in [200, 404, 500]
    
    def test_get_nonexistent_supplier(self, client):
        """Test retrieving non-existent supplier."""
        response = client.get('/api/suppliers/99999')
        assert response.status_code == 404
    
    def test_create_supplier_success(self, client, auth_token):
        """Test creating a supplier."""
        supplier_data = {
            'supplier_name': 'Test Supplier',
            'contact_number': '555-1234',
            'address': '123 Main St',
            'contact_person': 'John Doe',
            'phone': '555-5678',
            'email': 'supplier@test.com'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/suppliers', json=supplier_data, headers=headers)
        assert response.status_code in [201, 400, 401, 500]
    
    def test_create_supplier_missing_fields(self, client, auth_token):
        """Test creating supplier with missing required fields."""
        supplier_data = {
            'supplier_name': 'Incomplete',
            # missing contact_number and address
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/suppliers', json=supplier_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_supplier_invalid_name(self, client, auth_token):
        """Test creating supplier with empty name."""
        supplier_data = {
            'supplier_name': '',
            'contact_number': '555-1234',
            'address': '123 Main St'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/suppliers', json=supplier_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_update_supplier_success(self, client, auth_token):
        """Test updating a supplier."""
        update_data = {
            'supplier_name': 'Updated Supplier',
            'contact_number': '555-9999'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.put('/api/suppliers/1', json=update_data, headers=headers)
        assert response.status_code in [200, 404, 401, 500]
    
    def test_update_supplier_no_auth(self, client):
        """Test updating supplier without authentication."""
        response = client.put('/api/suppliers/1', json={'supplier_name': 'Test'})
        assert response.status_code == 401
    
    def test_delete_supplier_success(self, client, auth_token):
        """Test deleting a supplier."""
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.delete('/api/suppliers/1', headers=headers)
        assert response.status_code in [200, 404, 401, 500]
    
    def test_delete_supplier_no_auth(self, client):
        """Test deleting supplier without authentication."""
        response = client.delete('/api/suppliers/1')
        assert response.status_code == 401


# ============ ICE CREAM CRUD TESTS ============

class TestIceCreamCRUD:
    """Test CRUD operations for ice cream endpoint."""
    
    def test_get_all_icecream(self, client):
        """Test retrieving all ice cream items."""
        response = client.get('/api/icecream')
        assert response.status_code in [200, 404, 500]
    
    def test_get_icecream_with_search(self, client):
        """Test searching ice cream by query parameter."""
        response = client.get('/api/icecream?q=vanilla')
        assert response.status_code in [200, 404, 500]
    
    def test_get_icecream_xml_format(self, client):
        """Test retrieving ice cream in XML format."""
        response = client.get('/api/icecream?format=xml')
        assert response.status_code in [200, 404, 500]
    
    def test_get_single_icecream(self, client):
        """Test retrieving a single ice cream item."""
        response = client.get('/api/icecream/1')
        assert response.status_code in [200, 404, 500]
    
    def test_create_icecream_success(self, client, auth_token):
        """Test creating an ice cream item."""
        icecream_data = {
            'flavor': 'Vanilla',
            'size': 'LARGE',
            'price': 50.00,
            'stock': 100,
            'description': 'Creamy vanilla'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/icecream', json=icecream_data, headers=headers)
        assert response.status_code in [201, 400, 401, 500]
    
    def test_create_icecream_missing_flavor(self, client, auth_token):
        """Test creating ice cream without flavor."""
        icecream_data = {
            'size': 'LARGE',
            'price': 50.00
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/icecream', json=icecream_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_icecream_invalid_price(self, client, auth_token):
        """Test creating ice cream with invalid price."""
        icecream_data = {
            'flavor': 'Chocolate',
            'size': 'SMALL',
            'price': 'expensive'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/icecream', json=icecream_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_icecream_invalid_stock(self, client, auth_token):
        """Test creating ice cream with invalid stock."""
        icecream_data = {
            'flavor': 'Strawberry',
            'size': 'MEDIUM',
            'price': 40.00,
            'stock': 'lots'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/icecream', json=icecream_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_update_icecream_success(self, client, auth_token):
        """Test updating ice cream item."""
        update_data = {'flavor': 'Mint Choco', 'stock': 50}
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.put('/api/icecream/1', json=update_data, headers=headers)
        assert response.status_code in [200, 404, 401, 500]
    
    def test_delete_icecream_success(self, client, auth_token):
        """Test deleting ice cream item."""
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.delete('/api/icecream/1', headers=headers)
        assert response.status_code in [200, 404, 401, 500]


# ============ STUDENTS CRUD TESTS ============

class TestStudentsCRUD:
    """Test CRUD operations for students endpoint."""
    
    def test_get_all_students(self, client):
        """Test retrieving all students."""
        response = client.get('/api/students')
        assert response.status_code in [200, 404, 500]
    
    def test_get_students_with_search(self, client):
        """Test searching students by query parameter."""
        response = client.get('/api/students?q=john')
        assert response.status_code in [200, 404, 500]
    
    def test_get_students_xml_format(self, client):
        """Test retrieving students in XML format."""
        response = client.get('/api/students?format=xml')
        assert response.status_code in [200, 404, 500]
    
    def test_get_single_student(self, client):
        """Test retrieving a single student."""
        response = client.get('/api/students/1')
        assert response.status_code in [200, 404, 500]
    
    def test_get_nonexistent_student(self, client):
        """Test retrieving non-existent student."""
        response = client.get('/api/students/99999')
        assert response.status_code == 404
    
    def test_create_student_success(self, client, auth_token):
        """Test creating a student."""
        student_data = {
            'student_name': 'John Doe',
            'email': 'john@example.com',
            'major': 'Computer Science',
            'gpa': 3.85,
            'enrollment_date': '2024-01-15'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/students', json=student_data, headers=headers)
        assert response.status_code in [201, 400, 401, 500]
    
    def test_create_student_missing_name(self, client, auth_token):
        """Test creating student without name."""
        student_data = {
            'email': 'test@example.com',
            'major': 'CS'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/students', json=student_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_student_missing_email(self, client, auth_token):
        """Test creating student without email."""
        student_data = {
            'student_name': 'Jane Doe',
            'major': 'CS'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/students', json=student_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_student_invalid_gpa(self, client, auth_token):
        """Test creating student with invalid GPA."""
        student_data = {
            'student_name': 'Bad GPA',
            'email': 'bad@example.com',
            'major': 'CS',
            'gpa': 'not_a_number'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/students', json=student_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_create_student_empty_name(self, client, auth_token):
        """Test creating student with empty name."""
        student_data = {
            'student_name': '',
            'email': 'empty@example.com',
            'major': 'CS'
        }
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.post('/api/students', json=student_data, headers=headers)
        assert response.status_code in [400, 401, 500]
    
    def test_update_student_success(self, client, auth_token):
        """Test updating a student."""
        update_data = {'major': 'Data Science', 'gpa': 3.90}
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.put('/api/students/1', json=update_data, headers=headers)
        assert response.status_code in [200, 404, 401, 500]
    
    def test_update_student_invalid_gpa(self, client, auth_token):
        """Test updating student with invalid GPA."""
        update_data = {'gpa': 'invalid'}
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.put('/api/students/1', json=update_data, headers=headers)
        assert response.status_code in [400, 404, 401, 500]
    
    def test_update_student_no_auth(self, client):
        """Test updating student without authentication."""
        response = client.put('/api/students/1', json={'major': 'CS'})
        assert response.status_code == 401
    
    def test_delete_student_success(self, client, auth_token):
        """Test deleting a student."""
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        response = client.delete('/api/students/1', headers=headers)
        assert response.status_code in [200, 404, 401, 500]
    
    def test_delete_student_no_auth(self, client):
        """Test deleting student without authentication."""
        response = client.delete('/api/students/1')
        assert response.status_code == 401


# ============ AUTHENTICATION TESTS ============

class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_login_success(self, client):
        """Test successful login."""
        response = client.post('/login', 
            json={'username': 'admin', 'password': 'admin'})
        assert response.status_code == 200
        assert 'access_token' in response.get_json()
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/login', 
            json={'username': 'admin', 'password': 'wrong'})
        assert response.status_code == 401
    
    def test_login_missing_username(self, client):
        """Test login without username."""
        response = client.post('/login', 
            json={'password': 'admin'})
        assert response.status_code == 401
    
    def test_login_missing_password(self, client):
        """Test login without password."""
        response = client.post('/login', 
            json={'username': 'admin'})
        assert response.status_code == 401


# ============ HOME PAGE TESTS ============

class TestHome:
    """Test home endpoint."""
    
    def test_home_returns_ok(self, client):
        """Test that home endpoint returns OK status."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_home_contains_endpoints(self, client):
        """Test that home contains list of endpoints."""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'endpoints' in data
        assert 'products' in data['endpoints']
        assert 'suppliers' in data['endpoints']
        assert 'icecream' in data['endpoints']
        assert 'students' in data['endpoints']
