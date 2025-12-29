# Test Utterances and Expected Responses
## Group 4: Enum Validation & Group 5: Conversational Slot Filling

This document provides natural language utterances and their expected API responses for testing with watsonx Orchestrate.

---

## Group 4: Enum Nested Schemas

### Test Case 1: Simple Enum Validation (Account Status)

#### Utterance 1.1: Valid Personal Active Account
**User Says:**
> "Update account ACC-12345 to active status as a personal account"

**Expected Skill Invocation:**
```
Skill: update_account_status
Parameters:
  - account_id: "ACC-12345"
  - status: "active"
  - type: "personal"
```

**Expected API Response:**
```json
{
  "success": true,
  "message": "Account status updated successfully",
  "account_id": "ACC-12345",
  "status": "active",
  "type": "personal",
  "updated_at": "2024-01-29T08:00:00Z",
  "validation_summary": "All enum validations passed: status=active (valid), type=personal (valid)"
}
```

**Expected User Response:**
> "✅ Account ACC-12345 has been updated to active status as a personal account. All validations passed."

---

#### Utterance 1.2: Valid Business Inactive Account
**User Says:**
> "Set account ACC-67890 to inactive for business type"

**Expected Skill Invocation:**
```
Skill: update_account_status
Parameters:
  - account_id: "ACC-67890"
  - status: "inactive"
  - type: "business"
```

**Expected API Response:**
```json
{
  "success": true,
  "message": "Account status updated successfully",
  "account_id": "ACC-67890",
  "status": "inactive",
  "type": "business",
  "validation_summary": "All enum validations passed: status=inactive (valid), type=business (valid)"
}
```

**Expected User Response:**
> "✅ Account ACC-67890 has been set to inactive status for business type."

---

#### Utterance 1.3: Invalid Status Value (Should Fail)
**User Says:**
> "Update account ACC-99999 to pending status as personal"

**Expected Skill Invocation:**
```
Skill: update_account_status
Parameters:
  - account_id: "ACC-99999"
  - status: "pending"
  - type: "personal"
```

**Expected API Response:**
```json
{
  "success": false,
  "error": "VALIDATION_ERROR",
  "message": "Invalid enum value provided",
  "field": "status",
  "provided_value": "pending",
  "allowed_values": ["active", "inactive"]
}
```

**Expected User Response:**
> "❌ Error: Invalid status value 'pending'. Allowed values are: active, inactive"

---

### Test Case 2: Nested Enum Validation (Customer Profile)

#### Utterance 2.1: Valid Individual Customer in US
**User Says:**
> "Create a customer profile for John Doe, email john.doe@example.com, individual type, living at 123 Main St, New York, NY 10001, United States"

**Expected Skill Invocation:**
```
Skill: create_customer_profile
Parameters:
  - customer_id: "CUST-001"
  - customer:
      name: "John Doe"
      email: "john.doe@example.com"
      type: "individual"
      address:
        street: "123 Main St"
        city: "New York"
        state: "NY"
        zipcode: "10001"
        country: "US"
      contact:
        phone: "+1-555-0100"
        mobile: "+1-555-0101"
```

**Expected API Response:**
```json
{
  "success": true,
  "message": "Customer profile created successfully",
  "customer_id": "CUST-001",
  "customer_name": "John Doe",
  "customer_email": "john.doe@example.com",
  "customer_type": "individual",
  "address_formatted": "123 Main St, New York, NY, 10001, US",
  "country": "US",
  "contact_phone": "+1-555-0100",
  "contact_mobile": "+1-555-0101",
  "validation_summary": "All enum validations passed: type=individual (valid), country=US (valid)",
  "created_at": "2024-01-29T08:00:00Z"
}
```

**Expected User Response:**
> "✅ Customer profile created for John Doe (individual) at 123 Main St, New York, NY, 10001, US. All enum validations passed."

---

#### Utterance 2.2: Valid Corporate Customer in Canada
**User Says:**
> "Create corporate customer profile for Acme Corporation, email contact@acme.com, address 456 Business Ave, Toronto, ON M5H 2N2, Canada"

