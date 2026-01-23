#!/usr/bin/env node

/**
 * MCP Server for Enum Nested Schemas API
 * Local implementation with stdio transport
 * Direct implementation for enum validation in nested structures
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
    Tool,
} from "@modelcontextprotocol/sdk/types.js";

// Enum definitions
const ACCOUNT_STATUS_ENUM = ["active", "inactive"] as const;
const ACCOUNT_TYPE_ENUM = ["personal", "business"] as const;
const CUSTOMER_TYPE_ENUM = ["individual", "corporate"] as const;
const COUNTRY_ENUM = ["US", "CA", "UK"] as const;
const CONTACT_PREFERENCE_ENUM = ["email", "phone", "sms"] as const;

// Type definitions
type AccountStatus = typeof ACCOUNT_STATUS_ENUM[number];
type AccountType = typeof ACCOUNT_TYPE_ENUM[number];
type CustomerType = typeof CUSTOMER_TYPE_ENUM[number];
type Country = typeof COUNTRY_ENUM[number];
type ContactPreference = typeof CONTACT_PREFERENCE_ENUM[number];

interface Address {
    street: string;
    city: string;
    state?: string;
    zipcode?: string;
    country: Country;
}

interface Contact {
    phone?: string;
    mobile?: string;
    preference?: ContactPreference;
    timezone?: string;
}

interface Customer {
    name: string;
    email?: string;
    type: CustomerType;
    address: Address;
    contact?: Contact;
}

// Validation functions
function validateEnum<T extends string>(
    value: any,
    allowedValues: readonly T[],
    fieldName: string
): { valid: boolean; error?: string } {
    if (!allowedValues.includes(value as T)) {
        return {
            valid: false,
            error: `Invalid ${fieldName}: "${value}". Allowed values: ${allowedValues.join(", ")}`,
        };
    }
    return { valid: true };
}

// Tool implementations
function updateAccountStatus(args: any): any {
    const { account_id, status, type } = args;

    // Validate required fields
    if (!account_id || !status || !type) {
        return {
            error: "VALIDATION_ERROR",
            message: "Missing required fields: account_id, status, and type are required",
        };
    }

    // Validate status enum
    const statusValidation = validateEnum(status, ACCOUNT_STATUS_ENUM, "status");
    if (!statusValidation.valid) {
        return {
            error: "VALIDATION_ERROR",
            message: statusValidation.error,
            field: "status",
            provided_value: status,
            allowed_values: [...ACCOUNT_STATUS_ENUM],
        };
    }

    // Validate type enum
    const typeValidation = validateEnum(type, ACCOUNT_TYPE_ENUM, "type");
    if (!typeValidation.valid) {
        return {
            error: "VALIDATION_ERROR",
            message: typeValidation.error,
            field: "type",
            provided_value: type,
            allowed_values: [...ACCOUNT_TYPE_ENUM],
        };
    }

    // Return success response
    return {
        success: true,
        message: "Account status updated successfully",
        account_id,
        status,
        type,
        updated_at: new Date().toISOString(),
        validation_summary: `All enum validations passed: status=${status}, type=${type}`,
    };
}

function createCustomerProfileMultiLevel(args: any): any {
    const { profile_id, status, customer } = args;

    // Validate required fields
    if (!profile_id || !status || !customer) {
        return {
            error: "VALIDATION_ERROR",
            message: "Missing required fields: profile_id, status, and customer are required",
        };
    }

    const validationFailures: any[] = [];

    // Level 0: Validate profile status
    const statusValidation = validateEnum(status, ACCOUNT_STATUS_ENUM, "status");
    if (!statusValidation.valid) {
        validationFailures.push({
            field_path: "status",
            provided_value: status,
            allowed_values: [...ACCOUNT_STATUS_ENUM],
            nesting_level: 0,
        });
    }

    // Level 1: Validate customer type
    if (!customer.type) {
        return {
            error: "VALIDATION_ERROR",
            message: "Missing required field: customer.type",
        };
    }

    const customerTypeValidation = validateEnum(
        customer.type,
        CUSTOMER_TYPE_ENUM,
        "customer.type"
    );
    if (!customerTypeValidation.valid) {
        validationFailures.push({
            field_path: "customer.type",
            provided_value: customer.type,
            allowed_values: [...CUSTOMER_TYPE_ENUM],
            nesting_level: 1,
        });
    }

    // Level 2: Validate address country
    if (!customer.address) {
        return {
            error: "VALIDATION_ERROR",
            message: "Missing required field: customer.address",
        };
    }

    if (!customer.address.country) {
        return {
            error: "VALIDATION_ERROR",
            message: "Missing required field: customer.address.country",
        };
    }

    const countryValidation = validateEnum(
        customer.address.country,
        COUNTRY_ENUM,
        "customer.address.country"
    );
    if (!countryValidation.valid) {
        validationFailures.push({
            field_path: "customer.address.country",
            provided_value: customer.address.country,
            allowed_values: [...COUNTRY_ENUM],
            nesting_level: 2,
        });
    }

    // Level 3: Validate contact preference (optional)
    if (customer.contact && customer.contact.preference) {
        const preferenceValidation = validateEnum(
            customer.contact.preference,
            CONTACT_PREFERENCE_ENUM,
            "customer.contact.preference"
        );
        if (!preferenceValidation.valid) {
            validationFailures.push({
                field_path: "customer.contact.preference",
                provided_value: customer.contact.preference,
                allowed_values: [...CONTACT_PREFERENCE_ENUM],
                nesting_level: 3,
            });
        }
    }

    // If there are validation failures, return error response
    if (validationFailures.length > 0) {
        return {
            error: "ENUM_VALIDATION_ERROR",
            message: "One or more enum validation failures detected",
            validation_failures: validationFailures,
        };
    }

    // Build address formatted string
    const address = customer.address;
    const addressParts = [
        address.street,
        address.city,
        address.state,
        address.zipcode,
        address.country,
    ].filter(Boolean);
    const address_formatted = addressParts.join(", ");

    // Build enum validation report
    const enumValidationReport = {
        level_0_status: `${status} (valid)`,
        level_1_customer_type: `${customer.type} (valid)`,
        level_2_address_country: `${address.country} (valid)`,
        level_3_contact_preference: customer.contact?.preference
            ? `${customer.contact.preference} (valid)`
            : "not provided",
        total_enum_fields: customer.contact?.preference ? 4 : 3,
        all_valid: true,
    };

    // Return success response
    return {
        success: true,
        message: "Profile created with all enum validations passed",
        profile_id,
        profile_status: status,
        customer_name: customer.name,
        customer_email: customer.email || "",
        customer_type: customer.type,
        address_formatted,
        country: address.country,
        contact_phone: customer.contact?.phone || "",
        contact_preference: customer.contact?.preference || "",
        contact_timezone: customer.contact?.timezone || "",
        enum_validation_report: enumValidationReport,
        created_at: new Date().toISOString(),
    };
}

// Tool definitions
const TOOLS: Tool[] = [
    {
        name: "update_account_status",
        description: `Update account status with simple enum validation.

Tests simple enum validation at root level with two enum fields:
- status: "active" or "inactive"
- type: "personal" or "business"

Returns formatted account status confirmation with validation summary.`,
        inputSchema: {
            type: "object",
            properties: {
                account_id: {
                    type: "string",
                    description: "Unique account identifier",
                },
                status: {
                    type: "string",
                    enum: [...ACCOUNT_STATUS_ENUM],
                    description: "Account status (simple enum at root level)",
                },
                type: {
                    type: "string",
                    enum: [...ACCOUNT_TYPE_ENUM],
                    description: "Account type (simple enum at root level)",
                },
            },
            required: ["account_id", "status", "type"],
        },
    },
    {
        name: "create_customer_profile_multi_level",
        description: `Test multi-level enum validation across nested structures.

Combined test for enum validation at multiple nesting levels:
- Level 0: profile status ("active" or "inactive")
- Level 1: customer type ("individual" or "corporate")
- Level 2: address country ("US", "CA", or "UK")
- Level 3: contact preference ("email", "phone", or "sms") - optional

Returns comprehensive validation report with all enum validations.`,
        inputSchema: {
            type: "object",
            properties: {
                profile_id: {
                    type: "string",
                    description: "Unique profile identifier",
                },
                status: {
                    type: "string",
                    enum: [...ACCOUNT_STATUS_ENUM],
                    description: "Profile status (root level enum)",
                },
                customer: {
                    type: "object",
                    description: "Customer information with nested enum validations",
                    properties: {
                        name: {
                            type: "string",
                            description: "Customer full name or company name",
                        },
                        email: {
                            type: "string",
                            description: "Customer email address",
                        },
                        type: {
                            type: "string",
                            enum: [...CUSTOMER_TYPE_ENUM],
                            description: "Customer type (nested enum - level 1)",
                        },
                        address: {
                            type: "object",
                            description: "Customer address with country enum validation",
                            properties: {
                                street: {
                                    type: "string",
                                    description: "Street address",
                                },
                                city: {
                                    type: "string",
                                    description: "City name",
                                },
                                state: {
                                    type: "string",
                                    description: "State or province code",
                                },
                                zipcode: {
                                    type: "string",
                                    description: "Postal code",
                                },
                                country: {
                                    type: "string",
                                    enum: [...COUNTRY_ENUM],
                                    description: "Country code (nested enum - level 2)",
                                },
                            },
                            required: ["street", "city", "country"],
                        },
                        contact: {
                            type: "object",
                            description: "Contact information with preference enum validation",
                            properties: {
                                phone: {
                                    type: "string",
                                    description: "Primary phone number",
                                },
                                mobile: {
                                    type: "string",
                                    description: "Mobile phone number",
                                },
                                preference: {
                                    type: "string",
                                    enum: [...CONTACT_PREFERENCE_ENUM],
                                    description: "Contact preference (nested enum - level 3)",
                                },
                                timezone: {
                                    type: "string",
                                    description: "Preferred timezone",
                                },
                            },
                        },
                    },
                    required: ["name", "type", "address"],
                },
            },
            required: ["profile_id", "status", "customer"],
        },
    },
];

// Create MCP Server instance
const server = new Server(
    {
        name: "enum-nested-api",
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
        let result: any;

        if (name === "update_account_status") {
            result = updateAccountStatus(args);
        } else if (name === "create_customer_profile_multi_level") {
            result = createCustomerProfileMultiLevel(args);
        } else {
            return {
                content: [
                    {
                        type: "text",
                        text: `Unknown tool: ${name}`,
                    },
                ],
                isError: true,
            };
        }

        // Check if result is an error
        const isError = result.error !== undefined;

        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(result, null, 2),
                },
            ],
            isError,
        };
    } catch (error) {
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(
                        {
                            error: "INTERNAL_ERROR",
                            message: "Failed to process request",
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
});

/**
 * Start the server using stdio transport.
 * This allows the server to communicate via standard input/output streams.
 */
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Enum Nested API MCP server running on stdio");
}

main().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
});

// Made with Bob