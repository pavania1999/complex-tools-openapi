#!/bin/bash

# Test script for Address schema references in openapi_customer_order_deployed.yaml
# This tests that the Address schema ($ref: '#/components/schemas/Address') 
# is properly processed in three different locations:
# 1. customer.address
# 2. order.shipping_address  
# 3. order.billing_address

echo "=========================================="
echo "Testing Address Schema References"
echo "=========================================="
echo ""
echo "API Endpoint: https://complex-tools-openapi.onrender.com/api/v1/orders/process"
echo ""
echo "The Address schema is referenced in 3 places:"
echo "  1. Customer Address (customer.address)"
echo "  2. Shipping Address (order.shipping_address)"
echo "  3. Billing Address (order.billing_address)"
echo ""
echo "Test Payload:"
echo "  - Customer Address: 123 Main Street, San Francisco, CA 94102, USA"
echo "  - Shipping Address: 456 Delivery Lane, Los Angeles, CA 90001, USA"
echo "  - Billing Address: 789 Payment Boulevard, Seattle, WA 98101, USA"
echo ""
echo "=========================================="
echo "Sending POST request..."
echo "=========================================="
echo ""

response=$(curl -X POST \
  https://complex-tools-openapi.onrender.com/api/v1/orders/process \
  -H "Content-Type: application/json" \
  -d @nested_schemas/test_address_schema_payload.json \
  -w "\n%{http_code}" \
  -s)

# Extract HTTP status code (last line)
http_code=$(echo "$response" | tail -n 1)
# Extract JSON response (all but last line)
json_response=$(echo "$response" | head -n -1)

# Pretty print JSON
echo "$json_response" | jq '.'

echo ""
echo "HTTP Status Code: $http_code"

echo ""
echo "=========================================="
echo "Test Complete"
echo "=========================================="
echo ""
echo "Expected Response Fields:"
echo "  - customer_address: Should format customer.address"
echo "  - shipping_address: Should format order.shipping_address"
echo "  - billing_address: Should format order.billing_address"
echo ""
echo "All three addresses should be properly formatted as:"
echo "  'street, city, state, zipcode, country'"

# Made with Bob
