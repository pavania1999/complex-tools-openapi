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
const PORT = process.env.PORT || 3000;

// Type definitions matching the OpenAPI schema with nested references
interface Address {
    street?: string;
    city?: string;
    state?: string;
    zipcode?: string;
    country?: string;
}

interface Contact {
    phone?: string;
    mobile?: string;
}

interface ProductSpecifications {
    weight?: string;
    dimensions?: string;
    material?: string;
}

interface ProductDetails {
    description?: string;
    specifications?: ProductSpecifications;
}

interface Product {
    product_id?: string;
    name: string;
    details?: ProductDetails;
}

interface OrderItem {
    product: Product;
    quantity: number;
    price: number;
    delivery_address?: Address[];
}

interface ShippingLocation {
    location_id: string;
    location_name: string;
    address?: Address[];
    entityType: string;
    contact?: {
        phone?: string;
        email?: string;
    };
}

interface Customer {
    name: string;
    email?: string;
    address?: Address;
    contact?: Contact;
    entityType: "INDIVIDUAL" | "BUSINESS";
    customerId?: string;
}

interface Order {
    order_id: string;
    order_date?: string;
    items?: OrderItem[];
    shipping_address?: Address;
    billing_address?: Address;
    shipping_locations?: ShippingLocation[];
}

interface OrderRequestWithReferences {
    customer: Customer;
    order: Order;
}

interface ProcessedItem {
    product_name: string;
    product_id?: string;
    description?: string;
    quantity: number;
    price: number;
    subtotal: number;
    specifications?: string;
}

interface OrderResponse {
    customer_name: string;
    customer_email?: string;
    customer_address?: string;
    phone?: string;
    mobile?: string;
    order_id: string;
    order_date?: string;
    items?: ProcessedItem[];
    total_items: number;
    total_amount: number;
    shipping_address?: string;
    billing_address?: string;
    shipping_locations_count?: number;
    confirmation_message: string;
    order_summary: string;
}

interface ErrorResponse {
    error: string;
    code: string;
    details?: string;
}

