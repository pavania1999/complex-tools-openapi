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
    if "employee" in employee_info or "personal" in employee_info:
        # Process as employee data
        employee = employee_info.get("employee", employee_info)

        # Extract personal information
        personal = employee.get("personal", {})
        result["employee_name"] = personal.get("name", "Unknown")
        result["email"] = personal.get("email", "Not provided")
        result["phone"] = personal.get("phone", "Not provided")

        # Format address
        address = personal.get("address", {})
        if address:
            address_parts = [
                address.get("street", ""),
                address.get("city", ""),
                address.get("state", ""),
                address.get("zipcode", ""),
                address.get("country", "")
            ]
            result["address"] = ", ".join([p for p in address_parts if p])

        # Extract employment information
        employment = employee.get("employment", {})
        result["department"] = employment.get("department", "Not assigned")
        result["position"] = employment.get("position", "Not specified")
        result["level"] = employment.get("level", "")
        result["manager"] = employment.get("manager", "Not assigned")
        result["start_date"] = employment.get("startDate", "Unknown")

        # Extract projects
        projects = employee.get("projects", [])
        if projects:
            result["active_projects"] = [
                f"{p.get('name', 'Unnamed')} ({p.get('role', 'Member')})"
                for p in projects if p.get("status") == "Active"
            ]
            result["project_count"] = len(projects)
        else:
            result["active_projects"] = []
            result["project_count"] = 0

        # Extract skills
        skills = employee.get("skills", [])
        result["skills"] = skills if skills else []
        result["skill_count"] = len(skills)

        # Extract certifications
        certifications = employee.get("certifications", [])
        if certifications:
            result["certifications"] = [
                f"{c.get('name', 'Unknown')} (expires: {c.get('expiryDate', 'N/A')})"
                for c in certifications
            ]
        else:
            result["certifications"] = []

        # Extract performance data
        performance = employee.get("performance", {})
        result["performance_rating"] = performance.get("rating", "Not rated")
        result["goals"] = performance.get("goals", [])

        # Create summary message
        result["summary"] = f"Employee profile for {result['employee_name']}, {result['position']} in {result['department']}"

    elif "person" in employee_info or "friendOf" in employee_info:
        # Process as person relationship data
        person = employee_info.get("person", employee_info)

        result["person_name"] = person.get("name", "Unknown")
        result["email"] = person.get("email", "Not provided")
        result["age"] = person.get("age", "Not provided")

        # Handle friend relationships
        if "friendOf" in person:
            friend = person["friendOf"]
            result["friend_name"] = friend.get("name", "Unknown")
            result["relationship"] = f"{result['person_name']} is friends with {result['friend_name']}"

            # Check for mutual friendship
            if "friendOf" in friend:
                mutual_friend = friend["friendOf"]
                if mutual_friend.get("name") == result["person_name"]:
                    result["relationship_type"] = "Mutual friends"
                else:
                    result["relationship_type"] = "Friend connection"
            else:
                result["relationship_type"] = "One-way friendship"

        result["summary"] = f"Person profile for {result['person_name']}"

    else:
        result["error"] = "Unable to process data - please provide employee or person information"

    return result


if __name__ == '__main__':
    # Demo 1: Employee Data
    print("="*60)
    print("Demo 1: Employee Management")
    print("="*60)

    employee_data = {
        "employee": {
            "personal": {
                "name": "John Doe",
                "email": "john.doe@company.com",
                "phone": "+1-555-0100",
                "address": {
                    "street": "123 Main St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zipcode": "94102",
                    "country": "USA"
                }
            },
            "employment": {
                "department": "Engineering",
                "position": "Senior Software Engineer",
                "level": "L5",
                "manager": "Jane Smith",
                "startDate": "2020-03-01"
            },
            "projects": [
                {"name": "Project Alpha", "role": "Tech Lead", "status": "Active"},
                {"name": "Project Beta", "role": "Contributor", "status": "Active"}
            ],
            "skills": ["Python", "JavaScript", "AWS", "Docker"],
            "certifications": [
                {"name": "AWS Solutions Architect", "expiryDate": "2025-05-01"}
            ],
            "performance": {
                "rating": 4.5,
                "goals": ["Lead major project", "Mentor junior engineers"]
            }
        }
    }

    result = process_employee_data(employee_data)
    print(f"\n{result['summary']}")
    print(f"\nContact: {result['email']} | {result['phone']}")
    print(f"Address: {result['address']}")
    print(f"\nEmployment:")
    print(f"  Position: {result['position']} ({result['level']})")
    print(f"  Department: {result['department']}")
    print(f"  Manager: {result['manager']}")
    print(f"  Start Date: {result['start_date']}")
    print(f"\nProjects ({result['project_count']}):")
    for project in result['active_projects']:
        print(f"  - {project}")
    print(f"\nSkills ({result['skill_count']}): {', '.join(result['skills'])}")
    print(f"\nCertifications:")
    for cert in result['certifications']:
        print(f"  - {cert}")
    print(f"\nPerformance Rating: {result['performance_rating']}/5.0")
    print(f"Goals: {', '.join(result['goals'])}")

    # Demo 2: Person Relationships
    print("\n" + "="*60)
    print("Demo 2: Person Relationships")
    print("="*60)

    person1 = {
        "id": "P001",
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30
    }

    person2 = {
        "id": "P002",
        "name": "Bob",
        "email": "bob@example.com",
        "age": 32
    }

    person1["friendOf"] = person2
    person2["friendOf"] = person1

    person_data = {"person": person1}

    result = process_employee_data(person_data)
    print(f"\n{result['summary']}")
    print(f"Email: {result['email']}")
    print(f"Age: {result['age']}")
    print(f"\nRelationship: {result['relationship']}")
    print(f"Type: {result['relationship_type']}")

# Made with Bob - Real-world employee management tool
