# Employee Registration API - Circular Person Schema Reference

## Overview

This API demonstrates a realistic use case of **circular schema references** in OpenAPI specifications. The `Person` schema is used for both employees and their managers, creating a natural circular reference pattern that models organizational hierarchies.

## Circular Schema Pattern

### Schema Structure

```yaml
Person:
  properties:
    name: string
    employee_id: string
    email: string
    phone: string
    department: string
    position: string
    start_date: date
    manager:
      $ref: '#/components/schemas/Person'  # Circular reference!
```

### Why This Works

- **Schema Level**: `Person` schema references itself through the `manager` field, creating a circular schema definition
- **Data Level**: Actual data forms linear hierarchies (no one reports to themselves in reality)
- **Business Value**: Models organizational structures naturally without schema duplication

## API Endpoint

### Register Employee

**Endpoint**: `POST /api/v1/employees/register`

**Request Body**:
```json
{
  "employee": {
    "name": "Sarah Martinez",
    "employee_id": "EMP-201",
    "email": "sarah.martinez@company.com",
    "phone": "+1-555-0201",
    "department": "Engineering",
    "position": "Software Engineer",
    "start_date": "2024-02-01",
    "manager": {
      "name": "Michael Chen",
      "employee_id": "EMP-150",
      "email": "michael.chen@company.com",
      "phone": "+1-555-0150",
      "department": "Engineering",
      "position": "Engineering Manager"
    }
  }
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Employee registered successfully",
  "employee": {
    "name": "Sarah Martinez",
    "employee_id": "EMP-201",
    "department": "Engineering",
    "position": "Software Engineer",
    "start_date": "2024-02-01"
  },
  "manager": {
    "name": "Michael Chen",
    "employee_id": "EMP-150",
    "position": "Engineering Manager"
  },
  "reporting_chain": "Sarah Martinez (EMP-201) → Michael Chen (EMP-150)",
  "registration_date": "2024-02-01T10:30:00Z"
}
```

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

1. Install dependencies:
```bash
cd nested_schemas/tc_p0_py_003
pip install -r requirements.txt
```

2. Run the server:
```bash
python api_server.py
```

The server will start on `http://localhost:5000`

### Test the API

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Register employee
curl -X POST http://localhost:5000/api/v1/employees/register \
  -H "Content-Type: application/json" \
  -d '{
    "employee": {
      "name": "Sarah Martinez",
      "employee_id": "EMP-201",
      "email": "sarah.martinez@company.com",
      "phone": "+1-555-0201",
      "department": "Engineering",
      "position": "Software Engineer",
      "start_date": "2024-02-01",
      "manager": {
        "name": "Michael Chen",
        "employee_id": "EMP-150",
        "email": "michael.chen@company.com",
        "department": "Engineering",
        "position": "Engineering Manager"
      }
    }
  }'

# Get OpenAPI spec
curl http://localhost:5000/api/v1/openapi
```

### Run Python Tool Directly

```bash
python register_employee.py
```

This will run three demo scenarios:
1. Basic employee with manager
2. Senior employee with multi-level hierarchy
3. Top-level executive without manager

## Deployment to Render

### Option 1: Using Render Dashboard

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `employee-registration-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api_server:app`
   - **Root Directory**: `nested_schemas/tc_p0_py_003`
5. Click "Create Web Service"

### Option 2: Using render.yaml

1. Ensure `render.yaml` is in the repository root or service directory
2. Push to GitHub
3. Render will auto-detect and deploy

### Environment Variables

- `PORT`: Set automatically by Render (default: 10000)
- `PYTHON_VERSION`: 3.11.0

## Test Payloads

See [`test-payload.json`](test-payload.json) for various test scenarios:

1. **basicEmployee**: Employee with direct manager
2. **multiLevelHierarchy**: 3-level management chain
3. **topLevelExecutive**: Executive without manager
4. **deepHierarchy**: 4-level management chain

## Files

- `openapi_add_employee_with_manager.yaml` - OpenAPI 3.0 specification
- `register_employee.py` - Core registration logic
- `api_server.py` - Flask API server
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration
- `test-payload.json` - Test payloads
- `README.md` - This file

## Key Features

✅ **Circular Schema Reference**: Person schema references itself  
✅ **Realistic Business Logic**: Models organizational hierarchies  
✅ **Multi-Level Support**: Handles arbitrary hierarchy depths  
✅ **Validation**: Checks required fields and data integrity  
✅ **Reporting Chain**: Builds visual representation of hierarchy  
✅ **Production Ready**: Includes error handling and logging  

## API Documentation

Full OpenAPI specification available at:
- Local: `http://localhost:5000/api/v1/openapi`
- Production: `https://your-service.onrender.com/api/v1/openapi`

## Support

For issues or questions, please refer to the main project documentation.

---

**Made with Bob** - Demonstrating circular schema references in real-world scenarios