// Tool definitions with $ref references matching the OpenAPI spec
const TOOLS: Tool[] = [
    {
        name: "process_customer_order_with_references",
        description: `Process customer order with nested address references demonstrating the Moody's MCP tools issue pattern.

This tool demonstrates the nested reference pattern from GitHub issue #45755 where:
- The order.items array contains product details with delivery_address references
- The order.shipping_locations array contains address fields that reference the customer.address structure
- Uses $ref pointing to other properties within the same schema (#/properties/customer/properties/address)

This recreates the scenario where alerts.address references inquiry.address, which may cause:
1. Serialization issues during DB insertion (TypeError: Object of type dict is not JSON serializable)
2. LLM confusion during execution due to repeated field names after resolution

Features:
- Process orders with complete customer information
- Handle nested product details with specifications
- Support multiple delivery addresses per item
- Track shipping locations with address references
- Calculate order totals and generate confirmations

Returns a formatted order confirmation with customer details, itemized products, and shipping information.`,
        inputSchema: {
            type: "object",
            properties: {
                customer: {
                    type: "object",
                    description: "Customer information with primary address (referenced by other fields)",
                    required: ["name", "entityType"],
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
                            description: "Primary customer address (referenced by shipping_locations)",
                            properties: {
                                street: { type: "string", description: "Street address" },
                                city: { type: "string", description: "City name" },
                                state: { type: "string", description: "State or province" },
                                zipcode: { type: "string", description: "Postal code" },
                                country: { type: "string", description: "Country name" },
                            },
                            additionalProperties: false,
                        },
                        contact: {
                            type: "object",
                            description: "Contact information",
                            properties: {
                                phone: { type: "string", description: "Primary phone number" },
                                mobile: { type: "string", description: "Mobile phone number" },
                            },
                        },
                        entityType: {
                            type: "string",
                            description: "Type of customer entity",
                            enum: ["INDIVIDUAL", "BUSINESS"],
                        },
                        customerId: {
                            type: "string",
                            description: "Unique customer identifier",
                        },
                    },
                    additionalProperties: false,
                },
                order: {
                    type: "object",
                    description: "Order details with nested references",
                    required: ["order_id"],
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
                            description: "List of order items with delivery addresses",
                            items: {
                                type: "object",
                                required: ["product", "quantity", "price"],
                                properties: {
                                    product: {
                                        type: "object",
                                        required: ["name"],
                                        properties: {
                                            product_id: { type: "string", description: "Product identifier" },
                                            name: { type: "string", description: "Product name" },
                                            details: {
                                                type: "object",
                                                description: "Product details",
                                                properties: {
                                                    description: { type: "string", description: "Product description" },
                                                    specifications: {
                                                        type: "object",
                                                        description: "Product specifications",
                                                        properties: {
                                                            weight: { type: "string", description: "Product weight" },
                                                            dimensions: { type: "string", description: "Product dimensions" },
                                                            material: { type: "string", description: "Product material" },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    quantity: {
                                        type: "integer",
                                        minimum: 1,
                                        description: "Quantity ordered",
                                    },
                                    price: {
                                        type: "number",
                                        minimum: 0,
                                        description: "Unit price",
                                    },
                                    delivery_address: {
                                        type: "array",
                                        description: "Delivery addresses for this item. In the original Moody's schema, this pattern used: $ref: '#/properties/customer/properties/address'",
                                        items: {
                                            $ref: "#/properties/customer/properties/address"
                                        },
                                    },
                                },
                            },
                        },
                        shipping_address: {
                            $ref: "#/properties/customer/properties/address"
                        },
                        billing_address: {
                            $ref: "#/properties/customer/properties/address"
                        },
                        shipping_locations: {
                            type: "array",
                            description: "Array of shipping locations with address field referencing customer.address. This demonstrates the $ref pattern: '#/properties/customer/properties/address' similar to how alerts.address references inquiry.address in the Moody's case.",
                            minItems: 1,
                            items: {
                                type: "object",
                                required: ["location_id", "location_name", "entityType"],
                                properties: {
                                    location_id: {
                                        type: "string",
                                        description: "Location identifier",
                                    },
                                    location_name: {
                                        type: "string",
                                        description: "Name of the location",
                                    },
                                    address: {
                                        type: "array",
                                        description: "Address array that references the customer.address structure. This mimics: $ref: '#/properties/customer/properties/address'",
                                        items: {
                                            $ref: "#/properties/customer/properties/address"
                                        },
                                    },
                                    entityType: {
                                        type: "string",
                                        description: "Type of location entity",
                                    },
                                    contact: {
                                        type: "object",
                                        description: "Location contact information",
                                        properties: {
                                            phone: { type: "string" },
                                            email: { type: "string" },
                                        },
                                    },
                                },
                                additionalProperties: false,
                            },
                        },
                    },
                    additionalProperties: false,
                },
            },
            required: ["customer", "order"],
            additionalProperties: false,
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

// Store active servers and transports by session ID
const activeSessions = new Map<string, { server: Server; transport: SSEServerTransport }>();

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
    res.setHeader('X-Session-ID', sessionId);

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
    server.setRequestHandler(CallToolRequestSchema, async (request: any) => {
        console.log('Handling CallTool request:', request.params.name);
        const { name, arguments: args } = request.params;

        if (name === "process_customer_order_with_references") {
            try {
                const orderRequest = args as unknown as OrderRequestWithReferences;

                // Make API call to the deployed endpoint
                const response = await axios.post<OrderResponse>(
                    `${API_BASE_URL}/orders/process`,
                    orderRequest,
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
            } catch (error: unknown) {
                if (axios.isAxiosError(error)) {
                    const errorResponse = error.response?.data as ErrorResponse;
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
    activeSessions.set(sessionId, { server, transport });

    // Clean up on connection close
    req.on('close', () => {
        console.log(`SSE connection closed: ${sessionId}`);
        activeSessions.delete(sessionId);
    });

    try {
        await server.connect(transport);
        console.log(`MCP server connected via SSE: ${sessionId}`);
    } catch (error) {
        console.error('Error connecting MCP server:', error);
        activeSessions.delete(sessionId);
        if (!res.headersSent) {
            res.status(500).json({ error: 'Failed to establish SSE connection' });
        }
    }
});

// POST endpoint for MCP messages
app.post('/message', async (req: Request, res: Response) => {
    console.log('Received POST to /message');
    console.log('Request body:', JSON.stringify(req.body, null, 2));
    console.log(`Active sessions: ${activeSessions.size}`);

    // Try to get session ID from header or use the most recent session
    const sessionId = req.headers['x-session-id'] as string;
    let session = sessionId ? activeSessions.get(sessionId) : undefined;

    if (!session) {
        // Fall back to most recent session
        const sessions = Array.from(activeSessions.values());
        session = sessions[sessions.length - 1];
    }

    if (!session) {
        console.error('No active session found');
        return res.status(404).json({ error: 'No active SSE connection' });
    }

    try {
        console.log('Calling transport.handlePostMessage...');
        await session.transport.handlePostMessage(req, res);
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
    console.log(`Based on GitHub Issue #45755 - Nested Schema Reference Pattern`);
});

// Made with Bob