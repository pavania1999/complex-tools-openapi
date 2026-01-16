"""
Python tool using Pydantic models for raw array handling.
Based on openapi_array_handling_raw.yaml

This demonstrates raw array patterns where:
- Request body is directly an array type (valid OpenAPI 3.0)
- Arrays are NOT wrapped in object properties
- API receives array data directly: [{"name": "..."}, {"name": "..."}]
"""
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import Optional, List
from pydantic import BaseModel, Field, RootModel
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


class InventoryItemsRaw(RootModel):
    """Raw array of inventory items (not wrapped in object)"""
    root: List[InventoryItem] = Field(
        ...,
        description="Array of inventory items (raw array structure)",
        min_length=1,
        max_length=100
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
        description="Order items (nested array)",
        min_length=1
    )


class OrdersRaw(RootModel):
    """Raw array of orders (not wrapped in object)"""
    root: List[Order] = Field(
        ...,
        description="Array of orders (raw array structure)",
        min_length=1
    )


@tool(permission=ToolPermission.WRITE_ONLY)
def process_inventory_items_raw(items: InventoryItemsRaw) -> str:
    """
    Process inventory items with raw array structure.

    This function demonstrates raw array handling:
    - Request body is directly an array type
    - Arrays are NOT wrapped in object properties
    - Valid per OpenAPI 3.0 specification
    - API receives: [{"name": "Item1", "quantity": 10}, ...]

    :param items: Raw array of inventory items
    :return: Formatted processing result
    """
    items_list = items.root

    if not items_list:
        return "No items provided for processing."

    processed_items = []
    total_value = 0.0

    for idx, item in enumerate(items_list):
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
║                     INVENTORY PROCESSING RESULT (RAW)                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

STATUS: SUCCESS
MESSAGE: Successfully processed {len(items_list)} inventory items

PROCESSED ITEMS:
{chr(10).join(processed_items)}

SUMMARY:
  Total Items: {len(items_list)}
  Total Quantity: {sum(item.quantity for item in items_list)}
  Total Value: ${total_value:.2f}
  Categories: {', '.join(set(item.category.value for item in items_list if item.category))}

╔══════════════════════════════════════════════════════════════════════════════╗
║  Inventory processing complete with raw array structure                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    return result.strip()


@tool(permission=ToolPermission.WRITE_ONLY)
def process_batch_orders_raw(orders: OrdersRaw) -> str:
    """
    Process batch orders with raw array structure.

    This function demonstrates raw array handling with nested arrays:
    - Request body is a raw array of orders
    - Each order contains nested items array
    - Valid per OpenAPI 3.0 specification

    :param orders: Raw array of orders
    :return: Formatted processing result
    """
    orders_list = orders.root

    if not orders_list:
        return "No orders provided for processing."

    processed_orders = []
    total_revenue = 0.0

    for order in orders_list:
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
║                   BATCH ORDER PROCESSING RESULT (RAW)                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

STATUS: SUCCESS
MESSAGE: Successfully processed {len(orders_list)} batch orders

PROCESSED ORDERS:
{chr(10).join(processed_orders)}

SUMMARY:
  Total Orders: {len(orders_list)}
  Total Revenue: ${total_revenue:.2f}
  Average Order Value: ${total_revenue / len(orders_list):.2f}

╔══════════════════════════════════════════════════════════════════════════════╗
║  Batch processing complete with raw array structure                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    return result.strip()


if __name__ == '__main__':
    # Example 1: Process inventory items with raw array
    print("=" * 80)
    print("Example 1: Process inventory items (Raw Array)")
    print("=" * 80)

    items_raw = InventoryItemsRaw(
        root=[
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
            )
        ]
    )

    result = process_inventory_items_raw(items_raw)
    print(result)

    # Example 2: Process batch orders with raw array
    print("\n" + "=" * 80)
    print("Example 2: Process batch orders (Raw Array with Nested Items)")
    print("=" * 80)

    orders_raw = OrdersRaw(
        root=[
            Order(
                order_id="ORD-003",
                customer_name="Bob Wilson",
                items=[
                    OrderItem(
                        product_name="Keyboard",
                        quantity=1,
                        unit_price=79.99
                    ),
                    OrderItem(
                        product_name="Mouse",
                        quantity=1,
                        unit_price=29.99
                    )
                ]
            ),
            Order(
                order_id="ORD-004",
                customer_name="Alice Brown",
                items=[
                    OrderItem(
                        product_name="Laptop",
                        quantity=2,
                        unit_price=999.99
                    )
                ]
            )
        ]
    )

    result = process_batch_orders_raw(orders_raw)
    print(result)

# Made with Bob
