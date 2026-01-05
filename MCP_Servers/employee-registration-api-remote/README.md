# Employee Registration API - Remote MCP Server

Remote MCP Server for the Employee Registration API with circular schema references using SSE (Server-Sent Events) transport. This server can be deployed to cloud platforms and accessed remotely by multiple clients.

## Features

- **Remote Access**: Deploy once, access from anywhere via HTTPS
- **SSE Transport**: Uses Server-Sent Events for real-time communication
- **Circular Schema References**: Handles Person schema with self-referencing manager field
- **Multi-level Hierarchies**: Supports organizational hierarchies of any depth
- **Production Ready**: Connects to deployed API on Render.com
- **CORS Enabled**: Accessible from any origin

## Architecture

```
Client (Claude Desktop/Watson Orchestrate)
    ↓ HTTPS/SSE
Remote MCP Server (This Server)
    ↓ HTTPS
Employee Registration API (Render.com)
```

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
cd MCP_Servers/employee-registration-api-remote
npm install
```

## Building

```bash
npm run build
```

## Running Locally

```bash
# Development mode with auto-reload
npm run dev

# Production mode
npm start
```

The server will start on port 3000 (or PORT environment variable).

## Deployment to Render.com

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add remote MCP server"
   git push
   ```

2. **Create New Web Service on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `employee-registration-api-remote`
     - **Environment**: `Node`
     - **Build Command**: `npm install && npm run build`
     - **Start Command**: `npm start`
     - **Plan**: Free

3. **Deploy**: Render will automatically deploy your service

4. **Get Your URL**: After deployment, you'll receive a URL like:
   ```
   https://employee-registration-api-remote.onrender.com
   ```

## Usage with Claude Desktop

Add to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "employee-registration-api-remote": {
      "url": "https://your-deployment-url.onrender.com/sse",
      "transport": "sse"
    }
  }
}
```

Replace `your-deployment-url.onrender.com` with your actual Render deployment URL.

## Usage with Watson Orchestrate

Configure as a remote MCP server:

1. Go to Watson Orchestrate settings
2. Add new MCP server connection
3. Enter your deployment URL: `https://your-deployment-url.onrender.com/sse`
4. Select transport type: SSE
5. Save and test connection

## API Endpoints

### Health Check
```bash
GET /health
```

Returns server status and timestamp.

### Root
```bash
GET /
```

Returns server information and available endpoints.

### SSE Endpoint (MCP)
```bash
GET /sse
```

Server-Sent Events endpoint for MCP communication.

## Testing

### Test with curl

```bash
# Health check
curl https://your-deployment-url.onrender.com/health

# Server info
curl https://your-deployment-url.onrender.com/
```

### Test MCP Connection

Use the provided test payload:

```bash
cat test-payload.json
```

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

### Multi-level Hierarchy (3 Levels)

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

The `manager` field references the same `Person` schema, allowing representation of organizational hierarchies of any depth.

## Comparison: Local vs Remote MCP Server

| Feature | Local (Stdio) | Remote (SSE) |
|---------|--------------|--------------|
| **Transport** | Standard I/O | Server-Sent Events |
| **Deployment** | Local machine | Cloud (Render, AWS, etc.) |
| **Access** | Single user | Multiple users |
| **Configuration** | File path | HTTPS URL |
| **Scalability** | Limited | High |
| **Availability** | When running locally | 24/7 |
| **Use Case** | Personal use | Team/Production |

## Error Handling

The server handles various error scenarios:
- Invalid request data (400)
- Duplicate employee ID (409)
- API connection errors
- Timeout errors (30 second timeout)
- Server errors (500)

All errors are returned with detailed information including error code and description.

## Environment Variables

- `PORT`: Server port (default: 3000)
- `NODE_ENV`: Environment (development/production)

## Development

Watch mode for development:
```bash
npm run watch
```

## Security Notes

- CORS is enabled for all origins (configure for production)
- Consider adding authentication for production use
- Use HTTPS in production (Render provides this automatically)
- Rate limiting recommended for production

## License

MIT

## Author

IBM Bob

---

Made with Bob