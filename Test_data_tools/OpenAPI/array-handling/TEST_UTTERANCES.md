# Test Utterances for TC-P0-API-002: Array Handling

## Test Case Information
- **Test ID**: TC-P0-API-002
- **Test Name**: OpenAPI + React-Intrinsic + gpt-oss-120b + Array Handling
- **Priority**: P0 (Critical)
- **Focus**: Wrapped Arrays + Raw Arrays

---

## Test Setup

### Prerequisites
1. Import OpenAPI spec: `openapi_array_handling_wrapped.yaml`
2. Import OpenAPI spec: `openapi_array_handling_raw.yaml`
3. Configure agent with react-intrinsic style
4. Set model to gpt-oss-120b
5. Ensure Flask server is running on port 8002

---

## Category 1: Wrapped Array - Single Item

### Utterance 1.1: Basic Single Item Processing
```
Process this inventory item: Laptop, SKU LAP-001, quantity 5, price $999.99, category Electronics, brand TechCorp, model Pro-X1, warranty 2 years
```

**Expected Behavior**:
- Agent uses `processInventoryItems` tool
- Sends wrapped array: `{"items": [...]}`
- API returns success with inventory ID
- Response includes total value calculation

**Validation Points**:
- ✅ Wrapped array structure maintained
- ✅ Nested specifications object handled
- ✅ Single item processed successfully
- ✅ Inventory ID generated

---

### Utterance 1.2: Single Item with Minimal Data
```
Add a Monitor to inventory: SKU MON-004, quantity 3, price $299.99
```

**Expected Behavior**:
- Agent fills required fields
- Optional fields handled gracefully
- Wrapped array structure used
- Success response returned

---

## Category 2: Wrapped Array - Multiple Items

### Utterance 2.1: Multiple Items Processing
```
Process these inventory items:
1. Laptop - SKU LAP-001, quantity 5, price $999.99, Electronics, TechCorp Pro-X1, 2 year warranty
2. Mouse - SKU MOU-002, quantity 20, price $29.99, Accessories, TechCorp Wireless-M2, 1 year warranty
3. Keyboard - SKU KEY-003, quantity 15, price $79.99, Accessories, TechCorp Mechanical-K3, 1 year warranty
```

**Expected Behavior**:
- Agent processes all three items
- Wrapped array with multiple items: `{"items": [{...}, {...}, {...}]}`
- Total value calculated across all items
- Summary includes item count and categories

**Validation Points**:
- ✅ Multiple items in single request
- ✅ Each item has unique inventory ID
- ✅ Total value = 5×999.99 + 20×29.99 + 15×79.99 = $6,799.80
- ✅ Categories: Electronics, Accessories

---

### Utterance 2.2: Batch Processing Request
```
I need to add multiple items to inventory: Laptop (5 units at $999.99), Mouse (20 units at $29.99), and Keyboard (15 units at $79.99). All are TechCorp brand.
```

**Expected Behavior**:
- Agent extracts item details
- Creates wrapped array structure
- Processes batch successfully
- Returns summary with totals

---

## Category 3: Raw Array - Single Item

### Utterance 3.1: Raw Array Single Item
```
Use the raw array endpoint to process this item: Monitor, SKU MON-004, quantity 3, price $299.99, Electronics category, ViewTech UHD-27, 3 year warranty
```

**Expected Behavior**:
- Agent uses `processInventoryItemsRaw` tool
- Sends raw array: `[{...}]`
- API handles raw array correctly
- Success response returned

**Validation Points**:
- ✅ Raw array structure at request body level
- ✅ Single item in array
- ✅ Nested specifications handled
- ✅ Processing successful

---

### Utterance 3.2: Direct Array Format
```
Process inventory using direct array format: one Monitor, SKU MON-004, 3 units, $299.99 each
```

**Expected Behavior**:
- Agent recognizes raw array requirement
- Formats as `[{...}]` not `{"items": [...]}`
- API processes correctly
- Response matches wrapped array format

---

## Category 4: Raw Array - Multiple Items

