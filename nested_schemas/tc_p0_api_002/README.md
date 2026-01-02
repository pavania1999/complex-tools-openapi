# TC-P0-API-002: Array Handling Test Case

## Test Case Information

**Test ID**: TC-P0-API-002  
**Test Name**: OpenAPI + React-Intrinsic + gpt-oss-120b + Array Handling  
**Priority**: P0 (Critical)  
**Type**: Integration  
**Automation Status**: Automated  
**Epic**: #45755 - Nested Schema Support

## Test Objective

Validate that the system correctly handles both **wrapped arrays** and **raw arrays** in OpenAPI specifications when using react-intrinsic style with gpt-oss-120b model.

## Test Configuration

- **Agent Style**: react-intrinsic
- **Model**: gpt-oss-120b
- **Schema Type**: Array Handling (Group 2)
- **Array Types Tested**:
  - Wrapped Arrays (arrays within object properties)
  - Raw Arrays (arrays at request body level)

## Files in This Directory

### OpenAPI Specifications

1. **`openapi_array_handling_wrapped.yaml`**
   - Demonstrates wrapped array structure
   - Arrays are contained within object properties
   - Example: `{"items": [...]}`
   - **Status**: Valid OpenAPI 3.0 structure

2. **`openapi_array_handling_raw.yaml`**
   - Demonstrates raw array structure
   - Arrays at request body level
   - Example: `[{...}, {...}]`
   - **Status**: Valid OpenAPI 3.0 structure

3. **`openapi_array_handling_raw_NEGATIVE.yaml`** (deprecated)
   - Originally intended as negative test
   - Note: Raw arrays are valid per OpenAPI spec
   - Kept for reference only

### Implementation Files

4. **`process_array_handling.py`**
   - Flask API server implementation
   - Handles both wrapped and raw array endpoints
   - Includes demo examples and health check

5. **`requirements.txt`**
   - Python dependencies for the Flask server

## API Endpoints

### Wrapped Array Endpoints

#### 1. Process Inventory Items (Wrapped)
```
POST /api/v1/inventory/process-items
Content-Type: application/json

{
  "items": [
    {
      "name": "Laptop",
      "sku": "LAP-001",
      "quantity": 5,
      "price": 999.99,
      "category": "Electronics",
      "specifications": {
        "brand": "TechCorp",
        "model": "Pro-X1",
        "warranty": "2 years"
      }
    }
  ]
}
```

#### 2. Process Batch Orders (Wrapped)
```
POST /api/v1/orders/process-batch
Content-Type: application/json

{
  "orders": [
    {
      "order_id": "ORD-001",
      "customer_name": "John Doe",
      "items": [
        {
          "product_name": "Laptop",
          "quantity": 1,
          "unit_price": 999.99
        }
      ]
    }
  ]
}
```

### Raw Array Endpoints

#### 3. Process Inventory Items (Raw)
```
POST /api/v1/inventory/process-items-raw
Content-Type: application/json

[
  {
    "name": "Laptop",
    "sku": "LAP-001",
    "quantity": 5,
    "price": 999.99,
    "category": "Electronics",
    "specifications": {
      "brand": "TechCorp",
      "model": "Pro-X1",
      "warranty": "2 years"
    }
  }
]
```

#### 4. Process Batch Orders (Raw)
```
POST /api/v1/orders/process-batch-raw
Content-Type: application/json

[
  {
    "order_id": "ORD-001",
    "customer_name": "John Doe",
    "items": [
      {
        "product_name": "Laptop",
        "quantity": 1,
        "unit_price": 999.99
      }
    ]
  }
]
```

### Health Check
```
GET /health
```

## Test Steps

### Preconditions
1. OpenAPI specs with both wrapped and raw arrays available
2. Agent configured with react-intrinsic style
3. Model set to gpt-oss-120b
4. Flask server running on port 8002

### Test Execution

#### Test 1: Wrapped Arrays
1. Import `openapi_array_handling_wrapped.yaml`
   - **Expected**: Tool imported successfully
2. Send chat with wrapped array data
   - **Expected**: API receives `{"items": [...]}`
3. Verify API call succeeds
   - **Expected**: API processes array correctly
4. Check response format
   - **Expected**: Proper status and processed items returned

#### Test 2: Raw Arrays
1. Import `openapi_array_handling_raw.yaml`
   - **Expected**: Tool imported successfully
2. Send chat with raw array data
   - **Expected**: API receives `[{...}, {...}]`
3. Verify API call succeeds
   - **Expected**: API processes array correctly
4. Check response format
   - **Expected**: Proper status and processed items returned

## Running the Server

### Local Development

1. **Install Dependencies**
```bash
cd nested_schemas/tc_p0_api_002
pip install -r requirements.txt
```

2. **Run the Server**
```bash
python process_array_handling.py
```

The server will start on `http://0.0.0.0:8002`

