"""
Python tool using Pydantic models for nested reference schema validation.
Based on openapi_nested_reference_test.yaml

This demonstrates the nested reference pattern from GitHub Issue #45755 where:
- shipping_locations.address references customer.address structure
- delivery_address in items references the same address structure
- Similar to how alerts.address referenced inquiry.address in Moody's MCP tools
"""
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class EntityType(str, Enum):
    """Entity type enumeration"""
    INDIVIDUAL = "INDIVIDUAL"
    BUSINESS = "BUSINESS"


class Contact(BaseModel):
    """Contact information model"""
    phone: Optional[str] = Field(None, description="Primary phone number")
    mobile: Optional[str] = Field(None, description="Mobile phone number")


class Address(BaseModel):
    """Address structure used by customer, order, and shipping locations"""
    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State or province")
    zipcode: Optional[str] = Field(None, description="Postal code")
    country: Optional[str] = Field(None, description="Country name")


class ProductSpecifications(BaseModel):
    """Product specifications model"""
    weight: Optional[str] = Field(None, description="Product weight")
    dimensions: Optional[str] = Field(None, description="Product dimensions")
    material: Optional[str] = Field(None, description="Product material")


class ProductDetails(BaseModel):
    """Product details model"""
    description: Optional[str] = Field(None, description="Product description")
    specifications: Optional[ProductSpecifications] = Field(
        None, description="Product specifications")


class Product(BaseModel):
    """Product model"""
    product_id: Optional[str] = Field(None, description="Product identifier")
    name: str = Field(..., description="Product name")
    details: Optional[ProductDetails] = Field(
        None, description="Product details")


class OrderItem(BaseModel):
    """Order item model with delivery addresses"""
    product: Product = Field(..., description="Product information")
    quantity: int = Field(..., ge=1,
                          description="Quantity ordered (minimum 1)")
    price: float = Field(..., ge=0, description="Unit price (minimum 0)")
    delivery_address: Optional[List[Address]] = Field(
        None,
        description="Delivery addresses for this item (references customer.address structure)"
    )


class LocationContact(BaseModel):
    """Location contact information"""
    phone: Optional[str] = Field(None, description="Location phone number")
    email: Optional[EmailStr] = Field(
        None, description="Location email address")


class ShippingLocation(BaseModel):
    """Shipping location with address referencing customer.address structure"""
    location_id: str = Field(..., description="Location identifier")
    location_name: str = Field(..., description="Name of the location")
    address: Optional[List[Address]] = Field(
        None,
        description="Address array that references customer.address structure (mimics $ref pattern)"
    )
    entityType: str = Field(..., description="Type of location entity")
    contact: Optional[LocationContact] = Field(
        None, description="Location contact information")


class Order(BaseModel):
    """Order model with nested references"""
    order_id: str = Field(..., description="Unique order identifier")
    order_date: Optional[str] = Field(
        None, description="Order date (YYYY-MM-DD format)")
    items: Optional[List[OrderItem]] = Field(
        None, description="List of order items with delivery addresses")
    shipping_address: Optional[Address] = Field(
        None, description="Shipping address")
    billing_address: Optional[Address] = Field(
        None, description="Billing address")
    shipping_locations: Optional[List[ShippingLocation]] = Field(
        None,
        description="Array of shipping locations with address field referencing customer.address"
    )


class Customer(BaseModel):
    """Customer model with primary address"""
    name: str = Field(..., description="Customer full name")
    email: Optional[EmailStr] = Field(
        None, description="Customer email address")
    address: Optional[Address] = Field(
        None, description="Primary customer address (referenced by other fields)")
    contact: Optional[Contact] = Field(
        None, description="Customer contact information")
    entityType: EntityType = Field(..., description="Type of customer entity")
    customerId: Optional[str] = Field(
        None, description="Unique customer identifier")


