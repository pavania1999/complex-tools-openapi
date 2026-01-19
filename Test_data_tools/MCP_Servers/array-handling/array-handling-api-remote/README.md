# Array Handling API - Remote MCP Server

Remote MCP Server for Array Handling API (TC-P0-API-002) demonstrating raw array structures at request body level.

## Overview

This MCP server provides tools to process data with raw array structures, validating that raw arrays work correctly with the react-intrinsic agent style. The OpenAPI spec uses RAW ARRAYS (valid OpenAPI 3.0 structure) where the request body is directly an array type.

## Features

- **HTTP Transport**: Uses HTTP (JSON-RPC over HTTP POST) for remote MCP communication
- **Raw Array Handling**: Demonstrates raw arrays at request body level
- **Real API Integration**: Connects to deployed OpenAPI endpoint at `https://complex-tools-openapi.onrender.com`
- **Comprehensive Error Handling**: Proper error responses for API failures

## Available Tools

### `process_inventory_items_raw`

Process inventory items with raw array structure at request body level.

**Array Structure**: Request body is directly an array type  
**Expected Request**: `[{"name": "Item1", "quantity": 10}, ...]`

**Input Schema Features:**
- Basic information (name, SKU, quantity, price)
- Category enum (Electronics, Accessories, Furniture, Office Supplies)
- Nested specifications object (brand, model, warranty)
- Validation constraints (SKU pattern, quantity/price ranges)

**Example Usage:**
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
  },
  {
    "name": "Mouse",
    "sku": "MOU-002",
    "quantity": 20,
    "price": 29.99,
    "category": "Accessories",
    "specifications": {
      "brand": "TechCorp",
      "model": "Wireless-M2",
      "warranty": "1 year"
    }
  }
]
```

### `process_batch_orders_raw`

Process multiple orders in a batch with raw array structure.

**Array Structure**: Request body is a raw array of orders  
**Each order contains**: Nested items array

**Example Usage:**
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
      },
      {
        "product_name": "Mouse",
        "quantity": 2,
        "unit_price": 29.99
      }
    ]
  },
  {
    "order_id": "ORD-002",
    "customer_name": "Jane Smith",
    "items": [
      {
        "product_name": "Monitor",
        "quantity": 1,
        "unit_price": 299.99
      }
    ]
  }
]
```

## Deployment to Render.com

### Prerequisites
- GitHub account
- Render.com account (free tier available)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   cd Test_data_tools/MCP_Servers/array-handling/array-handling-api-remote
   git init
   git add .
   git commit -m "Initial commit: Array Handling API Remote MCP Server"
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
   - **Name**: `array-handling-api-remote`
   - **Environment**: Node
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Plan**: Free

4. **Environment Variables** (Auto-configured)
   - `NODE_VERSION`: 18.0.0
   - `PORT`: 10000

### After Deployment

Your MCP server will be available at:
- **MCP Endpoint**: `https://array-handling-api-remote.onrender.com/mcp`
- **Health Check**: `https://array-handling-api-remote.onrender.com/health`
- **Root**: `https://array-handling-api-remote.onrender.com/`

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
curl https://array-handling-api-remote.onrender.com/health
```

Test with the provided script:
```bash
node test-mcp-connection.js
```

Or use the shell script:
```bash
chmod +x test-tool-call.sh
./test-tool-call.sh https://array-handling-api-remote.onrender.com
```

## MCP Client Configuration

Add to your MCP client settings:

```json
{
  "mcpServers": {
    "array-handling-api": {
      "url": "https://array-handling-api-remote.onrender.com/mcp",
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

## Test Case Information

- **Test Case**: TC-P0-API-002
- **Purpose**: Validate raw array handling with react-intrinsic style
- **Agent Style**: react-intrinsic
- **Model**: gpt-oss-120b
- **Priority**: P0 (Critical)
- **Automation**: Automated

## Related Resources

- **OpenAPI Spec**: `Test_data_tools/OpenAPI/array-handling/openapi_array_handling_raw.yaml`
- **Backend API**: Complex Tools OpenAPI Server
- **Test Utterances**: `Test_data_tools/OpenAPI/array-handling/TEST_UTTERANCES.md`

## License

MIT

---

Made with Bob