"""
Employee Registration Tool with Circular Schema Reference using Pydantic
Demonstrates Pydantic handling of circular references where Person.manager references Person schema
Based on openapi_add_employee_with_manager.yaml
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import date, datetime
from enum import Enum


class DepartmentEnum(str, Enum):
    """Department enumeration"""
    ENGINEERING = "Engineering"
    PRODUCT = "Product"
    SALES = "Sales"
    MARKETING = "Marketing"
    HR = "HR"
    FINANCE = "Finance"
    OPERATIONS = "Operations"
    EXECUTIVE = "Executive"


class Person(BaseModel):
    """
    Person schema representing an employee or manager.
    The manager field references the same Person schema, creating a circular schema reference.
    This allows representing organizational hierarchies of any depth.
    """
    name: str = Field(..., description="Full name of the person")
    employee_id: str = Field(
        ...,
        description="Unique employee identifier",
        pattern=r'^EMP-[0-9]+$'
    )
    email: str = Field(..., description="Work email address")
    phone: Optional[str] = Field(None, description="Work phone number")
    department: DepartmentEnum = Field(..., description="Department name")
    position: str = Field(..., description="Job title/position")
    start_date: Optional[date] = Field(
        None, description="Employment start date")
    manager: Optional['Person'] = Field(
        None,
        description="Manager of this person. Uses the same Person schema, creating a circular reference that allows representing the full management hierarchy. This field is optional for top-level executives."
    )

    @field_validator('employee_id')
    @classmethod
    def validate_employee_id(cls, v: str) -> str:
        """Validate employee ID format"""
        if not v.startswith('EMP-'):
            raise ValueError('Employee ID must start with EMP-')
        return v

    class Config:
        # Enable forward references for circular dependencies
        arbitrary_types_allowed = True


# Update forward references for circular dependency
Person.model_rebuild()


class EmployeeRegistrationRequest(BaseModel):
    """Main request schema for employee registration"""
    employee: Person = Field(...,
                             description="Employee information to register")


class EmployeeSummary(BaseModel):
    """Employee summary for response"""
    name: str
    employee_id: str
    department: str
    position: str
    start_date: Optional[date]


class ManagerSummary(BaseModel):
    """Manager summary for response"""
    name: str
    employee_id: str
    position: str


class EmployeeRegistrationResponse(BaseModel):
    """Response schema for employee registration"""
    status: Literal["success", "error"]
    message: str
    employee: EmployeeSummary
    manager: Optional[ManagerSummary] = None
    reporting_chain: str
    hierarchy_levels: Optional[int] = None
    registration_date: datetime


@tool(permission=ToolPermission.WRITE_ONLY)
def register_employee_with_manager(registration_request: EmployeeRegistrationRequest) -> str:
    """
    Register new employee with manager information.

    Register a new employee by providing their personal information along with
    their manager's information. Both employee and manager use the same Person
    schema, creating a circular schema reference pattern where Person.manager
    references Person schema.

    Args:
        registration_request: Employee registration request with employee and manager details

    Returns:
        Formatted registration confirmation message
    """
    employee = registration_request.employee

    # Build reporting chain
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

    # Format employee details
    employee_name = employee.name
    employee_id = employee.employee_id
    employee_email = employee.email
    employee_phone = employee.phone or "N/A"
    employee_dept = employee.department.value
    employee_position = employee.position
    employee_start_date = employee.start_date.strftime(
        "%Y-%m-%d") if employee.start_date else "N/A"

    # Format manager details
    manager_info = "N/A"
    manager_name = "N/A"
    manager_id = "N/A"
    manager_position = "N/A"
    manager_dept = "N/A"
    manager_email = "N/A"
    manager_phone = "N/A"
    manager_start_date = "N/A"

    if employee.manager:
        manager = employee.manager
        manager_name = manager.name
        manager_id = manager.employee_id
        manager_position = manager.position
        manager_dept = manager.department.value
        manager_email = manager.email
        manager_phone = manager.phone or "N/A"
        manager_start_date = manager.start_date.strftime(
            "%Y-%m-%d") if manager.start_date else "N/A"

        manager_info = f"{manager_name} ({manager_id}) - {manager_position}"

    # Build confirmation message
    confirmation = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EMPLOYEE REGISTRATION CONFIRMATION                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

REGISTRATION STATUS: SUCCESS
Registration Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

EMPLOYEE INFORMATION:
  Name: {employee_name}
  Employee ID: {employee_id}
  Email: {employee_email}
  Phone: {employee_phone}
  Department: {employee_dept}
  Position: {employee_position}
  Start Date: {employee_start_date}

MANAGER INFORMATION:
  Manager: {manager_info}
  Name: {manager_name}
  Employee ID: {manager_id}
  Email: {manager_email}
  Phone: {manager_phone}
  Department: {manager_dept}
  Position: {manager_position}
  Start Date: {manager_start_date}

ORGANIZATIONAL HIERARCHY:
  Reporting Chain: {reporting_chain}
  Hierarchy Levels: {hierarchy_levels}

CONFIRMATION MESSAGE:
  Employee {employee_name} ({employee_id}) has been successfully registered
  under manager {manager_name} ({manager_id})

╔══════════════════════════════════════════════════════════════════════════════╗
║  Registration complete! Welcome to the team!                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    return confirmation.strip()


if __name__ == '__main__':
    # Example 1: Register new employee with manager
    print("=" * 80)
    print("Example 1: Register new employee with manager")
    print("=" * 80)

    registration_request = EmployeeRegistrationRequest(
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
                phone="+1-555-0150",
                department=DepartmentEnum.ENGINEERING,
                position="Engineering Manager",
                start_date=date(2022, 5, 15)
            )
        )
    )

    result = register_employee_with_manager(
        registration_request=registration_request)
    print(result)

    # Example 2: Register senior employee with multi-level hierarchy
    print("\n" + "=" * 80)
    print("Example 2: Register senior employee with executive manager (3-level hierarchy)")
    print("=" * 80)

    registration_request_senior = EmployeeRegistrationRequest(
        employee=Person(
            name="James Wilson",
            employee_id="EMP-202",
            email="james.wilson@company.com",
            phone="+1-555-0202",
            department=DepartmentEnum.PRODUCT,
            position="Senior Product Manager",
            start_date=date(2024, 3, 1),
            manager=Person(
                name="Lisa Anderson",
                employee_id="EMP-100",
                email="lisa.anderson@company.com",
                phone="+1-555-0100",
                department=DepartmentEnum.PRODUCT,
                position="VP of Product",
                start_date=date(2020, 1, 10),
                manager=Person(
                    name="Robert Taylor",
                    employee_id="EMP-001",
                    email="robert.taylor@company.com",
                    phone="+1-555-0001",
                    department=DepartmentEnum.EXECUTIVE,
                    position="Chief Product Officer",
                    start_date=date(2018, 6, 1)
                )
            )
        )
    )

    result = register_employee_with_manager(
        registration_request=registration_request_senior)
    print(result)

    # Example 3: Register top-level executive (no manager)
    print("\n" + "=" * 80)
    print("Example 3: Register top-level executive (no manager)")
    print("=" * 80)

    registration_request_exec = EmployeeRegistrationRequest(
        employee=Person(
            name="Jennifer Davis",
            employee_id="EMP-005",
            email="jennifer.davis@company.com",
            phone="+1-555-0005",
            department=DepartmentEnum.EXECUTIVE,
            position="Chief Executive Officer",
            start_date=date(2015, 1, 1)
        )
    )

    result = register_employee_with_manager(
        registration_request=registration_request_exec)
    print(result)

# Made with Bob
