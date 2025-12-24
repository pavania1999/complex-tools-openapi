import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import * as z from "zod";

const CountryCodeSchema = z.object({
    countryCodeValue: z.string().describe("2-letter country code"),
});

const AddressSchema = z.object({
    addr1: z.string().nullable(),
    city: z.string().nullable(),
    stateProv: z.string().nullable(),
    postalCode: z.string().nullable(),
    countryCode: z.union([CountryCodeSchema, z.null()]),
    country: z.string().nullable(),
});

const InquirySchema = z.object({
    name: z.string().min(1, "Name is required"),
    address: AddressSchema,
    dob: z.string().describe("Date of birth in YYYY-MM-DD format").optional(),
    entityType: z.enum(["person", "organization", "unknown"]),
    bvdId: z.string().nullable().optional(),
});

const CategorySchema = z.object({
    categoryCode: z.string().min(1),
    categoryDesc: z.string().min(1),
});

const SubCategorySchema = z.union([
    z.object({
        categoryCode: z.string(),
        categoryDesc: z.string(),
    }),
    z.null(),
]);

const EventSchema = z.object({
    category: CategorySchema,
    subCategory: SubCategorySchema,
    eventDesc: z.string().nullable(),
    eventDt: z.string().nullable(),
});

const DeceasedSchema = z.object({
    val: z.boolean(),
    date: z.string().nullable(),
});

const IdentificationSchema = z.object({
    idNumber: z.string().min(1),
    idType: z.string().min(1),
    idSource: z.string().optional(),
});

const AlertSchema = z.object({
    custom_id: z.string().optional(),
    name: z.string().min(1),
    address: z.array(AddressSchema),
    dob: z.array(z.string()),
    entityId: z.string().min(1),
    entityType: z.enum(["person", "organization", "unknown"]),
    alias: z.array(z.string()),
    events: z.array(EventSchema),
    deceased: DeceasedSchema,
    nationality: z.array(z.string()),
    images: z.array(z.string()),
    identification: z.array(IdentificationSchema),
    alertConfidence: z.number().min(0).max(1),
    bvdId: z.string().nullable(),
    faceMatchSimilarity: z
        .union([z.number().min(0).max(1), z.null(), z.undefined()])
        .optional(),
});

export const ScreeningSchema = z.object({
    name: z.string(),
    inquiry: InquirySchema,
    alerts: z.array(AlertSchema).min(1),
});


const server = new McpServer({
    name: "mcp-echo",
    version: "1.0.0",
    capabilities: {
        tools: []
    }
});

server.tool(
    "searchAndWait",
    "sample-tool",
    ScreeningSchema.shape,
    async (args) => {
        return {
            args,
            content: [{
                type: "text",
                text: "Result"
            }]
        };
    }
);

const transport = new StdioServerTransport();
await server.connect(transport);