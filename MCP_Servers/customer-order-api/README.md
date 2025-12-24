# Customer Order API MCP Server

MCP Server for the Customer Order Processing API with deeply nested schemas. This server provides tools to process customer orders with complete nested information including customer details, shipping/billing addresses, and product specifications.

## Features

- **Deep Nesting Support**: Handles nested data structures up to 6 levels deep
- **Schema References**: Supports reusable schema components via $ref
- **Complete Order Processing**: Processes customer information, order details, and product specifications
- **Production Ready**: Connects to deployed API on Render.com

## API Endpoint

- **Base URL**: `https://complex-tools-openapi.onrender.com/api/v1`
- **Endpoint**: `POST /orders/process`

## Available Tools

### process_customer_order

Process a customer order with complete nested information.

**Input Schema:**
```json
{
  "customer": {
    "name": "string (required)",
    "email": "string (optional)",
    "address": {
      "street": "string",
      "city": "string",
      "state": "string",
      "zipcode": "string",
      "country": "string"
    },
    "contact": {
      "phone": "string",
      "mobile": "string"
    }
  },
  "order": {
    "order_id": "string (required)",
    "order_date": "string (YYYY-MM-DD)",
    "items": [
      {
        "product": {
          "product_id": "string",
          "name": "string (required)",
          "details": {
            "description": "string",
            "specifications": {
              "weight": "string",
              "dimensions": "string",
              "material": "string"
            }
          }
        },
        "quantity": "integer (min: 1)",
        "price": "number (min: 0)"
      }
    ],
    "shipping_address": { /* Address object */ },
    "billing_address": { /* Address object */ }
  }
}
```

**Output:**
Returns a formatted order confirmation with:
- Customer details
- Order summary
- Item details with subtotals
- Total amount
- Formatted addresses
- Confirmation message

## Installation

```bash
npm install
```

## Building

```bash
npm run build
```

## Usage with Claude Desktop

Add to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "customer-order-api": {
      "command": "node",
      "args": ["/absolute/path/to/customer-order-api/build/index.js"]
    }
  }
}
```

## Usage with Watson Orchestrate

1. Import the MCP server zip file into Watson Orchestrate
2. Configure the server connection
3. Use the `process_customer_order` tool in your skills

## Example Usage

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
    }
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
            "description": "High-performance laptop for professionals",
            "specifications": {
              "weight": "1.5 kg",
              "dimensions": "35cm x 25cm x 2cm",
              "material": "Aluminum alloy"
            }
          }
        },
        "quantity": 1,
        "price": 1299.99
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
    }
  }
}
```

## Nested Schema Structure

This API demonstrates various levels of nesting:

1. **Level 1**: OrderRequest (customer, order)
2. **Level 2**: Customer (name, email, address, contact), Order (order_id, items, addresses)
3. **Level 3**: Address, Contact, OrderItem
4. **Level 4**: Product
5. **Level 5**: ProductDetails
6. **Level 6**: ProductSpecifications (deepest level)

## Error Handling

The server handles various error scenarios:
- Invalid request data (400)
- API connection errors
- Timeout errors (30 second timeout)
- Server errors (500)

All errors are returned with detailed information including error code and description.

## Development

Watch mode for development:
```bash
npm run watch
```

## License

MIT

## Author

IBM Bob

---

Made with Bob