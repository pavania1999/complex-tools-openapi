# TC-P0-PY-003: Python Tool with Complex Schemas and Circular References

## Overview

This Python tool implements **TC-P0-PY-003** from Epic #45755 (Nested Schema Support). It validates that Python tools can handle complex scenarios including:
1. Complex real-world data structures with 30+ fields
2. Circular reference detection and handling

## Test Configuration

- **Test ID**: TC-P0-PY-003
- **Test Name**: Python + React-Intrinsic + gpt-oss-120b + Complex Scenarios
- **Priority**: P0 (Critical)
- **Type**: Integration Test
- **Automation Status**: Automated
- **Epic**: #45755 - Nested Schema Support

## Tool Details

### Function: `process_complex_data`

Processes complex data structures to validate two scenarios:

1. **Complex Real-World (30+ fields)**: Employee data with comprehensive nested structures
2. **Circular References**: Self-referential data structures (person -> friendOf -> person)

### Scenario 1: Complex Real-World (30+ Fields)

Employee data structure with:
- Personal information (name, email, phone, address)
- Employment details (department, position, salary, benefits)
- Projects array with multiple projects
- Skills array
- Certifications array with details
- Performance metrics (rating, reviews, goals)
- Preferences

**Total Fields**: 30+ across all nested levels

### Scenario 2: Circular References

Person data structure with:
- Basic info (id, name, email, age)
- friendOf reference that can point back to original person
- Circular detection without infinite loops

## Usage

### Importing to watsonx Orchestrate

1. **Import the Python Tool**:
   - Navigate to Tools section
   - Import from: `agentic_data/tools/nested_schemas/tc_p0_py_003/process_complex_data.py`
   - Tool will be registered as `process_complex_data`

2. **Import the Agent**:
   - Navigate to Agents section
   - Import from: `agentic_data/agents/nested_schemas/tc_p0_py_003_agent.yaml`
   - Agent configured with react-intrinsic style and gpt-oss-120b model

### Testing Scenarios

#### Scenario 1: Complex Real-World Data
```
User: "Process employee John Doe with full details including personal info, 
       employment at Engineering department as Senior Software Engineer, 
       projects Alpha and Beta, skills in Python and AWS, 
       AWS certification, and 4.5 performance rating"
       
Expected: Tool processes 30+ fields successfully
```

#### Scenario 2: Circular References
```
User: "Process person Alice who is friends with Bob, and Bob is friends with Alice"

Expected: Tool detects circular reference and handles it without infinite loop
```

## Validation Criteria

### Complex Real-World Success Criteria
- ✅ `complex_real_world_validated`: True
- ✅ `has_30_plus_fields`: True
- ✅ `field_count`: >= 30
- ✅ All sections present: personal, employment, projects, skills, certifications, performance

### Circular Reference Success Criteria
- ✅ `circular_reference_scenario`: True
- ✅ `circular_refs_handled`: True
- ✅ `circular_refs_found`: > 0
- ✅ No infinite loops or stack overflow

## Expected Results

### Complex Real-World
```json
{
    "status": "success",
    "test_id": "TC-P0-PY-003",
    "field_count": 35,
    "validation": {
        "complex_real_world": true,
        "has_30_plus_fields": true,
        "personal_info_present": true,
        "employment_info_present": true,
        "projects_present": true,
        "skills_present": true,
        "certifications_present": true,
        "performance_present": true
    },
    "summary": {
        "complex_real_world_validated": true,
        "total_fields_processed": 35
    }
}
```

### Circular References
```json
{
    "status": "success",
    "test_id": "TC-P0-PY-003",
    "circular_refs_detected": ["person -> friendOf -> friendOf -> [CIRCULAR]"],
    "validation": {
        "circular_reference_scenario": true,
        "person_present": true,
        "friend_of_present": true,
        "circular_ref_detected": true,
        "circular_refs_handled": true
    },
    "summary": {
        "circular_refs_validated": true,
        "circular_refs_found": 1
    }
}
```

## Files

```
agentic_data/
├── tools/nested_schemas/tc_p0_py_003/
│   ├── process_complex_data.py      # Python tool (338 lines)
│   ├── requirements.txt              # Dependencies (none)
│   └── README.md                     # This file
└── agents/nested_schemas/
    └── tc_p0_py_003_agent.yaml      # Agent configuration
```

## Local Testing

Run the tool locally:

```bash
cd agentic_data/tools/nested_schemas/tc_p0_py_003
python process_complex_data.py
```

Expected output:
```
Test 1: Complex Real-World (30+ fields)
Complex real-world validated: True
Total fields: 35
Has 30+ fields: True

Test 2: Circular References
Circular refs validated: True
Circular refs found: 1
Circular paths: ['person -> friendOf -> friendOf -> [CIRCULAR]']
```

## Key Features

- ✅ Handles 30+ fields in complex nested structures
- ✅ Detects circular references without infinite loops
- ✅ Counts total fields dynamically
- ✅ Validates comprehensive employee data structure
- ✅ Processes person relationships with circular detection
- ✅ Returns detailed validation results
- ✅ Google-style docstring for proper schema parsing

## Related Test Cases

- TC-P0-PY-001: Standard Nesting (Basic/Deep/References)
- TC-P0-PY-002: Array Handling
- TC-P0-PY-004: Enums in Nested Schemas
- TC-P0-PY-005: Multi-Field Slot Filling

## Notes

- Tool uses only standard Python libraries (no external dependencies)
- Circular reference detection uses object ID tracking
- Field counting handles nested dictionaries and arrays
- Gracefully handles missing or incomplete data
- Prevents infinite loops in circular structures

## Support

For issues or questions:
1. Review validation results in tool output
2. Check field_count and circular_refs_detected
3. Verify input data structure matches expected format
4. Ensure agent is configured with react-intrinsic style