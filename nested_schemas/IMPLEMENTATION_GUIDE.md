# Nested Schema Support - Python Tools Implementation Guide

## Overview

This guide covers the implementation of Python tools and agents for testing nested schema support in watsonx Orchestrate (Epic #45755). The tools are real-world, production-ready implementations that demonstrate proper handling of nested data structures.

## Test Cases Implemented

### TC-P0-PY-001: Standard Nesting (Basic/Deep/References)
**Location**: `agentic_data/tools/nested_schemas/tc_p0_py_001/`

**Purpose**: Customer Order Processing System

**Nested Schema Levels**:
- **Basic Nesting (3-level)**: customer → address → street/city/state
- **Deep Nesting (5-level)**: customer → order → items → product → details → specifications
- **Schema References ($ref)**: Reusable Address components for shipping/billing

**Files**:
- `process_customer_order.py` - Main tool implementation
- `README.md` - Documentation
- `requirements.txt` - Dependencies (none required)

**Agent Configuration**: `agentic_data/agents/nested_schemas/tc_p0_py_001_agent.json`

**Key Features**:
- Processes customer orders with complete nested information
- Handles customer profiles with addresses
- Tracks order items with detailed product specifications
- Manages shipping and billing addresses using schema references
- Returns user-friendly order confirmations

**Example Usage**:
```python
order_data = {
    "customer": {
        "name": "Jane Smith",
        "email": "jane.smith@email.com",
        "address": {
            "street": "456 Oak Avenue",
            "city": "New York",
            "state": "NY",
            "zipcode": "10001",
            "country": "USA"
        }
    },
    "order": {
        "order_id": "ORD-2024-002",
        "items": [
            {
                "product": {
                    "name": "Premium Laptop",
                    "details": {
                        "specifications": {
                            "weight": "1.5 kg",
                            "dimensions": "35cm x 25cm x 2cm"
                        }
                    }
                },
                "quantity": 1,
                "price": 1299.99
            }
        ]
    }
}

result = process_customer_order(order_data)
# Returns: Order confirmation with formatted customer info, items, and addresses
```

---

### TC-P0-PY-003: Complex Scenarios (Real-World/Circular)
**Location**: `agentic_data/tools/nested_schemas/tc_p0_py_003/`

**Purpose**: Employee Management System

**Complex Scenarios**:
- **Complex Real-World Data**: 30+ fields across multiple nested levels
- **Circular References**: Person relationships (manager/reports) with cycle detection

**Files**:
- `process_complex_data.py` - Main tool implementation
- `README.md` - Documentation
- `requirements.txt` - Dependencies (none required)

**Agent Configuration**: `agentic_data/agents/nested_schemas/tc_p0_py_003_agent.yaml`

**Key Features**:
- Processes employee data with 30+ fields
- Handles complex nested structures (employment, projects, skills, certifications)
- Detects and manages circular references in relationships
- Returns user-friendly employee profiles
- Supports both employee data and person relationship scenarios

**Example Usage**:

**Scenario 1: Employee Data (30+ fields)**
```python
employee_data = {
    "employee": {
        "personal_info": {
            "name": "John Doe",
            "contact": {
                "email": "john.doe@company.com",
                "phone": "+1-555-0100"
            }
        },
        "employment": {
            "position": "Senior Software Engineer",
            "department": "Engineering",
            "projects": [
                {
                    "name": "Cloud Migration",
                    "role": "Tech Lead"
                }
            ]
        }
    }
}

result = process_employee_data(employee_data)
# Returns: Formatted employee profile with all details
```

**Scenario 2: Circular References**
```python
person_data = {
    "person": {
        "name": "Alice Johnson",
        "manager": {
            "name": "Bob Smith",
            "manager": {
                "name": "Alice Johnson"  # Circular reference!
            }
        }
    }
}

result = process_employee_data(person_data)
# Returns: Relationship structure with circular reference detection
```

---

## Agent Configurations

### TC-P0-PY-001 Agent (JSON Format)
```json
{
  "kind": "native",
  "name": "Customer_Order_Processing_Agent",
  "style": "react-intrinsic",
  "guidelines": [
    {
      "display_name": "Process customer orders with nested data",
      "action": "process_customer_order",
      "condition": "When user provides customer order information with addresses and product details",
      "tool": "process_customer_order"
    }
  ],
  "tools": ["process_customer_order"],
  "spec_version": "v1"
}
```

### TC-P0-PY-003 Agent (YAML Format)
```yaml
kind: native
name: Employee_Management_Agent
style: react-intrinsic
guidelines:
- display_name: "Process employee data with complex nested structures"
  action: process_employee_data
  condition: "When user provides employee information or person relationships"
  tool: process_employee_data
tools:
- process_employee_data
spec_version: v1
```

---

## Test Utterances

### TC-P0-PY-001: Customer Order Processing

**Basic Nesting Test**:
```
Process an order for John Smith at 123 Main Street, Boston, MA 02101
```

**Deep Nesting Test**:
```
Process order ORD-2024-001 for Jane Smith. She ordered 2 Premium Laptops at $1299.99 each. 
The laptop specs are: weight 1.5 kg, dimensions 35cm x 25cm x 2cm, aluminum alloy material.
```

**Schema References Test**:
```
Process order for John Doe at 456 Oak Avenue, New York, NY 10001. 
Ship to the same address but bill to 789 Pine Street, New York, NY 10002.
```

**Complete Order Test**:
```
Process a complete order:
Customer: Jane Smith, jane.smith@email.com, phone +1-555-0200
Address: 456 Oak Avenue, New York, NY 10001, USA
Order ID: ORD-2024-002, Date: 2024-01-16

Items:
- Premium Laptop (PROD-001): High-performance laptop, 1 unit at $1299.99
  Specs: 1.5 kg, 35cm x 25cm x 2cm, Aluminum alloy

Shipping: Same as customer address
Billing: 789 Pine Street, New York, NY 10002, USA
```

### TC-P0-PY-003: Employee Management

**Complex Data Test**:
```
Create employee profile:
Personal: John Doe, DOB 1990-05-15, SSN 123-45-6789
Contact: john.doe@company.com, +1-555-0100
Address: 123 Tech Street, San Francisco, CA 94105

Employment: 
- Position: Senior Software Engineer
- Department: Engineering
- Start Date: 2024-01-15
- Salary: $120,000

Projects:
1. Cloud Migration - Tech Lead - Active
2. API Redesign - Developer - Completed

Skills: Python (Expert, 5 years), AWS (Advanced, 3 years)
Certifications: AWS Solutions Architect (2023-06-15)
Performance: Rating 4.5/5, Last review 2023-12-01
```

**Circular Reference Test**:
```
Process person data: Alice Johnson reports to Bob Smith, who reports to Alice Johnson.
```

**Complete Test with Circular Reference**:
```
Analyze this reporting structure:
- Alice Johnson (Manager) oversees Bob Smith
- Bob Smith (Senior Dev) oversees Charlie Brown  
- Charlie Brown (Tech Lead) oversees Alice Johnson
```

**For more test utterances, see**: `TEST_UTTERANCES.md`

---

## Testing Requirements

### Test Configuration
- **Model**: gpt-oss-120b
- **Agent Style**: react-intrinsic
- **Tool Type**: Python Tools
- **Priority**: P0 (Critical Path)

### Validation Points

#### TC-P0-PY-001 Validation:
1. ✅ Basic nesting (3-level) - customer → address → street
2. ✅ Deep nesting (5-level) - customer → order → items → product → details → specifications
3. ✅ Schema references ($ref) - shipping_address and billing_address reuse Address schema
4. ✅ User-friendly output format
5. ✅ Proper Google-style docstring for schema generation

#### TC-P0-PY-003 Validation:
1. ✅ Complex real-world data (30+ fields)
2. ✅ Multiple nested levels (personal_info, employment, projects, skills, certifications)
3. ✅ Circular reference detection and handling
4. ✅ User-friendly output format
5. ✅ Proper Google-style docstring for schema generation

---

## Tool Import Process

### Step 1: Import Tool to watsonx Orchestrate
```bash
# Navigate to watsonx Orchestrate UI
# Go to: Tools → Import → Python Tool
# Select the tool file (process_customer_order.py or process_complex_data.py)
```

### Step 2: Verify Schema Generation
The tool decorator and Google-style docstring will automatically generate the schema:
- Function signature → parameter types
- Docstring Args section → parameter descriptions
- Docstring Returns section → return type description

### Step 3: Create Agent
```bash
# Go to: Agents → Create Agent
# Upload agent configuration (JSON or YAML)
# Verify tool is linked correctly
```

### Step 4: Test Agent
```bash
# Use the agent in a conversation
# Provide test utterances from TEST_UTTERANCES.md
# Verify nested data is processed correctly
# Check output is user-friendly
```

---

## Common Issues and Solutions

### Issue 1: Docstring Parsing Warning
**Problem**: Tool import shows warning about incorrectly formatted docstring

**Solution**: Use strict Google-style format:
```python
def my_tool(param: dict) -> dict:
    """Brief description.
    
    Detailed description.
    
    Args:
        param (dict): Description.
    
    Returns:
        dict: Description.
    """
```

### Issue 2: Schema Not Generated
**Problem**: Tool parameters not showing in UI

**Solution**: 
- Ensure function has type hints: `param: dict`
- Ensure docstring has Args section
- Use `@tool(permission=ToolPermission.READ_ONLY)` decorator

### Issue 3: Nested Data Not Processed
**Problem**: Nested fields return None or empty

**Solution**:
- Use `.get()` method with defaults: `data.get("field", {})`
- Check for None before accessing nested fields
- Provide clear error messages

---

## File Structure

```
agentic_data/
├── tools/
│   └── nested_schemas/
│       ├── tc_p0_py_001/
│       │   ├── process_customer_order.py
│       │   ├── README.md
│       │   └── requirements.txt
│       ├── tc_p0_py_003/
│       │   ├── process_complex_data.py
│       │   ├── README.md
│       │   └── requirements.txt
│       ├── IMPLEMENTATION_GUIDE.md (this file)
│       └── TEST_UTTERANCES.md
└── agents/
    └── nested_schemas/
        ├── tc_p0_py_001_agent.json
        └── tc_p0_py_003_agent.yaml
```

---

## Quick Start Guide

### 1. Run Tools Locally (Optional)
```bash
# Test TC-P0-PY-001
cd agentic_data/tools/nested_schemas/tc_p0_py_001
python process_customer_order.py

# Test TC-P0-PY-003
cd agentic_data/tools/nested_schemas/tc_p0_py_003
python process_complex_data.py
```

### 2. Import to watsonx Orchestrate
- Go to Tools → Import → Python Tool
- Upload `process_customer_order.py` or `process_complex_data.py`
- Verify schema is generated correctly

### 3. Create Agent
- Go to Agents → Create Agent
- Upload agent configuration (JSON or YAML)
- Link the imported tool

### 4. Test with Utterances
- Open chat interface
- Use test utterances from `TEST_UTTERANCES.md`
- Verify responses are correct and user-friendly

---

## Next Steps

### Remaining P0 Test Cases
The following test cases still need implementation:

1. **TC-P0-PY-002**: Array Handling (Wrapped/Raw)
2. **TC-P0-PY-004**: Enums in Nested Schemas
3. **TC-P0-PY-005**: Multi-Field Slot Filling

### Implementation Priority
1. TC-P0-PY-002 (Array Handling) - Next priority
2. TC-P0-PY-004 (Enums) - Requires enum support testing
3. TC-P0-PY-005 (Multi-Field) - Conversational flow testing

---

## References

- **Epic**: #45755 - Nested Schema Support
- **Test Plan**: QA_Analysis_Epic_45755_E2E_Test_Cases_CONSOLIDATED.md
- **Test Utterances**: TEST_UTTERANCES.md
- **Priority**: P0 (Critical Path Tests)
- **Model**: gpt-oss-120b
- **Style**: react-intrinsic

---

## Contact

For questions or issues with these implementations, refer to:
- Test plan document: `QA_Analysis_Epic_45755_E2E_Test_Cases_CONSOLIDATED.md`
- Test utterances: `TEST_UTTERANCES.md`
- Tool documentation: Individual README.md files in each test case directory

---

**Last Updated**: 2024-01-16
**Status**: TC-P0-PY-001 and TC-P0-PY-003 Complete ✅