class OrderRequestWithReferences(BaseModel):
    """
    Main order request model demonstrating nested reference pattern.

    This recreates the scenario from GitHub Issue #45755 where:
    - order.shipping_locations.address references customer.address
    - order.items.delivery_address references customer.address
    - Similar to alerts.address referencing inquiry.address in Moody's tools
    """
    customer: Customer = Field(...,
                               description="Customer information with primary address")
    order: Order = Field(...,
                         description="Order details with nested references")


@tool(permission=ToolPermission.WRITE_ONLY)
def process_customer_order_with_references(order_request: OrderRequestWithReferences) -> str:
    """
    Process customer order with nested address references.

    This function demonstrates the nested reference pattern from GitHub Issue #45755:
    - shipping_locations.address references customer.address structure
    - delivery_address in items references the same address structure
    - Tests serialization and execution behavior with complex nested references

    :param order_request: Order request with customer and order details
    :return: Formatted order confirmation message
    """
    # Extract customer information
    customer_name = order_request.customer.name
    customer_email = order_request.customer.email or "N/A"
    customer_entity = order_request.customer.entityType.value
    customer_id = order_request.customer.customerId or "N/A"

    # Format customer address
    customer_address = "N/A"
    if order_request.customer.address:
        addr = order_request.customer.address
        parts = [addr.street, addr.city,
                 addr.state, addr.zipcode, addr.country]
        customer_address = ", ".join(filter(None, parts))

    # Extract contact information
    phone = "N/A"
    mobile = "N/A"
    if order_request.customer.contact:
        phone = order_request.customer.contact.phone or "N/A"
        mobile = order_request.customer.contact.mobile or "N/A"

    # Extract order information
    order_id = order_request.order.order_id
    order_date = order_request.order.order_date or "N/A"

    # Process items
    total_items = 0
    total_amount = 0.0
    items_summary = []

    if order_request.order.items:
        for item in order_request.order.items:
            subtotal = item.quantity * item.price
            total_amount += subtotal
            total_items += item.quantity

            # Get product specifications
            specs = "N/A"
            if item.product.details and item.product.details.specifications:
                spec = item.product.details.specifications
                spec_parts = [spec.weight, spec.dimensions, spec.material]
                specs = ", ".join(filter(None, spec_parts))

            # Count delivery addresses
            delivery_addr_count = len(
                item.delivery_address) if item.delivery_address else 0

            items_summary.append(
                f"  - {item.product.name} (ID: {item.product.product_id or 'N/A'})\n"
                f"    Qty: {item.quantity}, Price: ${item.price:.2f}, Subtotal: ${subtotal:.2f}\n"
                f"    Specs: {specs}\n"
                f"    Delivery Addresses: {delivery_addr_count}"
            )

    # Format shipping address
    shipping_address = "N/A"
    if order_request.order.shipping_address:
        addr = order_request.order.shipping_address
        parts = [addr.street, addr.city,
                 addr.state, addr.zipcode, addr.country]
        shipping_address = ", ".join(filter(None, parts))

    # Format billing address
    billing_address = "N/A"
    if order_request.order.billing_address:
        addr = order_request.order.billing_address
        parts = [addr.street, addr.city,
                 addr.state, addr.zipcode, addr.country]
        billing_address = ", ".join(filter(None, parts))

    # Process shipping locations
    shipping_locations_count = 0
    shipping_locations_summary = []
    if order_request.order.shipping_locations:
        shipping_locations_count = len(order_request.order.shipping_locations)
        for loc in order_request.order.shipping_locations:
            addr_count = len(loc.address) if loc.address else 0
            contact_info = "N/A"
            if loc.contact:
                contact_parts = [loc.contact.phone, loc.contact.email]
                contact_info = ", ".join(filter(None, contact_parts))

            shipping_locations_summary.append(
                f"  - {loc.location_name} (ID: {loc.location_id})\n"
                f"    Type: {loc.entityType}, Addresses: {addr_count}\n"
                f"    Contact: {contact_info}"
            )

    # Build confirmation message
    confirmation = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        ORDER CONFIRMATION                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

