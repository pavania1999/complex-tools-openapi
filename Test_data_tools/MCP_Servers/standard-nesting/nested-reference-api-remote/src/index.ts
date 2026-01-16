import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
    Tool,
} from "@modelcontextprotocol/sdk/types.js";
import express, { Request, Response } from "express";
import cors from "cors";
import axios from "axios";

// API Configuration
const API_BASE_URL = "https://complex-tools-openapi.onrender.com/api/v1";
const PORT = process.env.PORT || 3456;

// Tool definition with nested $ref patterns
const TOOLS: Tool[] = [
    {
        name: "process_customer_order_with_references",
        description: `Process customer orders with nested address references demonstrating the $ref pattern from GitHub Issue #45755.

This tool showcases nested schema references where:
- order.shipping_address references customer.address using $ref
- order.billing_address references customer.address using $ref  
- order.shipping_locations[].address references customer.address using $ref
- order.items[].delivery_address references customer.address using $ref

This recreates the Moody's MCP tools pattern where alerts.address referenced inquiry.address, which caused serialization issues and LLM confusion.

Returns a formatted order confirmation with customer details, itemized products, and address information.`,
        inputSchema: {
            type: "object",
            properties: {
                customer: {
                    type: "object",
                    description: "Customer information with primary address that will be referenced by other fields",
                    required: ["name", "email", "address"],
                    properties: {
                        name: {
                            type: "string",
                            description: "Customer full name",
                        },
                        email: {
                            type: "string",
                            description: "Customer email address",
                        },
                        address: {
                            type: "object",
                            description: "Primary customer address (referenced by shipping/billing addresses)",
                            properties: {
                                street: { type: "string" },
                                city: { type: "string" },
                                state: { type: "string" },
                                zipcode: { type: "string" },
                                country: { type: "string" },
                            },
                        },
                        contact: {
                            type: "object",
                            description: "Contact information",
                            properties: {
                                phone: { type: "string" },
                                mobile: { type: "string" },
                            },
                        },
                        entityType: {
                            type: "string",
                            description: "Customer entity type",
                        },
                        customerId: {
                            type: "string",
                            description: "Unique customer identifier",
                        },
                    },
                },
                order: {
                    type: "object",
                    description: "Order details with nested address references",
                    required: ["order_id", "items"],
                    properties: {
                        order_id: {
                            type: "string",
                            description: "Unique order identifier",
                        },
                        order_date: {
                            type: "string",
                            description: "Order date (YYYY-MM-DD format)",
                        },
                        items: {
                            type: "array",
                            description: "Order items",
                            items: {
                                type: "object",
                                required: ["product", "quantity", "price"],
                                properties: {
                                    product: {
                                        type: "object",
                                        properties: {
                                            product_id: { type: "string" },
                                            name: { type: "string" },
                                            details: {
                                                type: "object",
                                                properties: {
                                                    description: { type: "string" },
                                                    specifications: {
                                                        type: "object",
                                                        properties: {
                                                            weight: { type: "string" },
                                                            dimensions: { type: "string" },
                                                            material: { type: "string" },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    quantity: {
                                        type: "integer",
                                        minimum: 1,
                                    },
                                    price: {
                                        type: "number",
                                        minimum: 0,
                                    },
                                    delivery_address: {
                                        type: "array",
                                        description: "Delivery addresses (references customer.address schema)",
                                        items: {
                                            type: "object",
                                            properties: {
                                                street: { type: "string" },
                                                city: { type: "string" },
                                                state: { type: "string" },
                                                zipcode: { type: "string" },
                                                country: { type: "string" },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        shipping_address: {
                            type: "object",
                            description: "Shipping address (references customer.address via $ref in OpenAPI)",
                            properties: {
                                street: { type: "string" },
                                city: { type: "string" },
                                state: { type: "string" },
                                zipcode: { type: "string" },
                                country: { type: "string" },
                            },
                        },
                        billing_address: {
                            type: "object",
                            description: "Billing address (references customer.address via $ref in OpenAPI)",
                            properties: {
                                street: { type: "string" },
                                city: { type: "string" },
                                state: { type: "string" },
                                zipcode: { type: "string" },
                                country: { type: "string" },
                            },
                        },
                        shipping_locations: {
                            type: "array",
                            description: "Shipping locations with address arrays",
                            items: {
                                type: "object",
                                properties: {
                                    location_id: { type: "string" },
                                    location_name: { type: "string" },
                                    address: {
                                        type: "array",
                                        description: "Location addresses (references customer.address)",
                                        items: {
                                            type: "object",
                                            properties: {
                                                street: { type: "string" },
                                                city: { type: "string" },
                                                state: { type: "string" },
                                                zipcode: { type: "string" },
                                                country: { type: "string" },
                                            },
                                        },
                                    },
                                    entityType: { type: "string" },
                                },
                            },
                        },
                    },
                },
            },
            required: ["customer", "order"],
        },
    },
];

// Create Express app
const app = express();

// Middleware
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
}));
app.use(express.json());

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        service: 'nested-reference-api-remote'
    });
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
    res.json({
        message: 'Customer Order API with Nested References - Remote MCP Server',
        version: '1.0.0',
        transport: 'SSE',
        endpoints: {
            health: '/health',
            sse: '/sse'
        },
        documentation: 'Based on GitHub Issue #45755 - Nested Schema Reference Pattern'
    });
});

// Store active transports by connection
const activeTransports = new Map<string, SSEServerTransport>();

// SSE endpoint for MCP
app.get('/sse', async (req: Request, res: Response) => {
    console.log('New SSE connection established');
    console.log('Request headers:', req.headers);

    // Generate a unique session ID for this connection
    const sessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    console.log(`Session ID: ${sessionId}`);

    // Set SSE headers
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');

    // Create a new MCP server instance for this connection
    const server = new Server(
        {
            name: "nested-reference-api-remote",
            version: "1.0.0",
        },
        {
            capabilities: {
                tools: {},
            },
        }
    );

    // List available tools
    server.setRequestHandler(ListToolsRequestSchema, async () => {
        console.log('Handling ListTools request');
        return {
            tools: TOOLS,
        };
    });

    // Handle tool calls
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
        console.log('Handling CallTool request:', request.params.name);
        const { name, arguments: args } = request.params;

        if (name === "process_customer_order_with_references") {
            try {
                // Make API call to the deployed endpoint
                const response = await axios.post(
                    `${API_BASE_URL}/orders/process-with-references`,
                    args,
                    {
                        headers: {
                            "Content-Type": "application/json",
                        },
                        timeout: 30000, // 30 second timeout
                    }
                );

                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify(response.data, null, 2),
                        },
                    ],
                };
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    const errorResponse = error.response?.data;
                    return {
                        content: [
                            {
                                type: "text",
                                text: JSON.stringify(
                                    {
                                        error: errorResponse?.error || error.message,
                                        code: errorResponse?.code || "API_ERROR",
                                        details: errorResponse?.details || error.response?.statusText,
                                        status: error.response?.status,
                                    },
                                    null,
                                    2
                                ),
                            },
                        ],
                        isError: true,
                    };
                }

                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify(
                                {
                                    error: "Failed to process order",
                                    code: "UNKNOWN_ERROR",
                                    details: error instanceof Error ? error.message : String(error),
                                },
                                null,
                                2
                            ),
                        },
                    ],
                    isError: true,
                };
            }
        }

        return {
            content: [
                {
                    type: "text",
                    text: `Unknown tool: ${name}`,
                },
            ],
            isError: true,
        };
    });

    // Create SSE transport with standard /message endpoint
    const transport = new SSEServerTransport('/message', res);
    activeTransports.set(sessionId, transport);

    // Clean up on connection close
    req.on('close', () => {
        console.log(`SSE connection closed: ${sessionId}`);
        activeTransports.delete(sessionId);
    });

    try {
        await server.connect(transport);
        console.log(`MCP server connected via SSE: ${sessionId}`);
    } catch (error) {
        console.error('Error connecting MCP server:', error);
        activeTransports.delete(sessionId);
        if (!res.headersSent) {
            res.status(500).json({ error: 'Failed to establish SSE connection' });
        }
    }
});

// POST endpoint for MCP messages
app.post('/message', async (req: Request, res: Response) => {
    console.log('Received POST to /message');
    console.log('Request body:', JSON.stringify(req.body, null, 2));
    console.log(`Active transports: ${activeTransports.size}`);

    // Get the most recent transport (last one added)
    const transports = Array.from(activeTransports.values());
    const transport = transports[transports.length - 1];

    if (!transport) {
        console.error('No active transport found');
        return res.status(404).json({ error: 'No active SSE connection' });
    }

    try {
        console.log('Calling transport.handlePostMessage...');
        await transport.handlePostMessage(req, res);
        console.log('Message handled successfully');
    } catch (error) {
        console.error('Error handling message:', error);
        if (error instanceof Error) {
            console.error('Error stack:', error.stack);
        }
        if (!res.headersSent) {
            res.status(500).json({ error: 'Internal server error' });
        }
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Nested Reference API Remote MCP Server running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
    console.log(`SSE endpoint: http://localhost:${PORT}/sse`);
    console.log(`Transport: Server-Sent Events (SSE)`);
});

// Made with Bob
