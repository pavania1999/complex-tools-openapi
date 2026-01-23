# Deployment Guide - Array Handling API Remote MCP Server

Complete guide to deploy the Array Handling API Remote MCP Server to Render.com.

## Prerequisites

1. **GitHub Account**: Required to host the repository
2. **Render.com Account**: Sign up at [render.com](https://render.com) (free tier available)
3. **Git**: Installed on your local machine

## Step-by-Step Deployment

### Step 1: Prepare the Repository

Navigate to the project directory:
```bash
cd Test_data_tools/MCP_Servers/array-handling/array-handling-api-remote
```

### Step 2: Initialize Git Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: Array Handling API Remote MCP Server (TC-P0-API-002)"
```

### Step 3: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `array-handling-api-remote`
3. Description: "Remote MCP Server for Array Handling API with raw array structures (TC-P0-API-002)"
4. Keep it public or private (your choice)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)

### Step 4: Push to GitHub

```bash
# Add remote origin (replace with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/array-handling-api-remote.git

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
   - Find and select `array-handling-api-remote` repository
   - Click "Connect"

4. **Configure Service** (Auto-detected from render.yaml)
   - **Name**: `array-handling-api-remote` (auto-filled)
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
https://array-handling-api-remote.onrender.com
```

Test the endpoints:

1. **Health Check**
   ```bash
   curl https://array-handling-api-remote.onrender.com/health
   ```
   
   Expected response:
   ```json
   {
     "status": "ok",
     "timestamp": "2024-01-16T...",
     "service": "array-handling-api-remote",
     "transport": "HTTP"
   }
   ```

2. **Root Endpoint**
   ```bash
   curl https://array-handling-api-remote.onrender.com/
   ```
   
   Expected response:
   ```json
   {
     "message": "Array Handling API - Remote MCP Server (TC-P0-API-002)",
     "version": "1.0.0",
     "transport": "HTTP",
     "endpoints": {
       "health": "/health",
       "mcp": "/mcp"
     },
     "documentation": "Test case for raw array handling with react-intrinsic style"
   }
   ```

3. **MCP Endpoint**
   ```bash
   curl -X POST https://array-handling-api-remote.onrender.com/mcp \
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
    "array-handling-api": {
      "url": "https://array-handling-api-remote.onrender.com/mcp",
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
    "array-handling-api": {
      "url": "https://array-handling-api-remote.onrender.com/mcp",
      "transport": "http"
    }
  }
}
```

## Testing the MCP Server

Once configured in your MCP client, you can test the tools:

**Prompt to test inventory items:**
```
Use the array-handling-api to process inventory items: a Laptop (LAP-001) with 5 units at $999.99 in Electronics category, and a Mouse (MOU-002) with 20 units at $29.99 in Accessories category
```

**Prompt to test batch orders:**
```
Use the array-handling-api to process batch orders: Order ORD-001 for John Doe with 1 Laptop at $999.99 and 2 Mice at $29.99 each, and Order ORD-002 for Jane Smith with 1 Monitor at $299.99
```

## Monitoring and Logs

### View Logs on Render

1. Go to your service dashboard on Render
2. Click on "Logs" tab
3. You'll see real-time logs including:
   - Server startup messages
   - HTTP connection events
   - Tool execution logs
   - API call results

### Common Log Messages

- `Array Handling API Remote MCP Server running on port 10000` - Server started
- `Received MCP request: initialize` - Client connecting
- `Received MCP request: tools/list` - Client requesting available tools
- `Handling CallTool request: process_inventory_items_raw` - Tool being executed

## Troubleshooting

### Issue: Service won't start

**Solution**: Check the logs for build errors. Common issues:
- Missing dependencies: Run `npm install` locally first
- TypeScript errors: Run `npm run build` locally to check
- Port conflicts: Render automatically assigns PORT environment variable

### Issue: HTTP connection fails

**Solution**: 
- Verify the URL is correct: `https://array-handling-api-remote.onrender.com/mcp`
- Check if the service is running: Visit the health endpoint
- Review Render logs for connection errors

### Issue: Tool execution fails

**Solution**:
- Verify the backend API is accessible: `https://complex-tools-openapi.onrender.com/api/v1`
- Check the request payload matches the schema (raw array format)
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
- **Test Case**: TC-P0-API-002 - Array Handling with react-intrinsic

---

Made with Bob