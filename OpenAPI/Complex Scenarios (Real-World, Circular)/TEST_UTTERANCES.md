# Test Utterances for TC-P0-API-003
## OpenAPI + React-Intrinsic + gpt-oss-120b + Complex Scenarios (Circular References)

**Test ID**: TC-P0-API-003  
**Priority**: P0 (Critical)  
**Tool Type**: OpenAPI  
**Style**: react-intrinsic  
**Model**: gpt-oss-120b  
**Schema Type**: Complex Scenarios - Circular Schema References

---

## Test Scenario Overview

This test validates the handling of **circular schema references** in OpenAPI specifications where the `Person` schema references itself through the `manager` field. This creates a natural pattern for modeling organizational hierarchies.

**API Endpoint**: `POST /api/v1/employees/register`  
**Deployed URL**: `https://complex-tools-openapi.onrender.com/api/v1/employees/register`

---

## Test Utterances

### Category 1: Basic Employee Registration (2-Level Hierarchy)

#### Utterance 1.1: Simple Employee with Manager
```
Register a new employee Sarah Martinez with ID EMP-201, email sarah.martinez@company.com, 
phone +1-555-0201, in the Engineering department as a Software Engineer starting on 
February 1st 2024. Her manager is Michael Chen with ID EMP-150, email michael.chen@company.com, 
phone +1-555-0150, also in Engineering as an Engineering Manager.
```

**Expected Behavior**:
- Tool invocation: `registerEmployee`
- Request body includes nested Person schema with employee and manager
- Response includes reporting chain: "Sarah Martinez (EMP-201) → Michael Chen (EMP-150)"
- Hierarchy levels: 2

#### Utterance 1.2: Conversational Registration
```
I need to register Sarah Martinez as a new software engineer. Her employee ID is EMP-201, 
email is sarah.martinez@company.com, and she'll be in the Engineering department. 
She reports to Michael Chen who is the Engineering Manager with ID EMP-150.
```

**Expected Behavior**:
- Natural language processing extracts structured data
- Tool correctly maps conversational input to Person schema
- Both employee and manager fields populated correctly

---

### Category 2: Multi-Level Hierarchy (3+ Levels)

#### Utterance 2.1: Three-Level Management Chain
```
Register James Wilson, employee ID EMP-202, email james.wilson@company.com, phone +1-555-0202, 
as a Senior Product Manager in the Product department starting March 1st 2024. He reports to 
Lisa Anderson (EMP-100, lisa.anderson@company.com, VP of Product) who reports to Robert Taylor 
(EMP-001, robert.taylor@company.com, Chief Product Officer in Executive department).
```

**Expected Behavior**:
- Tool handles 3-level nested Person schema
- Reporting chain: "James Wilson (EMP-202) → Lisa Anderson (EMP-100) → Robert Taylor (EMP-001)"
- Hierarchy levels: 3
- All manager relationships preserved

#### Utterance 2.2: Four-Level Deep Hierarchy
```
Add Alex Johnson as a Junior Developer with ID EMP-301, email alex.johnson@company.com, 
starting April 1st 2024 in Engineering. Alex reports to Sarah Martinez (EMP-201, Software Engineer), 
who reports to Michael Chen (EMP-150, Engineering Manager), who reports to David Kim 
(EMP-050, VP of Engineering).
```

**Expected Behavior**:
- Tool handles 4-level nested structure
- Circular schema reference allows arbitrary depth
- Reporting chain shows all 4 levels
- No recursion errors or stack overflow

---

### Category 3: Top-Level Executive (No Manager)

#### Utterance 3.1: CEO Registration
```
Register Jennifer Lee as Chief Executive Officer with employee ID EMP-001, 
email jennifer.lee@company.com, phone +1-555-0001, in the Executive department, 
starting January 1st 2015. She doesn't have a manager.
```

**Expected Behavior**:
- Tool accepts Person schema without manager field
- Response indicates no manager assigned
- Note: "No manager assigned - this may be a top-level executive"
- Reporting chain contains only the employee

#### Utterance 3.2: Founder Registration
```
Add Robert Taylor as the Chief Product Officer, ID EMP-001, email robert.taylor@company.com, 
in the Executive department. He's a founder and doesn't report to anyone.
```

**Expected Behavior**:
- Manager field is null/undefined
- Tool handles optional manager gracefully
- Single-person reporting chain

---

### Category 4: Complex Real-World Scenarios

#### Utterance 4.1: Department Transfer with New Manager
```
Register Maria Garcia, EMP-305, maria.garcia@company.com, as a Product Designer in the 
Product department starting May 15th 2024. She previously worked in Marketing but now 
reports to Lisa Anderson (EMP-100, VP of Product) who reports to Robert Taylor (EMP-001, CPO).
```

**Expected Behavior**:
- Tool processes multi-level hierarchy
- Department field correctly set to Product
- Manager chain properly established

#### Utterance 4.2: Cross-Department Reporting
```
Add Kevin Brown, EMP-401, kevin.brown@company.com, as a Data Analyst in the Operations 
department. He reports to Sarah Martinez (EMP-201) from Engineering who reports to 
Michael Chen (EMP-150, Engineering Manager).
```

**Expected Behavior**:
- Tool allows cross-department reporting structures
- Person schema flexible enough for complex org structures
- All relationships preserved despite department differences

---