**Expected Skill Invocation:**
```
Skill: create_customer_profile
Parameters:
  - customer_id: "CUST-002"
  - customer:
      name: "Acme Corporation"
      email: "contact@acme.com"
      type: "corporate"
      address:
        street: "456 Business Ave"
        city: "Toronto"
        state: "ON"
        zipcode: "M5H 2N2"
        country: "CA"
```

**Expected API Response:**
```json
{
  "success": true,
  "message": "Customer profile created successfully",
  "customer_id": "CUST-002",
  "customer_name": "Acme Corporation",
  "customer_email": "contact@acme.com",
  "customer_type": "corporate",
  "address_formatted": "456 Business Ave, Toronto, ON, M5H 2N2, CA",
  "country": "CA",
  "validation_summary": "All enum validations passed: type=corporate (valid), country=CA (valid)"
}
```

**Expected User Response:**
> "✅ Corporate customer profile created for Acme Corporation in Toronto, Canada."

---

#### Utterance 2.3: Invalid Customer Type (Should Fail)
**User Says:**
> "Create customer profile for Test User as partnership type in US"

**Expected Skill Invocation:**
```
Skill: create_customer_profile
Parameters:
  - customer:
      name: "Test User"
      type: "partnership"
      address:
        country: "US"
```

**Expected API Response:**
```json
{
  "success": false,
  "error": "VALIDATION_ERROR",
  "message": "Invalid enum value in request",
  "field": "customer.type",
  "provided_value": "partnership",
  "allowed_values": ["individual", "corporate"]
}
```

**Expected User Response:**
> "❌ Error: Invalid customer type 'partnership'. Allowed values are: individual, corporate"

---

#### Utterance 2.4: Invalid Country Code (Should Fail)
**User Says:**
> "Create individual customer profile for Jane Smith in France"

**Expected Skill Invocation:**
```
Skill: create_customer_profile
Parameters:
  - customer:
      name: "Jane Smith"
      type: "individual"
      address:
        country: "FR"
```

**Expected API Response:**
```json
{
  "success": false,
  "error": "VALIDATION_ERROR",
  "message": "Invalid enum value in request",
  "field": "customer.address.country",
  "provided_value": "FR",
  "allowed_values": ["US", "CA", "UK"]
}
```

**Expected User Response:**
> "❌ Error: Invalid country code 'FR'. Allowed values are: US, CA, UK"

---

### Test Case 3: Multi-Level Enum Validation

#### Utterance 3.1: All Valid Enums (4 Levels)
**User Says:**
> "Create active profile PROF-001 for Alice Johnson, individual type, at 321 Oak Ave, Seattle, WA 98101, US, with email preference and phone +1-206-555-0300"

**Expected Skill Invocation:**
```
Skill: create_multi_level_enum_profile
Parameters:
  - profile_id: "PROF-001"
  - status: "active"
  - customer:
      name: "Alice Johnson"
      email: "alice@example.com"
      type: "individual"
      address:
        street: "321 Oak Ave"
        city: "Seattle"
        state: "WA"
        zipcode: "98101"
        country: "US"
      contact:
        phone: "+1-206-555-0300"
        preference: "email"
        timezone: "PST"
```

**Expected API Response:**
```json
{
  "success": true,
  "message": "Profile created with all enum validations passed",
  "profile_id": "PROF-001",
  "profile_status": "active",
  "customer_name": "Alice Johnson",
  "customer_email": "alice@example.com",
  "customer_type": "individual",
  "address_formatted": "321 Oak Ave, Seattle, WA, 98101, US",
  "country": "US",
  "contact_phone": "+1-206-555-0300",
  "contact_preference": "email",
  "contact_timezone": "PST",
  "enum_validation_report": {
    "level_0_status": "status=active (valid)",
    "level_1_customer_type": "customer_type=individual (valid)",
    "level_2_address_country": "address_country=US (valid)",
    "level_3_contact_preference": "contact_preference=email (valid)",
    "total_enum_fields": 4,
    "all_valid": true
  },
  "created_at": "2024-01-29T08:00:00Z"
}
```

