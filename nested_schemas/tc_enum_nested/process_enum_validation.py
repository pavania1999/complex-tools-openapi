"""Enum Nested Schemas Validation System - Handle multi-level enum validation

REAL-TIME TOOL:
===============
This tool validates enum values at multiple nesting levels including account status,
customer types, address countries, and contact preferences. It provides comprehensive
validation reporting for nested enum structures.

PURPOSE:
--------
- Validate simple enums at root level (status, type)
- Validate nested enums in customer objects (type)
- Validate deeply nested enums in addresses (country)
- Validate contact preference enums
- Provide detailed validation reports

USAGE:
------
Input: Data with enum fields at various nesting levels
Output: Validation results with detailed enum checking
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime


def validate_enum(value: str, allowed_values: List[str], field_name: str) -> Tuple[bool, str]:
    """Validate a single enum value.

    Args:
        value: The value to validate
        allowed_values: List of allowed enum values
        field_name: Name of the field being validated

    Returns:
        Tuple of (is_valid, message)
    """
    if value in allowed_values:
        return True, f"{field_name}={value} (valid)"
    else:
        return False, f"{field_name}={value} (invalid - allowed: {', '.join(allowed_values)})"


def update_account_status(data: dict) -> dict:
    """Update account status with simple enum validation.

    Validates root-level enum fields: status and type.

    Args:
        data (dict): Account data with status, type, and account_id

    Returns:
        dict: Validation result with success status and details
    """
    result = {
        "success": True,
        "account_id": data.get("account_id", "Unknown"),
        "status": data.get("status"),
        "type": data.get("type"),
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }

    # Validate status enum
    status_valid, status_msg = validate_enum(
        data.get("status", ""),
        ["active", "inactive"],
        "status"
    )

    # Validate type enum
    type_valid, type_msg = validate_enum(
        data.get("type", ""),
        ["personal", "business"],
        "type"
    )

    if not status_valid or not type_valid:
        result["success"] = False
        result["error"] = "VALIDATION_ERROR"
        result["message"] = "Invalid enum value provided"

        if not status_valid:
            result["field"] = "status"
            result["provided_value"] = data.get("status")
            result["allowed_values"] = ["active", "inactive"]
        elif not type_valid:
            result["field"] = "type"
            result["provided_value"] = data.get("type")
            result["allowed_values"] = ["personal", "business"]
    else:
        result["message"] = "Account status updated successfully"
        result["validation_summary"] = f"All enum validations passed: {status_msg}, {type_msg}"

    return result


def create_customer_profile(data: dict) -> dict:
    """Create customer profile with nested enum validation.

    Validates nested enum fields: customer.type and customer.address.country.

    Args:
        data (dict): Customer profile data with nested customer object

    Returns:
        dict: Validation result with formatted customer information
    """
    customer = data.get("customer", {})
    address = customer.get("address", {})
    contact = customer.get("contact", {})

    result = {
        "success": True,
        "customer_id": data.get("customer_id", "Unknown"),
        "customer_name": customer.get("name", "Unknown"),
        "customer_email": customer.get("email", "Not provided"),
        "customer_type": customer.get("type"),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    # Validate customer type enum (level 1)
    type_valid, type_msg = validate_enum(
        customer.get("type", ""),
        ["individual", "corporate"],
        "type"
    )

    # Validate country enum (level 2)
    country_valid, country_msg = validate_enum(
        address.get("country", ""),
        ["US", "CA", "UK"],
        "country"
    )

    if not type_valid or not country_valid:
        result["success"] = False
        result["error"] = "VALIDATION_ERROR"
        result["message"] = "Invalid enum value in request"

        if not type_valid:
            result["field"] = "customer.type"
            result["provided_value"] = customer.get("type")
            result["allowed_values"] = ["individual", "corporate"]
        elif not country_valid:
            result["field"] = "customer.address.country"
            result["provided_value"] = address.get("country")
            result["allowed_values"] = ["US", "CA", "UK"]
    else:
        # Format address
        address_parts = [
            address.get("street", ""),
            address.get("city", ""),
            address.get("state", ""),
            address.get("zipcode", ""),
            address.get("country", "")
        ]
        result["address_formatted"] = ", ".join(
            [p for p in address_parts if p])
        result["country"] = address.get("country")
        result["contact_phone"] = contact.get("phone", "Not provided")
        result["contact_mobile"] = contact.get("mobile", "Not provided")
        result["message"] = "Customer profile created successfully"
        result["validation_summary"] = f"All enum validations passed: {type_msg}, {country_msg}"

    return result


def create_multi_level_enum_profile(data: dict) -> dict:
    """Create profile with multi-level enum validation.

    Validates enums at 4 levels:
    - Level 0: status (root)
    - Level 1: customer.type
    - Level 2: customer.address.country
    - Level 3: customer.contact.preference

    Args:
        data (dict): Profile data with nested structures

    Returns:
        dict: Comprehensive validation report with all enum checks
    """
    customer = data.get("customer", {})
    address = customer.get("address", {})
    contact = customer.get("contact", {})

    result = {
        "success": True,
        "profile_id": data.get("profile_id", "Unknown"),
        "profile_status": data.get("status"),
        "customer_name": customer.get("name", "Unknown"),
        "customer_email": customer.get("email", "Not provided"),
        "customer_type": customer.get("type"),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    # Validate all enum levels
    validations = []
    all_valid = True

    # Level 0: status
    status_valid, status_msg = validate_enum(
        data.get("status", ""),
        ["active", "inactive"],
        "status"
    )
    validations.append(("level_0_status", status_msg, status_valid,
                       0, "status", data.get("status"), ["active", "inactive"]))
    if not status_valid:
        all_valid = False

    # Level 1: customer.type
    type_valid, type_msg = validate_enum(
        customer.get("type", ""),
        ["individual", "corporate"],
        "customer_type"
    )
    validations.append(("level_1_customer_type", type_msg, type_valid, 1,
                       "customer.type", customer.get("type"), ["individual", "corporate"]))
    if not type_valid:
        all_valid = False

    # Level 2: address.country
    country_valid, country_msg = validate_enum(
        address.get("country", ""),
        ["US", "CA", "UK"],
        "address_country"
    )
    validations.append(("level_2_address_country", country_msg, country_valid,
                       2, "customer.address.country", address.get("country"), ["US", "CA", "UK"]))
    if not country_valid:
        all_valid = False

    # Level 3: contact.preference (if provided)
    preference = contact.get("preference")
    if preference:
        pref_valid, pref_msg = validate_enum(
            preference,
            ["email", "phone", "sms"],
            "contact_preference"
        )
        validations.append(("level_3_contact_preference", pref_msg, pref_valid, 3,
                           "customer.contact.preference", preference, ["email", "phone", "sms"]))
        if not pref_valid:
            all_valid = False

    if not all_valid:
        result["success"] = False
        result["error"] = "ENUM_VALIDATION_ERROR"
        result["message"] = "One or more enum validation failures detected"
        result["validation_failures"] = []

        for level_name, msg, is_valid, level, field_path, value, allowed in validations:
            if not is_valid:
                result["validation_failures"].append({
                    "field_path": field_path,
                    "provided_value": value,
                    "allowed_values": allowed,
                    "nesting_level": level
                })
    else:
        # Format address
        address_parts = [
            address.get("street", ""),
            address.get("city", ""),
            address.get("state", ""),
            address.get("zipcode", ""),
            address.get("country", "")
        ]
        result["address_formatted"] = ", ".join(
            [p for p in address_parts if p])
        result["country"] = address.get("country")
        result["contact_phone"] = contact.get("phone", "Not provided")
        result["contact_preference"] = contact.get(
            "preference", "Not specified")
        result["contact_timezone"] = contact.get("timezone", "Not specified")
        result["message"] = "Profile created with all enum validations passed"

        # Build enum validation report
        result["enum_validation_report"] = {
            "total_enum_fields": len(validations),
            "all_valid": True
        }

        for level_name, msg, is_valid, level, field_path, value, allowed in validations:
            result["enum_validation_report"][level_name] = msg

    return result


if __name__ == '__main__':
    print("="*70)
    print("Enum Nested Schemas Validation Demo")
    print("="*70)

    # Test 1: Simple enum validation
    print("\n" + "="*70)
    print("Test 1: Simple Enum Validation (Account Status)")
    print("="*70)

    account_data = {
        "status": "active",
        "type": "personal",
        "account_id": "ACC-12345"
    }

    result1 = update_account_status(account_data)
    print(f"\nResult: {result1['message']}")
    print(f"Account ID: {result1['account_id']}")
    print(f"Status: {result1['status']}")
    print(f"Type: {result1['type']}")
    print(f"Validation: {result1.get('validation_summary', 'N/A')}")

    # Test 2: Nested enum validation
    print("\n" + "="*70)
    print("Test 2: Nested Enum Validation (Customer Profile)")
    print("="*70)

    customer_data = {
        "customer_id": "CUST-001",
        "customer": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "type": "individual",
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zipcode": "10001",
                "country": "US"
            },
            "contact": {
                "phone": "+1-555-0100",
                "mobile": "+1-555-0101"
            }
        }
    }

    result2 = create_customer_profile(customer_data)
    print(f"\nResult: {result2['message']}")
    print(f"Customer: {result2['customer_name']} ({result2['customer_type']})")
    print(f"Email: {result2['customer_email']}")
    print(f"Address: {result2.get('address_formatted', 'N/A')}")
    print(f"Validation: {result2.get('validation_summary', 'N/A')}")

    # Test 3: Multi-level enum validation
    print("\n" + "="*70)
    print("Test 3: Multi-Level Enum Validation")
    print("="*70)

    profile_data = {
        "profile_id": "PROF-001",
        "status": "active",
        "customer": {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "type": "individual",
            "address": {
                "street": "321 Oak Ave",
                "city": "Seattle",
                "state": "WA",
                "zipcode": "98101",
                "country": "US"
            },
            "contact": {
                "phone": "+1-206-555-0300",
                "preference": "email",
                "timezone": "PST"
            }
        }
    }

    result3 = create_multi_level_enum_profile(profile_data)
    print(f"\nResult: {result3['message']}")
    print(f"Profile ID: {result3['profile_id']}")
    print(f"Status: {result3['profile_status']}")
    print(f"Customer: {result3['customer_name']} ({result3['customer_type']})")
    print(f"Address: {result3.get('address_formatted', 'N/A')}")
    print(f"Contact Preference: {result3.get('contact_preference', 'N/A')}")

    if 'enum_validation_report' in result3:
        print(f"\nEnum Validation Report:")
        report = result3['enum_validation_report']
        print(f"  Total Enum Fields: {report['total_enum_fields']}")
        print(f"  All Valid: {report['all_valid']}")
        for key, value in report.items():
            if key.startswith('level_'):
                print(f"  {key}: {value}")

    # Test 4: Invalid enum value
    print("\n" + "="*70)
    print("Test 4: Invalid Enum Value (Should Fail)")
    print("="*70)

    invalid_data = {
        "status": "pending",  # Invalid
        "type": "personal",
        "account_id": "ACC-99999"
    }

    result4 = update_account_status(invalid_data)
    print(f"\nResult: {result4.get('message', 'Error')}")
    if not result4['success']:
        print(f"Error: {result4.get('error')}")
        print(f"Field: {result4.get('field')}")
        print(f"Provided Value: {result4.get('provided_value')}")
        print(f"Allowed Values: {result4.get('allowed_values')}")

# Made with Bob - Enum validation tool
