import express, { Request, Response } from 'express';
import cors from 'cors';
import * as z from 'zod';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Zod Schemas (from server.js)
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

const ScreeningSchema = z.object({
    name: z.string(),
    inquiry: InquirySchema,
    alerts: z.array(AlertSchema).min(1),
});

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
    res.json({
        message: 'Screening API',
        version: '1.0.0',
        endpoints: {
            health: '/health',
            searchAndWait: '/api/searchAndWait'
        }
    });
});

// Main screening endpoint
app.post('/api/searchAndWait', async (req: Request, res: Response) => {
    try {
        // Validate request body against Zod schema
        const validatedData = ScreeningSchema.parse(req.body);

        // Process the screening request
        // In a real implementation, this would perform actual screening logic
        const response = {
            args: validatedData,
            content: [{
                type: "text",
                text: "Result"
            }]
        };

        res.json(response);
    } catch (error) {
        if (error instanceof z.ZodError) {
            res.status(400).json({
                error: 'Invalid request body',
                details: error.errors
            });
        } else {
            console.error('Error processing request:', error);
            res.status(500).json({
                error: 'Internal server error'
            });
        }
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Screening API server running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
    console.log(`API endpoint: http://localhost:${PORT}/api/searchAndWait`);
});

// Made with Bob
