#!/bin/bash

# Test script for employee-registration MCP server
# This script tests the MCP server by sending tool call requests

SERVER_PATH="./build/index.js"

echo "=== Testing Employee Registration MCP Server ==="
echo ""

# Test 1: Register employee with manager (2-level hierarchy)
echo "Test 1: Registering employee with direct manager..."
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"register_employee","arguments":{"employee":{"name":"Sarah Martinez","employee_id":"EMP-201","email":"sarah.martinez@company.com","phone":"+1-555-0201","department":"Engineering","position":"Software Engineer","start_date":"2024-02-01","manager":{"name":"Michael Chen","employee_id":"EMP-150","email":"michael.chen@company.com","phone":"+1-555-0150","department":"Engineering","position":"Engineering Manager","start_date":"2022-05-15"}}}}}' | node "$SERVER_PATH"
echo ""
echo "---"
echo ""

# Test 2: Register employee with 3-level hierarchy (employee -> manager -> manager's manager)
echo "Test 2: Registering employee with 3-level management hierarchy..."
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"register_employee","arguments":{"employee":{"name":"Alex Johnson","employee_id":"EMP-202","email":"alex.johnson@company.com","phone":"+1-555-0202","department":"Engineering","position":"Junior Developer","start_date":"2024-03-01","manager":{"name":"Sarah Martinez","employee_id":"EMP-201","email":"sarah.martinez@company.com","phone":"+1-555-0201","department":"Engineering","position":"Software Engineer","start_date":"2024-02-01","manager":{"name":"Michael Chen","employee_id":"EMP-150","email":"michael.chen@company.com","phone":"+1-555-0150","department":"Engineering","position":"Engineering Manager","start_date":"2022-05-15"}}}}}}' | node "$SERVER_PATH"
echo ""
echo "---"
echo ""

# Test 3: Register employee without manager (top-level executive)
echo "Test 3: Registering top-level executive without manager..."
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"register_employee","arguments":{"employee":{"name":"Jennifer Williams","employee_id":"EMP-001","email":"jennifer.williams@company.com","phone":"+1-555-0001","department":"Executive","position":"Chief Technology Officer","start_date":"2020-01-15"}}}}' | node "$SERVER_PATH"
echo ""
echo "---"
echo ""

# Test 4: Register employee in different department with manager
echo "Test 4: Registering employee in Sales department..."
echo '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"register_employee","arguments":{"employee":{"name":"David Brown","employee_id":"EMP-301","email":"david.brown@company.com","phone":"+1-555-0301","department":"Sales","position":"Sales Representative","start_date":"2024-01-10","manager":{"name":"Lisa Anderson","employee_id":"EMP-250","email":"lisa.anderson@company.com","phone":"+1-555-0250","department":"Sales","position":"Sales Manager","start_date":"2021-06-01"}}}}}' | node "$SERVER_PATH"
echo ""
echo "---"
echo ""

echo "=== All tests completed ==="

# Made with Bob