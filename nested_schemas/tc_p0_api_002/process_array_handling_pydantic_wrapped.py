"""
Python tool using Pydantic models for wrapped array handling.
Based on openapi_array_handling_wrapped.yaml

This demonstrates wrapped array patterns where:
- Arrays are wrapped in object properties (e.g., "items", "orders")
- Compatible with react-intrinsic style
- Proper structure for Watson Orchestrate tools
"""
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class CategoryEnum(str, Enum):
    """Item category enumeration"""
    ELECTRONICS = "Electronics"
    ACCESSORIES = "Accessories"
    FURNITURE = "Furniture"
    OFFICE_SUPPLIES = "Office Supplies"


class Specifications(BaseModel):
    """Product specifications model"""
    brand: Optional[str] = Field(None, description="Brand name")
    model: Optional[str] = Field(None, description="Model number")
    warranty: Optional[str] = Field(None, description="Warranty period")


class InventoryItem(BaseModel):
    """Inventory item model"""
    name: str = Field(..., description="Item name",
                      min_length=1, max_length=200)
    sku: str = Field(..., description="Stock Keeping Unit",
                     pattern=r'^[A-Z]{3}-[0-9]{3}$')
    quantity: int = Field(..., description="Quantity in stock", ge=0, le=10000)
    price: float = Field(..., description="Unit price", gt=0)
    category: Optional[CategoryEnum] = Field(None, description="Item category")
    specifications: Optional[Specifications] = Field(
        None, description="Nested specifications object")


class InventoryRequest(BaseModel):
    """Wrapped inventory request model"""
    items: List[InventoryItem] = Field(
        ...,
        description="List of inventory items to process (WRAPPED ARRAY - CORRECT)",
        min_items=1,
        max_items=100
    )


class OrderItem(BaseModel):
    """Order item model"""
    product_name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Quantity ordered", ge=1)
    unit_price: float = Field(..., description="Unit price", ge=0)


class Order(BaseModel):
    """Order model with nested items array"""
    order_id: str = Field(..., description="Unique order identifier")
    customer_name: str = Field(..., description="Customer name")
    items: List[OrderItem] = Field(
        ...,
        description="Order items (NESTED WRAPPED ARRAY - CORRECT)",
        min_items=1
    )


class BatchOrderRequest(BaseModel):
    """Wrapped batch order request model"""
    orders: List[Order] = Field(
        ...,
        description="List of orders to process (WRAPPED ARRAY - CORRECT)",
        min_items=1
    )


@tool(permission=ToolPermission.WRITE_ONLY)
def process_inventory_items_wrapped(inventory_request: InventoryRequest) -> str:
    """
    Process inventory items with wrapped array structure.

    This function demonstrates the CORRECT way to handle arrays:
    - Arrays are wrapped in an object property (e.g., "items")
    - Each item can have nested objects (e.g., "specifications")
    - Compatible with react-intrinsic style

    :param inventory_request: Request with wrapped items array
    :return: Formatted processing result
    """
    items = inventory_request.items

    if not items:
        return "No items provided for processing."

    processed_items = []
    total_value = 0.0

    for idx, item in enumerate(items):
        # Calculate item value
        item_value = item.quantity * item.price
        total_value += item_value

        # Extract specifications
        specs_info = "N/A"
        if item.specifications:
            spec_parts = [
                item.specifications.brand,
                item.specifications.model,
                item.specifications.warranty
            ]
            specs_info = ", ".join(filter(None, spec_parts))

        processed_items.append(
            f"  [{idx + 1}] {item.name} (SKU: {item.sku})\n"
            f"      Category: {item.category.value if item.category else 'N/A'}\n"
            f"      Quantity: {item.quantity}, Price: ${item.price:.2f}\n"
            f"      Item Value: ${item_value:.2f}\n"
            f"      Specifications: {specs_info}"
        )

    # Build result message
    result = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    INVENTORY PROCESSING RESULT (WRAPPED)                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

STATUS: SUCCESS
MESSAGE: Successfully processed {len(items)} inventory items

PROCESSED ITEMS:
{chr(10).join(processed_items)}

SUMMARY:
  Total Items: {len(items)}
  Total Quantity: {sum(item.quantity for item in items)}
  Total Value: ${total_value:.2f}
  Categories: {', '.join(set(item.category.value for item in items if item.category))}

