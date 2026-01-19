#!/usr/bin/env node

/**
 * Test script to verify MCP server initialization and list tools
 * Tests the HTTP connection and MCP protocol handshake
 */

import fetch from 'node-fetch';

const BASE_URL = process.env.TEST_URL || 'http://localhost:3457';
const MCP_URL = `${BASE_URL}/mcp`;

console.log('Testing MCP Server Connection...\n');
console.log('Base URL:', BASE_URL);
console.log('MCP URL:', MCP_URL);
console.log('---\n');

let messageId = 1;

async function testMCPServer() {
    try {
        // Step 1: Test health endpoint
        console.log('Step 1: Testing health endpoint...');
        const healthResponse = await fetch(`${BASE_URL}/health`);
        const healthData = await healthResponse.json();
        console.log('✓ Health check passed');
        console.log('  Status:', healthData.status);
        console.log('  Service:', healthData.service);
        console.log();

        // Step 2: Send initialize request
        console.log('Step 2: Sending initialize request...');
        const initRequest = {
            jsonrpc: '2.0',
            id: messageId++,
            method: 'initialize',
            params: {
                protocolVersion: '2024-11-05',
                capabilities: {},
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

        const initData = await initResponse.json();

        if (initData.error) {
            console.error('✗ Initialize failed:', initData.error);
            process.exit(1);
        }

        console.log('✓ Initialize successful');
        console.log('  Protocol version:', initData.result.protocolVersion);
        console.log('  Server name:', initData.result.serverInfo.name);
        console.log('  Server version:', initData.result.serverInfo.version);
        console.log();

        // Step 3: Send tools/list request
        console.log('Step 3: Sending tools/list request...');
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

        const toolsData = await toolsResponse.json();

        if (toolsData.error) {
            console.error('✗ Tools list failed:', toolsData.error);
            process.exit(1);
        }

        console.log('✓ Tools list received');
        console.log(`  Found ${toolsData.result.tools.length} tool(s):\n`);

        toolsData.result.tools.forEach((tool, idx) => {
            console.log(`  Tool ${idx + 1}:`);
            console.log(`    Name: ${tool.name}`);
            console.log(`    Description: ${tool.description.substring(0, 100)}...`);
            console.log();
        });

        console.log('✅ All tests passed successfully!');
        process.exit(0);

    } catch (error) {
        console.error('✗ Test failed:', error.message);
        if (error.cause) {
            console.error('  Cause:', error.cause);
        }
        process.exit(1);
    }
}

// Run tests
testMCPServer();

// Made with Bob