### Utterance 4.1: Multiple Items Raw Array
```
Use raw array format to process: Laptop (SKU LAP-001, 5 units, $999.99) and Mouse (SKU MOU-002, 20 units, $29.99)
```

**Expected Behavior**:
- Agent uses raw array endpoint
- Sends: `[{...}, {...}]`
- Both items processed
- Total value calculated

**Validation Points**:
- ✅ Raw array with multiple items
- ✅ No wrapper object
- ✅ All items processed
- ✅ Correct total: $5,599.75

---

## Category 5: Nested Arrays - Wrapped Batch Orders

### Utterance 5.1: Single Order with Multiple Items
```
Process this order: Order ID ORD-001 for John Doe with items: 1 Laptop at $999.99 and 2 Mice at $29.99 each
```

**Expected Behavior**:
- Agent uses `processBatchOrders` tool
- Wrapped structure: `{"orders": [{"order_id": "...", "items": [...]}]}`
- Nested items array handled
- Order total calculated: $1,059.97

**Validation Points**:
- ✅ Wrapped orders array
- ✅ Nested items array within order
- ✅ Multiple levels of nesting
- ✅ Correct calculations

---

### Utterance 5.2: Multiple Orders Batch
```
Process these orders:
- Order ORD-001 for John Doe: 1 Laptop ($999.99), 2 Mice ($29.99 each)
- Order ORD-002 for Jane Smith: 1 Monitor ($299.99)
```

**Expected Behavior**:
- Agent creates wrapped orders array
- Each order has nested items array
- Both orders processed
- Total revenue calculated: $1,359.96

**Validation Points**:
- ✅ Multiple orders in wrapped array
- ✅ Each order has nested items
- ✅ Order-level totals calculated
- ✅ Overall revenue calculated
- ✅ Average order value: $679.98

---

### Utterance 5.3: Complex Batch Order
```
I have a batch of orders to process:
1. ORD-001 for John Doe with Laptop, Mouse, and Keyboard
2. ORD-002 for Jane Smith with 2 Monitors
3. ORD-003 for Bob Wilson with Mouse and Keyboard
```

**Expected Behavior**:
- Agent handles three orders
- Each with multiple items
- Nested array structure maintained
- Complete summary provided

---

## Category 6: Nested Arrays - Raw Batch Orders

### Utterance 6.1: Raw Array Batch Orders
```
Use raw array format to process orders: ORD-003 for Bob Wilson (1 Keyboard at $79.99, 1 Mouse at $29.99) and ORD-004 for Alice Brown (2 Laptops at $999.99 each)
```

**Expected Behavior**:
- Agent uses `processBatchOrdersRaw` tool
- Raw array format: `[{...}, {...}]`
- Nested items arrays within each order
- Both orders processed

**Validation Points**:
- ✅ Raw array at top level
- ✅ Nested items arrays preserved
- ✅ Multiple levels of nesting
- ✅ Correct totals per order

---

## Category 7: Edge Cases

### Utterance 7.1: Empty Array Handling
```
Process an empty inventory list
```

**Expected Behavior**:
- Agent sends empty array
- API returns appropriate message
- No items processed
- Total value: 0

---

### Utterance 7.2: Single Item in Batch
```
Process a batch order with just one order: ORD-001 for John Doe with 1 Laptop at $999.99
```

**Expected Behavior**:
- Single order in array
- Single item in nested array
- Proper nesting maintained
- Correct calculations

---

### Utterance 7.3: Maximum Items
```
Process 10 different inventory items in one request
```

**Expected Behavior**:
- Agent handles large array
- All items processed
- Performance acceptable
- Complete summary returned

---

## Category 8: Error Handling

### Utterance 8.1: Missing Required Field
```
Add inventory item: Laptop, quantity 5, price $999.99 (missing SKU)
```

**Expected Behavior**:
- API returns 400 error
- Clear error message about missing SKU
- Agent reports error to user
- Suggests providing SKU

---

### Utterance 8.2: Invalid Data Type
```
Process inventory with quantity as text: "five" instead of 5
```

**Expected Behavior**:
- Schema validation fails
- Type mismatch error
- Clear error message
- Agent requests correction

