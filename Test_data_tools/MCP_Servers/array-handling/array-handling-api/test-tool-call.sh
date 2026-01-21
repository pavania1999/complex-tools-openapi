#!/bin/bash

# Test script for array-handling MCP server
# This script tests the MCP server by sending tool call requests

SERVER_PATH="./build/index.js"

echo "=== Testing Array Handling MCP Server ==="
echo ""

# Test 1: Wrapped Inventory (Single Item)
echo "Test 1: Processing single inventory item (wrapped array)..."
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"process_inventory_items_wrapped","arguments":{"items":[{"name":"Laptop","sku":"LAP-001","quantity":5,"price":999.99,"category":"Electronics","specifications":{"brand":"TechCorp","model":"Pro-X1","warranty":"2 years"}}]}}}' | node "$SERVER_PATH"
echo ""
echo "---"
echo ""

# Test 2: Wrapped Inventory (Multiple Items)
echo "Test 2: Processing multiple inventory items (wrapped array)..."
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"process_inventory_items_wrapped","arguments":{"items":[{"name":"Laptop","sku":"LAP-001","quantity":5,"price":999.99,"category":"Electronics","specifications":{"brand":"TechCorp","model":"Pro-X1","warranty":"2 years"}},{"name":"Mouse","sku":"MOU-002","quantity":20,"price":29.99,"category":"Accessories","specifications":{"brand":"TechCorp","model":"Wireless-M2","warranty":"1 year"}}]}}}' | node "$SERVER_PATH"
echo ""
echo "---"
echo ""

# Test 3: Raw Inventory (Single Item)
echo "Test 3: Processing single inventory item (raw array)..."
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"process_inventory_items_raw","arguments":{"items":[{"name":"Monitor","sku":"MON-004","quantity":3,"price":299.99,"category":"Electronics","specifications":{"brand":"ViewTech","model":"UHD-27","warranty":"3 years"}}]}}}' | node "$SERVER_PATH"
echo ""
echo "---"
echo ""

# Test 4: Wrapped Batch Orders
echo "Test 4: Processing batch orders (wrapped array with nested items)..."
echo '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"process_batch_orders_wrapped","arguments":{"orders":[{"order_id":"ORD-001","customer_name":"John Doe","items":[{"product_name":"Laptop","quantity":1,"unit_price":999.99},{"product_name":"Mouse","quantity":2,"unit_price":29.99}]},{"order_id":"ORD-002","customer_name":"Jane Smith","items":[{"product_name":"Monitor","quantity":1,"unit_price":299.99}]}]}}}' | node "$SERVER_PATH"
echo ""
echo "---"
echo ""

echo "=== All tests completed ==="

# Made with Bob
