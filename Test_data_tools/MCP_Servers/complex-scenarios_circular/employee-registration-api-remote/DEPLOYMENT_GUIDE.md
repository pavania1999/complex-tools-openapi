# Deployment Guide - Employee Registration API Remote MCP Server

Complete guide to deploy the Employee Registration API Remote MCP Server to Render.com.

## Prerequisites

1. **GitHub Account**: Required to host the repository
2. **Render.com Account**: Sign up at [render.com](https://render.com) (free tier available)
3. **Git**: Installed on your local machine

## Step-by-Step Deployment

### Step 1: Prepare the Repository

Navigate to the project directory:
```bash
cd Test_data_tools/MCP_Servers/complex-scenarios_circular/employee-registration-api-remote
```

### Step 2: Initialize Git Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: Employee Registration API Remote MCP Server with circular references"
```

### Step 3: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `employee-registration-api-remote`
3. Description: "Remote MCP Server for Employee Registration API with circular schema references"
4. Keep it public or private (your choice)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)

### Step 4: Push to GitHub

```bash
# Add remote origin (replace with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/employee-registration-api-remote.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 5: Deploy on Render.com

1. **Login to Render**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Sign in or create an account

2. **Create New Web Service**
   - Click "New +" button in the top right
   - Select "Web Service"

3. **Connect Repository**
   - Click "Connect account" if not already connected
   - Select your GitHub account
   - Find and select `employee-registration-api-remote` repository
   - Click "Connect"

4. **Configure Service** (Auto-detected from render.yaml)
   - **Name**: `employee-registration-api-remote` (auto-filled)
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: Node (auto-detected)
   - **Build Command**: `npm install && npm run build` (auto-filled)
   - **Start Command**: `npm start` (auto-filled)
   - **Plan**: Free

5. **Environment Variables** (Auto-configured)
   The following are automatically set from `render.yaml`:
   - `NODE_VERSION`: 18.0.0
   - `PORT`: 10000

6. **Deploy**
   - Click "Create Web Service"
   - Render will start building and deploying your service
   - Wait for the deployment to complete (usually 2-5 minutes)

### Step 6: Verify Deployment

Once deployed, your service will be available at:
```
https://employee-registration-api-remote.onrender.com
```

Test the endpoints:

1. **Health Check**
   ```bash
   curl https://employee-registration-api-remote.onrender.com/health
   ```
   
   Expected response:
   ```json
   {
     "status": "ok",
     "timestamp": "2024-01-16T...",
     "service": "employee-registration-api-remote"
   }
   ```

2. **Root Endpoint**
   ```bash
   curl https://employee-registration-api-remote.onrender.com/
   ```
   
   Expected response:
   ```json
   {
     "message": "Employee Registration API with Circular References - Remote MCP Server",
     "version": "1.0.0",
     "transport": "HTTP",
     "endpoints": {
       "health": "/health",
       "mcp": "/mcp"
     },
     "documentation": "Demonstrates circular schema references where Person.manager references Person schema"
   }
   ```

3. **MCP Initialize**
   ```bash
   curl -X POST https://employee-registration-api-remote.onrender.com/mcp \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "id": 1,
       "method": "initialize",
       "params": {
         "protocolVersion": "2024-11-05",
         "capabilities": {},
         "clientInfo": {
           "name": "test-client",
           "version": "1.0.0"
         }
       }
     }'
   ```

## MCP Client Configuration

### For Cline/Roo-Cline

Add to your MCP settings file (usually in VS Code settings):

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

### For Claude Desktop

Add to `claude_desktop_config.json`:

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

## Testing the MCP Server

Once configured in your MCP client, you can test the tool:

**Prompt to test:**
```
Use the employee-registration-api to register a new employee named Sarah Martinez (EMP-201) 
in the Engineering department as a Software Engineer, with Michael Chen (EMP-150) as her manager.
```

The tool should successfully register the employee and return a confirmation with:
- Employee details
- Manager information
- Reporting chain
- Registration timestamp

## Monitoring and Logs

### View Logs on Render

1. Go to your service dashboard on Render
2. Click on "Logs" tab
3. You'll see real-time logs including:
   - Server startup messages
   - MCP request handling
   - Tool execution logs
   - API call results

### Common Log Messages

- `Received MCP request: initialize` - Client initializing
- `Received MCP request: tools/list` - Client requesting available tools
- `Received MCP request: tools/call` - Tool being executed
- `Handling CallTool request: register_employee` - Employee registration in progress

## Troubleshooting

### Issue: Service won't start

**Solution**: Check the logs for build errors. Common issues:
- Missing dependencies: Run `npm install` locally first
- TypeScript errors: Run `npm run build` locally to check
- Port conflicts: Render automatically assigns PORT environment variable

### Issue: MCP connection fails

**Solution**: 
- Verify the URL is correct: `https://employee-registration-api-remote.onrender.com/mcp`
- Check if the service is running: Visit the health endpoint
- Review Render logs for connection errors

### Issue: Tool execution fails

**Solution**:
- Verify the backend API is accessible: `https://complex-tools-openapi.onrender.com/api/v1`
- Check the request payload matches the schema
- Review error messages in the response

### Issue: Free tier limitations

**Note**: Render free tier services:
- Spin down after 15 minutes of inactivity
- Take 30-60 seconds to spin up on first request
- Have 750 hours/month limit

**Solution**: Upgrade to paid tier for always-on service, or accept the cold start delay.

## Updating the Deployment

To update your deployed service:

```bash
# Make your changes
# ...

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

Render will automatically detect the push and redeploy your service.

## Environment Variables (Optional)

If you need to add custom environment variables:

1. Go to your service on Render dashboard
2. Click "Environment" tab
3. Add variables as needed
4. Click "Save Changes"
5. Service will automatically redeploy

## Cost Considerations

**Free Tier Includes:**
- 750 hours/month of runtime
- Automatic SSL certificates
- Custom domains
- Automatic deploys from Git

**Paid Plans Start At:**
- $7/month for always-on service
- More memory and CPU
- Priority support

## Security Notes

1. **HTTPS**: All Render services use HTTPS by default
2. **CORS**: Currently configured to allow all origins (`*`)
3. **API Keys**: No authentication required for this demo
4. **Rate Limiting**: Not implemented (consider adding for production)

## Support and Resources

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **MCP Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **OpenAPI Spec**: Circular reference pattern for organizational hierarchies

---

Made with Bob