#!/usr/bin/env node

/**
 * MCP Server for Nested Reference Simple Test API
 * Exposes the processOrderInternalRef endpoint from the OpenAPI spec
 * Based on: nested_schemas/openapi_nested_reference_simple.yaml
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import axios from 'axios';

// API Configuration
const API_BASE_URL = 'https://complex-tools-openapi.onrender.com/api/v1';

/**
 * Type definitions based on the OpenAPI schema
 */
interface Address {
  street: string;
  city: string;
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
  name?: string;
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

/**
 * Create an MCP server with tool capabilities
 */
const server = new Server(
  {
    name: "nested-reference-api",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Handler that lists available tools.
 * Exposes the processOrderInternalRef tool from the OpenAPI spec.
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "process_order_internal_ref",
        description: "Process customer order with internal address reference. This endpoint demonstrates nested reference pattern where billing_address references shipping_address within the same schema using $ref: \"#/properties/order/properties/shipping_address\"",
        inputSchema: {
          type: "object",
          required: ["customer", "order"],
          properties: {
            customer: {
              type: "object",
              required: ["name"],
              description: "Customer information",
              properties: {
                name: {
                  type: "string",
                  description: "Customer full name"
                },
                email: {
                  type: "string",
                  description: "Customer email address"
                },
                address: {
                  type: "object",
                  description: "Customer address",
                  properties: {
                    street: { type: "string" },
                    city: { type: "string" },
                    state: { type: "string" },
                    zipcode: { type: "string" },
                    country: { type: "string" }
                  }
                },
                contact: {
                  type: "object",
                  description: "Contact information",
                  properties: {
                    phone: { type: "string" },
                    mobile: { type: "string" }
                  }
                }
              }
            },
            order: {
              type: "object",
              required: ["order_id"],
              description: "Order details",
              properties: {
                order_id: {
                  type: "string",
                  description: "Unique order identifier"
                },
                order_date: {
                  type: "string",
                  description: "Order date (YYYY-MM-DD format)"
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
                                  material: { type: "string" }
                                }
                              }
                            }
                          }
                        }
                      },
                      quantity: {
                        type: "integer",
                        minimum: 1
                      },
                      price: {
                        type: "number",
                        minimum: 0
                      }
                    }
                  }
                },
                shipping_address: {
                  type: "object",
                  description: "Shipping address",
                  required: ["street", "city"],
                  properties: {
                    street: { type: "string" },
                    city: { type: "string" },
                    state: { type: "string" },
                    zipcode: { type: "string" },
                    country: { type: "string" }
                  }
                },
                billing_address: {
                  "$ref": "#/properties/order/properties/shipping_address"
                }
              }
            }
          }
        }
      }
    ]
  };
});

/**
 * Handler for the process_order_internal_ref tool.
 * Makes a POST request to the API endpoint with the order data.
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name !== "process_order_internal_ref") {
    throw new Error(`Unknown tool: ${request.params.name}`);
  }

  try {
    // Destructure and rename 'arguments' to avoid reserved keyword issues
    const { arguments: args } = request.params;
    const orderRequest = args as unknown as OrderRequest;

    // Validate required fields
    if (!orderRequest?.customer?.name || (typeof orderRequest.customer.name === 'string' && orderRequest.customer.name.trim() === '')) {
      throw new Error("Customer name is required and cannot be empty");
    }
    if (!orderRequest.order?.order_id || (typeof orderRequest.order.order_id === 'string' && orderRequest.order.order_id.trim() === '')) {
      throw new Error("Order ID is required and cannot be empty");
    }

    // Make API request
    const response = await axios.post(
      `${API_BASE_URL}/orders/process`,
      orderRequest,
      {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000, // 30 second timeout
      }
    );

    // Return successful response
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(response.data, null, 2),
        },
      ],
    };
  } catch (error) {
    // Handle errors
    if (axios.isAxiosError(error)) {
      const errorMessage = error.response?.data?.error || error.message;
      const errorDetails = error.response?.data?.details || '';
      const statusCode = error.response?.status || 'Unknown';

      return {
        content: [
          {
            type: "text",
            text: `API Error (${statusCode}): ${errorMessage}${errorDetails ? '\nDetails: ' + errorDetails : ''}`,
          },
        ],
        isError: true,
      };
    }

    // Handle non-axios errors
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
      isError: true,
    };
  }
});

/**
 * Start the server using stdio transport.
 * This allows the server to communicate via standard input/output streams.
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Nested Reference API MCP server running on stdio');
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});

// Made with Bob
