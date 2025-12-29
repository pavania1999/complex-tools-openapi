# Group 4 & 5: Enum Validation and Conversational Slot Filling APIs

## Overview

This implementation provides complete, deployable REST APIs for testing:
- **Group 4:** Enum validation in nested schemas (multi-level)
- **Group 5:** Conversational multi-field slot filling (incremental data collection)

## 📁 Project Structure

```
nested_schemas/
├── api_server.py                                      # Main Flask server (UPDATED)
├── api_requirements.txt                               # Python dependencies
│
├── tc_enum_nested/                                    # Group 4: Enum Validation
│   └── process_enum_validation.py                     # Enum validation logic
│
├── tc_conversational_slot_filling/                    # Group 5: Conversational
│   └── process_conversational_profile.py              # Session management logic
│
├── openapi_enum_nested_deployed.yaml                  # OpenAPI spec for enum APIs
├── openapi_conversational_slot_filling_deployed.yaml  # OpenAPI spec for conversational APIs
│
├── DEPLOYMENT_GUIDE_ENUM_CONVERSATIONAL.md            # Deployment instructions
├── ENUM_AND_CONVERSATIONAL_APIS_README.md             # API documentation
└── README_ENUM_CONVERSATIONAL.md                      # This file
```

## ✅ What's Been Created

### 1. Python Implementations

#### Enum Validation (`tc_enum_nested/process_enum_validation.py`)
- ✅ Simple enum validation (root level)
- ✅ Nested enum validation (2 levels)
- ✅ Multi-level enum validation (4 levels)
- ✅ Comprehensive error reporting
- ✅ Field path tracking for validation failures

**Functions:**
- `update_account_status()` - Validates status and type enums
- `create_customer_profile()` - Validates customer.type and address.country
- `create_multi_level_enum_profile()` - Validates enums at 4 nesting levels

#### Conversational Slot Filling (`tc_conversational_slot_filling/process_conversational_profile.py`)
- ✅ Session management with unique IDs
- ✅ Incremental data collection
- ✅ Completeness tracking (percentage)
- ✅ Smart field merging (no overwrites)
- ✅ Contextual prompts
- ✅ Missing field detection

**Functions:**
- `start_profile_session()` - Initialize new session
- `update_profile_session()` - Add/update fields incrementally
- `finalize_profile_session()` - Submit complete profile
- `get_session_status()` - Check current state

### 2. REST API Endpoints

#### Enum Validation Endpoints (3)
```
POST   /api/v1/account/status              # Simple enum validation
POST   /api/v1/customer/profile            # Nested enum validation
POST   /api/v1/customer/multi-level-enum   # Multi-level enum validation
```

#### Conversational Endpoints (4)
```
POST   /api/v1/conversation/profile/start                 # Start session
PATCH  /api/v1/conversation/profile/{id}/update           # Update profile
POST   /api/v1/conversation/profile/{id}/finalize         # Finalize profile
GET    /api/v1/conversation/profile/{id}/status           # Get status
```

#### OpenAPI Spec Endpoints (2)
```
GET    /api/v1/openapi/enum                # Enum validation spec
GET    /api/v1/openapi/conversational      # Conversational spec
```

### 3. OpenAPI Specifications

Both specs are production-ready with:
- ✅ Complete request/response schemas
- ✅ Multiple examples per endpoint
- ✅ Error response definitions
- ✅ Detailed descriptions
- ✅ Render.com server URLs

### 4. Documentation

- ✅ Deployment guide with step-by-step instructions
- ✅ API usage examples with curl commands
- ✅ Test scenarios for all endpoints
- ✅ Integration guide for watsonx Orchestrate

## 🚀 Quick Start

### Local Testing

1. **Install dependencies:**
```bash
cd nested_schemas
pip install flask flask-cors pyyaml
```

2. **Run the server:**
```bash
python3 api_server.py
```

3. **Test enum validation:**
```bash
curl -X POST http://localhost:5000/api/v1/account/status \
  -H "Content-Type: application/json" \
  -d '{"status": "active", "type": "personal", "account_id": "ACC-001"}'
```

4. **Test conversational flow:**
```bash
# Start
curl -X POST http://localhost:5000/api/v1/conversation/profile/start \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}'

# Update (use session_id from response)
curl -X PATCH http://localhost:5000/api/v1/conversation/profile/SESSION-XXX/update \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "type": "individual"}'
```

## 🌐 Deployment

### Deploy to Render.com

1. **Push to Git:**
```bash
git add nested_schemas/
git commit -m "Add enum and conversational APIs"
git push
```

2. **Render auto-deploys** (if enabled)

3. **Access at:**
```
https://complex-tools-openapi.onrender.com/api/v1/
```

See [`DEPLOYMENT_GUIDE_ENUM_CONVERSATIONAL.md`](./DEPLOYMENT_GUIDE_ENUM_CONVERSATIONAL.md) for detailed instructions.

