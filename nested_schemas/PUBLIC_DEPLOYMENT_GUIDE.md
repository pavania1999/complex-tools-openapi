# Public Deployment Guide - Expose APIs Publicly

## Overview

This guide shows you how to deploy the Nested Schema Testing APIs to public endpoints that can be accessed by anyone, including watsonx Orchestrate.

---

## Option 1: Render.com (Recommended - Free & Easy)

### Why Render?
- ✅ **Free tier available**
- ✅ **Automatic HTTPS**
- ✅ **Easy deployment from GitHub**
- ✅ **No credit card required**
- ✅ **Always-on public URL**

### Steps:

#### 1. Prepare Your Repository

Create a `render.yaml` file in the `nested_schemas` directory:

```yaml
services:
  - type: web
    name: nested-schema-api
    env: python
    buildCommand: pip install -r api_requirements.txt
    startCommand: python api_server.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

#### 2. Deploy to Render

1. **Sign up**: Go to https://render.com and create a free account
2. **New Web Service**: Click "New +" → "Web Service"
3. **Connect Repository**: 
   - Connect your GitHub/GitLab account
   - Select your repository
   - Set root directory to `agentic_data/tools/nested_schemas`
4. **Configure**:
   - Name: `nested-schema-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r api_requirements.txt`
   - Start Command: `python api_server.py`
5. **Deploy**: Click "Create Web Service"

#### 3. Get Your Public URL

After deployment (takes 2-3 minutes):
```
https://nested-schema-api.onrender.com
```

#### 4. Test Your Endpoints

```bash
# Health check
curl https://complex-tools-openapi.onrender.com/api/v1/health

# Get OpenAPI specs
curl https://complex-tools-openapi.onrender.com/api/v1/openapi/orders
curl https://complex-tools-openapi.onrender.com/api/v1/openapi/employees
```

#### 5. Import to watsonx Orchestrate

Use these URLs:
```
https://complex-tools-openapi.onrender.com/api/v1/openapi/orders
https://complex-tools-openapi.onrender.comapi/v1/openapi/employees
```

---

## Option 2: Railway.app (Alternative - Free Tier)

### Why Railway?
- ✅ **$5 free credit monthly**
- ✅ **Automatic HTTPS**
- ✅ **GitHub integration**
- ✅ **Simple deployment**

### Steps:

#### 1. Create `railway.json`

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python api_server.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. Deploy

1. **Sign up**: https://railway.app
2. **New Project**: Click "New Project"
3. **Deploy from GitHub**: Select your repository
4. **Configure**: Railway auto-detects Python
5. **Deploy**: Automatic deployment starts

#### 3. Get Public URL

Railway provides:
```
https://nested-schema-api-production.up.railway.app
```

---

## Option 3: Fly.io (Production-Ready)

### Why Fly.io?
- ✅ **Free tier: 3 VMs**
- ✅ **Global deployment**
- ✅ **Automatic HTTPS**
- ✅ **CLI-based deployment**

### Steps:

#### 1. Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

#### 2. Create `fly.toml`

```toml
app = "nested-schema-api"
primary_region = "iad"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services]]
  protocol = "tcp"
  internal_port = 8080

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

#### 3. Update `api_server.py` for Fly.io

Change the last line:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### 4. Deploy

```bash
cd agentic_data/tools/nested_schemas

# Login
flyctl auth login

# Launch app
flyctl launch

# Deploy
flyctl deploy
```

#### 5. Get Public URL

```
https://nested-schema-api.fly.dev
```

---

## Option 4: PythonAnywhere (Easiest for Beginners)

### Why PythonAnywhere?
- ✅ **Completely free tier**
- ✅ **No credit card needed**
- ✅ **Web-based interface**
- ✅ **Python-focused**

### Steps:

#### 1. Sign Up

Go to https://www.pythonanywhere.com and create a free account

#### 2. Upload Files

1. Go to **Files** tab
2. Create directory: `/home/yourusername/nested_schemas`
3. Upload all files:
   - `api_server.py`
   - `api_requirements.txt`
   - `tc_p0_py_001/` directory
   - `tc_p0_py_003/` directory

#### 3. Install Dependencies

1. Go to **Consoles** tab
2. Start a **Bash console**
3. Run:
```bash
cd nested_schemas
pip3 install --user -r api_requirements.txt
```

#### 4. Configure Web App

1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Flask**
4. Python version: **3.9**
5. Set path to: `/home/yourusername/nested_schemas/api_server.py`
6. Click **Reload**

#### 5. Get Public URL

```
https://yourusername.pythonanywhere.com
```

---

## Option 5: Heroku (Classic Option)

### Why Heroku?
- ✅ **Well-established platform**
- ✅ **Free tier available**
- ✅ **Git-based deployment**

### Steps:

#### 1. Create `Procfile`

```
web: python api_server.py
```

#### 2. Create `runtime.txt`

```
python-3.9.18
```

#### 3. Update `api_server.py`

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

#### 4. Deploy

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create nested-schema-api

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

