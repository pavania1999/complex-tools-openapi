"""Employee Registration System - Register employees with manager information

REAL-TIME TOOL:
===============
This tool registers new employees by collecting their personal information along
with their manager's details. Both employee and manager use the same Person schema,
creating a circular schema reference pattern that naturally models organizational
hierarchies.

PURPOSE:
--------
- Register new employees with complete information
- Capture manager details using the same schema structure
- Build organizational hierarchy chains
- Validate employee data before registration
- Return registration confirmation with reporting chain

USAGE:
------
Input: Employee information including manager details (both using Person schema)
Output: Registration confirmation with employee summary and reporting chain
"""

from typing import Dict, Any, Optional, List
from datetime import datetime


def register_employee(registration_data: dict) -> dict:
    """Register a new employee with their manager information.

    This tool registers employees by collecting their personal details along with
    their manager's information. Both employee and manager use the same Person schema
    structure, creating a circular schema reference that models organizational
    hierarchies naturally.

    Provide employee information including name, employee ID, email, phone, department,
    position, start date, and optionally their manager's information using the same
    structure. The tool will register the employee and return a confirmation with
    the reporting chain.

    Args:
        registration_data (dict): Employee registration data with employee object
                                 containing Person schema (name, employee_id, email,
                                 phone, department, position, start_date, and optional
                                 manager field using same Person schema).

    Returns:
        dict: Registration confirmation with status, employee summary, manager info,
              reporting chain, hierarchy levels, and registration timestamp.
    """
    result = {}

    # Extract employee data
    employee = registration_data.get("employee", {})

    if not employee:
        return {
            "status": "error",
            "error": "Missing employee data",
            "code": "INVALID_REQUEST",
            "details": "Employee information is required for registration"
        }

    # Validate required fields
    required_fields = ["name", "employee_id",
                       "email", "department", "position"]
    missing_fields = [
        field for field in required_fields if not employee.get(field)]

    if missing_fields:
        return {
            "status": "error",
            "error": "Validation failed",
            "code": "INVALID_REQUEST",
            "details": f"Required fields missing: {', '.join(missing_fields)}"
        }

    # Extract employee information
    result["status"] = "success"
    result["message"] = "Employee registered successfully"

    # Employee summary
    result["employee"] = {
        "name": employee.get("name"),
        "employee_id": employee.get("employee_id"),
        "department": employee.get("department"),
        "position": employee.get("position"),
        "start_date": employee.get("start_date", datetime.now().strftime("%Y-%m-%d"))
    }

    # Build reporting chain
    reporting_chain = []
    hierarchy_levels = 1
    current = employee
    visited_ids = set()

    # Add employee to chain
    reporting_chain.append(
        f"{current.get('name')} ({current.get('employee_id')})")
    visited_ids.add(current.get('employee_id'))

    # Traverse manager hierarchy
    while current.get("manager"):
        current = current.get("manager")
        manager_id = current.get("employee_id")

        # Check for circular reference (shouldn't happen in real data)
        if manager_id in visited_ids:
            result["warning"] = "Circular reference detected in management chain"
            break

        reporting_chain.append(
            f"{current.get('name')} ({current.get('employee_id')})")
        visited_ids.add(manager_id)
        hierarchy_levels += 1

        # Limit depth to prevent infinite loops
        if hierarchy_levels > 10:
            result["warning"] = "Management hierarchy exceeds maximum depth of 10 levels"
            break

    # Manager information (direct manager only)
    manager = employee.get("manager")
    if manager:
        result["manager"] = {
            "name": manager.get("name"),
            "employee_id": manager.get("employee_id"),
            "position": manager.get("position", "Manager")
        }
    else:
        result["manager"] = None
        result["note"] = "No manager assigned - this may be a top-level executive"

    # Reporting chain
    result["reporting_chain"] = " → ".join(reporting_chain)

    if hierarchy_levels > 1:
        result["hierarchy_levels"] = hierarchy_levels

    # Registration timestamp
    result["registration_date"] = datetime.now().isoformat() + "Z"

    return result