---

### Utterance 8.3: Invalid SKU Format
```
Add item with SKU: ABC123 (should be ABC-123)
```

**Expected Behavior**:
- Pattern validation fails
- Error about SKU format
- Expected format explained
- Agent requests correction

---

## Category 9: Comparison Tests

### Utterance 9.1: Same Data, Different Formats
```
First, process this item using wrapped array: Laptop, SKU LAP-001, 5 units, $999.99
Then process the same item using raw array format
```

**Expected Behavior**:
- Both requests succeed
- Same processing logic applied
- Identical results (except inventory IDs)
- Demonstrates format flexibility

**Validation Points**:
- ✅ Wrapped array works
- ✅ Raw array works
- ✅ Results are equivalent
- ✅ Both formats supported

---

### Utterance 9.2: Format Preference
```
What's the difference between wrapped and raw array formats for inventory processing?
```

**Expected Behavior**:
- Agent explains both formats
- Mentions both are supported
- May suggest wrapped for clarity
- Provides examples

---

## Category 10: Complex Scenarios

### Utterance 10.1: Mixed Categories
```
Process inventory across multiple categories: 5 Laptops (Electronics), 20 Mice (Accessories), 10 Desks (Furniture), 50 Pens (Office Supplies)
```

**Expected Behavior**:
- All items processed
- Categories tracked in summary
- Total value calculated
- Category breakdown provided

**Validation Points**:
- ✅ Multiple categories handled
- ✅ Summary includes all categories
- ✅ Correct item count per category
- ✅ Total value accurate

---

### Utterance 10.2: Specifications Variations
```
Add items with varying specification details:
1. Laptop with full specs (brand, model, warranty)
2. Mouse with partial specs (brand only)
3. Keyboard with no specs
```

**Expected Behavior**:
- All items processed
- Optional specs handled gracefully
- Missing specs shown as N/A
- No errors for missing optional fields

---

### Utterance 10.3: Large Batch Order
```
Process a large order: ORD-001 for Corporate Client with 50 Laptops, 100 Mice, 50 Keyboards, and 25 Monitors
```

**Expected Behavior**:
- Large nested array handled
- All items counted correctly
- Total calculated accurately
- Performance acceptable

**Validation Points**:
- ✅ 225 total items processed
- ✅ Correct quantity per product
- ✅ Accurate total calculation
- ✅ Response time reasonable

---

## Success Criteria Summary

### For Each Test Category:
1. **Tool Selection**: Correct tool chosen (wrapped vs raw)
2. **Array Structure**: Proper format maintained
3. **Nesting**: Multiple levels handled correctly
4. **Processing**: All items processed successfully
5. **Calculations**: Totals and summaries accurate
6. **Error Handling**: Invalid data rejected appropriately
7. **Response Format**: Consistent and complete

### Overall Test Pass Criteria:
- ✅ All wrapped array tests pass
- ✅ All raw array tests pass
- ✅ Nested arrays handled correctly
- ✅ Edge cases handled gracefully
- ✅ Error messages clear and helpful
- ✅ Performance acceptable
- ✅ Both formats produce equivalent results

---

## Test Execution Notes

### Recommended Test Order:
1. Start with simple single-item tests
2. Progress to multiple items
3. Test nested arrays
4. Verify edge cases
5. Validate error handling
6. Compare formats
7. Test complex scenarios

### Key Validation Points:
- Array structure (wrapped vs raw)
- Nested object handling
- Nested array handling
- Required field validation
- Optional field handling
- Calculation accuracy
- Error message clarity
- Response completeness

---

## Additional Test Scenarios

### Performance Testing:
```
Process 100 inventory items in a single request
```

### Concurrent Processing:
```
Process two separate inventory batches simultaneously
```

### Data Integrity:
```
Verify that inventory IDs are unique across multiple requests
```

### Format Switching:
```
Alternate between wrapped and raw formats in consecutive requests
```

---

**Last Updated**: 2024-01-02  
**Test Case**: TC-P0-API-002  
**Version**: 1.0.0