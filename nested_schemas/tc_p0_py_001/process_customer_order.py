"""Customer Order Processing System - Handle orders with nested customer and product data

REAL-TIME TOOL:
===============
This tool processes customer orders with comprehensive nested information including
customer details, shipping/billing addresses, and product specifications. It handles
complex nested structures and schema references for real-world e-commerce scenarios.

PURPOSE:
--------
- Process customer orders with complete information
- Manage customer profiles with addresses
- Track order items with detailed product specifications
- Handle shipping and billing addresses
- Return user-friendly order confirmations

USAGE:
------
Input: Customer order with personal info, address, and product details
Output: Clean, formatted order confirmation with all details
"""

from typing import Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


@tool(permission=ToolPermission.READ_ONLY)
def process_customer_order(order_data: dict) -> dict:
    """Process customer order and return a formatted order confirmation.

    This tool processes customer orders including customer information, shipping and billing
    addresses, and product details with specifications. It handles nested data structures
    and returns a user-friendly order confirmation.

    Provide customer name, email, address, order ID, and product details including specifications
    like weight, dimensions, and material. The tool will create a complete order confirmation.

    Args:
        order_data (dict): Order information with customer details (name, email, address with street/city/state/zipcode/country), order details (order_id, items with product specifications), and shipping/billing addresses.

    Returns:
        dict: Formatted order confirmation with customer info, order summary, shipping details, and product information in user-friendly format.
    """
    result = {}

    # Extract customer information
    customer = order_data.get("customer", {})
    result["customer_name"] = customer.get("name", "Unknown")
    result["customer_email"] = customer.get("email", "Not provided")

    # Format customer address
    address = customer.get("address", {})
    if address:
        address_parts = [
            address.get("street", ""),
            address.get("city", ""),
            address.get("state", ""),
            address.get("zipcode", ""),
            address.get("country", "")
        ]
        result["customer_address"] = ", ".join([p for p in address_parts if p])
    else:
        result["customer_address"] = "Not provided"

    # Extract contact info
    contact = customer.get("contact", {})
    result["phone"] = contact.get("phone", "Not provided")
    result["mobile"] = contact.get("mobile", "Not provided")

    # Extract order information
    order = order_data.get("order", {})
    result["order_id"] = order.get("order_id", "Unknown")
    result["order_date"] = order.get("order_date", "Not specified")

    # Process order items
    items = order.get("items", [])
    result["items"] = []
    result["total_items"] = len(items)
    result["total_amount"] = 0.0

    for item in items:
        product = item.get("product", {})
        details = product.get("details", {})
        specs = details.get("specifications", {})

        item_info = {
            "product_name": product.get("name", "Unknown Product"),
            "product_id": product.get("product_id", ""),
            "description": details.get("description", ""),
            "quantity": item.get("quantity", 1),
            "price": item.get("price", 0.0),
            "subtotal": item.get("quantity", 1) * item.get("price", 0.0)
        }

        # Add specifications if available
        if specs:
            item_info["specifications"] = f"{specs.get('weight', '')}, {specs.get('dimensions', '')}, {specs.get('material', '')}"

        result["items"].append(item_info)
        result["total_amount"] += item_info["subtotal"]

    # Format shipping address
    shipping = order.get("shipping_address", {})
    if shipping:
        shipping_parts = [
            shipping.get("street", ""),
            shipping.get("city", ""),
            shipping.get("state", ""),
            shipping.get("zipcode", ""),
            shipping.get("country", "")
        ]
        result["shipping_address"] = ", ".join(
            [p for p in shipping_parts if p])
    else:
        result["shipping_address"] = result["customer_address"]

    # Format billing address
    billing = order.get("billing_address", {})
    if billing:
        billing_parts = [
            billing.get("street", ""),
            billing.get("city", ""),
            billing.get("state", ""),
            billing.get("zipcode", ""),
            billing.get("country", "")
        ]
        result["billing_address"] = ", ".join([p for p in billing_parts if p])
    else:
        result["billing_address"] = result["customer_address"]

    # Create confirmation message
    result["confirmation_message"] = f"Order {result['order_id']} confirmed for {result['customer_name']}"
    result["order_summary"] = f"{result['total_items']} item(s), Total: ${result['total_amount']:.2f}"

    return result


if __name__ == '__main__':
    # Demo: Process customer order
    print("="*70)
    print("Customer Order Processing Demo")
    print("="*70)

    order = {
        "customer": {
            "name": "Jane Smith",
            "email": "jane.smith@email.com",
            "address": {
                "street": "456 Oak Avenue",
                "city": "New York",
                "state": "NY",
                "zipcode": "10001",
                "country": "USA"
            },
            "contact": {
                "phone": "+1-555-0200",
                "mobile": "+1-555-0201"
            }
        },
        "order": {
            "order_id": "ORD-2024-002",
            "order_date": "2024-01-16",
            "items": [
                {
                    "product": {
                        "product_id": "PROD-001",
                        "name": "Premium Laptop",
                        "details": {
                            "description": "High-performance laptop for professionals",
                            "specifications": {
                                "weight": "1.5 kg",
                                "dimensions": "35cm x 25cm x 2cm",
                                "material": "Aluminum alloy"
                            }
                        }
                    },
                    "quantity": 1,
                    "price": 1299.99
                }
            ],
            "shipping_address": {
                "street": "456 Oak Avenue",
                "city": "New York",
                "state": "NY",
                "zipcode": "10001",
                "country": "USA"
            },
            "billing_address": {
                "street": "789 Pine Street",
                "city": "New York",
                "state": "NY",
                "zipcode": "10002",
                "country": "USA"
            }
        }
    }

    result = process_customer_order(order)

    print(f"\n{result['confirmation_message']}")
    print(f"\nCustomer Information:")
    print(f"  Name: {result['customer_name']}")
    print(f"  Email: {result['customer_email']}")
    print(f"  Phone: {result['phone']}")
    print(f"  Address: {result['customer_address']}")

    print(f"\nOrder Details:")
    print(f"  Order ID: {result['order_id']}")
    print(f"  Order Date: {result['order_date']}")
    print(f"  {result['order_summary']}")

    print(f"\nItems:")
    for item in result['items']:
        print(f"  - {item['product_name']} (ID: {item['product_id']})")
        print(f"    {item['description']}")
        print(f"    Specs: {item.get('specifications', 'N/A')}")
        print(
            f"    Quantity: {item['quantity']} x ${item['price']:.2f} = ${item['subtotal']:.2f}")

    print(f"\nShipping Address:")
    print(f"  {result['shipping_address']}")

    print(f"\nBilling Address:")
    print(f"  {result['billing_address']}")

    print(f"\nTotal Amount: ${result['total_amount']:.2f}")

# Made with Bob - Real-world order processing tool
