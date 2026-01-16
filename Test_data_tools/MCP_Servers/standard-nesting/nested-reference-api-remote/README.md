# Nested Reference API - Remote MCP Server

Remote MCP Server for Customer Order API with nested schema references, demonstrating the pattern from GitHub Issue #45755.

## Overview

This MCP server provides tools to process customer orders with complex nested schema references, specifically demonstrating the pattern where:
- `order.shipping_locations.address` references `customer.address` using `$ref: "#/properties/customer/properties/address"`
- `order.shipping_address` and `order.billing_address` reference the same address schema
- `order.items[].delivery_address` references the address schema

This recreates the scenario from the Moody's MCP tools issue where `alerts.address` referenced `inquiry.address`, which caused:
1. Serialization issues during DB insertion (TypeError: Object of type dict is not JSON serializable)
2. LLM confusion during execution due to repeated field names after resolution

## Features

- **SSE Transport**: Uses Server-Sent Events for remote MCP communication
- **Nested References**: Demonstrates `$ref` patterns within the same schema
- **Real API Integration**: Connects to deployed OpenAPI endpoint at `https://complex-tools-openapi.onrender.com`
- **Comprehensive Error Handling**: Proper error responses for API failures

## Available Tools

### `process_customer_order_with_references`

Process customer orders with nested address references.

**Input Schema Features:**
- Customer information with primary address
- Order details with multiple items
- Product specifications with nested details
- Shipping locations that reference customer address using `$ref`
- Delivery addresses that reference the same address schema

**Example Usage:**
```json
{
  "customer": {
    "name": "Jane Smith",
    "email": "jane.smith@email.com",
    "address": {
      "street": "456 Oak Avenue",
      "city": "New York",
      "state": "NY",
      "zipcode": "10001",
      "country": "USA"
    },
    "contact": {
      "phone": "+1-555-0200",
      "mobile": "+1-555-0201"
    },
    "entityType": "INDIVIDUAL",
    "customerId": "CUST-001"
  },
  "order": {
    "order_id": "ORD-2024-002",
    "order_date": "2024-01-16",
    "items": [
      {
        "product": {
          "product_id": "PROD-001",
          "name": "Premium Laptop",
          "details": {
            "description": "High-performance laptop",
            "specifications": {
              "weight": "1.5 kg",
              "dimensions": "35cm x 25cm x 2cm",
              "material": "Aluminum alloy"
            }
          }
        },
        "quantity": 1,
        "price": 1299.99,
        "delivery_address": [
          {
            "street": "456 Oak Avenue",
            "city": "New York",
            "state": "NY",
            "zipcode": "10001",
            "country": "USA"
          }
        ]
      }
    ],
    "shipping_address": {
      "street": "456 Oak Avenue",
      "city": "New York",
      "state": "NY",
      "zipcode": "10001",
      "country": "USA"
    },
    "billing_address": {
      "street": "789 Pine Street",
      "city": "New York",
      "state": "NY",
      "zipcode": "10002",
      "country": "USA"
    },
    "shipping_locations": [
      {
        "location_id": "LOC-001",
        "location_name": "Primary Warehouse",
        "address": [
          {
            "street": "456 Oak Avenue",
            "city": "New York",
            "state": "NY",
            "zipcode": "10001",
            "country": "USA"
          }
        ],
        "entityType": "WAREHOUSE"
      }
    ]
  }
}
```

## Deployment to Render.com

### Prerequisites
- GitHub account
- Render.com account (free tier available)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   cd Test_data_tools/MCP_Servers/Standard\ Nesting\ \(Basic\,\ Deep\,\ References\)/nested-reference-api-remote
   git init
   git add .
   git commit -m "Initial commit: Nested Reference API Remote MCP Server"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render.com**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration
   - Click "Create Web Service"

3. **Configuration (Auto-detected from render.yaml)**
   - **Name**: `nested-reference-api-remote`
   - **Environment**: Node
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Plan**: Free

4. **Environment Variables** (Auto-configured)
   - `NODE_VERSION`: 18.0.0
   - `PORT`: 10000

### After Deployment

Your MCP server will be available at:
- **MCP Endpoint**: `https://nested-reference-api-remote.onrender.com/mcp`
- **Health Check**: `https://nested-reference-api-remote.onrender.com/health`
- **Root**: `https://nested-reference-api-remote.onrender.com/`

## Local Development

### Installation
```bash
npm install
```

### Development Mode
```bash
npm run dev
```

### Build
```bash
npm run build
```

### Production
```bash
npm start
```

## Testing

Test the health endpoint:
```bash
curl https://nested-reference-api-remote.onrender.com/health
```

## MCP Client Configuration

Add to your MCP client settings:

```json
{
  "mcpServers": {
    "nested-reference-api": {
      "url": "https://nested-reference-api-remote.onrender.com/mcp",
      "transport": "http"
    }
  }
}
```

## Architecture

- **Transport**: HTTP (JSON-RPC over HTTP POST)
- **Backend API**: `https://complex-tools-openapi.onrender.com/api/v1`
- **Framework**: Express.js with MCP SDK
- **Language**: TypeScript

## Related Resources

- **OpenAPI Spec**: `Test_data_tools/OpenAPI/Standard Nesting (Basic, Deep, References)/openapi_nested_reference_test.yaml`
- **GitHub Issue**: #45755 - Nested Schema Reference Pattern
- **Backend API**: Complex Tools OpenAPI Server

## License

MIT

---

Made with Bob