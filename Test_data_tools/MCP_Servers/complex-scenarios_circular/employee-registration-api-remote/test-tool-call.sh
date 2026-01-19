#!/bin/bash

# Test the tool call endpoint
BASE_URL="${1:-http://localhost:3457}"

echo "=========================================="
echo "Testing MCP Tool Call"
echo "Base URL: $BASE_URL"
echo "=========================================="
echo ""

# Test tool call with payload
echo "Test: Call register_employee tool"
echo "-------------------------------------------------------"
curl -X POST "$BASE_URL/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "register_employee",
      "arguments": {
        "employee": {
          "name": "Sarah Martinez",
          "employee_id": "EMP-201",
          "email": "sarah.martinez@company.com",
          "phone": "+1-555-0201",
          "department": "Engineering",
          "position": "Software Engineer",
          "start_date": "2024-02-01",
          "manager": {
            "name": "Michael Chen",
            "employee_id": "EMP-150",
            "email": "michael.chen@company.com",
            "phone": "+1-555-0150",
            "department": "Engineering",
            "position": "Engineering Manager",
            "start_date": "2022-05-15"
          }
        }
      }
    }
  }' | jq '.'

echo ""
echo "=========================================="
echo "Test Complete"
echo "=========================================="

# Made with Bob