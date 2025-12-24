# Screening API

A REST API for screening entities against watchlists and sanctions databases with complex nested schema validation using Zod.

## Features

- Complex nested schema validation using Zod
- RESTful API endpoints
- TypeScript implementation
- Express.js server
- OpenAPI 3.0 specification

## Nested Schema Structure

The API demonstrates deep nesting with the following structure:

```
ScreeningRequest
├── inquiry (Inquiry)
│   └── address (Address)
│       └── countryCode (CountryCode)
└── alerts[] (Alert)
    ├── address[] (Address)
    │   └── countryCode (CountryCode)
    ├── events[] (Event)
    │   ├── category (Category)
    │   └── subCategory (SubCategory)
    ├── deceased (Deceased)
    └── identification[] (Identification)
```

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Production

```bash
npm start
```

## API Endpoints

### Health Check
```
GET /health
```

### Root
```
GET /
```

### Search and Wait
```
POST /api/searchAndWait
```

**Request Body:**
```json
{
  "name": "John Doe Screening",
  "inquiry": {
    "name": "John Doe",
    "address": {
      "addr1": "123 Main Street",
      "city": "New York",
      "stateProv": "NY",
      "postalCode": "10001",
      "countryCode": {
        "countryCodeValue": "US"
      },
      "country": "United States"
    },
    "dob": "1980-01-15",
    "entityType": "person",
    "bvdId": null
  },
  "alerts": [
    {
      "custom_id": "alert-001",
      "name": "John Doe",
      "address": [
        {
          "addr1": "456 Oak Avenue",
          "city": "Los Angeles",
          "stateProv": "CA",
          "postalCode": "90001",
          "countryCode": {
            "countryCodeValue": "US"
          },
          "country": "United States"
        }
      ],
      "dob": ["1980-01-15"],
      "entityId": "ENT-12345",
      "entityType": "person",
      "alias": ["J. Doe", "Johnny Doe"],
      "events": [
        {
          "category": {
            "categoryCode": "SANC",
            "categoryDesc": "Sanctions"
          },
          "subCategory": {
            "categoryCode": "OFAC",
            "categoryDesc": "OFAC List"
          },
          "eventDesc": "Added to sanctions list",
          "eventDt": "2020-05-10"
        }
      ],
      "deceased": {
        "val": false,
        "date": null
      },
      "nationality": ["US"],
      "images": ["https://example.com/image1.jpg"],
      "identification": [
        {
          "idNumber": "123-45-6789",
          "idType": "SSN",
          "idSource": "US Government"
        }
      ],
      "alertConfidence": 0.95,
      "bvdId": null,
      "faceMatchSimilarity": 0.87
    }
  ]
}
```

## Testing

Test the API using the provided test payload:

```bash
curl -X POST http://localhost:3000/api/searchAndWait \
  -H "Content-Type: application/json" \
  -d @test-payload.json
```

## Deployment

This API is configured for deployment on Render.com. See the OpenAPI specification for deployment details.

## OpenAPI Specification

The complete OpenAPI 3.0 specification is available in `openapi_screening.yaml`.

## License

ISC