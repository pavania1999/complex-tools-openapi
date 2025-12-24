# Address Schema Reference Test

## Overview
This test validates that the `Address` schema defined in [`openapi_customer_order_deployed.yaml`](openapi_customer_order_deployed.yaml:159-181) is properly processed when referenced in multiple locations using `$ref`.

## Address Schema Definition
The Address schema is defined once at line 159-181:
```yaml
Address:
  type: object
  properties:
    street: string
    city: string
    state: string
    zipcode: string
    country: string
```

## Schema References
The Address schema is referenced in **3 different locations**:

1. **Customer Address** (line 154)
   ```yaml
   customer:
     address:
       $ref: '#/components/schemas/Address'
   ```

2. **Shipping Address** (line 217)
   ```yaml
   order:
     shipping_address:
       $ref: '#/components/schemas/Address'
   ```

3. **Billing Address** (line 219)
   ```yaml
   order:
     billing_address:
       $ref: '#/components/schemas/Address'
   ```

## Test Payload
The test payload [`test_address_schema_payload.json`](test_address_schema_payload.json) includes:

- **Customer Address**: 123 Main Street, San Francisco, CA 94102, USA
- **Shipping Address**: 456 Delivery Lane, Los Angeles, CA 90001, USA  
- **Billing Address**: 789 Payment Boulevard, Seattle, WA 98101, USA

## Running the Test

### Option 1: Using the Shell Script
```bash
./nested_schemas/test_address_schema.sh
```

### Option 2: Using curl directly
```bash
curl -X POST \
  https://complex-tools-openapi.onrender.com/api/v1/orders/process \
  -H "Content-Type: application/json" \
  -d @nested_schemas/test_address_schema_payload.json
```

### Option 3: Using Python
```python
import requests
import json

with open('nested_schemas/test_address_schema_payload.json', 'r') as f:
    payload = json.load(f)

response = requests.post(
    'https://complex-tools-openapi.onrender.com/api/v1/orders/process',
    json=payload
)

print(json.dumps(response.json(), indent=2))
```

## Expected Response
The API should return a 200 OK response with all three addresses properly formatted:

```json
{
  "customer_name": "John Doe",
  "customer_email": "john.doe@example.com",
  "customer_address": "123 Main Street, San Francisco, CA, 94102, USA",
  "phone": "+1-415-555-0100",
  "mobile": "+1-415-555-0101",
  "order_id": "ORD-2024-TEST-001",
  "order_date": "2024-12-23",
  "items": [...],
  "total_items": 2,
  "total_amount": 1499.97,
  "shipping_address": "456 Delivery Lane, Los Angeles, CA, 90001, USA",
  "billing_address": "789 Payment Boulevard, Seattle, WA, 98101, USA",
  "confirmation_message": "Order ORD-2024-TEST-001 confirmed for John Doe",
  "order_summary": "2 item(s), Total: $1499.97"
}
```

## Validation Points

✅ **Customer Address Processing**
- Verify `customer_address` field contains formatted customer address
- Format: "street, city, state, zipcode, country"

✅ **Shipping Address Processing**  
- Verify `shipping_address` field contains formatted shipping address
- Should be different from customer address

✅ **Billing Address Processing**
- Verify `billing_address` field contains formatted billing address  
- Should be different from both customer and shipping addresses

✅ **Schema Reusability**
- All three addresses use the same Address schema via `$ref`
- Each instance should be independently processed
- No data leakage between address instances

## Test Scenarios

### Scenario 1: All Addresses Different (Current Test)
Tests that each address reference is processed independently with unique values.

### Scenario 2: Same Address for All (Optional)
Set all three addresses to identical values to verify no conflicts:
```json
{
  "street": "100 Universal Street",
  "city": "Anytown",
  "state": "ST",
  "zipcode": "12345",
  "country": "USA"
}
```

### Scenario 3: Missing Optional Fields (Optional)
Test with minimal address data (only required fields if any).

## Success Criteria
- ✅ HTTP 200 status code
- ✅ All three address fields present in response
- ✅ Each address properly formatted
- ✅ Addresses match input values
- ✅ No schema resolution errors
- ✅ Deep nesting (6 levels) works correctly with address references

## Files
- [`test_address_schema_payload.json`](test_address_schema_payload.json) - Test payload
- [`test_address_schema.sh`](test_address_schema.sh) - Automated test script
- [`openapi_customer_order_deployed.yaml`](openapi_customer_order_deployed.yaml) - API specification