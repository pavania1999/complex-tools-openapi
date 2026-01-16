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

// Type definitions matching the OpenAPI schema with circular reference
interface Person {
    name: string;
    employee_id: string;
    email: string;
    phone?: string;
    department: "Engineering" | "Product" | "Sales" | "Marketing" | "HR" | "Finance" | "Operations" | "Executive";
    position: string;
    start_date?: string;
    manager?: Person; // Circular reference - manager is also a Person
}

interface EmployeeRegistrationRequest {
    employee: Person;
}

interface EmployeeSummary {
    name: string;
    employee_id: string;
    department: string;
    position: string;
    start_date?: string;
}

interface ManagerSummary {
    name: string;
    employee_id: string;
    position: string;
}

interface EmployeeRegistrationResponse {
    status: "success" | "error";
    message: string;
    employee?: EmployeeSummary;
    manager?: ManagerSummary;
    reporting_chain?: string;
    hierarchy_levels?: number;
    registration_date?: string;
}

interface ErrorResponse {
    status: "error";
    error: string;
    code: string;
    details?: string;
}

// Tool definitions
const TOOLS: Tool[] = [
    {
        name: "register_employee",
        description: `Register a new employee with their manager information. This tool demonstrates circular schema references where both employee and manager use the same Person schema.

The Person schema includes a 'manager' field that also references the Person schema, allowing representation of organizational hierarchies of any depth. This creates a circular reference pattern: Person → manager (Person) → manager (Person) → ...

Features:
- Register employees with complete personal information
- Include manager details using the same schema structure
- Support multi-level organizational hierarchies
- Validate department and position information
- Track reporting chains and hierarchy levels

Returns a formatted registration confirmation with employee details, manager information, and the complete reporting chain.`,
        inputSchema: {
            type: "object",
            properties: {
                employee: {
                    type: "object",
                    description: "Employee information to register. The manager field uses the same Person schema, creating a circular reference.",
                    required: ["name", "employee_id", "email", "department", "position"],
                    properties: {
                        name: {
                            type: "string",
                            description: "Full name of the employee",
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
                            enum: ["Engineering", "Product", "Sales", "Marketing", "HR", "Finance", "Operations", "Executive"],
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
                            type: "object",
                            description: "Manager information. Uses the same Person schema structure, creating a circular reference that allows representing the full management hierarchy.",
                            properties: {
                                name: {
                                    type: "string",
                                    description: "Full name of the manager",
                                },
                                employee_id: {
                                    type: "string",
                                    description: "Unique employee identifier for manager",
                                },
                                email: {
                                    type: "string",
                                    description: "Manager's work email address",
                                },
                                phone: {
                                    type: "string",
                                    description: "Manager's work phone number",
                                },
                                department: {
                                    type: "string",
                                    description: "Manager's department",
                                    enum: ["Engineering", "Product", "Sales", "Marketing", "HR", "Finance", "Operations", "Executive"],
                                },
                                position: {
                                    type: "string",
                                    description: "Manager's job title/position",
                                },
                                start_date: {
                                    type: "string",
                                    description: "Manager's employment start date",
                                },
                                manager: {
                                    type: "object",
                                    description: "Manager's manager (next level up in hierarchy). This continues the circular reference pattern.",
                                    properties: {
                                        name: { type: "string" },
                                        employee_id: { type: "string" },
                                        email: { type: "string" },
                                        phone: { type: "string" },
                                        department: {
                                            type: "string",
                                            enum: ["Engineering", "Product", "Sales", "Marketing", "HR", "Finance", "Operations", "Executive"],
                                        },
                                        position: { type: "string" },
                                        start_date: { type: "string" },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            required: ["employee"],
        },
    },
];

// Server implementation
const server = new Server(
    {
        name: "employee-registration-api-mcp",
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

    if (name === "register_employee") {
        try {
            const registrationRequest = args as unknown as EmployeeRegistrationRequest;

            // Make API call to the deployed endpoint
            const response = await axios.post<EmployeeRegistrationResponse>(
                `${API_BASE_URL}/employees/register`,
                registrationRequest,
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

// Start the server
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Employee Registration API MCP Server running on stdio");
}

main().catch((error) => {
    console.error("Fatal error in main():", error);
    process.exit(1);
});

// Made with Bob