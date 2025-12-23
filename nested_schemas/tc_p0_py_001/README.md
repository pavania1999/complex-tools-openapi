# TC-P0-PY-001: Python Tool with Nested Schema Support

## Overview

This Python tool implements **TC-P0-PY-001** from Epic #45755 (Nested Schema Support). It validates that Python tools with nested schemas work correctly with the react-intrinsic agent style and gpt-oss-120b model in watsonx Orchestrate.

## Test Configuration

- **Test ID**: TC-P0-PY-001
- **Test Name**: Python + React-Intrinsic + gpt-oss-120b + Standard Nesting
- **Priority**: P0 (Critical)
- **Type**: Integration Test
- **Automation Status**: Automated
- **Epic**: #45755 - Nested Schema Support

## Tool Details

### Function: `process_customer_order`

Processes customer orders with nested data structures to validate three types of nesting:

1. **Basic Nesting (3-level)**: `customer -> address -> street`
2. **Deep Nesting (5-level)**: `customer -> order -> items -> product -> details -> specifications`
3. **Schema References ($ref)**: Reusable Address components for shipping/billing addresses

### Input Schema

```python
{
    "customer": {
        "name": str,
        "email": str,
        "address": {              # Level 2
            "street": str,        # Level 3
            "city": str,
            "state": str,
            "zipcode": str,
            "country": str
        },
        "contact": {
            "phone": str,
            "mobile": str
        }
    },
    "order": {
        "order_id": str,
        "order_date": str,
        "items": [                # Level 2
            {
                "product": {      # Level 3
                    "product_id": str,
                    "name": str,
                    "details": {  # Level 4
                        "description": str,
                        "specifications": {  # Level 5
                            "weight": str,
                            "dimensions": str,
                            "material": str
                        }
                    }
                },
                "quantity": int,
                "price": float
            }
        ],
        "shipping_address": {     # Schema reference to Address
            "street": str,
            "city": str,
            "state": str,
            "zipcode": str,
            "country": str
        },
        "billing_address": {      # Schema reference to Address
            "street": str,
            "city": str,
            "state": str,
            "zipcode": str,
            "country": str
        }
    }
}
```

### Output Schema

```python
{
    "status": "success" | "error",
    "test_id": "TC-P0-PY-001",
    "validation": {
        "customer_present": bool,
        "address_present": bool,
        "basic_nesting_3_levels": bool,
        "order_present": bool,
        "items_present": bool,
        "product_present": bool,
        "details_present": bool,
        "deep_nesting_5_levels": bool,
        "shipping_address_schema_ref": bool,
        "billing_address_schema_ref": bool,
        "schema_references_resolved": bool
    },
    "processed_data": {
        "customer_street": str,
        "customer_city": str,
        "product_specifications": dict,
        "shipping_address": dict,
        "billing_address": dict,
        "max_nesting_depth": int
    },
    "summary": {
        "basic_nesting_validated": bool,
        "deep_nesting_validated": bool,
        "schema_refs_validated": bool,
        "all_validations_passed": bool
    }
}
```

## Agent Configuration

### Agent: `TC_P0_PY_001_Nested_Schema_Agent`

- **Model**: gpt-oss-120b
- **Style**: react-intrinsic
- **Tools**: process_customer_order
- **Location**: `agentic_data/agents/nested_schemas/tc_p0_py_001_agent.json`

### Agent Instructions

The agent is configured to:
1. Use the process_customer_order tool for handling nested customer data
2. Validate 3-level basic nesting (customer -> address -> street)
3. Validate 5-level deep nesting (full product specification hierarchy)
4. Verify schema references ($ref) are properly resolved
5. Return detailed validation results for each nesting level

## Usage

### Importing to watsonx Orchestrate

1. **Import the Python Tool**:
   - Navigate to Tools section in watsonx Orchestrate
   - Import from: `agentic_data/tools/nested_schemas/tc_p0_py_001/process_customer_order.py`
   - Tool will be registered as `process_customer_order`

2. **Import the Agent**:
   - Navigate to Agents section in watsonx Orchestrate
   - Import from: `agentic_data/agents/nested_schemas/tc_p0_py_001_agent.json`
   - Agent will be created with react-intrinsic style and gpt-oss-120b model

### Testing Scenarios

#### Scenario 1: Basic Nesting (3-level)
```
User: "Process an order for John Doe at 123 Main Street, San Francisco, CA 94102"
Expected: Tool validates customer -> address -> street hierarchy
```

#### Scenario 2: Deep Nesting (5-level)
```
User: "Process an order for Jane Smith with a Premium Laptop. 
       Product specs: weight 1.5kg, dimensions 35x25x2cm, aluminum material"
Expected: Tool validates full 5-level product specification hierarchy
```

#### Scenario 3: Schema References
```
User: "Process an order with shipping to 123 Main St, SF and billing to 456 Oak Ave, NY"
Expected: Tool validates Address schema is reused for both addresses
```

## Validation Criteria

### Success Criteria

All three validations must pass:
- ✅ `basic_nesting_validated`: True
- ✅ `deep_nesting_validated`: True
- ✅ `schema_refs_validated`: True

### Expected Results

```json
{
    "status": "success",
    "validation": {
        "customer_present": true,
        "address_present": true,
        "basic_nesting_3_levels": true,
        "order_present": true,
        "items_present": true,
        "product_present": true,
        "details_present": true,
        "deep_nesting_5_levels": true,
        "shipping_address_schema_ref": true,
        "billing_address_schema_ref": true,
        "schema_references_resolved": true
    },
    "summary": {
        "basic_nesting_validated": true,
        "deep_nesting_validated": true,
        "schema_refs_validated": true,
        "all_validations_passed": true
    }
}
```

## Files

```
agentic_data/
├── tools/nested_schemas/tc_p0_py_001/
│   ├── process_customer_order.py    # Python tool implementation
│   ├── requirements.txt              # Dependencies (none required)
│   └── README.md                     # This file
└── agents/nested_schemas/
    └── tc_p0_py_001_agent.json      # Agent configuration
```

## Testing

### Local Testing

Run the tool locally to verify functionality:

```bash
cd agentic_data/tools/nested_schemas/tc_p0_py_001
python process_customer_order.py
```

This will execute built-in test cases for:
- Basic nesting validation
- Deep nesting validation
- Schema reference validation

### Integration Testing

Use the test suite in `test/test_api/test_api_nested_schemas/` for comprehensive integration testing.

## Related Test Cases

This tool serves as the foundation for:
- TC-P0-PY-002: Python + React-Intrinsic + gpt-oss-120b + Array Handling
- TC-P0-PY-003: Python + React-Intrinsic + gpt-oss-120b + Complex Scenarios
- TC-P0-PY-004: Python + React-Intrinsic + gpt-oss-120b + Enums in Nested Schemas
- TC-P0-PY-005: Python + React-Intrinsic + gpt-oss-120b + Multi-Field Slot Filling

## Notes

- Tool uses only standard Python libraries (no external dependencies)
- Validates nested structures at each level before processing
- Calculates maximum nesting depth dynamically
- Provides detailed validation results for debugging
- Gracefully handles missing or incomplete nested data

## Support

For issues or questions about this test case:
1. Review the validation results in the tool output
2. Check the agent logs in watsonx Orchestrate
3. Verify the input data matches the expected schema structure
4. Ensure the agent is configured with react-intrinsic style and gpt-oss-120b model