╔══════════════════════════════════════════════════════════════════════════════╗
║  Inventory processing complete with wrapped array structure                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    return result.strip()


@tool(permission=ToolPermission.WRITE_ONLY)
def process_batch_orders_wrapped(batch_request: BatchOrderRequest) -> str:
    """
    Process batch orders with nested wrapped arrays.

    This function demonstrates nested wrapped arrays:
    - Orders are wrapped in "orders" property
    - Each order contains wrapped "items" array
    - Multiple levels of nesting with proper wrapping

    :param batch_request: Request with wrapped orders array
    :return: Formatted processing result
    """
    orders = batch_request.orders

    if not orders:
        return "No orders provided for processing."

    processed_orders = []
    total_revenue = 0.0

    for order in orders:
        order_total = 0.0
        items_summary = []

        for item in order.items:
            item_total = item.quantity * item.unit_price
            order_total += item_total

            items_summary.append(
                f"      - {item.product_name}: {item.quantity} x ${item.unit_price:.2f} = ${item_total:.2f}"
            )

        total_revenue += order_total

        processed_orders.append(
            f"  Order: {order.order_id}\n"
            f"    Customer: {order.customer_name}\n"
            f"    Items ({len(order.items)}):\n"
            f"{chr(10).join(items_summary)}\n"
            f"    Order Total: ${order_total:.2f}"
        )

    # Build result message
    result = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  BATCH ORDER PROCESSING RESULT (WRAPPED)                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

STATUS: SUCCESS
MESSAGE: Successfully processed {len(orders)} batch orders

PROCESSED ORDERS:
{chr(10).join(processed_orders)}

SUMMARY:
  Total Orders: {len(orders)}
  Total Revenue: ${total_revenue:.2f}
  Average Order Value: ${total_revenue / len(orders):.2f}

╔══════════════════════════════════════════════════════════════════════════════╗
║  Batch processing complete with nested wrapped array structure                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    return result.strip()


if __name__ == '__main__':
    # Example 1: Process inventory items with wrapped array
    print("=" * 80)
    print("Example 1: Process inventory items (Wrapped Array)")
    print("=" * 80)

    inventory_request = InventoryRequest(
        items=[
            InventoryItem(
                name="Laptop",
                sku="LAP-001",
                quantity=5,
                price=999.99,
                category=CategoryEnum.ELECTRONICS,
                specifications=Specifications(
                    brand="TechCorp",
                    model="Pro-X1",
                    warranty="2 years"
                )
            ),
            InventoryItem(
                name="Mouse",
                sku="MOU-002",
                quantity=20,
                price=29.99,
                category=CategoryEnum.ACCESSORIES,
                specifications=Specifications(
                    brand="TechCorp",
                    model="Wireless-M2",
                    warranty="1 year"
                )
            ),
            InventoryItem(
                name="Keyboard",
                sku="KEY-003",
                quantity=15,
                price=79.99,
                category=CategoryEnum.ACCESSORIES,
                specifications=Specifications(
                    brand="TechCorp",
                    model="Mechanical-K3",
                    warranty="1 year"
                )
            )
        ]
    )

    result = process_inventory_items_wrapped(inventory_request)
    print(result)

    # Example 2: Process batch orders with nested wrapped arrays
    print("\n" + "=" * 80)
    print("Example 2: Process batch orders (Nested Wrapped Arrays)")
    print("=" * 80)

    batch_request = BatchOrderRequest(
        orders=[
            Order(
                order_id="ORD-001",
                customer_name="John Doe",
                items=[
                    OrderItem(
                        product_name="Laptop",
                        quantity=1,
                        unit_price=999.99
                    ),
                    OrderItem(
                        product_name="Mouse",
                        quantity=2,
                        unit_price=29.99
                    )
                ]
            ),
            Order(
                order_id="ORD-002",
                customer_name="Jane Smith",
                items=[
                    OrderItem(
                        product_name="Monitor",
                        quantity=1,
                        unit_price=299.99
                    )
                ]
            )
        ]
    )

    result = process_batch_orders_wrapped(batch_request)
    print(result)

# Made with Bob
