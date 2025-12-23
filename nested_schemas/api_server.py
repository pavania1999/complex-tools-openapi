"""
Flask API Server for Nested Schema Testing
===========================================

This server exposes the Python tools as REST APIs for testing with watsonx Orchestrate.
It implements both TC-P0-PY-001 (Customer Order Processing) and TC-P0-PY-003 (Employee Management).

Usage:
    python api_server.py

The server will start on http://localhost:5000

Endpoints:
    POST /api/v1/orders/process - Process customer orders
    POST /api/v1/employees/process - Process employee data
    GET /api/v1/health - Health check
    GET /api/v1/openapi/orders - Get OpenAPI spec for orders
    GET /api/v1/openapi/employees - Get OpenAPI spec for employees
"""

from tc_p0_py_003.process_complex_data import process_employee_data
from tc_p0_py_001.process_customer_order import process_customer_order
import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml

# Add tool directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tc_p0_py_001'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tc_p0_py_003'))

# Import the tool functions

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Health check endpoint


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Nested Schema Testing API',
        'version': '1.0.0',
        'endpoints': {
            'orders': '/api/v1/orders/process',
            'employees': '/api/v1/employees/process',
            'openapi_orders': '/api/v1/openapi/orders',
            'openapi_employees': '/api/v1/openapi/employees'
        }
    }), 200


# Customer Order Processing endpoint (TC-P0-PY-001)
@app.route('/api/v1/orders/process', methods=['POST'])
def process_order():
    """
    Process customer order with nested data

    Request Body:
        {
            "customer": {...},
            "order": {...}
        }

    Returns:
        Order confirmation with formatted details
    """
    try:
        # Get request data
        order_data = request.get_json()

        if not order_data:
            return jsonify({
                'error': 'Invalid request',
                'code': 'INVALID_REQUEST',
                'details': 'Request body must be valid JSON'
            }), 400

        # Process the order
        result = process_customer_order(order_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


# Employee Management endpoint (TC-P0-PY-003)
@app.route('/api/v1/employees/process', methods=['POST'])
def process_employee():
    """
    Process employee data with complex nested structures

    Request Body:
        {
            "employee": {...}  // For employee data
            OR
            "person": {...}    // For circular reference testing
        }

    Returns:
        Employee profile or relationship analysis
    """
    try:
        # Get request data
        employee_data = request.get_json()

        if not employee_data:
            return jsonify({
                'error': 'Invalid request',
                'code': 'INVALID_REQUEST',
                'details': 'Request body must be valid JSON'
            }), 400

        # Process the employee data
        result = process_employee_data(employee_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


# OpenAPI spec endpoints
@app.route('/api/v1/openapi/orders', methods=['GET'])
def get_orders_openapi():
    """Get OpenAPI specification for orders endpoint"""
    try:
        spec_path = os.path.join(
            os.path.dirname(__file__),
            'tc_p0_py_001',
            'openapi_customer_order.yaml'
        )

        with open(spec_path, 'r') as f:
            spec = yaml.safe_load(f)

        # Update server URL to current host
        spec['servers'] = [
            {
                'url': f'{request.scheme}://{request.host}/api/v1',
                'description': 'Current server'
            }
        ]

        return jsonify(spec), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to load OpenAPI spec',
            'details': str(e)
        }), 500


@app.route('/api/v1/openapi/employees', methods=['GET'])
def get_employees_openapi():
    """Get OpenAPI specification for employees endpoint"""
    try:
        spec_path = os.path.join(
            os.path.dirname(__file__),
            'tc_p0_py_003',
            'openapi_employee_management.yaml'
        )

        with open(spec_path, 'r') as f:
            spec = yaml.safe_load(f)

        # Update server URL to current host
        spec['servers'] = [
            {
                'url': f'{request.scheme}://{request.host}/api/v1',
                'description': 'Current server'
            }
        ]

        return jsonify(spec), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to load OpenAPI spec',
            'details': str(e)
        }), 500


# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'service': 'Nested Schema Testing API',
        'version': '1.0.0',
        'description': 'REST API for testing nested schema support in watsonx Orchestrate',
        'test_cases': {
            'TC-P0-PY-001': 'Customer Order Processing (Standard Nesting)',
            'TC-P0-PY-003': 'Employee Management (Complex Scenarios)'
        },
        'endpoints': {
            'health': '/api/v1/health',
            'orders': '/api/v1/orders/process',
            'employees': '/api/v1/employees/process',
            'openapi_orders': '/api/v1/openapi/orders',
            'openapi_employees': '/api/v1/openapi/employees'
        },
        'documentation': {
            'orders_spec': f'{request.url_root}api/v1/openapi/orders',
            'employees_spec': f'{request.url_root}api/v1/openapi/employees'
        }
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'code': 'NOT_FOUND',
        'details': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method not allowed',
        'code': 'METHOD_NOT_ALLOWED',
        'details': 'The HTTP method is not allowed for this endpoint'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'code': 'INTERNAL_ERROR',
        'details': str(error)
    }), 500


if __name__ == '__main__':
    print("="*70)
    print("Nested Schema Testing API Server")
    print("="*70)
    print("\nStarting server on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /                              - API information")
    print("  GET  /api/v1/health                 - Health check")
    print("  POST /api/v1/orders/process         - Process customer orders")
    print("  POST /api/v1/employees/process      - Process employee data")
    print("  GET  /api/v1/openapi/orders         - Orders OpenAPI spec")
    print("  GET  /api/v1/openapi/employees      - Employees OpenAPI spec")
    print("\nTest Cases:")
    print("  TC-P0-PY-001: Customer Order Processing")
    print("  TC-P0-PY-003: Employee Management")
    print("\nPress Ctrl+C to stop the server")
    print("="*70)

    app.run(host='0.0.0.0', port=5000, debug=True)