#### 5. Get Public URL

```
https://nested-schema-api.herokuapp.com
```

---

## Quick Comparison

| Platform | Free Tier | Setup Time | Ease of Use | Always On |
|----------|-----------|------------|-------------|-----------|
| **Render** | ✅ Yes | 5 min | ⭐⭐⭐⭐⭐ | ✅ Yes |
| **Railway** | ✅ $5/month | 5 min | ⭐⭐⭐⭐⭐ | ✅ Yes |
| **Fly.io** | ✅ Yes | 10 min | ⭐⭐⭐⭐ | ⚠️ Auto-sleep |
| **PythonAnywhere** | ✅ Yes | 15 min | ⭐⭐⭐ | ✅ Yes |
| **Heroku** | ✅ Yes | 10 min | ⭐⭐⭐⭐ | ⚠️ Auto-sleep |

**Recommendation**: Use **Render.com** for the easiest setup with always-on free tier.

---

## After Deployment

### 1. Update OpenAPI Specs

Update the `servers` section in both YAML files:

**tc_p0_py_001/openapi_customer_order.yaml**:
```yaml
servers:
  - url: https://your-app.onrender.com/api/v1
    description: Production server
```

**tc_p0_py_003/openapi_employee_management.yaml**:
```yaml
servers:
  - url: https://your-app.onrender.com/api/v1
    description: Production server
```

### 2. Test Public Endpoints

```bash
# Replace with your actual URL
export API_URL="https://your-app.onrender.com"

# Health check
curl $API_URL/api/v1/health

# Test orders endpoint
curl -X POST $API_URL/api/v1/orders/process \
  -H "Content-Type: application/json" \
  -d '{"customer":{"name":"Test"},"order":{"order_id":"TEST-001","items":[]}}'

# Get OpenAPI specs
curl $API_URL/api/v1/openapi/orders
curl $API_URL/api/v1/openapi/employees
```

### 3. Import to watsonx Orchestrate

1. Go to **Tools → Import → OpenAPI**
2. Enter URL:
   ```
   https://your-app.onrender.com/api/v1/openapi/orders
   ```
3. Click **Import**
4. Repeat for employees endpoint:
   ```
   https://your-app.onrender.com/api/v1/openapi/employees
   ```

### 4. Create Agents

Use the agent configurations from `IMPLEMENTATION_GUIDE.md` but reference the OpenAPI tool names.

---

## Security Considerations

### For Public APIs:

1. **Rate Limiting** (Add to `api_server.py`):
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/v1/orders/process', methods=['POST'])
@limiter.limit("10 per minute")
def process_order():
    # ... existing code
```

2. **API Key Authentication** (Optional):
```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.environ.get('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/v1/orders/process', methods=['POST'])
@require_api_key
def process_order():
    # ... existing code
```

3. **Input Validation**:
```python
from jsonschema import validate, ValidationError

@app.route('/api/v1/orders/process', methods=['POST'])
def process_order():
    try:
        data = request.get_json()
        # Validate against schema
        validate(instance=data, schema=order_schema)
        # ... process
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
```

---

## Monitoring & Logs

### View Logs:

**Render**:
```bash
# In Render dashboard → Logs tab
```

**Railway**:
```bash
# In Railway dashboard → Deployments → View Logs
```

**Fly.io**:
```bash
flyctl logs
```

**Heroku**:
```bash
heroku logs --tail
```

---

## Troubleshooting

### Issue: App Sleeps After Inactivity

**Solution**: Use a service like UptimeRobot (free) to ping your endpoint every 5 minutes:
1. Sign up at https://uptimerobot.com
2. Add monitor with your health check URL
3. Set interval to 5 minutes

### Issue: CORS Errors

**Solution**: Already handled in `api_server.py` with `flask-cors`. If issues persist:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Allow all origins
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Issue: Slow Cold Starts

**Solution**: 
- Use Render (no cold starts on free tier)
- Or keep app warm with UptimeRobot pings

---

## Cost Estimates

All options have **FREE tiers** suitable for testing:

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Render | 750 hours/month | $7/month |
| Railway | $5 credit/month | Pay as you go |
| Fly.io | 3 VMs free | $1.94/month per VM |
| PythonAnywhere | 1 web app | $5/month |
| Heroku | 550 hours/month | $7/month |

**For testing**: Free tiers are sufficient
**For production**: Consider paid tiers for better performance

---

## Next Steps

1. ✅ Choose a deployment platform (Render recommended)
2. ✅ Deploy the API server
3. ✅ Test public endpoints
4. ✅ Update OpenAPI specs with public URL
5. ✅ Import to watsonx Orchestrate
6. ✅ Create agents
7. ✅ Test with utterances

---

## Support

If you encounter issues:
1. Check platform-specific documentation
2. Review server logs
3. Test endpoints with cURL/Postman
4. Verify OpenAPI spec is valid

---

**Last Updated**: 2024-01-16
**Recommended Platform**: Render.com
**Status**: Ready for Public Deployment ✅