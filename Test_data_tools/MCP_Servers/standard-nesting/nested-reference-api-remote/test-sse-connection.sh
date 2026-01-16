#!/bin/bash

# Test script for SSE MCP connection
# This script tests the complete MCP over SSE flow

BASE_URL="${1:-https://nested-reference-api-remote-mcp.onrender.com}"

echo "=========================================="
echo "Testing MCP Server SSE Connection"
echo "Base URL: $BASE_URL"
echo "=========================================="
echo ""

# Test 1: Health check
echo "Test 1: Health Check"
echo "--------------------"
curl -s "$BASE_URL/health" | jq '.' || echo "Health check failed"
echo ""
echo ""

# Test 2: Root endpoint
echo "Test 2: Root Endpoint"
echo "--------------------"
curl -s "$BASE_URL/" | jq '.' || echo "Root endpoint failed"
echo ""
echo ""

# Test 3: SSE Connection (with timeout)
echo "Test 3: SSE Connection (5 second test)"
echo "---------------------------------------"
echo "Establishing SSE connection..."
timeout 5 curl -N -v "$BASE_URL/sse" 2>&1 | head -30
echo ""
echo "SSE connection test complete (connection should stay open)"
echo ""
echo ""

# Test 4: Initialize request
echo "Test 4: MCP Initialize Request"
echo "-------------------------------"
echo "Note: This requires an active SSE connection"
echo "Sending initialize request..."
curl -X POST "$BASE_URL/message" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {
        "name": "test-client",
        "version": "1.0.0"
      }
    }
  }' 2>&1
echo ""
echo ""

# Test 5: Tools list request
echo "Test 5: MCP Tools List Request"
echo "-------------------------------"
echo "Note: This requires an active SSE connection"
echo "Sending tools/list request..."
curl -X POST "$BASE_URL/message" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }' 2>&1
echo ""
echo ""

echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo ""
echo "Expected Results:"
echo "1. ✅ Health check returns status 'ok'"
echo "2. ✅ Root endpoint returns server info"
echo "3. ✅ SSE connection establishes (Content-Type: text/event-stream)"
echo "4. ⚠️  Initialize/tools requests need active SSE (may show 404)"
echo ""
echo "To properly test MCP protocol:"
echo "1. Use an MCP client (like the test-mcp-connection.js script)"
echo "2. Or manually: Open SSE in one terminal, send POST in another"
echo ""
echo "For full integration test, run:"
echo "  node test-mcp-connection.js"
echo ""

# Made with Bob
