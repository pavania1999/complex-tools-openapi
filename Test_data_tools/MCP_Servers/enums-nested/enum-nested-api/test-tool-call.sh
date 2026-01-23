#!/bin/bash

# Test script for enum-nested-api MCP Server
# Tests both tools with various payloads

echo "=== Testing Enum Nested API MCP Server ==="
echo ""

# Load test payloads
PAYLOADS_FILE="test-payload.json"

if [ ! -f "$PAYLOADS_FILE" ]; then
    echo "Error: $PAYLOADS_FILE not found"
    exit 1
fi

# Test 1: Valid account status update
echo "Test 1: Valid account status update"
echo "-----------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"update_account_status","arguments":{"account_id":"ACC-12345","status":"active","type":"personal"}}}
EOF
echo ""
echo ""

# Test 2: Invalid account status (should fail)
echo "Test 2: Invalid account status (should fail)"
echo "--------------------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"update_account_status","arguments":{"account_id":"ACC-12345","status":"pending","type":"personal"}}}
EOF
echo ""
echo ""

# Test 3: Invalid account type (should fail)
echo "Test 3: Invalid account type (should fail)"
echo "------------------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"update_account_status","arguments":{"account_id":"ACC-12345","status":"active","type":"enterprise"}}}
EOF
echo ""
echo ""

# Test 4: Valid multi-level profile with all enums
echo "Test 4: Valid multi-level profile with all enums"
echo "------------------------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"create_customer_profile_multi_level","arguments":{"profile_id":"PROF-001","status":"active","customer":{"name":"Alice Johnson","email":"alice@example.com","type":"individual","address":{"street":"321 Oak Ave","city":"Seattle","state":"WA","zipcode":"98101","country":"US"},"contact":{"phone":"+1-206-555-0300","preference":"email","timezone":"PST"}}}}}
EOF
echo ""
echo ""

# Test 5: Invalid profile status (should fail)
echo "Test 5: Invalid profile status (should fail)"
echo "--------------------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"create_customer_profile_multi_level","arguments":{"profile_id":"PROF-002","status":"pending","customer":{"name":"Bob Smith","email":"bob@example.com","type":"individual","address":{"street":"456 Pine St","city":"Portland","state":"OR","zipcode":"97201","country":"US"}}}}}
EOF
echo ""
echo ""

# Test 6: Invalid customer type (should fail)
echo "Test 6: Invalid customer type (should fail)"
echo "-------------------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"create_customer_profile_multi_level","arguments":{"profile_id":"PROF-003","status":"active","customer":{"name":"Charlie Brown","email":"charlie@example.com","type":"government","address":{"street":"789 Elm St","city":"Vancouver","state":"BC","zipcode":"V6B 1A1","country":"CA"}}}}}
EOF
echo ""
echo ""

# Test 7: Invalid country (should fail)
echo "Test 7: Invalid country (should fail)"
echo "-------------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"create_customer_profile_multi_level","arguments":{"profile_id":"PROF-004","status":"active","customer":{"name":"Diana Prince","email":"diana@example.com","type":"individual","address":{"street":"101 Hero Lane","city":"Paris","state":"IDF","zipcode":"75001","country":"FR"}}}}}
EOF
echo ""
echo ""

# Test 8: Invalid contact preference (should fail)
echo "Test 8: Invalid contact preference (should fail)"
echo "------------------------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"create_customer_profile_multi_level","arguments":{"profile_id":"PROF-005","status":"active","customer":{"name":"Eve Adams","email":"eve@example.com","type":"corporate","address":{"street":"202 Business Blvd","city":"London","state":"ENG","zipcode":"SW1A 1AA","country":"UK"},"contact":{"phone":"+44-20-7946-0958","preference":"fax","timezone":"GMT"}}}}}
EOF
echo ""
echo ""

# Test 9: Valid profile without contact (optional field)
echo "Test 9: Valid profile without contact (optional field)"
echo "------------------------------------------------------"
node build/index.js << 'EOF'
{"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"create_customer_profile_multi_level","arguments":{"profile_id":"PROF-007","status":"inactive","customer":{"name":"Grace Hopper","email":"grace@example.com","type":"corporate","address":{"street":"404 Tech Drive","city":"Toronto","state":"ON","zipcode":"M5H 2N2","country":"CA"}}}}}
EOF
echo ""
echo ""

echo "=== All tests completed ==="

# Made with Bob
