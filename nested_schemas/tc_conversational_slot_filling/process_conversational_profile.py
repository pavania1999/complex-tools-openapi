"""Conversational Multi-Field Slot Filling System - Build profiles incrementally

REAL-TIME TOOL:
===============
This tool manages conversational profile building across multiple turns, tracking
completeness, providing contextual prompts, and supporting partial updates without
overwriting existing data.

PURPOSE:
--------
- Start profile sessions with minimal data
- Incrementally collect fields across multiple turns
- Track completeness percentage
- Identify missing required and optional fields
- Provide contextual next-step prompts
- Merge partial updates intelligently

USAGE:
------
Input: Incremental profile data across multiple conversation turns
Output: Session state with completeness tracking and smart prompts
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid


# In-memory session storage (in production, use a database)
SESSIONS = {}


def calculate_completeness(profile: dict) -> tuple:
    """Calculate profile completeness percentage and identify missing fields.

    Args:
        profile: Current profile state

    Returns:
        Tuple of (percentage, missing_required, missing_optional)
    """
    required_fields = [
        "name",
        "email",
        "type",
        "address.street",
        "address.city",
        "address.country"
    ]

    optional_fields = [
        "address.state",
        "address.zipcode",
        "contact.phone",
        "contact.mobile"
    ]

    def has_field(data: dict, field_path: str) -> bool:
        """Check if nested field exists and has a value."""
        parts = field_path.split('.')
        current = data
        for part in parts:
            if isinstance(current, dict) and part in current and current[part]:
                current = current[part]
            else:
                return False
        return True

    # Check required fields
    missing_required = [
        f for f in required_fields if not has_field(profile, f)]

    # Check optional fields
    missing_optional = [
        f for f in optional_fields if not has_field(profile, f)]

    # Calculate percentage
    total_fields = len(required_fields) + len(optional_fields)
    completed_fields = total_fields - \
        len(missing_required) - len(missing_optional)
    percentage = int((completed_fields / total_fields) * 100)

    return percentage, missing_required, missing_optional


def get_next_prompt(missing_required: List[str], missing_optional: List[str]) -> str:
    """Generate contextual prompt for next field to collect.

    Args:
        missing_required: List of missing required fields
        missing_optional: List of missing optional fields

    Returns:
        Contextual prompt string
    """
    if not missing_required and not missing_optional:
        return "Profile complete! Ready to submit?"

    if missing_required:
        field = missing_required[0]
        prompts = {
            "name": "What's your name?",
            "email": "Great! What's your email address?",
            "type": "Are you an individual or corporate customer?",
            "address.street": "What's your street address?",
            "address.city": "Which city are you in?",
            "address.country": "Which country are you in? (US, CA, or UK)"
        }
        return prompts.get(field, f"Please provide: {field}")

    if missing_optional:
        return "Would you like to add contact information? (optional)"

    return "Profile complete! Ready to submit?"


def merge_profile_data(existing: dict, updates: dict) -> dict:
    """Intelligently merge profile updates without overwriting existing data.

    Args:
        existing: Current profile state
        updates: New data to merge

    Returns:
        Merged profile
    """
    result = existing.copy()

    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = merge_profile_data(result[key], value)
        else:
            # Update or add new field
            result[key] = value

    return result


def start_profile_session(data: dict) -> dict:
    """Start a new conversational profile creation session.

    Args:
        data (dict): Initial data with at least a name

    Returns:
        dict: Session response with session_id and initial state
    """
    session_id = f"SESSION-{str(uuid.uuid4())[:8].upper()}"

    profile = {
        "name": data.get("name", "Unknown")
    }

    percentage, missing_required, missing_optional = calculate_completeness(
        profile)
    next_prompt = get_next_prompt(missing_required, missing_optional)

    session = {
        "session_id": session_id,
        "status": "in_progress",
        "profile": profile,
        "conversation_turn": 1,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }

    SESSIONS[session_id] = session

    return {
        "session_id": session_id,
        "status": "in_progress",
        "completeness_percentage": percentage,
        "profile": profile,
        "missing_required_fields": missing_required,
        "missing_optional_fields": missing_optional,
        "next_prompt": next_prompt,
        "conversation_turn": 1,
        "created_at": session["created_at"]
    }


def update_profile_session(session_id: str, updates: dict) -> dict:
    """Update profile with additional information incrementally.

    Args:
        session_id (str): Session identifier
        updates (dict): New fields to add or update

    Returns:
        dict: Updated session response
    """
    if session_id not in SESSIONS:
        return {
            "error": "SESSION_NOT_FOUND",
            "message": f"Session {session_id} not found"
        }

    session = SESSIONS[session_id]

    # Merge updates into existing profile
    session["profile"] = merge_profile_data(session["profile"], updates)
    session["conversation_turn"] += 1
    session["updated_at"] = datetime.utcnow().isoformat() + "Z"

    # Calculate new completeness
    percentage, missing_required, missing_optional = calculate_completeness(
        session["profile"])
    next_prompt = get_next_prompt(missing_required, missing_optional)

    # Update status if complete
    if not missing_required:
        session["status"] = "complete"

    return {
        "session_id": session_id,
        "status": session["status"],
        "completeness_percentage": percentage,
        "profile": session["profile"],
        "missing_required_fields": missing_required,
        "missing_optional_fields": missing_optional,
        "next_prompt": next_prompt,
        "conversation_turn": session["conversation_turn"],
        "updated_at": session["updated_at"]
    }


def finalize_profile_session(session_id: str) -> dict:
    """Finalize and submit the complete profile.

    Args:
        session_id (str): Session identifier

    Returns:
        dict: Finalized profile response
    """
    if session_id not in SESSIONS:
        return {
            "error": "SESSION_NOT_FOUND",
            "message": f"Session {session_id} not found"
        }

    session = SESSIONS[session_id]
    profile = session["profile"]

    # Check completeness
    percentage, missing_required, missing_optional = calculate_completeness(
        profile)

    if missing_required:
        return {
            "error": "VALIDATION_ERROR",
            "message": "Profile incomplete - missing required fields",
            "missing_fields": missing_required,
            "session_id": session_id
        }

    # Generate profile ID
    profile_id = f"PROF-{str(uuid.uuid4())[:8].upper()}"

    # Format address
    address = profile.get("address", {})
    address_parts = [
        address.get("street", ""),
        address.get("city", ""),
        address.get("state", ""),
        address.get("zipcode", ""),
        address.get("country", "")
    ]
    address_formatted = ", ".join([p for p in address_parts if p])

    # Calculate time to complete
    created = datetime.fromisoformat(
        session["created_at"].replace("Z", "+00:00"))
    updated = datetime.fromisoformat(
        session["updated_at"].replace("Z", "+00:00"))
    time_diff = updated - created
    minutes = int(time_diff.total_seconds() / 60)

    # Count fields collected
    fields_collected = 0
    for key, value in profile.items():
        if isinstance(value, dict):
            fields_collected += len([v for v in value.values() if v])
        elif value:
            fields_collected += 1

    contact = profile.get("contact", {})

    result = {
        "success": True,
        "message": "Profile finalized and submitted successfully",
        "profile_id": profile_id,
        "customer_name": profile.get("name", "Unknown"),
        "customer_email": profile.get("email", "Not provided"),
        "customer_type": profile.get("type", "Not specified"),
        "address_formatted": address_formatted,
        "contact_phone": contact.get("phone", "Not provided"),
        "contact_mobile": contact.get("mobile", "Not provided"),
        "conversation_summary": {
            "total_turns": session["conversation_turn"],
            "fields_collected": fields_collected,
            "time_to_complete": f"{minutes} minute{'s' if minutes != 1 else ''}"
        },
        "finalized_at": datetime.utcnow().isoformat() + "Z"
    }

    # Clean up session
    del SESSIONS[session_id]

    return result


def get_session_status(session_id: str) -> dict:
    """Get current session status.

    Args:
        session_id (str): Session identifier

    Returns:
        dict: Current session state
    """
    if session_id not in SESSIONS:
        return {
            "error": "SESSION_NOT_FOUND",
            "message": f"Session {session_id} not found"
        }

    session = SESSIONS[session_id]
    percentage, missing_required, missing_optional = calculate_completeness(
        session["profile"])
    next_prompt = get_next_prompt(missing_required, missing_optional)

    return {
        "session_id": session_id,
        "status": session["status"],
        "completeness_percentage": percentage,
        "profile": session["profile"],
        "missing_required_fields": missing_required,
        "missing_optional_fields": missing_optional,
        "next_prompt": next_prompt,
        "conversation_turn": session["conversation_turn"],
        "created_at": session["created_at"],
        "updated_at": session["updated_at"]
    }


if __name__ == '__main__':
    print("="*70)
    print("Conversational Multi-Field Slot Filling Demo")
    print("="*70)

    # Turn 1: Start session
    print("\n" + "="*70)
    print("Turn 1: Start Session with Name")
    print("="*70)

    result1 = start_profile_session({"name": "John Doe"})
    print(f"\nSession ID: {result1['session_id']}")
    print(f"Status: {result1['status']}")
    print(f"Completeness: {result1['completeness_percentage']}%")
    print(f"Profile: {result1['profile']}")
    print(f"Missing Required: {result1['missing_required_fields']}")
    print(f"Next Prompt: {result1['next_prompt']}")

    session_id = result1['session_id']

    # Turn 2: Add email and type
    print("\n" + "="*70)
    print("Turn 2: Add Email and Type")
    print("="*70)

    result2 = update_profile_session(session_id, {
        "email": "john.doe@example.com",
        "type": "individual"
    })
    print(f"\nCompleteness: {result2['completeness_percentage']}%")
    print(f"Profile: {result2['profile']}")
    print(f"Missing Required: {result2['missing_required_fields']}")
    print(f"Next Prompt: {result2['next_prompt']}")

    # Turn 3: Add partial address
    print("\n" + "="*70)
    print("Turn 3: Add Partial Address")
    print("="*70)

    result3 = update_profile_session(session_id, {
        "address": {
            "street": "123 Main St",
            "city": "New York"
        }
    })
    print(f"\nCompleteness: {result3['completeness_percentage']}%")
    print(f"Profile: {result3['profile']}")
    print(f"Missing Required: {result3['missing_required_fields']}")
    print(f"Next Prompt: {result3['next_prompt']}")

    # Turn 4: Complete address
    print("\n" + "="*70)
    print("Turn 4: Complete Address")
    print("="*70)

    result4 = update_profile_session(session_id, {
        "address": {
            "state": "NY",
            "zipcode": "10001",
            "country": "US"
        }
    })
    print(f"\nCompleteness: {result4['completeness_percentage']}%")
    print(f"Status: {result4['status']}")
    print(f"Profile: {result4['profile']}")
    print(f"Missing Required: {result4['missing_required_fields']}")
    print(f"Next Prompt: {result4['next_prompt']}")

    # Turn 5: Add contact (optional)
    print("\n" + "="*70)
    print("Turn 5: Add Contact Information")
    print("="*70)

    result5 = update_profile_session(session_id, {
        "contact": {
            "phone": "+1-555-0100",
            "mobile": "+1-555-0101"
        }
    })
    print(f"\nCompleteness: {result5['completeness_percentage']}%")
    print(f"Status: {result5['status']}")
    print(f"Profile: {result5['profile']}")
    print(f"Missing Fields: {result5['missing_required_fields']}")
    print(f"Next Prompt: {result5['next_prompt']}")

    # Turn 6: Finalize
    print("\n" + "="*70)
    print("Turn 6: Finalize Profile")
    print("="*70)

    result6 = finalize_profile_session(session_id)
    print(f"\nSuccess: {result6['success']}")
    print(f"Message: {result6['message']}")
    print(f"Profile ID: {result6['profile_id']}")
    print(f"Customer: {result6['customer_name']} ({result6['customer_type']})")
    print(f"Email: {result6['customer_email']}")
    print(f"Address: {result6['address_formatted']}")
    print(f"Phone: {result6['contact_phone']}")
    print(f"\nConversation Summary:")
    summary = result6['conversation_summary']
    print(f"  Total Turns: {summary['total_turns']}")
    print(f"  Fields Collected: {summary['fields_collected']}")
    print(f"  Time to Complete: {summary['time_to_complete']}")

# Made with Bob - Conversational profile building tool
