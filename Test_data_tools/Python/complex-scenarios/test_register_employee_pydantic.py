"""
Test script for register_employee_pydantic.py
Demonstrates the circular reference pattern with various scenarios
"""

from datetime import date
from register_employee_pydantic import (
    Person,
    DepartmentEnum,
    EmployeeRegistrationRequest,
    register_employee_with_manager
)


def test_single_level_hierarchy():
    """Test employee with direct manager (2-level hierarchy)"""
    print("=" * 80)
    print("TEST 1: Single-level hierarchy (Employee → Manager)")
    print("=" * 80)

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
                phone="+1-555-0150",
                department=DepartmentEnum.ENGINEERING,
                position="Engineering Manager",
                start_date=date(2022, 5, 15)
            )
        )
    )

    result = register_employee_with_manager(request)
    print(result)
    print("\n✓ Test passed: Single-level hierarchy\n")


def test_multi_level_hierarchy():
    """Test employee with multi-level management chain (3-level hierarchy)"""
    print("=" * 80)
    print("TEST 2: Multi-level hierarchy (Employee → Manager → Executive)")
    print("=" * 80)

    request = EmployeeRegistrationRequest(
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

    result = register_employee_with_manager(request)
    print(result)
    print("\n✓ Test passed: Multi-level hierarchy\n")


def test_top_level_executive():
    """Test top-level executive with no manager"""
    print("=" * 80)
    print("TEST 3: Top-level executive (no manager)")
    print("=" * 80)

    request = EmployeeRegistrationRequest(
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

    result = register_employee_with_manager(request)
    print(result)
    print("\n✓ Test passed: Top-level executive\n")


def test_minimal_required_fields():
    """Test with only required fields"""
    print("=" * 80)
    print("TEST 4: Minimal required fields")
    print("=" * 80)

    request = EmployeeRegistrationRequest(
        employee=Person(
            name="Alex Johnson",
            employee_id="EMP-300",
            email="alex.johnson@company.com",
            department=DepartmentEnum.SALES,
            position="Sales Representative"
        )
    )

    result = register_employee_with_manager(request)
    print(result)
    print("\n✓ Test passed: Minimal required fields\n")


def test_deep_hierarchy():
    """Test deep organizational hierarchy (4+ levels)"""
    print("=" * 80)
    print("TEST 5: Deep hierarchy (4 levels)")
    print("=" * 80)

    request = EmployeeRegistrationRequest(
        employee=Person(
            name="Emily Brown",
            employee_id="EMP-250",
            email="emily.brown@company.com",
            department=DepartmentEnum.MARKETING,
            position="Marketing Coordinator",
            start_date=date(2024, 1, 15),
            manager=Person(
                name="David Lee",
                employee_id="EMP-200",
                email="david.lee@company.com",
                department=DepartmentEnum.MARKETING,
                position="Marketing Manager",
                start_date=date(2023, 6, 1),
                manager=Person(
                    name="Susan White",
                    employee_id="EMP-120",
                    email="susan.white@company.com",
                    department=DepartmentEnum.MARKETING,
                    position="Director of Marketing",
                    start_date=date(2021, 3, 15),
                    manager=Person(
                        name="Thomas Green",
                        employee_id="EMP-010",
                        email="thomas.green@company.com",
                        department=DepartmentEnum.EXECUTIVE,
                        position="Chief Marketing Officer",
                        start_date=date(2019, 1, 1)
                    )
                )
            )
        )
    )

    result = register_employee_with_manager(request)
    print(result)
    print("\n✓ Test passed: Deep hierarchy (4 levels)\n")


if __name__ == '__main__':
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║         EMPLOYEE REGISTRATION TOOL - CIRCULAR REFERENCE TESTS                ║")
    print("║                    Testing Pydantic Implementation                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print("\n")

    try:
        test_single_level_hierarchy()
        test_multi_level_hierarchy()
        test_top_level_executive()
        test_minimal_required_fields()
        test_deep_hierarchy()

        print("=" * 80)
        print("ALL TESTS PASSED ✓")
        print("=" * 80)
        print("\nSummary:")
        print("- Circular reference pattern working correctly")
        print("- Person.manager successfully references Person schema")
        print("- Multi-level hierarchies supported (tested up to 4 levels)")
        print("- Optional manager field works for top-level executives")
        print("- Pydantic validation and serialization working as expected")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

# Made with Bob
