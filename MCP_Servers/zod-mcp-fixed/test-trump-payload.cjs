#!/usr/bin/env node

/**
 * Test script for zod-mcp-fixed MCP server with Trump screening payload
 */

const { spawn } = require('child_process');
const path = require('path');

// Test payload for Trump screening
const testPayload = {
    "alerts": [
        {
            "address": [
                {
                    "addr1": "White House",
                    "city": "Washington",
                    "country": "US",
                    "countryCode": {
                        "countryCodeValue": "US"
                    },
                    "postalCode": "20500",
                    "stateProv": "DC"
                }
            ],
            "alertConfidence": 0,
            "alias": [],
            "bvdId": null,
            "custom_id": "trump-pep-001",
            "deceased": {
                "date": null,
                "val": false
            },
            "dob": [
                "1946-06-14"
            ],
            "entityId": "placeholder",
            "entityType": "person",
            "events": [],
            "identification": [],
            "images": [],
            "name": "Donald J Trump",
            "nationality": []
        }
    ],
    "inquiry": {
        "address": {
            "addr1": "White House",
            "city": "Washington",
            "country": "US",
            "countryCode": {
                "countryCodeValue": "US"
            },
            "postalCode": "20500",
            "stateProv": "DC"
        },
        "dob": "1946-06-14",
        "entityType": "person",
        "name": "Donald J Trump"
    },
    "name": "Screen Donald J Trump"
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
        name: "searchAndWait",
        arguments: testPayload
    }
};

// Start the MCP server
const serverPath = path.join(__dirname, 'server.js');
console.log('Starting MCP server:', serverPath);
console.log('Test payload:', JSON.stringify(testPayload, null, 2));

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
    console.log(`\nServer exited with code ${code}`);
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
    server.stdin.write(JSON.stringify(callToolRequest) + '\n');
}, 2500);

setTimeout(() => {
    console.log('\n=== Test complete, closing server ===');
    server.kill();
    process.exit(0);
}, 8000);

// Made with Bob
