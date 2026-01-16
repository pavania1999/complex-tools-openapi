# Employee Registration Tool - Pydantic Implementation

## Overview

This Python tool demonstrates handling **circular schema references** and **enum references** using Pydantic, based on the OpenAPI specification [`openapi_add_employee_with_manager.yaml`](openapi_add_employee_with_manager.yaml).

The tool showcases two key patterns:
1. **Circular Reference**: The `Person` schema references itself through the `manager` field, allowing unlimited organizational hierarchy depth
2. **Enum Reference**: The `department` field references the `DepartmentEnum`, ensuring type-safe department values

## Files

- **`register_employee_pydantic.py`** - Main tool implementation with Pydantic models
- **`test_register_employee_pydantic.py`** - Comprehensive test suite
- **`openapi_add_employee_with_manager.yaml`** - OpenAPI specification

## Key Features

### 1. Circular Reference Pattern

```python
class Person(BaseModel):
    name: str
    employee_id: str
    email: EmailStr
    department: DepartmentEnum
    position: str
    manager: Optional['Person']  # ← Circular reference to Person
```

The `manager` field references the same `Person` schema, enabling:
- Multi-level organizational hierarchies
- Unlimited depth of reporting chains
- Self-referential data structures

### 2. Pydantic Forward References

```python
# Enable forward references for circular dependencies
Person.model_rebuild()
```

Pydantic's `model_rebuild()` resolves forward references after the class definition, allowing the circular reference to work correctly.

### 3. Department Enumeration (Enum Reference)

```python
class DepartmentEnum(str, Enum):
    """Department enumeration - referenced by Person.department"""
    ENGINEERING = "Engineering"
    PRODUCT = "Product"
    SALES = "Sales"
    MARKETING = "Marketing"
    HR = "HR"
    FINANCE = "Finance"
    OPERATIONS = "Operations"
    EXECUTIVE = "Executive"
```

**Enum Reference Benefits:**
- **Type Safety**: Only predefined department values are allowed
- **Validation**: Pydantic automatically validates against enum values
- **IDE Support**: Auto-completion for department values
- **Documentation**: Self-documenting valid department options
- **Consistency**: Ensures department names are consistent across the organization

**Usage in Person Schema:**
```python
department: DepartmentEnum = Field(..., description="Department name")
```

This creates a reference from the `Person` schema to the `DepartmentEnum`, similar to how `manager` creates a circular reference to `Person`.

### 4. Email Validation

```python
email: EmailStr = Field(..., description="Work email address")
```

Built-in email format validation using Pydantic's `EmailStr` type.

### 5. Employee ID Pattern Validation

```python
@field_validator('employee_id')
@classmethod
def validate_employee_id(cls, v: str) -> str:
    if not v.startswith('EMP-'):
        raise ValueError('Employee ID must start with EMP-')
    return v
```

Custom validation ensures employee IDs follow the `EMP-XXX` pattern.

## Usage Examples

### Example 1: Single-Level Hierarchy

```python
from register_employee_pydantic import (
    Person, DepartmentEnum, EmployeeRegistrationRequest,
    register_employee_with_manager
)
from datetime import date

request = EmployeeRegistrationRequest(
    employee=Person(
        name="Sarah Martinez",
        employee_id="EMP-201",
        email="sarah.martinez@company.com",
        phone="+1-555-0201",
        department=DepartmentEnum.ENGINEERING,
        position="Software Engineer",
        start_date=date(2024, 2, 1),
        manager=Person(
            name="Michael Chen",
            employee_id="EMP-150",
            email="michael.chen@company.com",
            department=DepartmentEnum.ENGINEERING,
            position="Engineering Manager",
            start_date=date(2022, 5, 15)
        )
    )
)

result = register_employee_with_manager(request)
print(result)
```

### Example 2: Multi-Level Hierarchy (3 Levels)

```python
request = EmployeeRegistrationRequest(
    employee=Person(
        name="James Wilson",
        employee_id="EMP-202",
        email="james.wilson@company.com",
        department=DepartmentEnum.PRODUCT,
        position="Senior Product Manager",
        start_date=date(2024, 3, 1),
        manager=Person(
            name="Lisa Anderson",
            employee_id="EMP-100",
            email="lisa.anderson@company.com",
            department=DepartmentEnum.PRODUCT,
            position="VP of Product",
            start_date=date(2020, 1, 10),
            manager=Person(
                name="Robert Taylor",
                employee_id="EMP-001",
                email="robert.taylor@company.com",
                department=DepartmentEnum.EXECUTIVE,
                position="Chief Product Officer",
                start_date=date(2018, 6, 1)
            )
        )
    )
)
```

### Example 3: Top-Level Executive (No Manager)

```python
request = EmployeeRegistrationRequest(
    employee=Person(
        name="Jennifer Davis",
        employee_id="EMP-005",
        email="jennifer.davis@company.com",
        department=DepartmentEnum.EXECUTIVE,
        position="Chief Executive Officer",
        start_date=date(2015, 1, 1)
        # No manager field - optional for top-level executives
    )
)
```

