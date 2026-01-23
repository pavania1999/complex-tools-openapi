#!/bin/bash

# Test the tool call endpoint locally
BASE_URL="${1:-http://localhost:3456}"

echo "=========================================="
echo "Testing MCP Tool Calls - Array Handling"
echo "Base URL: $BASE_URL"
echo "=========================================="
echo ""

# Test 1: Process Inventory Items (Raw Array)
echo "Test 1: Call process_inventory_items_raw tool"
echo "-------------------------------------------------------"
curl -X POST "$BASE_URL/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "process_inventory_items_raw",
      "arguments": {
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
      }
    }
  }' | jq '.'

echo ""
echo ""

# Test 2: Process Batch Orders (Raw Array)
echo "Test 2: Call process_batch_orders_raw tool"
echo "-------------------------------------------------------"
curl -X POST "$BASE_URL/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "process_batch_orders_raw",
      "arguments": {
        "orders": [
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
      }
    }
  }' | jq '.'

echo ""
echo "=========================================="
echo "Test Complete"
echo "=========================================="

# Made with Bob