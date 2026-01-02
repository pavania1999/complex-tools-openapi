# Employee Registration API - Deployment Guide

## Quick Deploy to Render

### Prerequisites
- GitHub account
- Render account (free tier available)
- Git repository with this code

### Deployment Steps

#### 1. Push Code to GitHub

```bash
cd nested_schemas/tc_p0_py_003
git add .
git commit -m "Add employee registration API with circular Person schema"
git push origin main
```

#### 2. Deploy on Render

**Option A: Using Render Dashboard**

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `employee-registration-api`
   - **Environment**: `Python 3`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Root Directory**: `nested_schemas/tc_p0_py_003`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api_server:app`
   - **Plan**: `Free`
5. Click **"Create Web Service"**

**Option B: Using render.yaml (Blueprint)**

1. Ensure `render.yaml` is in your repository
2. Go to https://dashboard.render.com/
3. Click **"New +"** → **"Blueprint"**
4. Connect your repository
5. Render will auto-detect `render.yaml` and deploy

#### 3. Verify Deployment

Once deployed, your service will be available at:
```
https://employee-registration-api.onrender.com
```

Test the endpoints:

```bash
# Health check
curl https://employee-registration-api.onrender.com/api/v1/health

# Get OpenAPI spec
curl https://employee-registration-api.onrender.com/api/v1/openapi

# Register employee
curl -X POST https://employee-registration-api.onrender.com/api/v1/employees/register \
  -H "Content-Type: application/json" \
  -d '{
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
        "department": "Engineering",
        "position": "Engineering Manager"
      }
    }
  }'
```

## Update OpenAPI Spec with Production URL

After deployment, update the OpenAPI spec with your production URL:

```yaml
servers:
  - url: https://employee-registration-api.onrender.com/api/v1
    description: Production server
  - url: http://localhost:5000/api/v1
    description: Local development server
```

## Environment Variables

Render automatically sets:
- `PORT`: 10000 (default for web services)
- `PYTHON_VERSION`: 3.11.0 (specified in render.yaml)

No additional environment variables needed for basic operation.

## Monitoring

### View Logs

1. Go to your service in Render Dashboard
2. Click **"Logs"** tab
3. Monitor real-time logs

### Check Service Status

```bash
curl https://employee-registration-api.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Employee Registration API",
  "version": "1.0.0",
  "endpoints": {
    "register": "/api/v1/employees/register",
    "health": "/api/v1/health",
    "openapi": "/api/v1/openapi"
  }
}
```

## Troubleshooting

### Build Fails

**Issue**: Dependencies not installing
**Solution**: Check `requirements.txt` is in the correct directory

**Issue**: Python version mismatch
**Solution**: Verify `PYTHON_VERSION` in render.yaml matches requirements

### Service Won't Start

**Issue**: Port binding error
**Solution**: Ensure `api_server.py` uses `PORT` environment variable:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

**Issue**: Import errors
**Solution**: Check all Python files are in the same directory

### API Returns 500 Error

**Issue**: Runtime error in code
**Solution**: Check Render logs for stack trace

**Issue**: Missing dependencies
**Solution**: Verify all imports are in `requirements.txt`

## Free Tier Limitations

Render's free tier includes:
- ✅ 750 hours/month of runtime
- ✅ Automatic HTTPS
- ✅ Automatic deploys from Git
- ⚠️ Service spins down after 15 minutes of inactivity
- ⚠️ Cold start time: ~30 seconds

**Note**: First request after inactivity may be slow due to cold start.

## Scaling

To upgrade from free tier:
1. Go to service settings in Render Dashboard
2. Click **"Change Plan"**
3. Select paid tier for:
   - No cold starts
   - More resources
   - Custom domains
   - Priority support

## CI/CD

Render automatically deploys when you push to your connected branch:

```bash
git add .
git commit -m "Update employee registration logic"
git push origin main
# Render automatically deploys the changes
```

## Custom Domain

To use a custom domain:
1. Go to service settings
2. Click **"Custom Domains"**
3. Add your domain
4. Update DNS records as instructed
5. Render handles SSL certificates automatically

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com/
- GitHub Issues: [Your repository issues page]

---

**Deployment Status**: Ready for production ✅

**Last Updated**: 2024-01-02