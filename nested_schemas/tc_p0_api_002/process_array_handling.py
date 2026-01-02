"""Array Handling API - TC-P0-API-002 Implementation

REAL-TIME TOOL:
===============
This tool demonstrates array handling with both wrapped and raw array structures.
It processes inventory items and batch orders with nested array structures.

TEST CASE: TC-P0-API-002
========================
- Test ID: TC-P0-API-002
- Priority: P0 (Critical)
- Type: Integration
- Focus: Array Handling (Wrapped Arrays + Raw Arrays)
- Agent Style: react-intrinsic
- Model: gpt-oss-120b

PURPOSE:
--------
- Validate both wrapped and raw array handling in OpenAPI specs
- Process inventory items with nested specifications
- Handle batch orders with nested item arrays
- Support both array structure types (wrapped and raw)

USAGE:
------
Input: Wrapped arrays of inventory items or batch orders
Output: Processed results with status and details
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


def process_inventory_items(request_data: dict) -> dict:
    """Process inventory items with wrapped array structure.

    This function demonstrates the CORRECT way to handle arrays:
    - Arrays are wrapped in an object property (e.g., "items")
    - Each item can have nested objects (e.g., "specifications")
    - Compatible with react-intrinsic style

    Args:
        request_data (dict): Request with wrapped items array

    Returns:
        dict: Processing result with status and processed items
    """
    try:
        # Extract wrapped array
        items = request_data.get("items", [])

        if not items:
            return {
                "status": "failed",
                "message": "No items provided",
                "processed_items": [],
                "total_value": 0
            }

        processed_items = []
        total_value = 0.0

        for idx, item in enumerate(items):
            # Extract item details
            name = item.get("name", "Unknown")
            sku = item.get("sku", "")
            quantity = item.get("quantity", 0)
            price = item.get("price", 0.0)
            category = item.get("category", "Uncategorized")

            # Extract nested specifications
            specs = item.get("specifications", {})
            brand = specs.get("brand", "N/A")
            model = specs.get("model", "N/A")
            warranty = specs.get("warranty", "N/A")

            # Calculate item value
            item_value = quantity * price
            total_value += item_value

            # Create processed item
            processed_item = {
                "name": name,
                "sku": sku,
                "status": "added",
                "inventory_id": f"INV-2024-{str(idx + 1).zfill(3)}",
                "quantity": quantity,
                "unit_price": price,
                "total_value": item_value,
                "category": category,
                "specifications": {
                    "brand": brand,
                    "model": model,
                    "warranty": warranty
                }
            }

            processed_items.append(processed_item)

            logger.info(
                f"Processed item: {name} (SKU: {sku}) - {quantity} units @ ${price}")

        result = {
            "status": "success",
            "message": f"Successfully processed {len(items)} inventory items",
            "processed_items": processed_items,
            "total_value": round(total_value, 2),
            "summary": {
                "total_items": len(items),
                "total_quantity": sum(item.get("quantity", 0) for item in items),
                "categories": list(set(item.get("category", "Uncategorized") for item in items))
            }
        }

        logger.info(
            f"Inventory processing complete: {len(items)} items, total value: ${total_value:.2f}")
        return result

    except Exception as e:
        logger.error(f"Error processing inventory items: {str(e)}")
        return {
            "status": "failed",
            "message": f"Error processing items: {str(e)}",
            "processed_items": [],
            "total_value": 0
        }


def process_batch_orders(request_data: dict) -> dict:
    """Process batch orders with nested wrapped arrays.

    This function demonstrates nested wrapped arrays:
    - Orders are wrapped in "orders" property
    - Each order contains wrapped "items" array
    - Multiple levels of nesting with proper wrapping

    Args:
        request_data (dict): Request with wrapped orders array

    Returns:
        dict: Processing result with order statuses
    """
    try:
        # Extract wrapped orders array
        orders = request_data.get("orders", [])

        if not orders:
            return {
                "status": "failed",
                "message": "No orders provided",
                "processed_orders": []
            }

        processed_orders = []
        total_revenue = 0.0

        for order in orders:
            order_id = order.get("order_id", "Unknown")
            customer_name = order.get("customer_name", "Unknown Customer")

            # Extract nested wrapped items array
            items = order.get("items", [])

            order_total = 0.0
            processed_items = []

            for item in items:
                product_name = item.get("product_name", "Unknown Product")
                quantity = item.get("quantity", 1)
                unit_price = item.get("unit_price", 0.0)
                item_total = quantity * unit_price

                processed_items.append({
                    "product_name": product_name,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "item_total": item_total
                })

                order_total += item_total

            total_revenue += order_total

            processed_order = {
                "order_id": order_id,
                "customer_name": customer_name,
                "status": "processed",
                "items_count": len(items),
                "items": processed_items,
                "total_amount": round(order_total, 2)
            }

            processed_orders.append(processed_order)

            logger.info(
                f"Processed order: {order_id} for {customer_name} - ${order_total:.2f}")

        result = {
            "status": "success",
            "message": f"Successfully processed {len(orders)} batch orders",
            "processed_orders": processed_orders,
            "summary": {
                "total_orders": len(orders),
                "total_revenue": round(total_revenue, 2),
                "average_order_value": round(total_revenue / len(orders), 2) if orders else 0
            }
        }

        logger.info(
            f"Batch processing complete: {len(orders)} orders, total revenue: ${total_revenue:.2f}")
        return result

    except Exception as e:
        logger.error(f"Error processing batch orders: {str(e)}")
        return {
            "status": "failed",
            "message": f"Error processing orders: {str(e)}",
            "processed_orders": []
        }


@app.route('/api/v1/inventory/process-items', methods=['POST'])
def api_process_inventory_items():
    """API endpoint for processing inventory items (wrapped array)."""
    try:
        request_data = request.get_json()

        if not request_data:
            return jsonify({
                "error": "Invalid request",
                "code": "INVALID_JSON",
                "details": {"message": "Request body must be valid JSON"}
            }), 400

        # Validate wrapped array structure
        if "items" not in request_data:
            return jsonify({
                "error": "Missing required field",
                "code": "MISSING_ITEMS",
                "details": {"message": "Request must contain 'items' array"}
            }), 400

        if not isinstance(request_data["items"], list):
            return jsonify({
                "error": "Invalid data type",
                "code": "INVALID_ITEMS_TYPE",
                "details": {"message": "'items' must be an array"}
            }), 400

        result = process_inventory_items(request_data)

        if result["status"] == "failed":
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "code": "SERVER_ERROR",
            "details": {"message": str(e)}
        }), 500


@app.route('/api/v1/inventory/process-items-raw', methods=['POST'])
def api_process_inventory_items_raw():
    """API endpoint for processing inventory items (raw array)."""
    try:
        request_data = request.get_json()

        if not request_data:
            return jsonify({
                "error": "Invalid request",
                "code": "INVALID_JSON",
                "details": {"message": "Request body must be valid JSON"}
            }), 400

        # For raw arrays, request_data is directly the array
        if not isinstance(request_data, list):
            return jsonify({
                "error": "Invalid data type",
                "code": "INVALID_TYPE",
                "details": {"message": "Request body must be an array"}
            }), 400

        # Wrap the raw array for processing
        wrapped_data = {"items": request_data}
        result = process_inventory_items(wrapped_data)

        if result["status"] == "failed":
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "code": "SERVER_ERROR",
            "details": {"message": str(e)}
        }), 500


@app.route('/api/v1/orders/process-batch', methods=['POST'])
def api_process_batch_orders():
    """API endpoint for processing batch orders (nested wrapped arrays)."""
    try:
        request_data = request.get_json()

        if not request_data:
            return jsonify({
                "error": "Invalid request",
                "code": "INVALID_JSON",
                "details": {"message": "Request body must be valid JSON"}
            }), 400

        # Validate wrapped array structure
        if "orders" not in request_data:
            return jsonify({
                "error": "Missing required field",
                "code": "MISSING_ORDERS",
                "details": {"message": "Request must contain 'orders' array"}
            }), 400

        if not isinstance(request_data["orders"], list):
            return jsonify({
                "error": "Invalid data type",
                "code": "INVALID_ORDERS_TYPE",
                "details": {"message": "'orders' must be an array"}
            }), 400

        result = process_batch_orders(request_data)

        if result["status"] == "failed":
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "code": "SERVER_ERROR",
            "details": {"message": str(e)}
        }), 500


@app.route('/api/v1/orders/process-batch-raw', methods=['POST'])
def api_process_batch_orders_raw():
    """API endpoint for processing batch orders (raw array)."""
    try:
        request_data = request.get_json()

        if not request_data:
            return jsonify({
                "error": "Invalid request",
                "code": "INVALID_JSON",
                "details": {"message": "Request body must be valid JSON"}
            }), 400

        # For raw arrays, request_data is directly the array
        if not isinstance(request_data, list):
            return jsonify({
                "error": "Invalid data type",
                "code": "INVALID_TYPE",
                "details": {"message": "Request body must be an array"}
            }), 400

        # Wrap the raw array for processing
        wrapped_data = {"orders": request_data}
        result = process_batch_orders(wrapped_data)

        if result["status"] == "failed":
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "code": "SERVER_ERROR",
            "details": {"message": str(e)}
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Array Handling API",
        "test_case": "TC-P0-API-002",
        "version": "1.0.0"
    }), 200


if __name__ == '__main__':
    print("="*70)
    print("Array Handling API - TC-P0-API-002")
    print("="*70)
    print("\nTest Case: OpenAPI + React-Intrinsic + gpt-oss-120b + Array Handling")
    print("Priority: P0 (Critical)")
    print("Focus: Wrapped Arrays + Raw Arrays")
    print("\nEndpoints:")
    print("  POST /api/v1/inventory/process-items (wrapped array)")
    print("  POST /api/v1/inventory/process-items-raw (raw array)")
    print("  POST /api/v1/orders/process-batch (wrapped array)")
    print("  POST /api/v1/orders/process-batch-raw (raw array)")
    print("  GET  /health")
    print("\nStarting server on http://0.0.0.0:8002")
    print("="*70)

    # Demo: Process inventory items
    print("\n" + "="*70)
    print("DEMO 1: Processing Inventory Items (Wrapped Array)")
    print("="*70)

    demo_inventory = {
        "items": [
            {
                "name": "Laptop",
                "sku": "LAP-001",
                "quantity": 5,
                "price": 999.99,
                "category": "Electronics",
                "specifications": {
                    "brand": "TechCorp",
                    "model": "Pro-X1",
                    "warranty": "2 years"
                }
            },
            {
                "name": "Mouse",
                "sku": "MOU-002",
                "quantity": 20,
                "price": 29.99,
                "category": "Accessories",
                "specifications": {
                    "brand": "TechCorp",
                    "model": "Wireless-M2",
                    "warranty": "1 year"
                }
            }
        ]
    }

    result = process_inventory_items(demo_inventory)
    print(f"\nStatus: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Total Value: ${result['total_value']}")
    print(f"\nProcessed Items:")
    for item in result['processed_items']:
        print(f"  - {item['name']} (ID: {item['inventory_id']})")
        print(f"    SKU: {item['sku']}, Quantity: {item['quantity']}")
        print(
            f"    Specs: {item['specifications']['brand']} {item['specifications']['model']}")

    # Demo: Process batch orders
    print("\n" + "="*70)
    print("DEMO 2: Processing Batch Orders (Nested Wrapped Arrays)")
    print("="*70)

    demo_batch = {
        "orders": [
            {
                "order_id": "ORD-001",
                "customer_name": "John Doe",
                "items": [
                    {
                        "product_name": "Laptop",
                        "quantity": 1,
                        "unit_price": 999.99
                    },
                    {
                        "product_name": "Mouse",
                        "quantity": 2,
                        "unit_price": 29.99
                    }
                ]
            },
            {
                "order_id": "ORD-002",
                "customer_name": "Jane Smith",
                "items": [
                    {
                        "product_name": "Monitor",
                        "quantity": 1,
                        "unit_price": 299.99
                    }
                ]
            }
        ]
    }

    result = process_batch_orders(demo_batch)
    print(f"\nStatus: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Total Revenue: ${result['summary']['total_revenue']}")
    print(f"\nProcessed Orders:")
    for order in result['processed_orders']:
        print(f"  - {order['order_id']} ({order['customer_name']})")
        print(
            f"    Items: {order['items_count']}, Total: ${order['total_amount']}")

    print("\n" + "="*70)

    # Start Flask server
    app.run(host='0.0.0.0', port=8002, debug=True)

# Made with Bob - Array Handling Test Implementation
