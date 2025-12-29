# Enum and Conversational Slot Filling APIs

This document describes the two new OpenAPI specifications created for testing Group 4 (Enums in Nested Schemas) and Group 5 (Conversational Multi-Field Slot Filling).

## Created Files

### 1. [`openapi_enum_nested_deployed.yaml`](./openapi_enum_nested_deployed.yaml)
**Purpose**: Test enum validation at multiple nesting levels

**Endpoints**:
- `POST /account/status` - Simple enum validation (root level)
- `POST /customer/profile` - Nested enum validation (2 levels)
- `POST /customer/multi-level-enum` - Multi-level enum validation (3+ levels)

**Test Coverage**:
- ✅ Simple enums at root level (status: active/inactive, type: personal/business)
- ✅ Nested enums level 1 (customer.type: individual/corporate)
- ✅ Nested enums level 2 (customer.address.country: US/CA/UK)
- ✅ Nested enums level 3 (customer.contact.preference: email/phone/sms)
- ✅ Combined multi-level enum validation
- ✅ Invalid enum value error handling

### 2. [`openapi_conversational_slot_filling_deployed.yaml`](./openapi_conversational_slot_filling_deployed.yaml)
**Purpose**: Test incremental data collection across multiple conversational turns

**Endpoints**:
- `POST /conversation/profile/start` - Start session with minimal data
- `PATCH /conversation/profile/{session_id}/update` - Incrementally add fields
- `POST /conversation/profile/{session_id}/finalize` - Submit complete profile
- `GET /conversation/profile/{session_id}/status` - Check current status

**Test Coverage**:
- ✅ Multi-turn conversation flow (5+ turns)
- ✅ Partial updates without overwriting existing data
- ✅ Completeness tracking (percentage)
- ✅ Missing field detection (required vs optional)
- ✅ Contextual prompts for next steps
- ✅ Incremental nested structure building

## Deployment

Both files are ready to be deployed to Render.com using the same pattern as existing deployed APIs:

```yaml
servers:
  - url: https://complex-tools-openapi.onrender.com/api/v1
    description: Render.com Production Deployment
```

## Test Scenarios

### Group 4: Enum Nested Schemas

#### Test Case 1: Simple Enum Validation
```bash
curl -X POST https://complex-tools-openapi.onrender.com/api/v1/account/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active",
    "type": "personal",
    "account_id": "ACC-12345"
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Account status updated successfully",
  "validation_summary": "All enum validations passed: status=active, type=personal"
}
```

#### Test Case 2: Nested Enum Validation
```bash
curl -X POST https://complex-tools-openapi.onrender.com/api/v1/customer/profile \
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
        "state": "NY",
        "zipcode": "10001",
        "country": "US"
      }
    }
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "customer_type": "individual",
  "country": "US",
  "validation_summary": "All enum validations passed: type=individual, country=US"
}
```

#### Test Case 3: Multi-Level Enum Validation
```bash
curl -X POST https://complex-tools-openapi.onrender.com/api/v1/customer/multi-level-enum \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "enum_validation_report": {
    "level_0_status": "active (valid)",
    "level_1_customer_type": "individual (valid)",
    "level_2_address_country": "US (valid)",
    "level_3_contact_preference": "email (valid)",
    "total_enum_fields": 4,
    "all_valid": true
  }
}
```

#### Test Case 4: Invalid Enum Values
```bash
# Invalid status
curl -X POST https://complex-tools-openapi.onrender.com/api/v1/account/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "pending",
    "type": "personal",
    "account_id": "ACC-12345"
  }'
```

**Expected Response** (400 Bad Request):
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid enum value provided",
  "field": "status",
  "provided_value": "pending",
  "allowed_values": ["active", "inactive"]
}
```

### Group 5: Conversational Slot Filling

#### Conversational Flow Example

**Turn 1: Start Session**
```bash
curl -X POST https://complex-tools-openapi.onrender.com/api/v1/conversation/profile/start \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe"
  }'
