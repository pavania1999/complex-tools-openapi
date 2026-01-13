# Test Utterances for Nested Schema Support - Python Tools

## Overview
This document provides test utterances (user prompts) to validate the Python tools and agents for nested schema support testing. Each utterance is designed to trigger the agent and test specific nested schema scenarios.

---

## TC-P0-PY-001: Customer Order Processing Agent

### Test Scenario 1: Basic Nesting (3-level)
**Schema Path**: customer → address → street/city/state

**Utterance 1 (Simple)**:
```
Process an order for John Smith at 123 Main Street, Boston, MA 02101
```

**Utterance 2 (Detailed)**:
```
I need to process a customer order. The customer is John Smith, email john.smith@email.com, 
living at 123 Main Street, Boston, Massachusetts, 02101, USA. Phone: +1-555-0100
```

**Expected Response**: Agent should extract customer info and nested address details

---

### Test Scenario 2: Deep Nesting (5-level)
**Schema Path**: customer → order → items → product → details → specifications

**Utterance 3 (Product with Specifications)**:
```
Process order ORD-2024-001 for Jane Smith. She ordered 2 Premium Laptops at $1299.99 each. 
The laptop specs are: weight 1.5 kg, dimensions 35cm x 25cm x 2cm, aluminum alloy material.
```

**Utterance 4 (Multiple Items)**:
```
Create an order for customer Jane Smith, email jane@email.com. Order ID is ORD-2024-002.
Items:
1. Premium Laptop - quantity 1, price $1299.99, specs: 1.5kg, 35x25x2cm, aluminum
2. Wireless Mouse - quantity 2, price $29.99, specs: 0.1kg, 10x6x3cm, plastic
```

**Expected Response**: Agent should process nested product details and specifications

---

### Test Scenario 3: Schema References ($ref)
**Schema Path**: shipping_address and billing_address using Address schema

**Utterance 5 (Different Addresses)**:
```
Process order for John Doe at 456 Oak Avenue, New York, NY 10001. 
Ship to the same address but bill to 789 Pine Street, New York, NY 10002.
```

**Utterance 6 (Same Address)**:
```
Create order ORD-2024-003 for Alice Johnson, 321 Elm Street, Chicago, IL 60601.
Use the same address for both shipping and billing.
```

**Expected Response**: Agent should handle address schema references correctly

---

### Test Scenario 4: Complete Order (All Nesting Levels)
**Tests**: Basic + Deep + Schema References combined

**Utterance 7 (Comprehensive)**:
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

**Expected Response**: Complete order confirmation with all nested details formatted

---

## TC-P0-PY-003: Employee Management Agent

### Test Scenario 1: Complex Real-World Data (30+ fields)
**Schema**: Multiple nested levels with 30+ fields

**Utterance 1 (New Employee)**:
```
Add a new employee: John Doe, employee ID EMP-001, email john.doe@company.com, 
phone +1-555-0100. Position: Senior Software Engineer in Engineering department.
Start date: 2024-01-15, salary $120,000. Manager: Jane Smith (EMP-100).
```

**Utterance 2 (Employee with Projects)**:
```
Process employee data for Sarah Johnson, ID EMP-002. She's a Tech Lead in Engineering.
Contact: sarah.j@company.com, +1-555-0150. 
Projects: Cloud Migration (Tech Lead role), API Redesign (Developer role).
Skills: Python (Expert), AWS (Advanced), Docker (Intermediate).
```

**Utterance 3 (Complete Employee Profile)**:
```
Create employee profile:
Personal: John Doe, DOB 1990-05-15, SSN 123-45-6789
Contact: john.doe@company.com, +1-555-0100, mobile +1-555-0101
Address: 123 Tech Street, San Francisco, CA 94105
Emergency: Jane Doe, Spouse, +1-555-0102

Employment: 
- Position: Senior Software Engineer
- Department: Engineering
- Start Date: 2024-01-15
- Salary: $120,000
- Manager: Bob Smith (EMP-100)

Projects:
1. Cloud Migration - Tech Lead - Active
2. API Redesign - Developer - Completed

Skills: Python (Expert, 5 years), AWS (Advanced, 3 years), Docker (Intermediate, 2 years)

Certifications: AWS Solutions Architect (2023-06-15), Python Professional (2022-03-20)

Performance: Rating 4.5/5, Last review 2023-12-01, Next review 2024-06-01
```

**Expected Response**: Formatted employee profile with all nested details

---

### Test Scenario 2: Circular References
**Schema**: Person relationships with cycle detection

**Utterance 4 (Simple Circular Reference)**:
```
Process person data: Alice Johnson reports to Bob Smith, who reports to Alice Johnson.
```

**Utterance 5 (Complex Circular Reference)**:
```
Analyze this reporting structure:
- Alice Johnson (Manager) oversees Bob Smith
- Bob Smith (Senior Dev) oversees Charlie Brown  
- Charlie Brown (Tech Lead) oversees Alice Johnson
```