## 📊 Test Results

### Enum Validation Tests
```
✅ Test 1: Simple Enum Validation - PASSED
   - Validates status: active/inactive
   - Validates type: personal/business
   
✅ Test 2: Nested Enum Validation - PASSED
   - Validates customer.type: individual/corporate
   - Validates address.country: US/CA/UK
   
✅ Test 3: Multi-Level Enum Validation - PASSED
   - Level 0: status (root)
   - Level 1: customer.type
   - Level 2: address.country
   - Level 3: contact.preference
   
✅ Test 4: Invalid Enum Value - PASSED
   - Correctly rejects invalid values
   - Returns detailed error with allowed values
```

### Conversational Flow Tests
```
✅ Turn 1: Start Session - PASSED
   - Creates session with unique ID
   - Tracks 10% completeness
   - Provides contextual prompt
   
✅ Turn 2: Add Email & Type - PASSED
   - Merges new fields
   - Updates to 30% completeness
   - Suggests next field
   
✅ Turn 3: Partial Address - PASSED
   - Adds nested fields incrementally
   - Reaches 50% completeness
   - Identifies missing country
   
✅ Turn 4: Complete Address - PASSED
   - Completes required fields
   - Achieves 80% completeness
   - Status changes to "complete"
   
✅ Turn 5: Add Contact - PASSED
   - Adds optional fields
   - Reaches 100% completeness
   - Ready for finalization
   
✅ Turn 6: Finalize - PASSED
   - Validates completeness
   - Generates profile ID
   - Returns conversation summary
```

## 🎯 Key Features

### Enum Validation
- ✅ Multi-level nesting support (0-3 levels)
- ✅ Detailed validation reports
- ✅ Field path tracking
- ✅ Comprehensive error messages
- ✅ Allowed values in errors

### Conversational Slot Filling
- ✅ Session-based state management
- ✅ Incremental data collection
- ✅ Smart field merging
- ✅ Completeness tracking
- ✅ Contextual prompts
- ✅ Required vs optional field distinction
- ✅ Conversation analytics

## 📝 API Examples

### Enum Validation Example

**Request:**
```json
POST /api/v1/customer/multi-level-enum
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
      "preference": "email"
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile created with all enum validations passed",
  "enum_validation_report": {
    "level_0_status": "status=active (valid)",
    "level_1_customer_type": "customer_type=individual (valid)",
    "level_2_address_country": "address_country=US (valid)",
    "level_3_contact_preference": "contact_preference=email (valid)",
    "total_enum_fields": 4,
    "all_valid": true
  }
}
```

### Conversational Flow Example

**Turn 1 - Start:**
```json
POST /api/v1/conversation/profile/start
{"name": "John Doe"}

Response:
{
  "session_id": "SESSION-ABC123",
  "completeness_percentage": 10,
  "missing_required_fields": ["email", "type", "address.street", "address.city", "address.country"],
  "next_prompt": "Great! What's your email address?"
}
```

**Turn 2 - Update:**
```json
PATCH /api/v1/conversation/profile/SESSION-ABC123/update
{"email": "john@example.com", "type": "individual"}

Response:
{
  "completeness_percentage": 30,
  "missing_required_fields": ["address.street", "address.city", "address.country"],
  "next_prompt": "What's your street address?"
}
```

## 🔗 Integration with watsonx Orchestrate

1. **Import OpenAPI specs:**
   - Enum: `https://your-domain.onrender.com/api/v1/openapi/enum`
   - Conversational: `https://your-domain.onrender.com/api/v1/openapi/conversational`

2. **Create skills** from imported specs

3. **Test flows** with provided examples

## 📚 Documentation Files

- [`DEPLOYMENT_GUIDE_ENUM_CONVERSATIONAL.md`](./DEPLOYMENT_GUIDE_ENUM_CONVERSATIONAL.md) - Complete deployment guide
- [`ENUM_AND_CONVERSATIONAL_APIS_README.md`](./ENUM_AND_CONVERSATIONAL_APIS_README.md) - Detailed API documentation
- [`openapi_enum_nested_deployed.yaml`](./openapi_enum_nested_deployed.yaml) - Enum validation OpenAPI spec
- [`openapi_conversational_slot_filling_deployed.yaml`](./openapi_conversational_slot_filling_deployed.yaml) - Conversational OpenAPI spec

## 🎉 Summary

You now have:
- ✅ 2 complete Python implementations
- ✅ 7 REST API endpoints
- ✅ 2 OpenAPI specifications
- ✅ Full integration with existing Flask server
- ✅ Comprehensive test coverage
- ✅ Production-ready deployment
- ✅ Complete documentation

**Ready to deploy to Render.com and test with watsonx Orchestrate!**

## Made with Bob 🤖