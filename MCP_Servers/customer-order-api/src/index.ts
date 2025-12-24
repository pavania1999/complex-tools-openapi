#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
    Tool,
} from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";

// API Configuration
const API_BASE_URL = "https://complex-tools-openapi.onrender.com/api/v1";

// Type definitions matching the OpenAPI schema
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

interface Customer {
    name: string;
    email?: string;
    address?: Address;
    contact?: Contact;
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
}

interface Order {
    order_id: string;
    order_date?: string;
    items?: OrderItem[];
    shipping_address?: Address;
    billing_address?: Address;
}

interface OrderRequest {
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
    confirmation_message: string;
    order_summary: string;
}

interface ErrorResponse {
    error: string;
    code: string;
    details?: string;
}

// Tool definitions
const TOOLS: Tool[] = [
    {
        name: "process_customer_order",
        description: `Process a customer order with complete nested information including customer details, shipping/billing addresses, and product specifications. 
    
This tool handles deeply nested data structures:
- Customer information (name, email, address, contact)
- Order details (order_id, order_date, items)
- Product specifications (nested up to 6 levels deep)
- Shipping and billing addresses (reusable schema references)

Returns a formatted order confirmation with all details including totals and summaries.`,
        inputSchema: {
            type: "object",
            properties: {
                customer: {
                    type: "object",
                    required: ["name"],
                    description: "Customer information",
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
                            description: "Customer address",
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
                    },
                },
                order: {
                    type: "object",
                    required: ["order_id"],
                    description: "Order details",
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
                                        required: ["name"],
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
                                },
                            },
                        },
                        shipping_address: {
                            type: "object",
                            description: "Shipping address",
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
                            description: "Billing address",
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
            required: ["customer", "order"],
        },
    },
];

// Server implementation
const server = new Server(
    {
        name: "customer-order-api-mcp",
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

    if (name === "process_customer_order") {
        try {
            const orderRequest = args as unknown as OrderRequest;

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
        } catch (error) {
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

// Start the server
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Customer Order API MCP Server running on stdio");
}

main().catch((error) => {
    console.error("Fatal error in main():", error);
    process.exit(1);
});

// Made with Bob
