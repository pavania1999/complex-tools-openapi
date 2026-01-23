# PR #2342 Analysis: Improved Tool Schema Validation for Broader MCP Server Compatibility

## PR Overview
**Title:** Improved Tool Schema Validation for Broader MCP Server Compatibility  
**Link:** https://github.com/IBM/mcp-context-forge/pull/2342  
**Branch:** `2322_json_validation_failures_gateways` → `main`  
**Status:** Open (Bug-fix PR)

## Problem Statement

### Original Issue
The Context Forge Gateway was **only validating Draft 7 JSON schemas**, causing import failures for MCP servers using other JSON Schema draft versions. This resulted in:

1. **ValueError exceptions** when encountering non-Draft 7 schemas
2. **Import failures** for legitimate MCP servers with valid schemas
3. **Poor error visibility** - crashes instead of warnings

### Affected Scenarios
- MCP servers using Draft 4, 6, 2019-09, or 2020-12 schemas
- Tools with enum validation (like `array-handling-api-remote` and `screening_mcp`)
- Complex nested schemas with `anyOf`, type unions, etc.

## Root Cause

### The Real Issue (NOT Enums!)
After analyzing PR #2342, **the problem is NOT with enum handling in the MCP servers themselves**. The issue is in the **Context Forge Gateway's schema validation logic**.

**Before PR #2342:**
```python
# Only Draft 7 validator was used
jsonschema.Draft7Validator.check_schema(target.input_schema)
```

This would **raise a ValueError** for any schema not conforming to Draft 7, even if it was valid under other drafts.

**After PR #2342:**
```python
# Detects the correct validator automatically
allowed_validator_names = {
    "Draft4Validator",
    "Draft6Validator", 
    "Draft7Validator",
    "Draft201909Validator",
    "Draft202012Validator",
}

# Use jsonschema.validators.validator_for to detect appropriate validator
validator = jsonschema.validators.validator_for(schema)

if validator.__name__ not in allowed_validator_names:
    logger.warning(f"Unsupported JSON Schema draft: {validator.__name__}")
else:
    validator.check_schema(schema)
```

## Key Changes in PR #2342

### 1. Automatic Draft Detection
```python
# NEW: Automatically detects the correct schema draft
schema = target.input_schema
validator = jsonschema.validators.validator_for(schema)
```

### 2. Multi-Draft Support
Supports 5 different JSON Schema drafts:
- Draft 4
- Draft 6
- Draft 7
- Draft 2019-09
- Draft 2020-12

### 3. Graceful Error Handling
```python
# OLD: Raised ValueError, crashed the import
except jsonschema.exceptions.SchemaError as e:
    raise ValueError(f"Invalid schema: {e}")

# NEW: Logs warning, continues operation
if validator.__name__ not in allowed_validator_names:
    logger.warning(f"Unsupported JSON Schema draft: {validator.__name__}")
```

### 4. Better Logging
- Warnings for unsupported drafts instead of crashes
- Clear visibility into schema validation issues
- Improved debugging capabilities

## Impact on Our MCP Servers

### ✅ enum-nested-api-remote (Working)
**Why it works:** Uses Draft 7 schema (the only one supported before PR #2342)

```typescript
// This schema is Draft 7 compliant
inputSchema: {
    type: "object",
    properties: {
        status: {
            type: "string",
            enum: [...ACCOUNT_STATUS_ENUM],  // Valid in Draft 7
        }
    }
}
```

### ❌ array-handling-api-remote (Failing)
**Why it fails:** Likely uses a different draft version OR has schema features not in Draft 7

```typescript
// This might be Draft 6 or have Draft 6 features
inputSchema: {
    properties: {
        category: {
            type: "string",
            enum: ["Electronics", "Accessories", "Furniture", "Office Supplies"],
        }
    }
}
```

**Potential issues:**
1. Schema might be auto-detected as Draft 6 (which has slightly different enum handling)
2. The `exclusiveMinimum: true` syntax is Draft 6+ (Draft 4 uses numeric values)
3. Array validation with `minItems`, `maxItems` might differ between drafts

### ❌ screening_mcp:startScreen (Failing)
**Why it fails:** Complex schema with features that may not be Draft 7 compliant

```json
{
    "type": ["string", "null"],  // Type arrays - Draft 6+
    "anyOf": [...],              // Complex anyOf nesting
    "additionalProperties": true // Permissive validation
}
```

## Solution: Does PR #2342 Fix Our Issues?

### ✅ YES - For Gateway-Side Validation
PR #2342 **will fix the import failures** by:
1. Automatically detecting the correct schema draft
2. Using the appropriate validator for each schema
3. Logging warnings instead of crashing on unsupported schemas

### ⚠️ PARTIAL - For MCP Server Compatibility
The PR improves compatibility but doesn't guarantee all schemas will work. Servers still need:
1. Valid JSON Schema (any supported draft)
2. Proper enum syntax for their draft version
3. Correct type definitions

## Recommendations

### For array-handling-api-remote

**Option 1: Ensure Draft 7 Compliance (Safest)**
```typescript
// Explicitly use Draft 7 syntax
const CATEGORY_ENUM = ["Electronics", "Accessories", "Furniture", "Office Supplies"] as const;

inputSchema: {
    type: "object",
    properties: {
        category: {
            type: "string",
            enum: [...CATEGORY_ENUM],  // Spread for proper serialization
        },
        price: {
            type: "number",
            minimum: 0,
            exclusiveMinimum: 0,  // Draft 7 syntax
        }
    }
}
```

**Option 2: Use Draft 6 Explicitly**
Add `$schema` to explicitly declare the draft:
```typescript
inputSchema: {
    $schema: "http://json-schema.org/draft-06/schema#",
    type: "object",
    properties: {
        // ... rest of schema
    }
}
```

### For screening_mcp:startScreen

**Simplify the schema structure:**
```json
{
    "entityType": {
        "type": "string",
        "enum": ["person", "organization", "unknown"],
        "default": "unknown"
    },
    "address": {
        "type": "object",
        "properties": {
            "countryCode": {
                "type": "string",  // Simplified from anyOf
                "description": "ISO 3166-1 alpha-2 country code"
            }
        }
    }
}
```

## Testing After PR #2342 Merge

1. **Wait for PR merge** to main branch
2. **Update Context Forge Gateway** to latest version
3. **Re-test imports** for both failing servers
4. **Check logs** for any schema validation warnings
5. **Verify tool execution** works correctly

## Conclusion

**The enum issue was a red herring!** The real problem is:
- ❌ **NOT** the enum syntax in MCP servers
- ✅ **YES** the Gateway's rigid Draft 7-only validation

**PR #2342 solves this by:**
- Supporting multiple JSON Schema drafts
- Auto-detecting the correct validator
- Gracefully handling validation errors

**Expected outcome after PR merge:**
- ✅ `array-handling-api-remote` should import successfully
- ✅ `screening_mcp:startScreen` should import successfully
- ✅ Better error messages for actual schema issues

**Action items:**
1. Monitor PR #2342 for merge
2. Update Gateway after merge
3. Re-test all failing MCP servers
4. Document any remaining issues (if any)