**Expected User Response:**
> "✅ Profile PROF-001 created for Alice Johnson with all 4 enum validations passed:
> - Status: active ✓
> - Customer Type: individual ✓
> - Country: US ✓
> - Contact Preference: email ✓"

---

#### Utterance 3.2: Invalid at Multiple Levels (Should Fail)
**User Says:**
> "Create suspended profile for Bob Wilson, nonprofit type, in Mexico, with fax preference"

**Expected Skill Invocation:**
```
Skill: create_multi_level_enum_profile
Parameters:
  - status: "suspended"
  - customer:
      name: "Bob Wilson"
      type: "nonprofit"
      address:
        country: "MX"
      contact:
        preference: "fax"
```

**Expected API Response:**
```json
{
  "success": false,
  "error": "ENUM_VALIDATION_ERROR",
  "message": "One or more enum validation failures detected",
  "validation_failures": [
    {
      "field_path": "status",
      "provided_value": "suspended",
      "allowed_values": ["active", "inactive"],
      "nesting_level": 0
    },
    {
      "field_path": "customer.type",
      "provided_value": "nonprofit",
      "allowed_values": ["individual", "corporate"],
      "nesting_level": 1
    },
    {
      "field_path": "customer.address.country",
      "provided_value": "MX",
      "allowed_values": ["US", "CA", "UK"],
      "nesting_level": 2
    },
    {
      "field_path": "customer.contact.preference",
      "provided_value": "fax",
      "allowed_values": ["email", "phone", "sms"],
      "nesting_level": 3
    }
  ]
}
```

**Expected User Response:**
> "❌ Multiple enum validation failures detected:
> - Level 0 (status): 'suspended' invalid, allowed: active, inactive
> - Level 1 (customer.type): 'nonprofit' invalid, allowed: individual, corporate
> - Level 2 (country): 'MX' invalid, allowed: US, CA, UK
> - Level 3 (preference): 'fax' invalid, allowed: email, phone, sms"

---

## Group 5: Conversational Slot Filling

### Test Case 4: Complete Conversational Flow

#### Turn 1: Start Session
**User Says:**
> "I want to create a new customer profile. My name is John Doe"

**Expected Skill Invocation:**
```
Skill: start_profile_session
Parameters:
  - name: "John Doe"
```

**Expected API Response:**
```json
{
  "session_id": "SESSION-ABC123",
  "status": "in_progress",
  "completeness_percentage": 10,
  "profile": {
    "name": "John Doe"
  },
  "missing_required_fields": [
    "email",
    "type",
    "address.street",
    "address.city",
    "address.country"
  ],
  "missing_optional_fields": [
    "address.state",
    "address.zipcode",
    "contact.phone",
    "contact.mobile"
  ],
  "next_prompt": "Great! What's your email address?",
  "conversation_turn": 1,
  "created_at": "2024-01-29T08:00:00Z"
}
```

**Expected User Response:**
> "✅ Profile session started for John Doe (10% complete).
> 
> Next: What's your email address?"

---

#### Turn 2: Add Email and Type
**User Says:**
> "My email is john.doe@example.com and I'm an individual customer"

**Expected Skill Invocation:**
```
Skill: update_profile_session
Parameters:
  - session_id: "SESSION-ABC123"
  - email: "john.doe@example.com"
  - type: "individual"
```

**Expected API Response:**
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
  "missing_required_fields": [
    "address.street",
    "address.city",
    "address.country"
  ],
  "missing_optional_fields": [
    "address.state",
    "address.zipcode",
    "contact.phone",
    "contact.mobile"
  ],
  "next_prompt": "What's your street address?",
  "conversation_turn": 2,
  "updated_at": "2024-01-29T08:01:00Z"
}
```

**Expected User Response:**
> "✅ Profile updated (30% complete).
> 
> Added:
> - Email: john.doe@example.com
> - Type: individual
> 
> Next: What's your street address?"

---

#### Turn 3: Add Partial Address
**User Says:**
> "I live at 123 Main Street in New York"

**Expected Skill Invocation:**
```
Skill: update_profile_session
Parameters:
  - session_id: "SESSION-ABC123"
  - address:
      street: "123 Main Street"
      city: "New York"
