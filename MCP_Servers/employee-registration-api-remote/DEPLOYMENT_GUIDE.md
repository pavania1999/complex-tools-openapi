# Deployment Guide - Employee Registration API Remote MCP Server

Complete guide for deploying the Employee Registration API as a remote MCP server.

## Prerequisites

- Node.js 18+ installed
- Git repository
- Render.com account (free tier available)
- GitHub account

## Local Setup

### 1. Install Dependencies

```bash
cd MCP_Servers/employee-registration-api-remote
npm install
```

### 2. Build the Project

```bash
npm run build
```

### 3. Test Locally

```bash
# Development mode with auto-reload
npm run dev

# Or production mode
npm start
```

The server will start on `http://localhost:3000`

### 4. Verify Local Installation

Open another terminal and test:

```bash
# Health check
curl http://localhost:3000/health

# Server info
curl http://localhost:3000/
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2024-01-05T10:00:00.000Z",
  "service": "employee-registration-api-remote"
}
```

## Deployment to Render.com

### Option 1: Deploy via GitHub (Recommended)

#### Step 1: Push to GitHub

```bash
# Initialize git if not already done
git init

# Add files
git add .

# Commit
git commit -m "Add employee registration remote MCP server"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/your-repo.git

# Push
git push -u origin main
```

#### Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** and authorize Render
4. Select your repository
5. Configure the service:

   **Basic Settings:**
   - **Name**: `employee-registration-api-remote`
   - **Region**: Choose closest to your users (e.g., Oregon)
   - **Branch**: `main`
   - **Root Directory**: `MCP_Servers/employee-registration-api-remote`

   **Build & Deploy:**
   - **Runtime**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`

   **Plan:**
   - Select **Free** tier

6. Click **"Create Web Service"**

#### Step 3: Wait for Deployment

Render will:
- Clone your repository
- Install dependencies
- Build the TypeScript code
- Start the server

This typically takes 2-5 minutes.

#### Step 4: Get Your Deployment URL

After successful deployment, you'll see:
```
https://employee-registration-api-remote.onrender.com
```

### Option 2: Deploy via render.yaml (Infrastructure as Code)

The project includes a `render.yaml` file for automated deployment.

1. Push your code to GitHub
2. Go to Render Dashboard
3. Click **"New +"** → **"Blueprint"**
4. Connect your repository
5. Render will automatically detect `render.yaml` and configure the service
6. Click **"Apply"**

## Post-Deployment Verification

### 1. Test Health Endpoint

```bash
curl https://your-deployment-url.onrender.com/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2024-01-05T10:00:00.000Z",
  "service": "employee-registration-api-remote"
}
```

### 2. Test Server Info

```bash
curl https://your-deployment-url.onrender.com/
```

Expected response:
```json
{
  "message": "Employee Registration API - Remote MCP Server",
  "version": "1.0.0",
  "transport": "SSE",
  "endpoints": {
    "health": "/health",
    "sse": "/sse"
  }
}
```

### 3. Test SSE Endpoint

```bash
curl https://your-deployment-url.onrender.com/sse
```

This should establish an SSE connection (you'll see connection headers).

## Configure MCP Clients

### Claude Desktop Configuration

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

Add this configuration:

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

**Important**: Replace `your-deployment-url.onrender.com` with your actual Render URL.

### Watson Orchestrate Configuration

1. Open Watson Orchestrate
2. Go to **Settings** → **MCP Servers**
3. Click **"Add Server"**
4. Configure:
   - **Name**: `Employee Registration API`
   - **URL**: `https://your-deployment-url.onrender.com/sse`
   - **Transport**: `SSE`
5. Click **"Test Connection"**
6. Click **"Save"**

## Monitoring & Maintenance

### View Logs

1. Go to Render Dashboard
2. Select your service
3. Click **"Logs"** tab
4. View real-time logs

### Monitor Performance

1. Go to Render Dashboard
2. Select your service
3. Click **"Metrics"** tab
4. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Update Deployment

Render automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push
```

Render will automatically:
- Detect the push
- Rebuild the service
- Deploy the new version
- Zero-downtime deployment

## Troubleshooting

### Issue: Build Fails

**Solution**: Check build logs in Render dashboard
- Verify `package.json` dependencies
- Ensure TypeScript compiles locally first
- Check Node version compatibility

### Issue: Server Won't Start

**Solution**: Check start command
- Verify `npm start` works locally
- Check `dist/index.js` exists after build
- Review environment variables

### Issue: SSE Connection Fails

**Solution**: 
- Verify CORS settings in `src/index.ts`
- Check firewall/network settings
- Test with curl first
- Verify URL in client configuration

### Issue: API Calls Timeout

**Solution**:
- Check underlying API is accessible: `https://complex-tools-openapi.onrender.com/api/v1`
- Verify network connectivity
- Check Render service status
- Review timeout settings (currently 30s)

### Issue: Free Tier Limitations

Render Free Tier:
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 750 hours/month free

**Solutions**:
- Upgrade to paid tier for always-on service
- Use external monitoring to keep service warm
- Accept cold start delay for free tier

## Environment Variables

Set in Render Dashboard → Service → Environment:

| Variable | Value | Description |
|----------|-------|-------------|
| `PORT` | `10000` | Server port (auto-set by Render) |
| `NODE_ENV` | `production` | Environment mode |
| `NODE_VERSION` | `18.0.0` | Node.js version |

## Security Best Practices

### For Production Use:

1. **Add Authentication**:
   ```typescript
   // Add API key validation
   app.use((req, res, next) => {
     const apiKey = req.headers['x-api-key'];
     if (apiKey !== process.env.API_KEY) {
       return res.status(401).json({ error: 'Unauthorized' });
     }
     next();
   });
   ```

2. **Configure CORS**:
   ```typescript
   app.use(cors({
     origin: ['https://your-allowed-domain.com'],
     credentials: true
   }));
   ```

3. **Add Rate Limiting**:
   ```bash
   npm install express-rate-limit
   ```

4. **Use HTTPS**: Render provides this automatically

5. **Set Environment Variables**: Never commit secrets to Git

## Scaling

### Horizontal Scaling

Render automatically handles:
- Load balancing
- Multiple instances
- Auto-scaling (paid plans)

### Vertical Scaling

Upgrade Render plan for:
- More CPU
- More memory
- Faster response times

## Cost Estimation

### Free Tier
- **Cost**: $0/month
- **Limitations**: 
  - 750 hours/month
  - Spins down after inactivity
  - Shared resources

### Starter Plan
- **Cost**: $7/month
- **Benefits**:
  - Always on
  - Dedicated resources
  - Better performance

### Professional Plan
- **Cost**: $25/month
- **Benefits**:
  - Auto-scaling
  - Priority support
  - Advanced metrics

## Support

- **Render Documentation**: https://render.com/docs
- **MCP Documentation**: https://modelcontextprotocol.io
- **GitHub Issues**: Create issue in your repository

---

**Created**: 2026-01-05
**Author**: IBM Bob
**Version**: 1.0.0

Made with Bob