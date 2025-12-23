# Complex Tools OpenAPI Specifications

This repository contains OpenAPI specifications and API server implementations for testing nested schemas and complex data structures.

## 📁 Repository Structure

```
nested_schemas/
├── api_server.py              # Flask API server serving OpenAPI specs
├── api_requirements.txt       # Python dependencies
├── render.yaml               # Render.com deployment configuration
├── IMPLEMENTATION_GUIDE.md   # Implementation details
├── PUBLIC_DEPLOYMENT_GUIDE.md # Deployment instructions
├── TEST_UTTERANCES.md        # Test cases and utterances
├── tc_p0_py_001/            # Customer Order API
│   ├── openapi_customer_order.yaml
│   ├── process_customer_order.py
│   └── README.md
└── tc_p0_py_003/            # Employee Management API
    ├── openapi_employee_management.yaml
    ├── process_complex_data.py
    ├── requirements.txt
    └── README.md
```

## 🚀 Quick Start

### Local Development

1. Install dependencies:
```bash
cd nested_schemas
pip install -r api_requirements.txt
```

2. Run the API server:
```bash
python api_server.py
```

3. Access OpenAPI specs:
- Customer Order API: `http://localhost:8080/openapi/customer-order`
- Employee Management API: `http://localhost:8080/openapi/employee-management`

## 🌐 Public URLs

Once deployed, the OpenAPI specifications will be available at:
- `https://your-app.onrender.com/openapi/customer-order`
- `https://your-app.onrender.com/openapi/employee-management`

## 📚 API Endpoints

### Customer Order API (`tc_p0_py_001`)
- **POST** `/process-customer-order` - Process customer orders with nested product details
- Supports complex nested schemas with products, addresses, and payment information

### Employee Management API (`tc_p0_py_003`)
- **POST** `/process-complex-data` - Process employee data with nested structures
- Handles employee records with departments, projects, and contact information

## 🔧 Deployment

See [PUBLIC_DEPLOYMENT_GUIDE.md](nested_schemas/PUBLIC_DEPLOYMENT_GUIDE.md) for detailed deployment instructions on Render.com or other platforms.

## 📖 Documentation

- [Implementation Guide](nested_schemas/IMPLEMENTATION_GUIDE.md) - Technical implementation details
- [Test Utterances](nested_schemas/TEST_UTTERANCES.md) - Test cases and example requests

## 🧪 Testing

Each API includes example test cases and utterances for validation. See the individual README files in each test case directory.

## 📄 License

This project is available for testing and educational purposes.