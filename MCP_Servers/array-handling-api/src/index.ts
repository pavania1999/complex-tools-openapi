#!/usr/bin/env node

/**
 * Array Handling API MCP Server
 * 
 * This MCP server provides tools for the TC-P0-API-002 test case,
 * demonstrating array handling with both wrapped and raw array structures.
 * 
 * Test Case: TC-P0-API-002
 * Priority: P0 (Critical)
 * Focus: Array Handling (Wrapped Arrays + Raw Arrays)
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
    Tool,
} from "@modelcontextprotocol/sdk/types.js";

// API Base URL
const API_BASE_URL = "https://complex-tools-openapi.onrender.com/api/v1";

// Tool definitions
const TOOLS: Tool[] = [
    {
        name: "process_inventory_items_wrapped",
        description: `Process inventory items with wrapped array structure. This demonstrates the CORRECT way to handle arrays in OpenAPI specs for react-intrinsic style compatibility.

**Array Structure**: Items are wrapped in an object property called "items"
**Expected Request**: {"items": [{"name": "Item1", "quantity": 10}, ...]}

Use this tool to:
- Process inventory items with nested specifications
- Calculate total inventory value
- Generate inventory IDs
- Validate item data

Example usage: Process a list of electronics items with their specifications, quantities, and prices.`,
        inputSchema: {
            type: "object",
            properties: {
                items: {
                    type: "array",
                    description: "List of inventory items to process (WRAPPED ARRAY - CORRECT)",
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
                                description: "Stock Keeping Unit (format: XXX-###)",
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
                            },
                            category: {
                                type: "string",
                                description: "Item category",
                                enum: ["Electronics", "Accessories", "Furniture", "Office Supplies"],
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
            required: ["items"],
        },
    },
    {
        name: "process_inventory_items_raw",
        description: `Process inventory items with raw array structure. This demonstrates raw arrays at request body level.

**Array Structure**: Direct array at request body level (sent as wrapped for MCP compatibility)
**Expected Request**: {"items": [{"name": "Item1", "quantity": 10}, ...]}

Use this tool to:
- Process inventory items using raw array format
- Calculate total inventory value
- Generate inventory IDs
- Validate item data

Example usage: Process a direct array of electronics items without wrapper object.`,
        inputSchema: {
            type: "object",
            description: "Wrapper for raw array of inventory items",
            properties: {
                items: {
                    type: "array",
                    description: "List of inventory items to process (RAW ARRAY)",
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
                                description: "Stock Keeping Unit (format: XXX-###)",
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
                            },
                            category: {
                                type: "string",
                                description: "Item category",
                                enum: ["Electronics", "Accessories", "Furniture", "Office Supplies"],
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
            required: ["items"],
        },
    },
    {
        name: "process_batch_orders_wrapped",
        description: `Process batch orders with wrapped array structure. Demonstrates nested arrays within wrapped structure.

**Array Structure**: Orders wrapped in "orders" property, each order contains wrapped "items" array

Use this tool to:
- Process multiple orders in a batch
- Handle nested arrays (orders containing items)
- Calculate order totals and revenue
- Track order status

Example usage: Process multiple customer orders, each containing multiple items.`,
        inputSchema: {
            type: "object",
            properties: {
                orders: {
                    type: "array",
                    description: "List of orders to process (WRAPPED ARRAY - CORRECT)",
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
                                description: "Order items (NESTED WRAPPED ARRAY - CORRECT)",
                                minItems: 1,
                                items: {
                                    type: "object",
                                    required: ["product_name", "quantity", "unit_price"],
                                    properties: {
                                        product_name: {
                                            type: "string",
                                            description: "Product name",
                                        },
                                        quantity: {
                                            type: "integer",
                                            description: "Quantity ordered",
                                            minimum: 1,
                                        },
                                        unit_price: {
                                            type: "number",
                                            description: "Unit price",
                                            minimum: 0,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            required: ["orders"],
        },
    },
    {
        name: "process_batch_orders_raw",
        description: `Process batch orders with raw array structure. Demonstrates nested arrays with raw format.

**Array Structure**: Direct array of orders at request body level (sent as wrapped for MCP compatibility)

Use this tool to:
- Process multiple orders using raw array format
- Handle nested arrays (orders containing items)
- Calculate order totals and revenue
- Track order status

Example usage: Process a direct array of customer orders without wrapper object.`,
        inputSchema: {
            type: "object",
            description: "Wrapper for raw array of orders",
            properties: {
                orders: {
                    type: "array",
                    description: "List of orders to process (RAW ARRAY)",
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
                                description: "Order items (NESTED ARRAY)",
                                minItems: 1,
                                items: {
                                    type: "object",
                                    required: ["product_name", "quantity", "unit_price"],
                                    properties: {
                                        product_name: {
                                            type: "string",
                                            description: "Product name",
                                        },
                                        quantity: {
                                            type: "integer",
                                            description: "Quantity ordered",
                                            minimum: 1,
                                        },
                                        unit_price: {
                                            type: "number",
                                            description: "Unit price",
                                            minimum: 0,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            required: ["orders"],
        },
    },
];

// Helper function to make API calls
async function callAPI(endpoint: string, data: any): Promise<any> {
    const url = `${API_BASE_URL}${endpoint}`;

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                `API error (${response.status}): ${result.error || result.message || "Unknown error"}`
            );
        }

        return result;
    } catch (error) {
        if (error instanceof Error) {
            throw new Error(`Failed to call API: ${error.message}`);
        }
        throw error;
    }
}

// Create server instance
const server = new Server(
    {
        name: "array-handling-api",
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
    return {
        tools: TOOLS,
    };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
        switch (name) {
            case "process_inventory_items_wrapped": {
                const result = await callAPI("/inventory/process-items", args);
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify(result, null, 2),
                        },
                    ],
                };
            }

            case "process_inventory_items_raw": {
                // Extract the items array and send as raw array
                const items = (args as any).items;
                const result = await callAPI("/inventory/process-items-raw", items);
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify(result, null, 2),
                        },
                    ],
                };
            }

            case "process_batch_orders_wrapped": {
                const result = await callAPI("/orders/process-batch", args);
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify(result, null, 2),
                        },
                    ],
                };
            }

            case "process_batch_orders_raw": {
                // Extract the orders array and send as raw array
                const orders = (args as any).orders;
                const result = await callAPI("/orders/process-batch-raw", orders);
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify(result, null, 2),
                        },
                    ],
                };
            }

            default:
                throw new Error(`Unknown tool: ${name}`);
        }
    } catch (error) {
        if (error instanceof Error) {
            return {
                content: [
                    {
                        type: "text",
                        text: `Error: ${error.message}`,
                    },
                ],
                isError: true,
            };
        }
        throw error;
    }
});

// Start the server
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Array Handling API MCP Server running on stdio");
}

main().catch((error) => {
    console.error("Fatal error in main():", error);
    process.exit(1);
});

// Made with Bob