```

**Response**:
```json
{
  "session_id": "SESSION-001",
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

**Turn 2: Add Email and Type**
```bash
curl -X PATCH https://complex-tools-openapi.onrender.com/api/v1/conversation/profile/SESSION-001/update \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "type": "individual"
  }'
```

**Response**:
```json
{
  "session_id": "SESSION-001",
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

**Turn 3: Add Partial Address**
```bash
curl -X PATCH https://complex-tools-openapi.onrender.com/api/v1/conversation/profile/SESSION-001/update \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "street": "123 Main St",
      "city": "New York"
    }
  }'
```

**Response**:
```json
{
  "session_id": "SESSION-001",
  "completeness_percentage": 50,
  "profile": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "type": "individual",
    "address": {
      "street": "123 Main St",
      "city": "New York"
    }
  },
  "missing_required_fields": ["address.country"],
  "next_prompt": "Which country are you in? (US, CA, or UK)",
  "conversation_turn": 3
}
```

**Turn 4: Complete Address**
```bash
curl -X PATCH https://complex-tools-openapi.onrender.com/api/v1/conversation/profile/SESSION-001/update \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "state": "NY",
      "zipcode": "10001",
      "country": "US"
    }
  }'
```

**Response**:
```json
{
  "session_id": "SESSION-001",
  "completeness_percentage": 80,
  "status": "in_progress",
  "missing_required_fields": [],
  "next_prompt": "Would you like to add contact information? (optional)",
  "conversation_turn": 4
}
```

**Turn 5: Add Contact (Optional)**
```bash
curl -X PATCH https://complex-tools-openapi.onrender.com/api/v1/conversation/profile/SESSION-001/update \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "phone": "+1-555-0100",
      "mobile": "+1-555-0101"
    }
  }'
```

**Response**:
```json
{
  "session_id": "SESSION-001",
  "status": "complete",
  "completeness_percentage": 100,
  "missing_required_fields": [],
  "missing_optional_fields": [],
  "next_prompt": "Profile complete! Ready to submit?",
  "conversation_turn": 5
}
```

**Turn 6: Finalize**
```bash
curl -X POST https://complex-tools-openapi.onrender.com/api/v1/conversation/profile/SESSION-001/finalize \
  -H "Content-Type: application/json"
```

**Response**:
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

## Key Features

### Enum Nested Schemas API
1. **Multi-Level Validation**: Tests enums at 0-3 nesting levels
2. **Comprehensive Error Reporting**: Detailed validation failure messages
3. **Field Path Tracking**: Shows exact location of invalid enum values
4. **Validation Summary**: Reports all enum validations in response

### Conversational Slot Filling API
1. **Session Management**: Persistent session across multiple turns
2. **Completeness Tracking**: Real-time percentage of completion
3. **Smart Prompting**: Context-aware next question suggestions
4. **Partial Updates**: Merge new data without overwriting existing
5. **Field Classification**: Distinguishes required vs optional fields
6. **Turn Counting**: Tracks conversation progress

## Integration with Existing APIs

These APIs follow the same deployment pattern as:
- [`openapi_customer_order_deployed.yaml`](./openapi_customer_order_deployed.yaml)
- [`openapi_employee_management_deployed.yaml`](./openapi_employee_management_deployed.yaml)

They can be deployed to the same Render.com instance and will be accessible at:
- Enum API: `https://complex-tools-openapi.onrender.com/api/v1/account/*`
- Conversational API: `https://complex-tools-openapi.onrender.com/api/v1/conversation/*`

## Testing Recommendations

### For Enum Validation:
1. Test each enum field individually with valid values
2. Test each enum field with invalid values
3. Test combinations of valid enums at different levels
4. Test combinations with one invalid enum at each level
5. Verify error messages include field path and allowed values

### For Conversational Flow:
1. Test minimal start (name only)
2. Test incremental updates in sequence
3. Test out-of-order updates (e.g., contact before address)
4. Test partial address updates
5. Test completeness calculation at each turn
6. Test finalization with incomplete profile (should fail)
7. Test finalization with complete profile (should succeed)

## Made with Bob