"""
Flask API Server for Employee Registration
===========================================

This server exposes the employee registration tool as a REST API for deployment to Render.
It implements the registerEmployee endpoint with circular Person schema references.

Usage:
    python api_server.py

The server will start on the port specified by the PORT environment variable (default: 5000)

Endpoints:
    POST /api/v1/employees/register - Register new employee with manager information
    GET /api/v1/health - Health check
    GET /api/v1/openapi - Get OpenAPI specification
"""

from register_employee import register_employee
import os
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yaml

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the registration function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Health check endpoint


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Employee Registration API',
        'version': '1.0.0',
        'endpoints': {
            'register': '/api/v1/employees/register',
            'health': '/api/v1/health',
            'openapi': '/api/v1/openapi'
        }
    })

# Employee registration endpoint


@app.route('/api/v1/employees/register', methods=['POST'])
def register_employee_endpoint():
    """Register new employee with manager information"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'error': 'Invalid request',
                'code': 'INVALID_JSON',
                'details': 'Request body must be valid JSON'
            }), 400

        # Process the registration
        result = register_employee(data)

        # Check if there was an error
        if result.get('status') == 'error':
            status_code = 400
            if result.get('code') == 'DUPLICATE_EMPLOYEE':
                status_code = 409
            return jsonify(result), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e)
        }), 500

# OpenAPI specification endpoint


@app.route('/api/v1/openapi', methods=['GET'])
def get_openapi_spec():
    """Get OpenAPI specification"""
    try:
        openapi_path = os.path.join(os.path.dirname(
            __file__), 'openapi_add_employee_with_manager.yaml')

        if not os.path.exists(openapi_path):
            return jsonify({
                'error': 'OpenAPI specification not found'
            }), 404

        with open(openapi_path, 'r') as f:
            spec = yaml.safe_load(f)

        return jsonify(spec), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to load OpenAPI specification',
            'details': str(e)
        }), 500

# Root endpoint


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'service': 'Employee Registration API',
        'version': '1.0.0',
        'description': 'Register employees with manager information using circular Person schema references',
        'endpoints': {
            'register': {
                'method': 'POST',
                'path': '/api/v1/employees/register',
                'description': 'Register new employee with manager information'
            },
            'health': {
                'method': 'GET',
                'path': '/api/v1/health',
                'description': 'Health check endpoint'
            },
            'openapi': {
                'method': 'GET',
                'path': '/api/v1/openapi',
                'description': 'Get OpenAPI specification'
            }
        },
        'documentation': 'https://github.com/your-repo/employee-registration-api'
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    print(f"Starting Employee Registration API on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Endpoints:")
    print(f"  POST /api/v1/employees/register - Register employee")
    print(f"  GET  /api/v1/health - Health check")
    print(f"  GET  /api/v1/openapi - OpenAPI spec")

    app.run(host='0.0.0.0', port=port, debug=debug)

# Made with Bob
