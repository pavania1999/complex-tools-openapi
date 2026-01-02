#!/bin/bash

# Test Script for TC-P0-API-002: Array Handling API
# This script tests both wrapped and raw array endpoints

BASE_URL="http://localhost:8002/api/v1"
HEALTH_URL="http://localhost:8002/health"

echo "=========================================="
echo "TC-P0-API-002: Array Handling API Tests"
echo "=========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print test header
print_test() {
    echo ""
    echo "${YELLOW}=========================================="
    echo "TEST: $1"
    echo "==========================================${NC}"
    echo ""
}

# Function to print success
print_success() {
    echo "${GREEN}✓ $1${NC}"
}

# Function to print error
print_error() {
    echo "${RED}✗ $1${NC}"
}

# Check if server is running
print_test "Health Check"
response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)
if [ $response -eq 200 ]; then
    print_success "Server is running"
    curl -s $HEALTH_URL | jq '.'
else
    print_error "Server is not running on port 8002"
    echo "Please start the server with: python process_array_handling.py"
    exit 1
fi

# Test 1: Wrapped Array - Single Item
print_test "1. Wrapped Array - Single Item"
curl -s -X POST $BASE_URL/inventory/process-items \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | jq '.'

# Test 2: Wrapped Array - Multiple Items
print_test "2. Wrapped Array - Multiple Items"
curl -s -X POST $BASE_URL/inventory/process-items \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | jq '.'

# Test 3: Raw Array - Single Item
print_test "3. Raw Array - Single Item"
curl -s -X POST $BASE_URL/inventory/process-items-raw \
  -H "Content-Type: application/json" \
  -d '[
    {
      "name": "Monitor",
      "sku": "MON-004",
      "quantity": 3,
      "price": 299.99,
      "category": "Electronics",
      "specifications": {
        "brand": "ViewTech",
        "model": "UHD-27",
        "warranty": "3 years"
      }
    }
  ]' | jq '.'

# Test 4: Raw Array - Multiple Items
print_test "4. Raw Array - Multiple Items"
curl -s -X POST $BASE_URL/inventory/process-items-raw \
  -H "Content-Type: application/json" \
  -d '[
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
  ]' | jq '.'

# Test 5: Wrapped Batch Orders
print_test "5. Wrapped Batch Orders (Nested Arrays)"
curl -s -X POST $BASE_URL/orders/process-batch \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | jq '.'

# Test 6: Raw Batch Orders
print_test "6. Raw Batch Orders (Nested Arrays)"
curl -s -X POST $BASE_URL/orders/process-batch-raw \
  -H "Content-Type: application/json" \
  -d '[
    {
      "order_id": "ORD-003",
      "customer_name": "Bob Wilson",
      "items": [
        {
          "product_name": "Keyboard",
          "quantity": 1,
          "unit_price": 79.99
        },
        {
          "product_name": "Mouse",
          "quantity": 1,
          "unit_price": 29.99
        }
      ]
    },
    {
      "order_id": "ORD-004",
      "customer_name": "Alice Brown",
      "items": [
        {
          "product_name": "Laptop",
          "quantity": 2,
          "unit_price": 999.99
        }
      ]
    }
  ]' | jq '.'

# Test 7: Error Handling - Missing Required Field
print_test "7. Error Handling - Missing Required Field (SKU)"
curl -s -X POST $BASE_URL/inventory/process-items \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "name": "Laptop",
        "quantity": 5,
        "price": 999.99,
        "category": "Electronics"
      }
    ]
  }' | jq '.'

# Test 8: Error Handling - Invalid Data Type
print_test "8. Error Handling - Missing Items Array"
curl -s -X POST $BASE_URL/inventory/process-items \
  -H "Content-Type: application/json" \
  -d '{
    "data": []
  }' | jq '.'

# Test 9: Error Handling - Empty Array
print_test "9. Edge Case - Empty Array"
curl -s -X POST $BASE_URL/inventory/process-items \
  -H "Content-Type: application/json" \
  -d '{
    "items": []
  }' | jq '.'

echo ""
echo "${GREEN}=========================================="
echo "All tests completed!"
echo "==========================================${NC}"
echo ""
echo "Summary:"
echo "- Tested wrapped array endpoints"
echo "- Tested raw array endpoints"
echo "- Tested nested arrays"
echo "- Tested error handling"
echo ""
echo "For more tests, see TEST_UTTERANCES.md"

# Made with Bob
