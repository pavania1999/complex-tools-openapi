# Employee Registration API - Remote MCP Server

Remote MCP Server for Employee Registration API with circular schema references, demonstrating the pattern where Person.manager references Person schema.

## Overview

This MCP server provides tools to register employees with their manager information, demonstrating circular schema references where:
- Person schema has a `manager` field that references Person schema using `$ref: "#/properties/employee"`
- This allows representing organizational hierarchies of any depth
- Manager can have their own manager, creating a recursive structure

This recreates the circular reference pattern from the OpenAPI spec where `Person.manager` uses `$ref: '#/components/schemas/Person'`.

## Features

- **HTTP Transport**: Uses HTTP POST for remote MCP communication
- **Circular References**: Demonstrates `$ref` patterns for recursive schemas
- **Real API Integration**: Connects to deployed OpenAPI endpoint at `https://complex-tools-openapi.onrender.com`
- **Comprehensive Error Handling**: Proper error responses for API failures

## Available Tools

### `register_employee`

Register a new employee with their manager information.

**Input Schema Features:**
- Employee information using Person schema
- Manager field that references the same Person schema using `$ref`
- Supports unlimited hierarchy depth through recursive manager references
- Department enum validation
- Required fields: name, employee_id, email, department, position

**Example Usage:**
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

## Deployment to Render.com

### Prerequisites
- GitHub account
- Render.com account (free tier available)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   cd Test_data_tools/MCP_Servers/complex-scenarios_circular/employee-registration-api-remote
   git init
   git add .
   git commit -m "Initial commit: Employee Registration API Remote MCP Server"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render.com**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration
   - Click "Create Web Service"

3. **Configuration (Auto-detected from render.yaml)**
   - **Name**: `employee-registration-api-remote`
   - **Environment**: Node
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Plan**: Free

4. **Environment Variables** (Auto-configured)
   - `NODE_VERSION`: 18.0.0
   - `PORT`: 10000

### After Deployment

Your MCP server will be available at:
- **MCP Endpoint**: `https://employee-registration-api-remote.onrender.com/mcp`
- **Health Check**: `https://employee-registration-api-remote.onrender.com/health`
- **Root**: `https://employee-registration-api-remote.onrender.com/`

## Local Development

### Installation
```bash
npm install
```

### Development Mode
```bash
npm run dev
```

### Build
```bash
npm run build
```

### Production
```bash
npm start
```

## Testing

Test the health endpoint:
```bash
curl https://employee-registration-api-remote.onrender.com/health
```

## MCP Client Configuration

Add to your MCP client settings:

```json
{
  "mcpServers": {
    "employee-registration-api": {
      "url": "https://employee-registration-api-remote.onrender.com/mcp",
      "transport": "http"
    }
  }
}
```

## Architecture

- **Transport**: HTTP (JSON-RPC over HTTP POST)
- **Backend API**: `https://complex-tools-openapi.onrender.com/api/v1`
- **Framework**: Express.js with MCP SDK
- **Language**: TypeScript

## Circular Reference Pattern

This server demonstrates the circular reference pattern from the OpenAPI spec:

**OpenAPI Pattern:**
```yaml
Person:
  properties:
    manager:
      $ref: '#/components/schemas/Person'
```

**MCP Tool Schema:**
```typescript
{
  properties: {
    employee: {
      properties: {
        manager: {
          $ref: "#/properties/employee"
        }
      }
    }
  }
}
```

The `manager` field uses `$ref: "#/properties/employee"` to reference the employee schema itself, creating the same circular pattern as the OpenAPI spec.

## Related Resources

- **OpenAPI Spec**: `Test_data_tools/OpenAPI/complex-scenarios_circular/openapi_add_employee_with_manager.yaml`
- **Backend API**: Complex Tools OpenAPI Server
- **Pattern**: Circular Schema References (Person.manager → Person)

## License

MIT

---

Made with Bob