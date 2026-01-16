#!/usr/bin/env node

/**
 * Test script to verify MCP server initialization and list tools
 * Tests the SSE connection and MCP protocol handshake
 */

import EventSource from 'eventsource';
import fetch from 'node-fetch';

const SSE_URL = 'https://nested-reference-api-remote-mcp.onrender.com/sse';
const MESSAGE_URL = 'https://nested-reference-api-remote-mcp.onrender.com/message';

console.log('Testing MCP Server Connection...\n');
console.log('SSE URL:', SSE_URL);
console.log('Message URL:', MESSAGE_URL);
console.log('---\n');

// Step 1: Connect to SSE endpoint
console.log('Step 1: Connecting to SSE endpoint...');
const eventSource = new EventSource(SSE_URL);

eventSource.onopen = () => {
    console.log('✓ SSE connection established\n');

    // Step 2: Send initialize request
    setTimeout(async () => {
        console.log('Step 2: Sending initialize request...');
        try {
            const initRequest = {
                jsonrpc: '2.0',
                id: 1,
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

            const response = await fetch(MESSAGE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(initRequest)
            });

            console.log('Initialize response status:', response.status);
            const text = await response.text();
            console.log('Initialize response:', text);
            console.log('');

            // Step 3: Send list tools request
            setTimeout(async () => {
                console.log('Step 3: Sending tools/list request...');
                try {
                    const listToolsRequest = {
                        jsonrpc: '2.0',
                        id: 2,
                        method: 'tools/list',
                        params: {}
                    };

                    const toolsResponse = await fetch(MESSAGE_URL, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(listToolsRequest)
                    });

                    console.log('List tools response status:', toolsResponse.status);
                    const toolsText = await toolsResponse.text();
                    console.log('List tools response:', toolsText);

                    // Parse and display tools
                    try {
                        const toolsData = JSON.parse(toolsText);
                        if (toolsData.result && toolsData.result.tools) {
                            console.log('\n✓ Tools found:', toolsData.result.tools.length);
                            toolsData.result.tools.forEach((tool, idx) => {
                                console.log(`\nTool ${idx + 1}:`);
                                console.log('  Name:', tool.name);
                                console.log('  Description:', tool.description.substring(0, 100) + '...');
                            });
                        }
                    } catch (e) {
                        console.log('Could not parse tools response');
                    }

                    console.log('\n✓ Test completed successfully!');
                    eventSource.close();
                    process.exit(0);
                } catch (error) {
                    console.error('✗ Error listing tools:', error.message);
                    eventSource.close();
                    process.exit(1);
                }
            }, 2000);

        } catch (error) {
            console.error('✗ Error initializing:', error.message);
            eventSource.close();
            process.exit(1);
        }
    }, 2000);
};

eventSource.onerror = (error) => {
    console.error('✗ SSE connection error:', error);
    eventSource.close();
    process.exit(1);
};

eventSource.onmessage = (event) => {
    console.log('Received SSE message:', event.data);
};

// Timeout after 30 seconds
setTimeout(() => {
    console.error('✗ Test timeout after 30 seconds');
    eventSource.close();
    process.exit(1);
}, 30000);

// Made with Bob