**Utterance 6 (Circular with Details)**:
```
Check this employee relationship:
Person: Alice Johnson, ID EMP-001, Manager: Bob Smith (EMP-002)
Bob Smith's manager is Charlie Brown (EMP-003)
Charlie Brown's manager is Alice Johnson (EMP-001)
```

**Expected Response**: Relationship structure with circular reference detection message

---

### Test Scenario 3: Mixed Scenarios
**Tests**: Both employee data and circular references

**Utterance 7 (Employee with Circular Manager Chain)**:
```
Add employee: David Lee, ID EMP-004, Senior Developer
Contact: david.lee@company.com
Manager: Alice Johnson (EMP-001)
Note: Alice reports to Bob (EMP-002), Bob reports to Charlie (EMP-003), 
and Charlie reports back to Alice (EMP-001)
```

**Expected Response**: Employee profile with circular reference warning

---

## Testing Guidelines

### For Each Utterance:

1. **Start Conversation**: Open watsonx Orchestrate chat
2. **Invoke Agent**: Type the utterance exactly as shown
3. **Verify Response**: Check that agent:
   - Correctly identifies the tool to use
   - Extracts all nested data properly
   - Returns user-friendly formatted output
   - Handles edge cases (missing data, circular refs)

### Success Criteria:

✅ **TC-P0-PY-001 Success**:
- All 7 utterances processed correctly
- Nested data extracted at all levels (3-level, 5-level)
- Schema references handled properly
- Order confirmations are clear and complete

✅ **TC-P0-PY-003 Success**:
- All 7 utterances processed correctly
- 30+ fields extracted and formatted
- Circular references detected and reported
- Employee profiles are comprehensive and readable

### Validation Points:

**For Customer Orders**:
- [ ] Customer name extracted
- [ ] Email and phone captured
- [ ] Address parsed (street, city, state, zip, country)
- [ ] Order ID and date recorded
- [ ] Product details with specifications
- [ ] Shipping and billing addresses handled
- [ ] Total amount calculated

**For Employee Data**:
- [ ] Personal information complete
- [ ] Contact details formatted
- [ ] Employment information captured
- [ ] Projects listed with roles
- [ ] Skills with proficiency levels
- [ ] Certifications with dates
- [ ] Performance data included
- [ ] Circular references detected

---

## Edge Cases to Test

### TC-P0-PY-001 Edge Cases:

**Utterance E1 (Missing Optional Fields)**:
```
Process order for John Smith. Order ID: ORD-2024-999. 
One laptop at $1299.99.
```
*Expected*: Should handle missing email, phone, address gracefully

**Utterance E2 (Minimal Product Info)**:
```
Order for Jane: 1 item, $50
```
*Expected*: Should process with minimal data, use defaults

---

### TC-P0-PY-003 Edge Cases:

**Utterance E3 (Minimal Employee Data)**:
```
Add employee: John Doe, ID EMP-999
```
*Expected*: Should create profile with available data only

**Utterance E4 (Self-Referencing)**:
```
Process person: Alice Johnson, manager is Alice Johnson
```
*Expected*: Should detect immediate self-reference

---

## Quick Test Commands

### Test TC-P0-PY-001:
```bash
# Run the tool directly
cd agentic_data/tools/nested_schemas/tc_p0_py_001
python process_customer_order.py
```

### Test TC-P0-PY-003:
```bash
# Run the tool directly
cd agentic_data/tools/nested_schemas/tc_p0_py_003
python process_complex_data.py
```

---

## Troubleshooting

### Agent Not Responding:
- Check agent is deployed and active
- Verify tool is imported correctly
- Check agent guidelines match tool name

### Incorrect Data Extraction:
- Review tool docstring format
- Check schema generation in UI
- Verify nested field paths

### Missing Fields in Output:
- Check tool handles None values
- Verify `.get()` methods with defaults
- Review nested data structure

---

## Test Results Template

```
Test Case: TC-P0-PY-001
Date: ___________
Tester: ___________

Utterance 1: ☐ Pass ☐ Fail - Notes: ___________
Utterance 2: ☐ Pass ☐ Fail - Notes: ___________
Utterance 3: ☐ Pass ☐ Fail - Notes: ___________
Utterance 4: ☐ Pass ☐ Fail - Notes: ___________
Utterance 5: ☐ Pass ☐ Fail - Notes: ___________
Utterance 6: ☐ Pass ☐ Fail - Notes: ___________
Utterance 7: ☐ Pass ☐ Fail - Notes: ___________

Overall Result: ☐ Pass ☐ Fail
```

---

**Last Updated**: 2024-01-16
**Test Cases**: TC-P0-PY-001, TC-P0-PY-003
**Priority**: P0 (Critical Path)