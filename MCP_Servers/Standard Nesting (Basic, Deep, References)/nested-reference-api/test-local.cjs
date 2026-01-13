#!/usr/bin/env node

/**
 * Local test script for nested-reference-api MCP server
 */

const { spawn } = require('child_process');
const path = require('path');

// Test payload
const testPayload = {
    "customer": {
        "address": {
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "street": "123 Main Street",
            "zipcode": "94102"
        },
        "contact": {
            "mobile": "+1-415-555-0101",
            "phone": "+1-415-555-0100"
        },
        "email": "john.doe@example.com",
        "name": "John Doe update"
    },
    "order": {
        "billing_address": {
            "city": "Seattle",
            "country": "USA",
            "state": "WA",
            "street": "789 Payment Boulevard",
            "zipcode": "98101"
        },
        "items": [
            {
                "price": 599.99,
                "product": {
                    "details": {
                        "description": "Testing nested schema with address references",
                        "specifications": {
                            "dimensions": "40cm x 30cm x 5cm",
                            "material": "Carbon fiber composite",
                            "weight": "2.5 kg"
                        }
                    },
                    "name": "Test Product Alpha",
                    "product_id": "PROD-TEST-001"
                },
                "quantity": 2
            },
            {
                "price": 299.99,
                "product": {
                    "details": {
                        "description": "Additional product to test multiple items",
                        "specifications": {
                            "dimensions": "15cm x 10cm x 3cm",
                            "material": "Titanium alloy",
                            "weight": "0.8 kg"
                        }
                    },
                    "name": "Test Product Beta",
                    "product_id": "PROD-TEST-002"
                },
                "quantity": 1
            }
        ],
        "order_date": "2024-12-23",
        "order_id": "ORD-2024-TEST-001",
        "shipping_address": {
            "city": "Los Angeles",
            "country": "USA",
            "state": "CA",
            "street": "456 Delivery Lane",
            "zipcode": "90001"
        }
    }
};

// MCP protocol messages
const initializeRequest = {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
        protocolVersion: "2024-11-05",
        capabilities: {},
        clientInfo: {
            name: "test-client",
            version: "1.0.0"
        }
    }
};

const listToolsRequest = {
    jsonrpc: "2.0",
    id: 2,
    method: "tools/list",
    params: {}
};

const callToolRequest = {
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
        name: "process_order_internal_ref",
        arguments: testPayload
    }
};

// Start the MCP server
const serverPath = path.join(__dirname, 'build', 'index.js');
console.log('Starting MCP server:', serverPath);

const server = spawn('node', [serverPath], {
    stdio: ['pipe', 'pipe', 'pipe']
});

let responseBuffer = '';

server.stdout.on('data', (data) => {
    responseBuffer += data.toString();

    // Try to parse complete JSON-RPC messages
    const lines = responseBuffer.split('\n');
    responseBuffer = lines.pop(); // Keep incomplete line in buffer

    lines.forEach(line => {
        if (line.trim()) {
            try {
                const response = JSON.parse(line);
                console.log('\n=== Response ===');
                console.log(JSON.stringify(response, null, 2));
            } catch (e) {
                console.log('Raw output:', line);
            }
        }
    });
});

server.stderr.on('data', (data) => {
    console.error('Server stderr:', data.toString());
});

server.on('close', (code) => {
    console.log(`Server exited with code ${code}`);
});

// Send requests
setTimeout(() => {
    console.log('\n=== Sending initialize request ===');
    server.stdin.write(JSON.stringify(initializeRequest) + '\n');
}, 500);

setTimeout(() => {
    console.log('\n=== Sending list tools request ===');
    server.stdin.write(JSON.stringify(listToolsRequest) + '\n');
}, 1500);

setTimeout(() => {
    console.log('\n=== Sending call tool request ===');
    console.log('Payload:', JSON.stringify(testPayload, null, 2));
    server.stdin.write(JSON.stringify(callToolRequest) + '\n');
}, 2500);

setTimeout(() => {
    console.log('\n=== Test complete, closing server ===');
    server.kill();
    process.exit(0);
}, 5000);

// Made with Bob
