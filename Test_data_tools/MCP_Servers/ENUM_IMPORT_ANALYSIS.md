# MCP Server Import Failure Analysis - Enum Issues

## Problem Summary
Both `array-handling-api-remote` and the `screening_mcp:startScreen` tool fail to import, while `enum-nested-api-remote` succeeds. The root cause is **inconsistent enum handling**.

## Key Differences

### ✅ Working: enum-nested-api-remote
```typescript
// CORRECT: Enum defined as const array
const ACCOUNT_STATUS_ENUM = ["active", "inactive"] as const;

// CORRECT: Spread operator used in schema
inputSchema: {
    properties: {
        status: {
            type: "string",
            enum: [...ACCOUNT_STATUS_ENUM],  // ✅ Spread operator
        }
    }
}
```

### ❌ Failing: array-handling-api-remote
```typescript
// PROBLEM: Inline enum array without spread
inputSchema: {
    properties: {
        category: {
            type: "string",
            enum: ["Electronics", "Accessories", "Furniture", "Office Supplies"],  // ❌ Direct array
        }
    }
}
```

### ❌ Failing: screening_mcp:startScreen
```json
{
    "entityType": {
        "type": "string",
        "enum": ["person", "organization", "unknown"]  // ❌ Direct array in JSON
    }
}
```

## Root Cause Analysis

### Issue 1: TypeScript Enum Serialization
When TypeScript compiles enum arrays directly in object literals, the MCP SDK may not properly serialize them for the JSON-RPC protocol. The spread operator forces proper array serialization.

### Issue 2: Type Inference
Using `as const` creates a readonly tuple type, which TypeScript handles differently during compilation:
- `["a", "b"]` → mutable array, may lose type information
- `["a", "b"] as const` → readonly tuple, preserves exact values

### Issue 3: MCP SDK Validation
The MCP SDK likely validates tool schemas during registration. Direct enum arrays may fail validation due to:
1. Incorrect type inference
2. Missing readonly markers
3. Serialization issues in the JSON-RPC transport layer

## Solutions

### Solution 1: For TypeScript MCP Servers (array-handling-api-remote)

**Before:**
```typescript
enum: ["Electronics", "Accessories", "Furniture", "Office Supplies"]
```

**After:**
```typescript
// Step 1: Define enum as const
const CATEGORY_ENUM = ["Electronics", "Accessories", "Furniture", "Office Supplies"] as const;

// Step 2: Use spread operator in schema
enum: [...CATEGORY_ENUM]
```

### Solution 2: For JSON Schema Tools (screening_mcp:startScreen)

The issue with `screening_mcp:startScreen` is more complex because it's a JSON schema, not TypeScript code. The problem could be:

1. **Schema Validation Issue**: The MCP server at `https://screening-ai-services.npe.moodys.cloud/mcp` may have issues with its schema definition
2. **Transport Issue**: The `streamable_http` transport may not properly handle enum validation
3. **Nested anyOf with enum**: The combination of `anyOf`, nested objects, and enums may cause parsing issues

**Potential fixes for screening_mcp:**
```json
{
    "entityType": {
        "type": "string",
        "description": "Type of entity being screened",
        "enum": ["person", "organization", "unknown"],
        "default": "unknown"  // Add default value
    }
}
```

Or simplify the address structure:
```json
{
    "address": {
        "type": "object",
        "properties": {
            "countryCode": {
                "type": "string",  // Simplify from anyOf
                "description": "ISO 3166-1 alpha-2 country code"
            }
        }
    }
}
```

## Testing Recommendations

### For array-handling-api-remote:
1. Apply the enum constant pattern
2. Rebuild: `npm run build`
3. Test import with MCP client
4. Verify tool listing works

### For screening_mcp:startScreen:
1. Check server logs at `https://screening-ai-services.npe.moodys.cloud/mcp`
2. Test with simplified schema (remove `anyOf` complexity)
3. Verify enum values are properly quoted strings
4. Check if server supports the MCP protocol version

## Additional Observations

### Complex Schema Patterns That May Cause Issues:

1. **Nested anyOf with enums**:
```json
"anyOf": [
    {"type": "object", "properties": {...}},
    {"type": "null"}
]
```

2. **Type arrays with null**:
```json
"type": ["string", "null"]
```

3. **Deep nesting with optional fields**:
```json
"address": {
    "anyOf": [
        {
            "type": "object",
            "properties": {
                "countryCode": {
                    "anyOf": [...]  // Triple nesting
                }
            }
        }
    ]
}
```

## Recommended Pattern for All MCP Servers

```typescript
// 1. Define all enums as const arrays at the top
const STATUS_ENUM = ["active", "inactive"] as const;
const TYPE_ENUM = ["person", "organization"] as const;

// 2. Create type definitions
type Status = typeof STATUS_ENUM[number];
type Type = typeof TYPE_ENUM[number];

// 3. Use spread operator in schemas
const TOOLS: Tool[] = [
    {
        name: "my_tool",
        inputSchema: {
            type: "object",
            properties: {
                status: {
                    type: "string",
                    enum: [...STATUS_ENUM],  // Always use spread
                },
                type: {
                    type: "string",
                    enum: [...TYPE_ENUM],
                }
            }
        }
    }
];
```

## Conclusion

The import failure is caused by **improper enum handling**. The working server uses:
1. Const array definitions with `as const`
2. Spread operator when using enums in schemas
3. Proper type inference

The failing servers use:
1. Direct inline enum arrays
2. Complex nested `anyOf` structures
3. Type unions that may confuse the MCP SDK

**Fix Priority:**
1. **High**: Fix array-handling-api-remote enum (simple fix)
2. **Medium**: Simplify screening_mcp schema complexity
3. **Low**: Add validation tests for all enum patterns