### Category 5: Validation and Error Handling

#### Utterance 5.1: Missing Required Fields
```
Register a new employee named John Doe in the Engineering department.
```

**Expected Behavior**:
- Tool returns validation error
- Error message: "Required fields missing: employee_id, email"
- Status: 400 Bad Request

#### Utterance 5.2: Invalid Email Format
```
Register employee Tom Smith with ID EMP-500, email tom.smith.company.com (no @), 
in Sales as Account Executive.
```

**Expected Behavior**:
- Email validation fails
- Error indicates invalid email format
- Request rejected before processing

---

### Category 6: Circular Reference Detection (Safety)

#### Utterance 6.1: Self-Reporting (Invalid)
```
Register employee Alice Cooper, EMP-600, alice.cooper@company.com, as a Manager in HR. 
She reports to herself (Alice Cooper, EMP-600).
```

**Expected Behavior**:
- Tool detects circular reference in data
- Warning: "Circular reference detected in management chain"
- Processing stops to prevent infinite loop

#### Utterance 6.2: Circular Chain (Invalid)
```
Register Bob Johnson, EMP-700, who reports to Carol White, EMP-701, who reports to 
Dave Brown, EMP-702, who reports back to Bob Johnson, EMP-700.
```

**Expected Behavior**:
- Circular reference detection activates
- Warning message in response
- Chain traversal stops at detection point

---

### Category 7: Edge Cases

#### Utterance 7.1: Very Deep Hierarchy (10+ Levels)
```
Register an intern who reports through 12 levels of management up to the CEO.
```

**Expected Behavior**:
- Tool limits depth to 10 levels (safety mechanism)
- Warning: "Management hierarchy exceeds maximum depth of 10 levels"
- Processing continues but stops traversal at limit

#### Utterance 7.2: Minimal Information
```
Register employee with just the required fields: name John Smith, ID EMP-800, 
email john.smith@company.com, department Sales, position Sales Rep.
```

**Expected Behavior**:
- Tool accepts minimal required fields
- Optional fields (phone, start_date, manager) are null/default
- Registration succeeds with available information

---

### Category 8: Conversational Multi-Turn

#### Utterance 8.1: Progressive Information Gathering
**Turn 1:**
```
I need to register a new employee.
```

**Turn 2:**
```
Her name is Emma Wilson, employee ID EMP-900, email emma.wilson@company.com.
```

**Turn 3:**
```
She's in the Marketing department as a Marketing Manager starting June 1st 2024.
```

**Turn 4:**
```
She reports to Lisa Anderson who is the VP of Product with ID EMP-100.
```

**Expected Behavior**:
- Tool accumulates information across turns
- Final invocation includes all collected data
- Proper Person schema structure maintained

---

## Validation Checklist

For each utterance, verify:

- ✅ **Schema Recognition**: Tool correctly identifies circular Person schema reference
- ✅ **Nested Structure**: Manager field properly references Person schema
- ✅ **Depth Handling**: Arbitrary hierarchy depths supported (up to safety limit)
- ✅ **Required Fields**: Validation enforces required Person fields
- ✅ **Optional Fields**: Manager field is optional (for executives)
- ✅ **Reporting Chain**: Visual representation of hierarchy generated
- ✅ **Circular Detection**: Safety mechanism prevents infinite loops
- ✅ **Error Messages**: Clear, actionable error responses
- ✅ **Response Format**: Structured JSON with employee summary and manager info

---

## Success Criteria

### Critical (Must Pass)
1. Basic 2-level hierarchy registration works
2. Multi-level (3-4 levels) hierarchy handled correctly
3. Top-level executives (no manager) accepted
4. Required field validation enforced
5. Circular reference detection prevents infinite loops

### Important (Should Pass)
6. Conversational input correctly mapped to schema
7. Cross-department reporting structures supported
8. Deep hierarchies (10+ levels) handled with safety limits
9. Error messages are clear and actionable
10. Response includes complete reporting chain

### Nice to Have (May Pass)
11. Multi-turn conversations accumulate data correctly
12. Edge cases handled gracefully
13. Performance acceptable for deep hierarchies
14. Validation messages suggest corrections

---

## Test Data Files

- **OpenAPI Spec**: [`openapi_add_employee_with_manager.yaml`](openapi_add_employee_with_manager.yaml)
- **Test Payloads**: [`test-payload.json`](test-payload.json)
- **Python Implementation**: [`register_employee.py`](register_employee.py)
- **API Server**: [`api_server.py`](api_server.py)

---

## Notes

1. **Circular Schema vs Circular Data**: The schema has a circular reference (Person → manager → Person), but actual data should form linear hierarchies (no one reports to themselves).

2. **Safety Mechanisms**: The implementation includes:
   - Visited set to detect circular data references
   - Maximum depth limit (10 levels)
   - Required field validation

3. **Real-World Pattern**: This pattern is common in business applications:
   - Employee → manager → Employee
   - Person → spouse → Person
   - Node → parent → Node
   - Category → subcategory → Category

4. **watsonx Orchestrate Limitation**: Note that watsonx Orchestrate's Pydantic validation may reject circular schema references during import. This is a platform limitation, not a schema design issue.

---

**Test Case**: TC-P0-API-003  
**Created**: 2024-01-05  
**Last Updated**: 2024-01-05  
**Status**: Ready for Testing ✅