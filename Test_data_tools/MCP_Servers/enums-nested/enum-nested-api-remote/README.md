# Enum Nested API - Remote MCP Server

Remote MCP Server for testing enum validation within nested structures at multiple levels. This implementation provides **direct enum validation logic** without calling external APIs.

## Overview

This MCP server implements the Enum Nested Schemas API with direct validation logic for testing enum constraints in nested data structures. It demonstrates:

- **Simple Enums**: Root-level enum validation (status, type)
- **Nested Enums**: Multi-level enum validation in nested objects
- **Direct Implementation**: No external API calls - all validation is done locally

## Features

### Tool 1: `update_account_status`
Tests simple enum validation at root level.

**Enums Validated:**
- `status`: "active" | "inactive"
- `type`: "personal" | "business"

**Example:**
```json
{
  "account_id": "ACC-12345",
  "status": "active",
  "type": "personal"
}
```

### Tool 2: `create_customer_profile_multi_level`
Tests multi-level enum validation across nested structures.

**Enums Validated:**
- Level 0: `status` - "active" | "inactive"
- Level 1: `customer.type` - "individual" | "corporate"
- Level 2: `customer.address.country` - "US" | "CA" | "UK"
- Level 3: `customer.contact.preference` - "email" | "phone" | "sms" (optional)

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

```bash
cd Test_data_tools/MCP_Servers/enums-nested/enum-nested-api-remote
npm install
```

## Development

```bash
# Build TypeScript
npm run build

# Run in development mode
npm run dev

# Start production server
npm start
```

## Deployment

### Deploy to Render.com

1. Push code to GitHub repository
2. Connect repository to Render.com
3. Use the provided `render.yaml` configuration
4. Deploy as a Web Service

The server will be available at: `https://your-service.onrender.com`

### Endpoints

- **Health Check**: `GET /health`
- **MCP Protocol**: `POST /mcp`
- **Root Info**: `GET /`

## MCP Configuration

Add to your MCP settings file:

```json
{
  "mcpServers": {
    "enum-nested-api-remote": {
      "url": "https://your-service.onrender.com/mcp",
      "transport": "http"
    }
  }
}
```

## Testing

### Test Account Status Update

```bash
curl -X POST http://localhost:3457/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "update_account_status",
      "arguments": {
        "account_id": "ACC-12345",
        "status": "active",
        "type": "personal"
      }
    }
  }'
```

### Test Multi-Level Enum Validation

```bash
curl -X POST http://localhost:3457/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "create_customer_profile_multi_level",
      "arguments": {
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
    }
  }'
```

## Validation Logic

The server implements direct enum validation:

1. **Field Validation**: Checks if provided values match allowed enum values
2. **Error Reporting**: Returns detailed error messages with field paths and allowed values
3. **Multi-Level Tracking**: Reports validation status at each nesting level
4. **Comprehensive Reports**: Provides enum validation reports showing all validated fields

## Error Responses

### Simple Validation Error
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid status: \"pending\". Allowed values: active, inactive",
  "field": "status",
  "provided_value": "pending",
  "allowed_values": ["active", "inactive"]
}
```

### Multi-Level Validation Error
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

## Architecture

- **Transport**: HTTP with JSON-RPC 2.0
- **Protocol**: Model Context Protocol (MCP)
- **Implementation**: Direct validation logic (no external API calls)
- **Framework**: Express.js with TypeScript
- **Deployment**: Render.com (free tier)

## Related Files

- OpenAPI Spec: `Test_data_tools/OpenAPI/enums-nested/openapi_enum_nested_deployed.yaml`
- Test Utterances: `Test_data_tools/OpenAPI/enums-nested/TEST_UTTERANCES_ENUM_CONVERSATIONAL.md`

## Made with Bob