```

**Expected API Response:**
```json
{
  "session_id": "SESSION-ABC123",
  "status": "in_progress",
  "completeness_percentage": 50,
  "profile": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "type": "individual",
    "address": {
      "street": "123 Main Street",
      "city": "New York"
    }
  },
  "missing_required_fields": [
    "address.country"
  ],
  "missing_optional_fields": [
    "address.state",
    "address.zipcode",
    "contact.phone",
    "contact.mobile"
  ],
  "next_prompt": "Which country are you in? (US, CA, or UK)",
  "conversation_turn": 3,
  "updated_at": "2024-01-29T08:02:00Z"
}
```

**Expected User Response:**
> "✅ Profile updated (50% complete).
> 
> Address added:
> - Street: 123 Main Street
> - City: New York
> 
> Next: Which country are you in? (US, CA, or UK)"

---

#### Turn 4: Complete Address
**User Says:**
> "I'm in the United States, New York state, zip code 10001"

**Expected Skill Invocation:**
```
Skill: update_profile_session
Parameters:
  - session_id: "SESSION-ABC123"
  - address:
      state: "NY"
      zipcode: "10001"
      country: "US"
```

**Expected API Response:**
```json
{
  "session_id": "SESSION-ABC123",
  "status": "complete",
  "completeness_percentage": 80,
  "profile": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "type": "individual",
    "address": {
      "street": "123 Main Street",
      "city": "New York",
      "state": "NY",
      "zipcode": "10001",
      "country": "US"
    }
  },
  "missing_required_fields": [],
  "missing_optional_fields": [
    "contact.phone",
    "contact.mobile"
  ],
  "next_prompt": "Would you like to add contact information? (optional)",
  "conversation_turn": 4,
  "updated_at": "2024-01-29T08:03:00Z"
}
```

**Expected User Response:**
> "✅ Profile updated (80% complete). All required fields collected!
> 
> Address completed:
> - 123 Main Street, New York, NY, 10001, US
> 
> Next: Would you like to add contact information? (optional)"

---

#### Turn 5: Add Contact Information
**User Says:**
> "Yes, my phone is +1-555-0100 and mobile is +1-555-0101"

**Expected Skill Invocation:**
```
Skill: update_profile_session
Parameters:
  - session_id: "SESSION-ABC123"
  - contact:
      phone: "+1-555-0100"
      mobile: "+1-555-0101"
```

**Expected API Response:**
```json
{
  "session_id": "SESSION-ABC123",
  "status": "complete",
  "completeness_percentage": 100,
  "profile": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "type": "individual",
    "address": {
      "street": "123 Main Street",
      "city": "New York",
      "state": "NY",
      "zipcode": "10001",
      "country": "US"
    },
    "contact": {
      "phone": "+1-555-0100",
      "mobile": "+1-555-0101"
    }
  },
  "missing_required_fields": [],
  "missing_optional_fields": [],
  "next_prompt": "Profile complete! Ready to submit?",
  "conversation_turn": 5,
  "updated_at": "2024-01-29T08:04:00Z"
}
```

**Expected User Response:**
> "✅ Profile 100% complete!
> 
> Contact information added:
> - Phone: +1-555-0100
> - Mobile: +1-555-0101
> 
> Next: Profile complete! Ready to submit?"

---

#### Turn 6: Finalize Profile
**User Says:**
> "Yes, please submit the profile"

**Expected Skill Invocation:**
```
Skill: finalize_profile_session
Parameters:
  - session_id: "SESSION-ABC123"
