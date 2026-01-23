#!/usr/bin/env node

/**
 * Test script to verify MCP server initialization and list tools
 * Tests the HTTP connection and MCP protocol handshake
 */

import fetch from 'node-fetch';

const MCP_URL = process.env.TEST_URL || 'http://localhost:3456/mcp';

console.log('Testing MCP Server Connection...\n');
console.log('MCP URL:', MCP_URL);
console.log('---\n');

let messageId = 1;

async function testMCPServer() {
    try {
        // Step 1: Initialize
        console.log('Step 1: Sending initialize request...');
        const initRequest = {
            jsonrpc: '2.0',
            id: messageId++,
            method: 'initialize',
            params: {
                protocolVersion: '2024-11-05',
                capabilities: {
                    roots: {
                        listChanged: true
                    }
                },
                clientInfo: {
                    name: 'test-client',
                    version: '1.0.0'
                }
            }
        };

        const initResponse = await fetch(MCP_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(initRequest)
        });

        if (!initResponse.ok) {
            throw new Error(`Initialize failed: ${initResponse.status} ${initResponse.statusText}`);
        }

        const initData = await initResponse.json();
        console.log('✓ Initialize successful!');
        console.log('Server info:', JSON.stringify(initData.result.serverInfo, null, 2));

        // Step 2: List tools
        console.log('\nStep 2: Sending tools/list request...');
        const listToolsRequest = {
            jsonrpc: '2.0',
            id: messageId++,
            method: 'tools/list',
            params: {}
        };

        const toolsResponse = await fetch(MCP_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(listToolsRequest)
        });

        if (!toolsResponse.ok) {
            throw new Error(`List tools failed: ${toolsResponse.status} ${toolsResponse.statusText}`);
        }

        const toolsData = await toolsResponse.json();
        console.log('✓ Tools list received!');

        if (toolsData.result.tools) {
            console.log(`\nFound ${toolsData.result.tools.length} tool(s):`);
            toolsData.result.tools.forEach((tool, idx) => {
                console.log(`\n  Tool ${idx + 1}:`);
                console.log(`    Name: ${tool.name}`);
                console.log(`    Description: ${tool.description.substring(0, 100)}...`);
            });
        }

        console.log('\n✅ Test completed successfully!');
        process.exit(0);

    } catch (error) {
        console.error('\n✗ Error:', error.message);
        if (error.stack) {
            console.error('Stack:', error.stack);
        }
        process.exit(1);
    }
}

// Run the test
testMCPServer();

// Made with Bob