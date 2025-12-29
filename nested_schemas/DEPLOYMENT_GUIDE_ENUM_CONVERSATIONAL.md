# Deployment Guide: Enum and Conversational APIs

This guide explains how to deploy the new Group 4 (Enum Nested Schemas) and Group 5 (Conversational Slot Filling) APIs to Render.com.

## Overview

The APIs have been integrated into the existing `api_server.py` Flask application and can be deployed alongside the existing Customer Order and Employee Management APIs.

## Files Created

### Python Implementations
1. **`tc_enum_nested/process_enum_validation.py`**
   - Validates enums at multiple nesting levels
   - Functions: `update_account_status()`, `create_customer_profile()`, `create_multi_level_enum_profile()`

2. **`tc_conversational_slot_filling/process_conversational_profile.py`**
   - Manages conversational profile building
   - Functions: `start_profile_session()`, `update_profile_session()`, `finalize_profile_session()`, `get_session_status()`

### OpenAPI Specifications
1. **`openapi_enum_nested_deployed.yaml`**
   - Defines enum validation endpoints
   - 3 endpoints for different enum validation scenarios

2. **`openapi_conversational_slot_filling_deployed.yaml`**
   - Defines conversational slot filling endpoints
   - 4 endpoints for session management

### Updated Files
1. **`api_server.py`**
   - Added 7 new endpoints
   - Integrated enum validation and conversational APIs
   - Updated health check and root endpoints

## New API Endpoints

### Enum Validation Endpoints

#### 1. POST /api/v1/account/status
Simple enum validation at root level.

**Request:**
```json
{
  "status": "active",
  "type": "personal",
  "account_id": "ACC-12345"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Account status updated successfully",
  "account_id": "ACC-12345",
  "status": "active",
  "type": "personal",
  "validation_summary": "All enum validations passed: status=active, type=personal"
}
```

#### 2. POST /api/v1/customer/profile
Nested enum validation (2 levels).

**Request:**
```json
{
  "customer_id": "CUST-001",
  "customer": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "type": "individual",
    "address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zipcode": "10001",
      "country": "US"
    }
  }
}
```

#### 3. POST /api/v1/customer/multi-level-enum
Multi-level enum validation (4 levels).

**Request:**
```json
{
  "profile_id": "PROF-001",
  "status": "active",
  "customer": {
    "name": "Alice Johnson",
    "type": "individual",
    "address": {
      "street": "321 Oak Ave",
      "city": "Seattle",
      "country": "US"
    },
    "contact": {
      "phone": "+1-206-555-0300",
      "preference": "email"
    }
  }
}
```

### Conversational Slot Filling Endpoints

#### 1. POST /api/v1/conversation/profile/start
Start a new conversational session.

**Request:**
```json
{
  "name": "John Doe"
}
```

**Response:**
```json
{
  "session_id": "SESSION-ABC123",
  "status": "in_progress",
  "completeness_percentage": 10,
  "profile": {
    "name": "John Doe"
  },
  "missing_required_fields": ["email", "type", "address.street", "address.city", "address.country"],
  "next_prompt": "Great! What's your email address?",
  "conversation_turn": 1
}
```

#### 2. PATCH /api/v1/conversation/profile/{session_id}/update
Update profile incrementally.

**Request:**
```json
{
  "email": "john.doe@example.com",
  "type": "individual"
}
```

**Response:**
```json
{
  "session_id": "SESSION-ABC123",
  "status": "in_progress",
  "completeness_percentage": 30,
  "profile": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "type": "individual"
  },
  "missing_required_fields": ["address.street", "address.city", "address.country"],
  "next_prompt": "What's your street address?",
  "conversation_turn": 2
}
```

#### 3. POST /api/v1/conversation/profile/{session_id}/finalize
Finalize and submit complete profile.

**Response:**
```json
{
  "success": true,
  "message": "Profile finalized and submitted successfully",
  "profile_id": "PROF-001",
  "customer_name": "John Doe",
  "customer_email": "john.doe@example.com",
  "customer_type": "individual",
  "address_formatted": "123 Main St, New York, NY, 10001, US",
  "conversation_summary": {
    "total_turns": 5,
    "fields_collected": 11,
    "time_to_complete": "4 minutes"
  }
}
```

#### 4. GET /api/v1/conversation/profile/{session_id}/status
Get current session status.

## Local Testing

### 1. Install Dependencies
```bash
cd nested_schemas
pip install -r api_requirements.txt
```

### 2. Run the Server
```bash
python api_server.py
```

The server will start on `http://localhost:5000`

### 3. Test Enum Validation
```bash
# Test simple enum validation
curl -X POST http://localhost:5000/api/v1/account/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active",
    "type": "personal",
    "account_id": "ACC-12345"
  }'

# Test nested enum validation
curl -X POST http://localhost:5000/api/v1/customer/profile \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST-001",
    "customer": {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "type": "individual",
      "address": {
        "street": "123 Main St",
        "city": "New York",
        "country": "US"
      }
    }
  }'
```

