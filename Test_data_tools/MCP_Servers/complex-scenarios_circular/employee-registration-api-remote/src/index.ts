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
const PORT = process.env.PORT || 3457;

// Tool definition with circular reference pattern matching OpenAPI spec
// In OpenAPI: Person.manager uses $ref: '#/components/schemas/Person'
// Here we use $ref to reference the employee schema, creating the same circular pattern
const TOOLS: Tool[] = [
    {
        name: "register_employee",
        description: `Register a new employee with their manager information, demonstrating circular schema references.

This tool showcases circular schema references where:
- Person schema has a 'manager' field that references Person schema using $ref
- This allows representing organizational hierarchies of any depth
- Manager can have their own manager, creating a recursive structure

This pattern matches the OpenAPI spec where Person.manager uses $ref: '#/components/schemas/Person',
creating a circular reference that allows unlimited hierarchy depth.

Returns employee registration confirmation with reporting chain information.`,
        inputSchema: {
            type: "object",
            properties: {
                employee: {
                    type: "object",
                    description: "Employee information to register (Person schema with circular manager reference)",
                    required: ["name", "employee_id", "email", "department", "position"],
                    properties: {
                        name: {
                            type: "string",
                            description: "Full name of the person",
                        },
                        employee_id: {
                            type: "string",
                            description: "Unique employee identifier (format: EMP-XXX)",
                        },
                        email: {
                            type: "string",
                            description: "Work email address",
                        },
                        phone: {
                            type: "string",
                            description: "Work phone number",
                        },
                        department: {
                            type: "string",
                            description: "Department name",
                            enum: [
                                "Engineering",
                                "Product",
                                "Sales",
                                "Marketing",
                                "HR",
                                "Finance",
                                "Operations",
                                "Executive"
                            ],
                        },
                        position: {
                            type: "string",
                            description: "Job title/position",
                        },
                        start_date: {
                            type: "string",
                            description: "Employment start date (YYYY-MM-DD format)",
                        },
                        manager: {
                            $ref: "#/properties/employee",
                            description: "Manager of this person (circular reference to employee/Person schema)"
                        },
                    },
                },
            },
            required: ["employee"],
        },
    },
];

// Create MCP Server instance
const server = new Server(
    {
        name: "employee-registration-api-remote",
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

    if (name === "register_employee") {
        try {
            // Make API call to the deployed endpoint
            const response = await axios.post(
                `${API_BASE_URL}/employees/register`,
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
                                error: "Failed to register employee",
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
        service: 'employee-registration-api-remote',
        transport: 'HTTP'
    });
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
    res.json({
        message: 'Employee Registration API with Circular References - Remote MCP Server',
        version: '1.0.0',
        transport: 'HTTP',
        endpoints: {
            health: '/health',
            mcp: '/mcp'
        },
        documentation: 'Demonstrates circular schema references where Person.manager references Person schema'
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
                        name: 'employee-registration-api-remote',
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

            if (name === "register_employee") {
                try {
                    // Make API call to the deployed endpoint
                    const response = await axios.post(
                        `${API_BASE_URL}/employees/register`,
                        args,
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
                                                error: "Failed to register employee",
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
    console.log(`Employee Registration API Remote MCP Server running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
    console.log(`MCP endpoint: http://localhost:${PORT}/mcp`);
    console.log(`Transport: HTTP (JSON-RPC over HTTP POST)`);
});

// Made with Bob