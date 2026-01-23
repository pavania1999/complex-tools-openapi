import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
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

// Enum definitions
const CATEGORY_ENUM = ["Electronics", "Accessories", "Furniture", "Office Supplies"] as const;

// Type definitions
type Category = typeof CATEGORY_ENUM[number];

// Tool definitions with wrapped arrays for TypeScript compatibility
const TOOLS: Tool[] = [
    {
        name: "process_inventory_items_raw",
        description: `Process inventory items with array structure (TC-P0-API-002).

This tool demonstrates array handling for inventory processing.
The request contains an array of inventory items.

Each inventory item includes:
- Basic information (name, SKU, quantity, price)
- Category (Electronics, Accessories, Furniture, Office Supplies)
- Nested specifications object (brand, model, warranty)

Returns a response with processing status, processed items details, and total value.`,
        inputSchema: {
            type: "object",
            required: ["items"],
            properties: {
                items: {
                    type: "array",
                    description: "Array of inventory items",
                    minItems: 1,
                    maxItems: 100,
                    items: {
                        type: "object",
                        required: ["name", "sku", "quantity", "price"],
                        properties: {
                            name: {
                                type: "string",
                                description: "Item name",
                                minLength: 1,
                                maxLength: 200,
                            },
                            sku: {
                                type: "string",
                                description: "Stock Keeping Unit",
                                pattern: "^[A-Z]{3}-[0-9]{3}$",
                            },
                            quantity: {
                                type: "integer",
                                description: "Quantity in stock",
                                minimum: 0,
                                maximum: 10000,
                            },
                            price: {
                                type: "number",
                                description: "Unit price",
                                minimum: 0,
                                exclusiveMinimum: true,
                            },
                            category: {
                                type: "string",
                                description: "Item category",
                            },
                            specifications: {
                                type: "object",
                                description: "Nested specifications object",
                                properties: {
                                    brand: {
                                        type: "string",
                                        description: "Brand name",
                                    },
                                    model: {
                                        type: "string",
                                        description: "Model number",
                                    },
                                    warranty: {
                                        type: "string",
                                        description: "Warranty period",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
    {
        name: "process_batch_orders_raw",
        description: `Process multiple orders in a batch with array structure (TC-P0-API-002).

This tool demonstrates array handling for batch order processing.
Each order contains nested items array.

Each order includes:
- Order ID and customer name
- Nested items array with product details (product_name, quantity, unit_price)

Returns a response with batch processing status and details for each processed order.`,
        inputSchema: {
            type: "object",
            required: ["orders"],
            properties: {
                orders: {
                    type: "array",
                    description: "Array of orders",
                    minItems: 1,
                    items: {
                        type: "object",
                        required: ["order_id", "customer_name", "items"],
                        properties: {
                            order_id: {
                                type: "string",
                                description: "Unique order identifier",
                            },
                            customer_name: {
                                type: "string",
                                description: "Customer name",
                            },
                            items: {
                                type: "array",
                                description: "Order items (nested array)",
                                minItems: 1,
                                items: {
                                    type: "object",
                                    required: ["product_name", "quantity", "unit_price"],
                                    properties: {
                                        product_name: {
                                            type: "string",
                                        },
                                        quantity: {
                                            type: "integer",
                                            minimum: 1,
                                        },
                                        unit_price: {
                                            type: "number",
                                            minimum: 0,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
];

// Create MCP Server instance
const server = new Server(
    {
        name: "array-handling-api-remote",
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

    if (name === "process_inventory_items_raw") {
        try {
            // Extract items array from wrapped object and send as raw array to API
            const items = (args as any).items;
            const response = await axios.post(
                `${API_BASE_URL}/inventory/process-items-raw`,
                items,
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
                                error: "Failed to process inventory items",
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

    if (name === "process_batch_orders_raw") {
        try {
            // Extract orders array from wrapped object and send as raw array to API
            const orders = (args as any).orders;
            const response = await axios.post(
                `${API_BASE_URL}/orders/process-batch-raw`,
                orders,
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                    timeout: 30000,
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
                                error: "Failed to process batch orders",
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

// Create Express app for HTTP transport
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
        service: 'array-handling-api-remote',
        transport: 'HTTP'
    });
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
    res.json({
        message: 'Array Handling API - Remote MCP Server (TC-P0-API-002)',
        version: '1.0.0',
        transport: 'HTTP',
        endpoints: {
            health: '/health',
            mcp: '/mcp'
        },
        documentation: 'Test case for raw array handling with react-intrinsic style'
    });
});

// MCP endpoint - handles all MCP protocol messages via HTTP POST
app.post('/mcp', async (req: Request, res: Response) => {
    console.log('Received MCP request:', req.body.method);

    try {
        // Handle the JSON-RPC request
        const request = req.body;

        if (request.method === 'initialize') {
            res.json({
                jsonrpc: '2.0',
                id: request.id,
                result: {
                    protocolVersion: '2024-11-05',
                    capabilities: {
                        tools: {}
                    },
                    serverInfo: {
                        name: 'array-handling-api-remote',
                        version: '1.0.0'
                    }
                }
            });
        } else if (request.method === 'tools/list') {
            res.json({
                jsonrpc: '2.0',
                id: request.id,
                result: {
                    tools: TOOLS
                }
            });
        } else if (request.method === 'notifications/initialized') {
            // Handle initialized notification - just acknowledge it
            console.log('Client initialized notification received');
            res.status(200).json({
                jsonrpc: '2.0',
                result: {}
            });
        } else if (request.method === 'tools/call') {
            // Call the tool directly through the handler
            const { name, arguments: args } = request.params;

            if (name === "process_inventory_items_raw") {
                try {
                    // Extract items array from wrapped object and send as raw array to API
                    const items = (args as any).items;
                    const response = await axios.post(
                        `${API_BASE_URL}/inventory/process-items-raw`,
                        items,
                        {
                            headers: {
                                "Content-Type": "application/json",
                            },
                            timeout: 30000,
                        }
                    );

                    res.json({
                        jsonrpc: '2.0',
                        id: request.id,
                        result: {
                            content: [
                                {
                                    type: "text",
                                    text: JSON.stringify(response.data, null, 2),
                                },
                            ],
                        }
                    });
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        const errorResponse = error.response?.data;
                        res.json({
                            jsonrpc: '2.0',
                            id: request.id,
                            result: {
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
                            }
                        });
                    } else {
                        res.json({
                            jsonrpc: '2.0',
                            id: request.id,
                            result: {
                                content: [
                                    {
                                        type: "text",
                                        text: JSON.stringify(
                                            {
                                                error: "Failed to process inventory items",
                                                code: "UNKNOWN_ERROR",
                                                details: error instanceof Error ? error.message : String(error),
                                            },
                                            null,
                                            2
                                        ),
                                    },
                                ],
                                isError: true,
                            }
                        });
                    }
                }
            } else if (name === "process_batch_orders_raw") {
                try {
                    // Extract orders array from wrapped object and send as raw array to API
                    const orders = (args as any).orders;
                    const response = await axios.post(
                        `${API_BASE_URL}/orders/process-batch-raw`,
                        orders,
                        {
                            headers: {
                                "Content-Type": "application/json",
                            },
                            timeout: 30000,
                        }
                    );

                    res.json({
                        jsonrpc: '2.0',
                        id: request.id,
                        result: {
                            content: [
                                {
                                    type: "text",
                                    text: JSON.stringify(response.data, null, 2),
                                },
                            ],
                        }
                    });
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        const errorResponse = error.response?.data;
                        res.json({
                            jsonrpc: '2.0',
                            id: request.id,
                            result: {
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
                            }
                        });
                    } else {
                        res.json({
                            jsonrpc: '2.0',
                            id: request.id,
                            result: {
                                content: [
                                    {
                                        type: "text",
                                        text: JSON.stringify(
                                            {
                                                error: "Failed to process batch orders",
                                                code: "UNKNOWN_ERROR",
                                                details: error instanceof Error ? error.message : String(error),
                                            },
                                            null,
                                            2
                                        ),
                                    },
                                ],
                                isError: true,
                            }
                        });
                    }
                }
            } else {
                res.status(400).json({
                    jsonrpc: '2.0',
                    id: request.id,
                    error: {
                        code: -32602,
                        message: `Unknown tool: ${name}`
                    }
                });
            }
        } else {
            console.log(`Unknown method: ${request.method}`);
            res.status(400).json({
                jsonrpc: '2.0',
                id: request.id,
                error: {
                    code: -32601,
                    message: `Method not found: ${request.method}`
                }
            });
        }
    } catch (error) {
        console.error('Error handling MCP request:', error);
        res.status(500).json({
            jsonrpc: '2.0',
            id: req.body.id,
            error: {
                code: -32603,
                message: 'Internal error',
                data: error instanceof Error ? error.message : String(error)
            }
        });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Array Handling API Remote MCP Server running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
    console.log(`MCP endpoint: http://localhost:${PORT}/mcp`);
    console.log(`Transport: HTTP (JSON-RPC over HTTP POST)`);
});

// Made with Bob