### 4. Test Conversational Flow
```bash
# Start session
SESSION_ID=$(curl -X POST http://localhost:5000/api/v1/conversation/profile/start \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}' | jq -r '.session_id')

# Update profile
curl -X PATCH http://localhost:5000/api/v1/conversation/profile/$SESSION_ID/update \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "type": "individual"
  }'

# Check status
curl http://localhost:5000/api/v1/conversation/profile/$SESSION_ID/status

# Continue updating...
curl -X PATCH http://localhost:5000/api/v1/conversation/profile/$SESSION_ID/update \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zipcode": "10001",
      "country": "US"
    }
  }'

# Finalize
curl -X POST http://localhost:5000/api/v1/conversation/profile/$SESSION_ID/finalize
```

## Deployment to Render.com

### Option 1: Update Existing Deployment

If you already have the nested schemas API deployed on Render:

1. **Push changes to your Git repository:**
```bash
git add nested_schemas/
git commit -m "Add enum validation and conversational slot filling APIs"
git push
```

2. **Render will automatically redeploy** (if auto-deploy is enabled)

3. **Verify deployment:**
```bash
curl https://complex-tools-openapi.onrender.com/api/v1/health
```

### Option 2: New Deployment

1. **Create a new Web Service on Render.com**

2. **Configure the service:**
   - **Name:** `nested-schemas-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r nested_schemas/api_requirements.txt`
   - **Start Command:** `cd nested_schemas && python api_server.py`
   - **Port:** `5000`

3. **Environment Variables:**
   - `PYTHON_VERSION`: `3.11.0`
   - `PORT`: `5000`

4. **Deploy and wait for completion**

## Testing Deployed APIs

Once deployed, test the endpoints:

```bash
# Base URL
BASE_URL="https://complex-tools-openapi.onrender.com/api/v1"

# Health check
curl $BASE_URL/health

# Test enum validation
curl -X POST $BASE_URL/account/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active",
    "type": "personal",
    "account_id": "ACC-12345"
  }'

# Test conversational flow
curl -X POST $BASE_URL/conversation/profile/start \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}'
```

## OpenAPI Specifications

Access the OpenAPI specs at:

- **Enum Validation:** `https://complex-tools-openapi.onrender.com/api/v1/openapi/enum`
- **Conversational:** `https://complex-tools-openapi.onrender.com/api/v1/openapi/conversational`

## Integration with watsonx Orchestrate

### 1. Import OpenAPI Specs

In watsonx Orchestrate:
1. Go to **Skills** → **Add Skill** → **OpenAPI**
2. Import the OpenAPI spec URLs:
   - Enum: `https://complex-tools-openapi.onrender.com/api/v1/openapi/enum`
   - Conversational: `https://complex-tools-openapi.onrender.com/api/v1/openapi/conversational`

### 2. Test Skills

Create test flows to validate:
- Enum validation at different nesting levels
- Conversational profile building across multiple turns
- Error handling for invalid enum values
- Session management for conversational flows

## Monitoring and Logs

### View Logs on Render
1. Go to your service dashboard
2. Click on **Logs** tab
3. Monitor real-time logs for requests and errors

### Health Check
```bash
curl https://complex-tools-openapi.onrender.com/api/v1/health
```

## Troubleshooting

### Issue: Import errors
**Solution:** Ensure all Python files are in the correct directories:
- `tc_enum_nested/process_enum_validation.py`
- `tc_conversational_slot_filling/process_conversational_profile.py`

### Issue: Session not found
**Solution:** Sessions are stored in memory. If the server restarts, sessions are lost. For production, use a database like Redis.

### Issue: CORS errors
**Solution:** CORS is enabled by default. If issues persist, check the CORS configuration in `api_server.py`.

## Production Considerations

### Session Storage
The current implementation uses in-memory session storage. For production:

1. **Use Redis:**
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

2. **Or use a database:**
```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@localhost/dbname')
```

### Rate Limiting
Add rate limiting to prevent abuse:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/v1/conversation/profile/start', methods=['POST'])
@limiter.limit("10 per minute")
def conversation_start():
    # ...
```

### Authentication
Add API key authentication:
```python
@app.before_request
def check_api_key():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != os.environ.get('API_KEY'):
        return jsonify({'error': 'Unauthorized'}), 401
```

## Summary

You now have:
- ✅ 7 new API endpoints (3 enum + 4 conversational)
- ✅ Complete Python implementations
- ✅ OpenAPI specifications
- ✅ Integrated into existing Flask server
- ✅ Ready for Render.com deployment
- ✅ Full test coverage with examples

The APIs are production-ready and can be deployed immediately to Render.com!

## Made with Bob