if __name__ == '__main__':
    # Demo 1: Register employee with manager
    print("="*70)
    print("Demo 1: Register Employee with Manager")
    print("="*70)

    registration_data_1 = {
        "employee": {
            "name": "Sarah Martinez",
            "employee_id": "EMP-201",
            "email": "sarah.martinez@company.com",
            "phone": "+1-555-0201",
            "department": "Engineering",
            "position": "Software Engineer",
            "start_date": "2024-02-01",
            "manager": {
                "name": "Michael Chen",
                "employee_id": "EMP-150",
                "email": "michael.chen@company.com",
                "phone": "+1-555-0150",
                "department": "Engineering",
                "position": "Engineering Manager",
                "start_date": "2022-05-15"
            }
        }
    }

    result = register_employee(registration_data_1)
    print(f"\nStatus: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"\nEmployee:")
    print(f"  Name: {result['employee']['name']}")
    print(f"  ID: {result['employee']['employee_id']}")
    print(f"  Department: {result['employee']['department']}")
    print(f"  Position: {result['employee']['position']}")
    print(f"  Start Date: {result['employee']['start_date']}")
    print(f"\nManager:")
    if result['manager']:
        print(f"  Name: {result['manager']['name']}")
        print(f"  ID: {result['manager']['employee_id']}")
        print(f"  Position: {result['manager']['position']}")
    print(f"\nReporting Chain: {result['reporting_chain']}")
    print(f"Registration Date: {result['registration_date']}")

    # Demo 2: Register senior employee with multi-level hierarchy
    print("\n" + "="*70)
    print("Demo 2: Register Senior Employee with Multi-Level Hierarchy")
    print("="*70)

    registration_data_2 = {
        "employee": {
            "name": "James Wilson",
            "employee_id": "EMP-202",
            "email": "james.wilson@company.com",
            "phone": "+1-555-0202",
            "department": "Product",
            "position": "Senior Product Manager",
            "start_date": "2024-03-01",
            "manager": {
                "name": "Lisa Anderson",
                "employee_id": "EMP-100",
                "email": "lisa.anderson@company.com",
                "phone": "+1-555-0100",
                "department": "Product",
                "position": "VP of Product",
                "start_date": "2020-01-10",
                "manager": {
                    "name": "Robert Taylor",
                    "employee_id": "EMP-001",
                    "email": "robert.taylor@company.com",
                    "phone": "+1-555-0001",
                    "department": "Executive",
                    "position": "Chief Product Officer",
                    "start_date": "2018-06-01"
                }
            }
        }
    }

    result = register_employee(registration_data_2)
    print(f"\nStatus: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"\nEmployee:")
    print(f"  Name: {result['employee']['name']}")
    print(f"  ID: {result['employee']['employee_id']}")
    print(f"  Department: {result['employee']['department']}")
    print(f"  Position: {result['employee']['position']}")
    print(f"\nManager:")
    if result['manager']:
        print(f"  Name: {result['manager']['name']}")
        print(f"  ID: {result['manager']['employee_id']}")
        print(f"  Position: {result['manager']['position']}")
    print(f"\nReporting Chain: {result['reporting_chain']}")
    print(f"Hierarchy Levels: {result.get('hierarchy_levels', 1)}")
    print(f"Registration Date: {result['registration_date']}")

    # Demo 3: Register top-level executive (no manager)
    print("\n" + "="*70)
    print("Demo 3: Register Top-Level Executive (No Manager)")
    print("="*70)

    registration_data_3 = {
        "employee": {
            "name": "Jennifer Lee",
            "employee_id": "EMP-001",
            "email": "jennifer.lee@company.com",
            "phone": "+1-555-0001",
            "department": "Executive",
            "position": "Chief Executive Officer",
            "start_date": "2015-01-01"
        }
    }

    result = register_employee(registration_data_3)
    print(f"\nStatus: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"\nEmployee:")
    print(f"  Name: {result['employee']['name']}")
    print(f"  ID: {result['employee']['employee_id']}")
    print(f"  Department: {result['employee']['department']}")
    print(f"  Position: {result['employee']['position']}")
    print(f"\nManager: {result['manager']}")
    if 'note' in result:
        print(f"Note: {result['note']}")
    print(f"\nReporting Chain: {result['reporting_chain']}")
    print(f"Registration Date: {result['registration_date']}")

# Made with Bob - Real-world employee registration tool with circular schema references
