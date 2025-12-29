"""
Flask API Server for Nested Schema Testing
===========================================

This server exposes the Python tools as REST APIs for testing with watsonx Orchestrate.
It implements:
- TC-P0-PY-001 (Customer Order Processing)
- TC-P0-PY-003 (Employee Management)
- Enum Nested Schemas (Group 4)
- Conversational Slot Filling (Group 5)

Usage:
    python api_server.py

The server will start on http://localhost:5000

Endpoints:
    POST /api/v1/orders/process - Process customer orders
    POST /api/v1/employees/process - Process employee data
    POST /api/v1/account/status - Update account status (enum validation)
    POST /api/v1/customer/profile - Create customer profile (nested enums)
    POST /api/v1/customer/multi-level-enum - Multi-level enum validation
    POST /api/v1/conversation/profile/start - Start conversational session
    PATCH /api/v1/conversation/profile/<session_id>/update - Update profile
    POST /api/v1/conversation/profile/<session_id>/finalize - Finalize profile
    GET /api/v1/conversation/profile/<session_id>/status - Get session status
    GET /api/v1/health - Health check
    GET /api/v1/openapi/* - Get OpenAPI specs
"""

from tc_p0_py_003.process_complex_data import process_employee_data
from tc_p0_py_001.process_customer_order import process_customer_order
from tc_enum_nested.process_enum_validation import (
    update_account_status,
    create_customer_profile,
    create_multi_level_enum_profile
)
from tc_conversational_slot_filling.process_conversational_profile import (
    start_profile_session,
    update_profile_session,
    finalize_profile_session,
    get_session_status
)
import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml

# Add tool directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tc_p0_py_001'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tc_p0_py_003'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tc_enum_nested'))
sys.path.insert(0, os.path.join(os.path.dirname(
    __file__), 'tc_conversational_slot_filling'))

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
            'account_status': '/api/v1/account/status',
            'customer_profile': '/api/v1/customer/profile',
            'multi_level_enum': '/api/v1/customer/multi-level-enum',
            'conversation_start': '/api/v1/conversation/profile/start',
            'conversation_update': '/api/v1/conversation/profile/<session_id>/update',
            'conversation_finalize': '/api/v1/conversation/profile/<session_id>/finalize',
            'conversation_status': '/api/v1/conversation/profile/<session_id>/status',
            'openapi_orders': '/api/v1/openapi/orders',
            'openapi_employees': '/api/v1/openapi/employees',
            'openapi_enum': '/api/v1/openapi/enum',
            'openapi_conversational': '/api/v1/openapi/conversational'
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


# Enum Nested Schemas endpoints
@app.route('/api/v1/account/status', methods=['POST'])
def account_status():
    """Update account status with simple enum validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'code': 'INVALID_REQUEST',
                'details': 'Request body must be valid JSON'
            }), 400

        result = update_account_status(data)
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


@app.route('/api/v1/customer/profile', methods=['POST'])
def customer_profile():
    """Create customer profile with nested enum validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'code': 'INVALID_REQUEST',
                'details': 'Request body must be valid JSON'
            }), 400

        result = create_customer_profile(data)
        status_code = 201 if result.get('success') else 400
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


@app.route('/api/v1/customer/multi-level-enum', methods=['POST'])
def multi_level_enum():
    """Create profile with multi-level enum validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'code': 'INVALID_REQUEST',
                'details': 'Request body must be valid JSON'
            }), 400

        result = create_multi_level_enum_profile(data)
        status_code = 201 if result.get('success') else 400
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


# Conversational Slot Filling endpoints
@app.route('/api/v1/conversation/profile/start', methods=['POST'])
def conversation_start():
    """Start a new conversational profile creation session"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'code': 'INVALID_REQUEST',
                'details': 'Request body must be valid JSON'
            }), 400

        result = start_profile_session(data)
        return jsonify(result), 201

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


