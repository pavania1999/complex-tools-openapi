# Enum Nested API - Local MCP Server

Local MCP Server implementation for testing enum validation in nested data structures. This server provides direct implementation without external API calls, using stdio transport for local communication.

## Overview

This MCP server demonstrates enum validation at multiple nesting levels:
- **Level 0**: Root-level enums (account status, profile status)
- **Level 1**: First-level nested enums (customer type)
- **Level 2**: Second-level nested enums (address country)
- **Level 3**: Third-level nested enums (contact preference)

## Features

- ✅ Direct implementation (no external API dependencies)
- ✅ Stdio transport for local MCP communication
- ✅ Comprehensive enum validation at multiple nesting levels
- ✅ Detailed error messages with validation failures
- ✅ Test payloads for both valid and invalid scenarios

## Tools

### 1. update_account_status

Update account status with simple enum validation at root level.

**Parameters:**
- `account_id` (string, required): Unique account identifier
- `status` (enum, required): Account status - "active" or "inactive"
- `type` (enum, required): Account type - "personal" or "business"

**Example:**
```json
{
  "account_id": "ACC-12345",
  "status": "active",
  "type": "personal"
}
```

### 2. create_customer_profile_multi_level

Test multi-level enum validation across nested structures.

**Parameters:**
- `profile_id` (string, required): Unique profile identifier
- `status` (enum, required): Profile status - "active" or "inactive"
- `customer` (object, required): Customer information with nested enums
  - `name` (string, required): Customer full name
  - `email` (string, optional): Customer email
  - `type` (enum, required): Customer type - "individual" or "corporate"
  - `address` (object, required): Customer address
    - `street` (string, required): Street address
    - `city` (string, required): City name
    - `state` (string, optional): State/province code
    - `zipcode` (string, optional): Postal code
    - `country` (enum, required): Country code - "US", "CA", or "UK"
  - `contact` (object, optional): Contact information
    - `phone` (string, optional): Primary phone
    - `mobile` (string, optional): Mobile phone
    - `preference` (enum, optional): Contact preference - "email", "phone", or "sms"
    - `timezone` (string, optional): Preferred timezone

**Example:**
```json
{
  "profile_id": "PROF-001",
  "status": "active",
  "customer": {
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "type": "individual",
    "address": {
      "street": "321 Oak Ave",
      "city": "Seattle",
      "state": "WA",
      "zipcode": "98101",
      "country": "US"
    },
    "contact": {
      "phone": "+1-206-555-0300",
      "preference": "email",
      "timezone": "PST"
    }
  }
}
```

## Installation

1. Install dependencies:
```bash
npm install
```

2. Build the project:
```bash
npm run build
```

## Usage

### As MCP Server

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "enum-nested-api": {
      "command": "node",
      "args": ["/path/to/enum-nested-api/build/index.js"]
    }
  }
}
```

### Testing

Run the test script:
```bash
chmod +x test-tool-call.sh
./test-tool-call.sh
```

Or use the MCP Inspector:
```bash
npm run inspector
```

## Test Scenarios

The `test-payload.json` file includes comprehensive test cases:

1. **Valid account status update** - All enums valid
2. **Invalid account status** - Tests status enum validation
3. **Invalid account type** - Tests type enum validation
4. **Valid multi-level profile** - All nested enums valid
5. **Invalid profile status** - Tests root-level enum validation
6. **Invalid customer type** - Tests level 1 enum validation
7. **Invalid country** - Tests level 2 enum validation
8. **Invalid contact preference** - Tests level 3 enum validation
9. **Multiple invalid enums** - Tests multiple validation failures
10. **Valid without optional contact** - Tests optional nested enum

## Validation Behavior

### Success Response
When all validations pass:
```json
{
  "success": true,
  "message": "Profile created with all enum validations passed",
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

### Error Response
When validation fails:
```json
{
  "error": "ENUM_VALIDATION_ERROR",
  "message": "One or more enum validation failures detected",
  "validation_failures": [
    {
      "field_path": "customer.address.country",
      "provided_value": "FR",
      "allowed_values": ["US", "CA", "UK"],
      "nesting_level": 2
    }
  ]
}
```

## Development

Watch mode for development:
```bash
npm run watch
```

## Architecture

- **Transport**: Stdio (standard input/output)
- **Protocol**: MCP (Model Context Protocol)
- **Implementation**: Direct validation logic (no external APIs)
- **Language**: TypeScript
- **Runtime**: Node.js

## Related Files

- `src/index.ts` - Main server implementation
- `test-payload.json` - Test data for all scenarios
- `test-tool-call.sh` - Automated test script
- `package.json` - Dependencies and scripts
- `tsconfig.json` - TypeScript configuration

## Made with Bob

This MCP server was created to demonstrate enum validation patterns in nested data structures for testing AI agent tool calling capabilities.