ORDER DETAILS:
  Order ID: {order_id}
  Order Date: {order_date}
  Status: CONFIRMED

CUSTOMER INFORMATION:
  Name: {customer_name}
  Email: {customer_email}
  Entity Type: {customer_entity}
  Customer ID: {customer_id}
  Address: {customer_address}
  Phone: {phone}
  Mobile: {mobile}

ORDER ITEMS ({total_items} item(s)):
{chr(10).join(items_summary) if items_summary else "  No items"}

SHIPPING INFORMATION:
  Shipping Address: {shipping_address}
  Billing Address: {billing_address}
  Shipping Locations: {shipping_locations_count}

{chr(10).join(shipping_locations_summary) if shipping_locations_summary else ""}

ORDER SUMMARY:
  Total Items: {total_items}
  Total Amount: ${total_amount:.2f}

CONFIRMATION MESSAGE:
  Order {order_id} confirmed for {customer_name}

╔══════════════════════════════════════════════════════════════════════════════╗
║  Thank you for your order! Your order is being processed.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    return confirmation.strip()


if __name__ == '__main__':
    # Example 1: Complete order with all nested references
    print("=" * 80)
    print("Example 1: Complete order with nested address references")
    print("=" * 80)

    order_request = OrderRequestWithReferences(
        customer=Customer(
            name="Jane Smith",
            email="jane.smith@email.com",
            address=Address(
                street="456 Oak Avenue",
                city="New York",
                state="NY",
                zipcode="10001",
                country="USA"
            ),
            contact=Contact(
                phone="+1-555-0200",
                mobile="+1-555-0201"
            ),
            entityType=EntityType.INDIVIDUAL,
            customerId="CUST-001"
        ),
        order=Order(
            order_id="ORD-2024-002",
            order_date="2024-01-16",
            items=[
                OrderItem(
                    product=Product(
                        product_id="PROD-001",
                        name="Premium Laptop",
                        details=ProductDetails(
                            description="High-performance laptop for professionals",
                            specifications=ProductSpecifications(
                                weight="1.5 kg",
                                dimensions="35cm x 25cm x 2cm",
                                material="Aluminum alloy"
                            )
                        )
                    ),
                    quantity=1,
                    price=1299.99,
                    delivery_address=[
                        Address(
                            street="456 Oak Avenue",
                            city="New York",
                            state="NY",
                            zipcode="10001",
                            country="USA"
                        )
                    ]
                )
            ],
            shipping_address=Address(
                street="456 Oak Avenue",
                city="New York",
                state="NY",
                zipcode="10001",
                country="USA"
            ),
            billing_address=Address(
                street="789 Pine Street",
                city="New York",
                state="NY",
                zipcode="10002",
                country="USA"
            ),
            shipping_locations=[
                ShippingLocation(
                    location_id="LOC-001",
                    location_name="Primary Warehouse",
                    address=[
                        Address(
                            street="456 Oak Avenue",
                            city="New York",
                            state="NY",
                            zipcode="10001",
                            country="USA"
                        )
                    ],
                    entityType="WAREHOUSE",
                    contact=LocationContact(
                        phone="+1-555-0300",
                        email="warehouse@example.com"
                    )
                )
            ]
        )
    )

    result = process_customer_order_with_references(order_request)
    print(result)

    # Example 2: Minimal valid order
    print("\n" + "=" * 80)
    print("Example 2: Minimal valid order")
    print("=" * 80)

    minimal_order = OrderRequestWithReferences(
        customer=Customer(
            name="Bob Johnson",
            entityType=EntityType.BUSINESS
        ),
        order=Order(
            order_id="ORD-2024-003"
        )
    )

    result = process_customer_order_with_references(minimal_order)
    print(result)

# Made with Bob
