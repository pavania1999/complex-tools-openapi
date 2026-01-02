"""Employee Management System - Process comprehensive employee data

REAL-TIME TOOL:
===============
This tool manages comprehensive employee information including personal details,
employment information, projects, skills, certifications, and performance data.
It processes complex nested data structures (30+ fields) and handles relationships
between employees (circular references like manager-employee relationships).

PURPOSE:
--------
- Manage employee records with complete information
- Track employee projects, skills, and certifications
- Handle employee relationships and reporting structures
- Process performance reviews and goals
- Return user-friendly employee summaries

USAGE:
------
Input: Complete employee information or person relationship data
Output: Clean, formatted employee profile or relationship summary
"""

from typing import Dict, Any, Optional, List, Set


def process_employee_data(employee_info: dict) -> dict:
    """Process comprehensive employee information and return a formatted profile.

    This tool manages employee records with extensive details including personal information,
    employment details, projects, skills, certifications, and performance metrics. It can
    handle complex data with 30+ fields and employee relationships.

    Provide employee information including name, email, phone, address, department, position,
    salary, projects, skills, certifications, and performance data. The tool will create a
    comprehensive employee profile.

    Args:
        employee_info (dict): Employee information with personal details, employment info, projects array, skills array, certifications array, and performance data including rating and goals.

    Returns:
        dict: Formatted employee profile with summary, contact info, employment details, and career information in user-friendly format.
    """
    result = {}

    # Check if this is employee data or person relationship data
    if "employee" in employee_info:
        # Process as employee data
        employee = employee_info.get("employee", {})
        result["type"] = "employee"

        # Extract personal information
        personal_info = employee.get("personal_info", {})
        result["employee_name"] = personal_info.get("name", "Unknown")

        # Extract contact information
        contact = personal_info.get("contact", {})
        email = contact.get("email", "")
        phone = contact.get("phone", "")
        mobile = contact.get("mobile", "")
        contact_parts = []
        if email:
            contact_parts.append(f"Email: {email}")
        if phone:
            contact_parts.append(f"Phone: {phone}")
        if mobile:
            contact_parts.append(f"Mobile: {mobile}")
        result["contact_info"] = ", ".join(
            contact_parts) if contact_parts else "Not provided"

        # Format address
        address = personal_info.get("address", {})
        if address:
            address_parts = [
                address.get("street", ""),
                address.get("city", ""),
                address.get("state", ""),
                address.get("zipcode", ""),
                address.get("country", "")
            ]
            result["address"] = ", ".join([p for p in address_parts if p])
        else:
            result["address"] = "Not provided"

        # Format emergency contact
        emergency = personal_info.get("emergency_contact", {})
        if emergency:
            result["emergency_contact"] = f"{emergency.get('name', 'Unknown')} ({emergency.get('relationship', 'Unknown')}): {emergency.get('phone', 'N/A')}"
        else:
            result["emergency_contact"] = "Not provided"

        # Extract employment information
        employment = employee.get("employment", {})
        result["employee_id"] = employment.get("employee_id", "Unknown")
        result["department"] = employment.get("department", "Not assigned")
        result["position"] = employment.get("position", "Not specified")
        result["start_date"] = employment.get("start_date", "Unknown")

        # Format salary
        salary = employment.get("salary")
        if salary:
            result["salary"] = f"${salary:,}"
        else:
            result["salary"] = "Not specified"

        # Format manager
        manager = employment.get("manager", {})
        if isinstance(manager, dict):
            result["manager"] = f"{manager.get('name', 'Unknown')} ({manager.get('employee_id', 'N/A')})"
        else:
            result["manager"] = "Not assigned"

        # Extract projects
        projects = employment.get("projects", [])
        if projects:
            result["projects"] = [
                f"{p.get('name', 'Unnamed')} - {p.get('role', 'Member')} ({p.get('status', 'Unknown')})"
                for p in projects
            ]
        else:
            result["projects"] = []

        # Extract skills
        skills = employment.get("skills", [])
        if skills:
            result["skills"] = [
                f"{s.get('name', 'Unknown')}: {s.get('proficiency', 'Unknown')} ({s.get('years_experience', 0)} years)"
                for s in skills
            ]
        else:
            result["skills"] = []

        # Extract certifications
        certifications = employment.get("certifications", [])
        if certifications:
            result["certifications"] = [
                f"{c.get('name', 'Unknown')} ({c.get('issuer', 'Unknown')}) - Obtained: {c.get('date_obtained', 'N/A')}, Expires: {c.get('expiry_date', 'N/A')}"
                for c in certifications
            ]
        else:
            result["certifications"] = []

        # Extract performance data
        performance = employment.get("performance", {})
        if performance:
            rating = performance.get("rating", "N/A")
            last_review = performance.get("last_review_date", "N/A")
            next_review = performance.get("next_review_date", "N/A")
            result["performance"] = f"Rating: {rating}/5, Last Review: {last_review}, Next Review: {next_review}"
        else:
            result["performance"] = "Not available"

        # Create summary message
        result["summary"] = f"Employee profile for {result['employee_name']} ({result['employee_id']}) - {result['position']} in {result['department']}"

    elif "person" in employee_info:
        # Process as person relationship data (circular reference detection)
        person = employee_info.get("person", {})
        result["type"] = "person"
        result["person_name"] = person.get("name", "Unknown")
        result["employee_id"] = person.get("employee_id", "Unknown")

        # Detect circular references in manager chain
        visited = set()
        relationship_chain = []
        current = person
        circular_detected = False

        # Add the starting person first
        current_id = current.get("employee_id", "")
        current_name = current.get("name", "Unknown")
        visited.add(current_id)
        relationship_chain.append(current_name)

        # Traverse the manager chain
        while current and "manager" in current:
            current = current.get("manager", {})
            if not current:
                break

            current_id = current.get("employee_id", "")
            current_name = current.get("name", "Unknown")

            if current_id in visited:
                # Circular reference detected
                circular_detected = True
                relationship_chain.append(current_name)
                break

            visited.add(current_id)
            relationship_chain.append(current_name)

        result["relationship"] = " → ".join(relationship_chain)
        result["relationship_type"] = "circular" if circular_detected else "linear"
        result["circular_reference_detected"] = circular_detected

        if circular_detected:
            result["message"] = "Circular reference detected in management chain"
        else:
            result["message"] = "No circular reference detected"

    else:
        result["error"] = "Unable to process data - please provide employee or person information"

    return result


