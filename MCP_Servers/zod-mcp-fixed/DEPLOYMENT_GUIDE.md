# Deployment Guide for Screening API on Render.com

## Quick Deploy Steps

Since you already have a GitHub repository linked, follow these steps:

### Step 1: Push Changes to GitHub

```bash
cd /Users/pavaniaddepalli/Documents/Docs/BOB/Complex_Tools/MCP_Servers/zod-mcp-fixed
git add .
git commit -m "Add Screening API with nested schemas"
git push
```

### Step 2: Deploy on Render.com

#### Option A: Using render.yaml (Recommended)

1. Go to https://render.com/
2. Sign in to your account
3. Click "New +" → "Blueprint"
4. Select your connected GitHub repository
5. Render will automatically detect the `render.yaml` file
6. Click "Apply" to deploy

#### Option B: Manual Setup

1. Go to https://render.com/
2. Click "New +" → "Web Service"
3. Select your GitHub repository
4. Configure:
   - **Name**: `screening-api`
   - **Region**: Oregon (US West)
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `MCP_Servers/zod-mcp-fixed`
   - **Environment**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Plan**: Free
5. Click "Create Web Service"

### Step 3: Verify Deployment

Once deployed, test your API:

**Health Check:**
```bash
curl https://your-service-name.onrender.com/health
```

**API Endpoint:**
```bash
curl -X POST https://your-service-name.onrender.com/api/searchAndWait \
  -H "Content-Type: application/json" \
  -d @test-payload.json
```

### Step 4: Update OpenAPI Spec

After deployment, update `openapi_screening.yaml` with your actual Render URL:

```yaml
servers:
  - url: https://your-service-name.onrender.com
    description: Production server
```

## API Features

✅ Complex nested schema validation using Zod
✅ RESTful endpoints
✅ TypeScript implementation
✅ Express.js server
✅ OpenAPI 3.0 specification

## Nested Schema Structure

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

## Free Tier Notes

- Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- 750 hours of runtime per month (free tier)

## Troubleshooting

**Build Fails:**
- Check build logs in Render dashboard
- Verify all dependencies are in `package.json`

**Service Won't Start:**
- Check that PORT environment variable is used
- Review service logs for errors

**API Errors:**
- Test locally first
- Verify request payload matches schema
- Check logs for detailed error messages