## Output Format

The tool returns a formatted confirmation message:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EMPLOYEE REGISTRATION CONFIRMATION                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

REGISTRATION STATUS: SUCCESS
Registration Date: 2024-02-01 10:30:00

EMPLOYEE INFORMATION:
  Name: Sarah Martinez
  Employee ID: EMP-201
  Email: sarah.martinez@company.com
  Phone: +1-555-0201
  Department: Engineering
  Position: Software Engineer
  Start Date: 2024-02-01

MANAGER INFORMATION:
  Manager: Michael Chen (EMP-150) - Engineering Manager
  Name: Michael Chen
  Employee ID: EMP-150
  Email: michael.chen@company.com
  Phone: +1-555-0150
  Department: Engineering
  Position: Engineering Manager
  Start Date: 2022-05-15

ORGANIZATIONAL HIERARCHY:
  Reporting Chain: Sarah Martinez (EMP-201) → Michael Chen (EMP-150)
  Hierarchy Levels: 2

CONFIRMATION MESSAGE:
  Employee Sarah Martinez (EMP-201) has been successfully registered
  under manager Michael Chen (EMP-150)

╔══════════════════════════════════════════════════════════════════════════════╗
║  Registration complete! Welcome to the team!                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Running Tests

```bash
# Install dependencies
pip install pydantic ibm-watsonx-orchestrate

# Run the test suite
python test_register_employee_pydantic.py
```

The test suite includes:
1. Single-level hierarchy (Employee → Manager)
2. Multi-level hierarchy (Employee → Manager → Executive)
3. Top-level executive (no manager)
4. Minimal required fields
5. Deep hierarchy (4+ levels)

## Technical Details

### Circular Reference Resolution

Pydantic handles circular references through:

1. **Forward Reference Syntax**: Using string annotation `'Person'` instead of direct `Person`
2. **Model Rebuild**: Calling `Person.model_rebuild()` after class definition
3. **Optional Type**: Making `manager` optional with `Optional['Person']`

### Validation Features

- **Email Format**: Automatic validation via `EmailStr`
- **Pattern Matching**: Employee ID must match `^EMP-[0-9]+$`
- **Enum Validation**: Department must be one of predefined values
- **Date Handling**: Proper date serialization and validation

### Reporting Chain Algorithm

```python
reporting_chain_parts = []
hierarchy_levels = 1
current_person = employee

while current_person:
    reporting_chain_parts.append(
        f"{current_person.name} ({current_person.employee_id})"
    )
    if current_person.manager:
        hierarchy_levels += 1
        current_person = current_person.manager
    else:
        break

reporting_chain = " → ".join(reporting_chain_parts)
```

This algorithm traverses the circular reference chain to build the complete reporting hierarchy.

## Comparison with Reference Implementation

This implementation follows the same pattern as [`process_customer_order_pydantic.py`](../../Test_data_tools/Python/Standard%20Nesting%20(Basic,%20Deep,%20References)/process_customer_order_pydantic.py):

| Feature | Customer Order Tool | Employee Registration Tool |
|---------|-------------------|---------------------------|
| **Nested References** | `shipping_locations.address` → `customer.address` | `employee.manager` → `Person` (circular) |
| **Validation** | Pydantic models with Field validators | Pydantic models with custom validators |
| **Tool Decorator** | `@tool(permission=ToolPermission.WRITE_ONLY)` | `@tool(permission=ToolPermission.WRITE_ONLY)` |
| **Output Format** | Formatted confirmation with box drawing | Formatted confirmation with box drawing |
| **Test Coverage** | Multiple scenarios with examples | 5 test scenarios covering edge cases |

## Key Differences

1. **Reference Type**:
   - Customer Order: Cross-schema references (address reuse)
   - Employee Registration: Self-referential circular reference

2. **Depth Handling**:
   - Customer Order: Fixed depth (2-3 levels)
   - Employee Registration: Unlimited depth via recursion

3. **Validation Complexity**:
   - Customer Order: Basic field validation
   - Employee Registration: Pattern matching + enum validation

## Watson Orchestrate Integration

This tool is designed for IBM Watson Orchestrate and includes:

- `@tool` decorator for skill registration
- `ToolPermission.WRITE_ONLY` for appropriate access control
- Pydantic models for automatic schema generation
- Type hints for parameter validation

## Related Files

- [`openapi_add_employee_with_manager.yaml`](openapi_add_employee_with_manager.yaml) - OpenAPI specification
- [`register_employee.py`](register_employee.py) - Original implementation
- [`process_customer_order_pydantic.py`](../../Test_data_tools/Python/Standard%20Nesting%20(Basic,%20Deep,%20References)/process_customer_order_pydantic.py) - Reference implementation

---

**Made with Bob** 🤖
