# Array Handling API MCP Server

MCP Server for TC-P0-API-002 test case - demonstrates array handling with both wrapped and raw array structures.

## Test Case Information

- **Test ID**: TC-P0-API-002
- **Priority**: P0 (Critical)
- **Type**: Integration
- **Focus**: Array Handling (Wrapped Arrays + Raw Arrays)
- **Agent Style**: react-intrinsic
- **Model**: gpt-oss-120b

## Overview

This MCP server provides tools to interact with the Array Handling API, which demonstrates:
- Wrapped arrays (arrays within object properties)
- Raw arrays (arrays at request body level)
- Nested arrays (arrays within arrays)
- Nested objects within array items

## Available Tools

### 1. process_inventory_items_wrapped
Process inventory items with wrapped array structure.

**Input**: Object with `items` array property
```json
{
  "items": [
    {
      "name": "Laptop",
      "sku": "LAP-001",
      "quantity": 5,
      "price": 999.99,
      "category": "Electronics",
      "specifications": {
        "brand": "TechCorp",
        "model": "Pro-X1",
        "warranty": "2 years"
      }
    }
  ]
}
```

### 2. process_inventory_items_raw
Process inventory items with raw array structure.

**Input**: Direct array
```json
[
  {
    "name": "Laptop",
    "sku": "LAP-001",
    "quantity": 5,
    "price": 999.99,
    "category": "Electronics",
    "specifications": {
      "brand": "TechCorp",
      "model": "Pro-X1",
      "warranty": "2 years"
    }
  }
]
```

### 3. process_batch_orders_wrapped
Process batch orders with wrapped array structure and nested items.

**Input**: Object with `orders` array property
```json
{
  "orders": [
    {
      "order_id": "ORD-001",
      "customer_name": "John Doe",
      "items": [
        {
          "product_name": "Laptop",
          "quantity": 1,
          "unit_price": 999.99
        }
      ]
    }
  ]
}
```

### 4. process_batch_orders_raw
Process batch orders with raw array structure.

**Input**: Direct array of orders
```json
[
  {
    "order_id": "ORD-001",
    "customer_name": "John Doe",
    "items": [
      {
        "product_name": "Laptop",
        "quantity": 1,
        "unit_price": 999.99
      }
    ]
  }
]
```

## Installation

```bash
cd MCP_Servers/array-handling-api
npm install
npm run build
```

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "array-handling-api": {
      "command": "node",
      "args": [
        "/absolute/path/to/MCP_Servers/array-handling-api/build/index.js"
      ]
    }
  }
}
```

### With Cline

Add to your Cline MCP settings:

```json
{
  "mcpServers": {
    "array-handling-api": {
      "command": "node",
      "args": [
        "/absolute/path/to/MCP_Servers/array-handling-api/build/index.js"
      ]
    }
  }
}
```

## API Endpoints

The tools connect to the deployed API at:
- **Base URL**: `https://complex-tools-openapi.onrender.com/api/v1`
- **Health Check**: `https://complex-tools-openapi.onrender.com/health`

### Endpoints:
- `POST /inventory/process-items` - Wrapped array inventory processing
- `POST /inventory/process-items-raw` - Raw array inventory processing
- `POST /orders/process-batch` - Wrapped array batch order processing
- `POST /orders/process-batch-raw` - Raw array batch order processing

## Response Format

All tools return JSON responses with:
- `status`: "success", "partial_success", or "failed"
- `message`: Descriptive message
- `processed_items` or `processed_orders`: Array of processed results
- `total_value` or `summary`: Calculated totals and summaries

## Example Response

```json
{
  "status": "success",
  "message": "Successfully processed 2 inventory items",
  "processed_items": [
    {
      "name": "Laptop",
      "sku": "LAP-001",
      "status": "added",
      "inventory_id": "INV-2024-001",
      "quantity": 5,
      "unit_price": 999.99,
      "total_value": 4999.95,
      "category": "Electronics",
      "specifications": {
        "brand": "TechCorp",
        "model": "Pro-X1",
        "warranty": "2 years"
      }
    }
  ],
  "total_value": 4999.95,
  "summary": {
    "total_items": 2,
    "total_quantity": 25,
    "categories": ["Electronics", "Accessories"]
  }
}
```

## Testing

See `test-payload.json` for example payloads to test each tool.

## Related Files

- OpenAPI Spec: `../../nested_schemas/tc_p0_api_002/openapi_array_handling_wrapped.yaml`
- Python Implementation: `../../nested_schemas/tc_p0_api_002/process_array_handling.py`
- Test Payloads: `../../nested_schemas/tc_p0_api_002/test_payloads.json`

## License

MIT