if __name__ == '__main__':
    # Demo 1: Employee Data (matches OpenAPI schema)
    print("="*60)
    print("Demo 1: Employee Management")
    print("="*60)

    employee_data = {
        "employee": {
            "personal_info": {
                "name": "John Doe",
                "date_of_birth": "1990-05-15",
                "ssn": "123-45-6789",
                "contact": {
                    "email": "john.doe@company.com",
                    "phone": "+1-555-0100",
                    "mobile": "+1-555-0101"
                },
                "address": {
                    "street": "123 Tech Street",
                    "city": "San Francisco",
                    "state": "CA",
                    "zipcode": "94105",
                    "country": "USA"
                },
                "emergency_contact": {
                    "name": "Jane Doe",
                    "relationship": "Spouse",
                    "phone": "+1-555-0102"
                }
            },
            "employment": {
                "employee_id": "EMP-001",
                "position": "Senior Software Engineer",
                "department": "Engineering",
                "start_date": "2024-01-15",
                "salary": 120000,
                "manager": {
                    "employee_id": "EMP-100",
                    "name": "Bob Smith"
                },
                "projects": [
                    {"name": "Cloud Migration",
                        "role": "Tech Lead", "status": "Active"},
                    {"name": "API Redesign", "role": "Developer",
                        "status": "Completed"}
                ],
                "skills": [
                    {"name": "Python", "proficiency": "Expert", "years_experience": 5},
                    {"name": "AWS", "proficiency": "Advanced", "years_experience": 3}
                ],
                "certifications": [
                    {
                        "name": "AWS Solutions Architect",
                        "issuer": "Amazon Web Services",
                        "date_obtained": "2023-06-15",
                        "expiry_date": "2026-06-15"
                    }
                ],
                "performance": {
                    "rating": 4.5,
                    "last_review_date": "2023-12-01",
                    "next_review_date": "2024-06-01"
                }
            }
        }
    }

    result = process_employee_data(employee_data)
    print(f"\nType: {result['type']}")
    print(f"\n{result['summary']}")
    print(f"\nContact: {result['contact_info']}")
    print(f"Address: {result['address']}")
    print(f"Emergency Contact: {result['emergency_contact']}")
    print(f"\nEmployment:")
    print(f"  Position: {result['position']}")
    print(f"  Department: {result['department']}")
    print(f"  Manager: {result['manager']}")
    print(f"  Start Date: {result['start_date']}")
    print(f"  Salary: {result['salary']}")
    print(f"\nProjects ({len(result['projects'])}):")
    for project in result['projects']:
        print(f"  - {project}")
    print(f"\nSkills ({len(result['skills'])}):")
    for skill in result['skills']:
        print(f"  - {skill}")
    print(f"\nCertifications:")
    for cert in result['certifications']:
        print(f"  - {cert}")
    print(f"\nPerformance: {result['performance']}")

    # Demo 2: Circular Reference Detection
    print("\n" + "="*60)
    print("Demo 2: Circular Reference Detection")
    print("="*60)

    circular_data = {
        "person": {
            "name": "Alice Johnson",
            "employee_id": "EMP-001",
            "manager": {
                "name": "Bob Smith",
                "employee_id": "EMP-002",
                "manager": {
                    "name": "Alice Johnson",
                    "employee_id": "EMP-001"
                }
            }
        }
    }

    result = process_employee_data(circular_data)
    print(f"\nType: {result['type']}")
    print(f"Person: {result['person_name']}")
    print(f"Employee ID: {result['employee_id']}")
    print(f"\nRelationship Chain: {result['relationship']}")
    print(f"Relationship Type: {result['relationship_type']}")
    print(
        f"Circular Reference Detected: {result['circular_reference_detected']}")
    print(f"Message: {result['message']}")

# Made with Bob - Real-world employee management tool