@app.route('/api/v1/conversation/profile/<session_id>/update', methods=['PATCH'])
def conversation_update(session_id):
    """Update profile with additional information"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'code': 'INVALID_REQUEST',
                'details': 'Request body must be valid JSON'
            }), 400

        result = update_profile_session(session_id, data)
        if 'error' in result:
            return jsonify(result), 404
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


@app.route('/api/v1/conversation/profile/<session_id>/finalize', methods=['POST'])
def conversation_finalize(session_id):
    """Finalize and submit the complete profile"""
    try:
        result = finalize_profile_session(session_id)
        if 'error' in result:
            status_code = 404 if result['error'] == 'SESSION_NOT_FOUND' else 400
            return jsonify(result), status_code
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


@app.route('/api/v1/conversation/profile/<session_id>/status', methods=['GET'])
def conversation_status(session_id):
    """Get current session status"""
    try:
        result = get_session_status(session_id)
        if 'error' in result:
            return jsonify(result), 404
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500


# OpenAPI spec endpoints for new tools
@app.route('/api/v1/openapi/enum', methods=['GET'])
def get_enum_openapi():
    """Get OpenAPI specification for enum validation endpoints"""
    try:
        spec_path = os.path.join(
            os.path.dirname(__file__),
            'openapi_enum_nested_deployed.yaml'
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


@app.route('/api/v1/openapi/conversational', methods=['GET'])
def get_conversational_openapi():
    """Get OpenAPI specification for conversational slot filling endpoints"""
    try:
        spec_path = os.path.join(
            os.path.dirname(__file__),
            'openapi_conversational_slot_filling_deployed.yaml'
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
            'TC-P0-PY-003': 'Employee Management (Complex Scenarios)',
            'Group 4': 'Enum Nested Schemas (Multi-level enum validation)',
            'Group 5': 'Conversational Slot Filling (Incremental data collection)'
        },
        'endpoints': {
            'health': '/api/v1/health',
            'orders': '/api/v1/orders/process',
            'employees': '/api/v1/employees/process',
            'account_status': '/api/v1/account/status',
            'customer_profile': '/api/v1/customer/profile',
            'multi_level_enum': '/api/v1/customer/multi-level-enum',
            'conversation_start': '/api/v1/conversation/profile/start',
            'conversation_update': '/api/v1/conversation/profile/<session_id>/update',
            'conversation_finalize': '/api/v1/conversation/profile/<session_id>/finalize',
            'conversation_status': '/api/v1/conversation/profile/<session_id>/status',
            'openapi_orders': '/api/v1/openapi/orders',
            'openapi_employees': '/api/v1/openapi/employees',
            'openapi_enum': '/api/v1/openapi/enum',
            'openapi_conversational': '/api/v1/openapi/conversational'
        },
        'documentation': {
            'orders_spec': f'{request.url_root}api/v1/openapi/orders',
            'employees_spec': f'{request.url_root}api/v1/openapi/employees',
            'enum_spec': f'{request.url_root}api/v1/openapi/enum',
            'conversational_spec': f'{request.url_root}api/v1/openapi/conversational'
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
    print("  GET  /                                                  - API information")
    print("  GET  /api/v1/health                                     - Health check")
    print("  POST /api/v1/orders/process                             - Process customer orders")
    print("  POST /api/v1/employees/process                          - Process employee data")
    print("  POST /api/v1/account/status                             - Update account status (enum)")
    print("  POST /api/v1/customer/profile                           - Create customer profile (nested enum)")
    print("  POST /api/v1/customer/multi-level-enum                  - Multi-level enum validation")
    print("  POST /api/v1/conversation/profile/start                 - Start conversational session")
    print("  PATCH /api/v1/conversation/profile/<id>/update          - Update profile")
    print("  POST /api/v1/conversation/profile/<id>/finalize         - Finalize profile")
    print("  GET  /api/v1/conversation/profile/<id>/status           - Get session status")
    print("  GET  /api/v1/openapi/orders                             - Orders OpenAPI spec")
    print("  GET  /api/v1/openapi/employees                          - Employees OpenAPI spec")
    print("  GET  /api/v1/openapi/enum                               - Enum validation OpenAPI spec")
    print("  GET  /api/v1/openapi/conversational                     - Conversational OpenAPI spec")
    print("\nTest Cases:")
    print("  TC-P0-PY-001: Customer Order Processing")
    print("  TC-P0-PY-003: Employee Management")
    print("  Group 4: Enum Nested Schemas")
    print("  Group 5: Conversational Slot Filling")
    print("\nPress Ctrl+C to stop the server")
    print("="*70)

    app.run(host='0.0.0.0', port=5000, debug=True)
