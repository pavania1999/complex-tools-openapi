#!/bin/bash

# Test script for Enum Nested API Remote MCP Server
# Tests both tools with various valid and invalid enum values

SERVER_URL="http://localhost:3457/mcp"

echo "=========================================="
echo "Enum Nested API - MCP Server Test Suite"
echo "=========================================="
echo ""

# Test 1: Valid Account Status
echo "Test 1: Valid Account Status (active, personal)"
curl -X POST $SERVER_URL \
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
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 2: Invalid Account Status
echo "Test 2: Invalid Account Status (pending - should fail)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "update_account_status",
      "arguments": {
        "account_id": "ACC-12345",
        "status": "pending",
        "type": "personal"
      }
    }
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 3: Invalid Account Type
echo "Test 3: Invalid Account Type (enterprise - should fail)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "update_account_status",
      "arguments": {
        "account_id": "ACC-12345",
        "status": "active",
        "type": "enterprise"
      }
    }
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 4: Valid Multi-Level Enum Profile
echo "Test 4: Valid Multi-Level Enum Profile (all enums valid)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
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
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 5: Invalid Profile Status
echo "Test 5: Invalid Profile Status (pending - should fail)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 5,
    "method": "tools/call",
    "params": {
      "name": "create_customer_profile_multi_level",
      "arguments": {
        "profile_id": "PROF-002",
        "status": "pending",
        "customer": {
          "name": "Bob Smith",
          "email": "bob@example.com",
          "type": "individual",
          "address": {
            "street": "456 Pine St",
            "city": "Portland",
            "state": "OR",
            "zipcode": "97201",
            "country": "US"
          }
        }
      }
    }
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 6: Invalid Customer Type
echo "Test 6: Invalid Customer Type (government - should fail)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 6,
    "method": "tools/call",
    "params": {
      "name": "create_customer_profile_multi_level",
      "arguments": {
        "profile_id": "PROF-003",
        "status": "active",
        "customer": {
          "name": "Charlie Brown",
          "email": "charlie@example.com",
          "type": "government",
          "address": {
            "street": "789 Elm St",
            "city": "Vancouver",
            "state": "BC",
            "zipcode": "V6B 1A1",
            "country": "CA"
          }
        }
      }
    }
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 7: Invalid Country
echo "Test 7: Invalid Country (FR - should fail)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 7,
    "method": "tools/call",
    "params": {
      "name": "create_customer_profile_multi_level",
      "arguments": {
        "profile_id": "PROF-004",
        "status": "active",
        "customer": {
          "name": "Diana Prince",
          "email": "diana@example.com",
          "type": "individual",
          "address": {
            "street": "101 Hero Lane",
            "city": "Paris",
            "state": "IDF",
            "zipcode": "75001",
            "country": "FR"
          }
        }
      }
    }
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 8: Invalid Contact Preference
echo "Test 8: Invalid Contact Preference (fax - should fail)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 8,
    "method": "tools/call",
    "params": {
      "name": "create_customer_profile_multi_level",
      "arguments": {
        "profile_id": "PROF-005",
        "status": "active",
        "customer": {
          "name": "Eve Adams",
          "email": "eve@example.com",
          "type": "corporate",
          "address": {
            "street": "202 Business Blvd",
            "city": "London",
            "state": "ENG",
            "zipcode": "SW1A 1AA",
            "country": "UK"
          },
          "contact": {
            "phone": "+44-20-7946-0958",
            "preference": "fax",
            "timezone": "GMT"
          }
        }
      }
    }
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 9: Multiple Invalid Enums
echo "Test 9: Multiple Invalid Enums (should report all failures)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 9,
    "method": "tools/call",
    "params": {
      "name": "create_customer_profile_multi_level",
      "arguments": {
        "profile_id": "PROF-006",
        "status": "suspended",
        "customer": {
          "name": "Frank Miller",
          "email": "frank@example.com",
          "type": "nonprofit",
          "address": {
            "street": "303 Charity Circle",
            "city": "Berlin",
            "state": "BE",
            "zipcode": "10115",
            "country": "DE"
          },
          "contact": {
            "phone": "+49-30-1234-5678",
            "preference": "mail",
            "timezone": "CET"
          }
        }
      }
    }
  }' | jq '.'
echo ""
echo "----------------------------------------"
echo ""

# Test 10: Valid Profile Without Contact
echo "Test 10: Valid Profile Without Contact (optional field)"
curl -X POST $SERVER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 10,
    "method": "tools/call",
    "params": {
      "name": "create_customer_profile_multi_level",
      "arguments": {
        "profile_id": "PROF-007",
        "status": "inactive",
        "customer": {
          "name": "Grace Hopper",
          "email": "grace@example.com",
          "type": "corporate",
          "address": {
            "street": "404 Tech Drive",
            "city": "Toronto",
            "state": "ON",
            "zipcode": "M5H 2N2",
            "country": "CA"
          }
        }
      }
    }
  }' | jq '.'
echo ""
echo "=========================================="
echo "Test Suite Complete"
echo "=========================================="

# Made with Bob