```

**Expected API Response:**
```json
{
  "success": true,
  "message": "Profile finalized and submitted successfully",
  "profile_id": "PROF-5F48FBAA",
  "customer_name": "John Doe",
  "customer_email": "john.doe@example.com",
  "customer_type": "individual",
  "address_formatted": "123 Main Street, New York, NY, 10001, US",
  "contact_phone": "+1-555-0100",
  "contact_mobile": "+1-555-0101",
  "conversation_summary": {
    "total_turns": 5,
    "fields_collected": 10,
    "time_to_complete": "4 minutes"
  },
  "finalized_at": "2024-01-29T08:04:30Z"
}
```

**Expected User Response:**
> "✅ Profile successfully submitted!
> 
> **Profile ID:** PROF-5F48FBAA
> 
> **Customer:** John Doe (individual)
> **Email:** john.doe@example.com
> **Address:** 123 Main Street, New York, NY, 10001, US
> **Phone:** +1-555-0100
> **Mobile:** +1-555-0101
> 
> **Conversation Summary:**
> - Total turns: 5
> - Fields collected: 10
> - Time to complete: 4 minutes"

---

### Test Case 5: Check Session Status

#### Utterance 5.1: Check Status Mid-Conversation
**User Says:**
> "What's the status of my profile session SESSION-ABC123?"

**Expected Skill Invocation:**
```
Skill: get_session_status
Parameters:
  - session_id: "SESSION-ABC123"
```

**Expected API Response:**
```json
{
  "session_id": "SESSION-ABC123",
  "status": "in_progress",
  "completeness_percentage": 50,
  "profile": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "type": "individual",
    "address": {
      "street": "123 Main Street",
      "city": "New York"
    }
  },
  "missing_required_fields": ["address.country"],
  "missing_optional_fields": ["address.state", "address.zipcode", "contact.phone", "contact.mobile"],
  "next_prompt": "Which country are you in? (US, CA, or UK)",
  "conversation_turn": 3,
  "created_at": "2024-01-29T08:00:00Z",
  "updated_at": "2024-01-29T08:02:00Z"
}
```

**Expected User Response:**
> "📊 Session Status: SESSION-ABC123
> 
> **Progress:** 50% complete (Turn 3)
> **Status:** in_progress
> 
> **Current Profile:**
> - Name: John Doe
> - Email: john.doe@example.com
> - Type: individual
> - Address: 123 Main Street, New York
> 
> **Still Missing:**
> - Required: address.country
> - Optional: address.state, address.zipcode, contact.phone, contact.mobile
> 
> **Next Step:** Which country are you in? (US, CA, or UK)"

---

### Test Case 6: Error Scenarios

#### Utterance 6.1: Session Not Found
**User Says:**
> "Update session SESSION-INVALID with email test@example.com"

**Expected API Response:**
```json
{
  "error": "SESSION_NOT_FOUND",
  "message": "Session SESSION-INVALID not found"
}
```

**Expected User Response:**
> "❌ Error: Session SESSION-INVALID not found. Please start a new profile session."

---

#### Utterance 6.2: Finalize Incomplete Profile
**User Says:**
> "Finalize session SESSION-ABC123"
(when profile is incomplete)

**Expected API Response:**
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Profile incomplete - missing required fields",
  "missing_fields": ["address.country"],
  "session_id": "SESSION-ABC123"
}
```

**Expected User Response:**
> "❌ Cannot finalize: Profile is incomplete.
> 
> Missing required fields:
> - address.country
> 
> Please provide these fields before finalizing."

---

## Summary of Test Coverage

### Enum Validation (Group 4)
- ✅ 3 endpoints tested
- ✅ 10 test utterances
- ✅ Valid enum values at all levels
- ✅ Invalid enum values at all levels
- ✅ Multi-level validation scenarios
- ✅ Comprehensive error messages

### Conversational Slot Filling (Group 5)
- ✅ 4 endpoints tested
- ✅ 8 test utterances
- ✅ Complete 6-turn conversation flow
- ✅ Incremental data collection
- ✅ Session status checking
- ✅ Error handling scenarios

## Made with Bob 🤖