3. **Test with curl**

Wrapped array:
```bash
curl -X POST http://localhost:8002/api/v1/inventory/process-items \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "name": "Laptop",
        "sku": "LAP-001",
        "quantity": 5,
        "price": 999.99,
        "category": "Electronics",
        "specifications": {
          "brand": "TechCorp",
          "model": "Pro-X1",
          "warranty": "2 years"
        }
      }
    ]
  }'
```

Raw array:
```bash
curl -X POST http://localhost:8002/api/v1/inventory/process-items-raw \
  -H "Content-Type: application/json" \
  -d '[
    {
      "name": "Laptop",
      "sku": "LAP-001",
      "quantity": 5,
      "price": 999.99,
      "category": "Electronics",
      "specifications": {
        "brand": "TechCorp",
        "model": "Pro-X1",
        "warranty": "2 years"
      }
    }
  ]'
```

### Production Deployment

The API is deployed on Render.com:
- **Base URL**: `https://complex-tools-openapi.onrender.com/api/v1`
- **Health Check**: `https://complex-tools-openapi.onrender.com/health`

## Expected Results

### Success Criteria

1. **Import Success**
   - Both wrapped and raw array specs import without errors
   - Tools appear in agent's tool catalog

2. **API Processing**
   - Wrapped arrays: Correctly processes `{"items": [...]}`
   - Raw arrays: Correctly processes `[{...}, {...}]`
   - Nested arrays within items are handled properly

3. **Response Format**
   - Status: "success"
   - Message: Descriptive success message
   - Processed items: Array of processed results
   - Total value/revenue: Calculated correctly

### Sample Success Response

```json
{
  "status": "success",
  "message": "Successfully processed 2 inventory items",
  "processed_items": [
    {
      "name": "Laptop",
      "sku": "LAP-001",
      "status": "added",
      "inventory_id": "INV-2024-001",
      "quantity": 5,
      "unit_price": 999.99,
      "total_value": 4999.95,
      "category": "Electronics",
      "specifications": {
        "brand": "TechCorp",
        "model": "Pro-X1",
        "warranty": "2 years"
      }
    }
  ],
  "total_value": 4999.95,
  "summary": {
    "total_items": 2,
    "total_quantity": 25,
    "categories": ["Electronics", "Accessories"]
  }
}
```

## Key Features Tested

### 1. Wrapped Arrays
- ✅ Arrays contained in object properties
- ✅ Descriptive property names (items, orders)
- ✅ Compatible with all agent styles
- ✅ Clear structure for nested data

### 2. Raw Arrays
- ✅ Arrays at request body level
- ✅ Valid per OpenAPI 3.0 specification
- ✅ Direct array processing
- ✅ Efficient for simple list operations

### 3. Nested Arrays
- ✅ Arrays within arrays (orders containing items)
- ✅ Multiple levels of nesting
- ✅ Proper schema references
- ✅ Complex data structures

### 4. Nested Objects
- ✅ Specifications within items
- ✅ Multiple nested properties
- ✅ Optional nested fields
- ✅ Schema composition

## Validation Points

1. **Schema Validation**
   - Required fields enforced
   - Data types validated
   - Constraints checked (min/max, patterns)

2. **Array Handling**
   - Empty arrays handled gracefully
   - Single item arrays processed
   - Multiple item arrays processed
   - Array size limits respected

3. **Nested Structure**
   - Nested objects accessed correctly
   - Nested arrays iterated properly
   - Deep nesting supported
   - Schema references resolved

4. **Error Handling**
   - Invalid JSON rejected
   - Missing required fields reported
   - Type mismatches caught
   - Clear error messages provided

## Related Test Cases

- **TC-P0-API-001**: Standard Nesting (Basic/Deep/References)
- **TC-P0-API-003**: Complex Scenarios (Real-World/Circular)
- **TC-P0-API-004**: Enums in Nested Schemas
- **TC-P0-API-005**: Multi-Field Slot Filling

## Notes

- Both wrapped and raw arrays are valid OpenAPI 3.0 structures
- The choice between wrapped and raw depends on use case and API design
- Wrapped arrays provide better context and extensibility
- Raw arrays are more concise for simple list operations
- The implementation handles both formats seamlessly

## Troubleshooting

### Common Issues

1. **Import Fails**
   - Check OpenAPI spec syntax
   - Verify server URL is accessible
   - Ensure schema references are valid

2. **API Returns 400**
   - Validate request body format
   - Check required fields are present
   - Verify data types match schema

3. **Server Not Starting**
   - Check port 8002 is available
   - Verify dependencies are installed
   - Review server logs for errors

## Contact

For questions or issues related to this test case:
- **QA Team**: qa-support@example.com
- **Epic**: #45755
- **Test Case**: TC-P0-API-002

---

**Last Updated**: 2024-01-02  
**Version**: 1.0.0  
**Status**: Active