import express, { Request, Response } from "express";
import cors from "cors";
import axios from "axios";

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
    Tool,
} from "@modelcontextprotocol/sdk/types.js";

/* ============================
   CONFIG
============================ */

const API_BASE_URL = "https://complex-tools-openapi.onrender.com/api/v1";
const PORT = process.env.PORT || 3000;

/* ============================
   TOOL DEFINITION
============================ */

const TOOLS: Tool[] = [
    {
        name: "process_customer_order_with_references",
        description:
            "Process customer order with nested address references (MCP nested $ref reproduction)",
        inputSchema: {
            type: "object",
            required: ["customer", "order"],
            properties: {
                customer: {
                    type: "object",
                    required: ["name", "entityType"],
                    properties: {
                        name: { type: "string" },
                        email: { type: "string" },
                        entityType: { type: "string", enum: ["INDIVIDUAL", "BUSINESS"] },
                        address: {
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
                order: {
                    type: "object",
                    required: ["order_id"],
                    properties: {
                        order_id: { type: "string" },
                        order_date: { type: "string" },
                        shipping_address: {
                            $ref: "#/properties/customer/properties/address",
                        },
                        billing_address: {
                            $ref: "#/properties/customer/properties/address",
                        },
                    },
                },
            },
            additionalProperties: false,
        },
    },
];

/* ============================
   EXPRESS APP
============================ */

const app = express();

app.use(cors({ origin: "*", methods: ["GET", "POST"] }));
app.use(express.json());

/* ============================
   HEALTH
============================ */

app.get("/health", (_req, res) => {
    res.json({
        status: "ok",
        service: "nested-reference-api-remote",
        transport: "sse",
    });
});

/* ============================
   MCP SSE ENDPOINT
============================ */

let transport: SSEServerTransport | null = null;

app.get("/sse", async (req: Request, res: Response) => {
    console.log("🔌 SSE connection opened");

    const server = new Server(
        { name: "nested-reference-api-remote", version: "1.0.0" },
        { capabilities: { tools: {} } }
    );

    /* ---- tools/list ---- */
    server.setRequestHandler(ListToolsRequestSchema, async () => {
        console.log("📋 tools/list called");
        return { tools: TOOLS };
    });

    /* ---- tools/call ---- */
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
        const { name, arguments: args } = request.params;

        if (name !== "process_customer_order_with_references") {
            return {
                content: [{ type: "text", text: `Unknown tool: ${name}` }],
                isError: true,
            };
        }

        try {
            const response = await axios.post(
                `${API_BASE_URL}/orders/process`,
                args,
                { timeout: 30000 }
            );

            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(response.data, null, 2),
                    },
                ],
            };
        } catch (err: any) {
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(
                            {
                                error: err?.message || "API error",
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

    /* ---- transport ---- */
    transport = new SSEServerTransport("/message", res);

    await server.connect(transport);

    /* 🔴 REQUIRED FOR MCP CLIENTS */
    transport.send({
        jsonrpc: "2.0",
        method: "initialized",
    });

    req.on("close", () => {
        console.log("🔌 SSE connection closed");
        transport = null;
    });
});

/* ============================
   MCP MESSAGE ENDPOINT
============================ */

app.post("/message", async (req: Request, res: Response) => {
    if (!transport) {
        return res.status(404).json({
            error: "No active SSE connection",
        });
    }

    await transport.handlePostMessage(req, res);
});

/* ============================
   START SERVER
============================ */

app.listen(PORT, () => {
    console.log(`🚀 MCP Server running on port ${PORT}`);
    console.log(`🔗 SSE: http://localhost:${PORT}/sse`);
});
