# Employee Registration API MCP Server

MCP Server for the Employee Registration API with circular schema references. This server provides tools to register employees with their manager information, where both employee and manager use the same Person schema, creating a circular reference pattern.

## Features

- **Circular Schema References**: Handles Person schema with self-referencing manager field
- **Multi-level Hierarchies**: Supports organizational hierarchies of any depth
- **Complete Employee Registration**: Processes employee information including manager details
- **Production Ready**: Connects to deployed API on Render.com

## API Endpoint

- **Base URL**: `https://complex-tools-openapi.onrender.com/api/v1`
- **Endpoint**: `POST /employees/register`

## Available Tools

### register_employee

Register a new employee with their manager information. This tool demonstrates circular schema references where both employee and manager use the same Person schema.

**Input Schema:**
```json
{
  "employee": {
    "name": "string (required)",
    "employee_id": "string (required, format: EMP-XXX)",
    "email": "string (required)",
    "phone": "string (optional)",
    "department": "string (required, enum: Engineering|Product|Sales|Marketing|HR|Finance|Operations|Executive)",
    "position": "string (required)",
    "start_date": "string (optional, format: YYYY-MM-DD)",
    "manager": {
      "name": "string",
      "employee_id": "string",
      "email": "string",
      "phone": "string",
      "department": "string (enum)",
      "position": "string",
      "start_date": "string",
      "manager": {
        // Circular reference continues...
        // Can nest to any depth
      }
    }
  }
}
```

**Output:**
Returns a formatted registration confirmation with:
- Employee summary (name, ID, department, position, start date)
- Manager summary (name, ID, position)
- Reporting chain visualization
- Hierarchy levels count
- Registration timestamp

## Installation

```bash
npm install
```

## Building

```bash
npm run build
```

## Usage with Claude Desktop

Add to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "employee-registration-api": {
      "command": "node",
      "args": ["/absolute/path/to/employee-registration-api/build/index.js"]
    }
  }
}
```

## Usage with Watson Orchestrate

1. Import the MCP server zip file into Watson Orchestrate
2. Configure the server connection
3. Use the `register_employee` tool in your skills

## Example Usage

### Simple Employee with Manager

```json
{
  "employee": {
    "name": "Sarah Martinez",
    "employee_id": "EMP-201",
    "email": "sarah.martinez@company.com",
    "phone": "+1-555-0201",
    "department": "Engineering",
    "position": "Software Engineer",
    "start_date": "2024-02-01",
    "manager": {
      "name": "Michael Chen",
      "employee_id": "EMP-150",
      "email": "michael.chen@company.com",
      "phone": "+1-555-0150",
      "department": "Engineering",
      "position": "Engineering Manager",
      "start_date": "2022-05-15"
    }
  }
}
```

### Multi-level Hierarchy

```json
{
  "employee": {
    "name": "James Wilson",
    "employee_id": "EMP-202",
    "email": "james.wilson@company.com",
    "phone": "+1-555-0202",
    "department": "Product",
    "position": "Senior Product Manager",
    "start_date": "2024-03-01",
    "manager": {
      "name": "Lisa Anderson",
      "employee_id": "EMP-100",
      "email": "lisa.anderson@company.com",
      "phone": "+1-555-0100",
      "department": "Product",
      "position": "VP of Product",
      "start_date": "2020-01-10",
      "manager": {
        "name": "Robert Taylor",
        "employee_id": "EMP-001",
        "email": "robert.taylor@company.com",
        "phone": "+1-555-0001",
        "department": "Executive",
        "position": "Chief Product Officer",
        "start_date": "2018-06-01"
      }
    }
  }
}
```

## Circular Schema Pattern

This API demonstrates the circular schema reference pattern:

```
Person Schema
├── name
├── employee_id
├── email
├── phone
├── department
├── position
├── start_date
└── manager → Person Schema (circular reference)
    ├── name
    ├── employee_id
    ├── ...
    └── manager → Person Schema (continues...)
```

The `manager` field references the same `Person` schema, allowing representation of organizational hierarchies of any depth. This creates a self-referential structure where:
- Employee is a Person
- Manager is also a Person
- Manager's manager is also a Person
- And so on...

## Error Handling

The server handles various error scenarios:
- Invalid request data (400)
- Duplicate employee ID (409)
- API connection errors
- Timeout errors (30 second timeout)
- Server errors (500)

All errors are returned with detailed information including error code and description.

## Development

Watch mode for development:
```bash
npm run watch
```

## License

MIT

## Author

IBM Bob

---

Made with Bob