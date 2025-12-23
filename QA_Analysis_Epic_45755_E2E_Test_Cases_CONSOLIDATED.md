# E2E Test Cases: Nested Schema Support - Epic #45755 (FINAL CONSOLIDATED)

## CRITICAL CONSTRAINTS

### 1. React-Intrinsic Style Availability
**⚠️ React-Intrinsic Style is ONLY available with gpt-oss models (gpt-oss-20b, gpt-oss-120b)**

### 2. Testing Focus
- **Primary Model**: **gpt-oss-120b** (94% success rate, handles circular refs)
- **gpt-oss-20b**: NOT included in test matrix (0% success on circular refs, lower priority)
- **Other models**: Test 1 style each for backward compatibility

### 3. Enum Support
- **MCP Tools**: Support enums in nested schemas
- **Python Tools**: Support enums in nested schemas
- **OpenAPI Tools**: Support enums via OpenAPI spec
- **Langflow Tools**: Support enums in input schemas

---

## Consolidated Test Matrix Overview

**Total Test Scenarios**: ~80 tests

**Breakdown**:
- **P0 (Critical)**: 20 tests - React-intrinsic + gpt-oss-120b (PRIMARY FEATURE)
- **P1 (High)**: 12 tests - Other gpt-oss styles (Default, React, Planner)
- **P2 (Medium)**: 24 tests - Other models backward compatibility
- **P3 (Low)**: 24 tests - Tool flows, edge cases, extended coverage

---

## Schema Type Logical Groupings

### Group 1: Standard Nesting (Basic + Deep + Schema References)
**Rationale**: All three test nested object structures with varying depth
- **Basic Nested** (2-3 levels): `{customer: {name, address: {street, city}}}`
- **Deep Nested** (4-5 levels): `{company: {dept: {team: {member: {contact}}}}}`
- **Schema References** ($ref/$defs): Reusable components with nesting

**Combined Test**: Verify nested structure preservation at multiple depths with references

### Group 2: Array Handling (Wrapped Arrays + Raw Arrays)
**Rationale**: Both test array structures; raw arrays are negative case
- **Wrapped Arrays**: `{alerts: [{name, type, date}]}`
- **Raw Arrays**: `[{name, email}]` (NOT SUPPORTED - negative test)

**Combined Test**: Verify wrapped arrays work; raw arrays fail with clear error

### Group 3: Complex Scenarios (Complex Real-World + Circular References)
**Rationale**: Both test advanced schema patterns requiring robust handling
- **Complex Real-World** (30+ fields): Large nested structures like Moody's screenAndWait
- **Circular References**: Self-referencing schemas like Person.friendOf → Person

**Combined Test**: Verify large complex schemas and circular references

### Group 4: Enums in Nested Schemas (NEW)
**Rationale**: Test enum validation within nested structures
- **Simple Enums**: `{status: "active" | "inactive", type: "personal" | "business"}`
- **Nested Enums**: `{customer: {type: "individual" | "corporate", address: {country: "US" | "CA" | "UK"}}}`

**Combined Test**: Verify enum validation at multiple nesting levels

### Group 5: Conversational (Multi-Field Slot Filling)
**Rationale**: Tests incremental data collection across multiple turns
- **Multi-Field Slot Filling**: Building nested structure through conversation

**Standalone Test**: Requires conversational flow testing

---

## Priority 0 (P0) - Critical Path Tests (20 tests)

### Test Criteria:
- Agent Style: **React-Intrinsic ONLY**
- Model: **gpt-oss-120b** (primary and only model for P0)
- All Tool Types (4) × Schema Groups (5) = 20 tests

**This is the PRIMARY feature - nested schema support with react-intrinsic style**

---

### Section: MCP Tools with React-Intrinsic + gpt-oss-120b

#### Test Case: MCP + React-Intrinsic + gpt-oss-120b + Standard Nesting (Basic/Deep/References)
**Test ID**: TC-P0-MCP-001  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- MCP toolkit with nested schema containing:
  - Basic nesting (2-3 levels): `{customer: {name, email, address: {street, city, state}}}`
  - Deep nesting (4-5 levels): `{company: {department: {team: {member: {contact}}}}}`
  - Schema references ($ref/$defs): Reusable Address definition used in multiple places
- Agent configured with **react-intrinsic** style and **gpt-oss-120b** model

**Test Steps**:
1. Import MCP toolkit with combined nested schema (basic + deep + $ref)
   **Expected**: Tool imported successfully; all references resolved
2. Create agent with react-intrinsic style and gpt-oss-120b
   **Expected**: Agent created; react-intrinsic available for gpt-oss-120b
3. **Test Basic Nesting**: Send chat "Add customer John Doe, email john@example.com, address 123 Main St, New York, NY"
   **Expected**: LLM generates 3-level nested JSON: `{name: "John Doe", email: "john@example.com", address: {street: "123 Main St", city: "New York", state: "NY"}}`
4. Verify MCP server receives nested structure (NOT flattened)
   **Expected**: Tool executes successfully with nested JSON
5. **Test Deep Nesting**: Send chat "Add John Doe, Engineer in Team Alpha, Engineering Dept, Acme Corp, email john@acme.com"
   **Expected**: LLM generates 5-level nested JSON with all hierarchy levels
6. Verify MCP server processes deep nesting
   **Expected**: Tool executes successfully with 5-level structure
7. **Test Schema References**: Send chat "Add customer with billing address 123 Main St and shipping address 456 Oak Ave"
   **Expected**: LLM generates nested JSON with both addresses using same structure (resolved $ref)
8. Verify MCP server receives expanded addresses
   **Expected**: Tool executes successfully; both addresses have identical structure

---

#### Test Case: MCP + React-Intrinsic + gpt-oss-120b + Array Handling (Wrapped/Raw)
**Test ID**: TC-P0-MCP-002  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- MCP toolkit with wrapped array schema: `{alerts: [{name, type, date}]}`
- MCP toolkit with raw array schema: `[{name, email}]` (for negative test)
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. **Test Wrapped Arrays**: Import MCP toolkit with wrapped arrays
   **Expected**: Tool imported successfully
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. Send chat: "Screen John Doe with 2 alerts: sanctions alert on 2024-01-15 and watchlist alert on 2024-02-20"
   **Expected**: LLM generates array of objects: `{alerts: [{name: "sanctions", date: "2024-01-15"}, {name: "watchlist", date: "2024-02-20"}]}`
4. Verify MCP server receives array structure
   **Expected**: Tool executes successfully; array preserved in nested format
5. **Test Raw Arrays (NEGATIVE)**: Attempt to import MCP toolkit with raw array schema
   **Expected**: Import fails with error: "Top-level arrays are not supported. Please wrap array in an object property."
6. Verify no tool added to catalog
   **Expected**: Tool does not appear; error suggests: "Use {items: [{...}]} instead of [{...}]"

---

#### Test Case: MCP + React-Intrinsic + gpt-oss-120b + Complex Scenarios (Real-World/Circular)
**Test ID**: TC-P0-MCP-003  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- MCP toolkit with complex real-world schema (30+ fields, multiple nesting levels)
  - Example: Moody's screenAndWait with inquiry, alerts, events, identification, etc.
- MCP toolkit with circular reference schema: Person.friendOf → Person
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. **Test Complex Real-World**: Import MCP toolkit with 30+ fields
   **Expected**: Tool imported successfully; large schema loaded
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. Send comprehensive chat with information for 15-20 fields
   **Expected**: LLM extracts multiple fields and generates large nested structure
4. Verify MCP server receives large nested JSON (15-20 fields)
   **Expected**: Tool executes successfully; 94% success rate per PoC; response time < 15 seconds
5. **Test Circular References**: Import MCP toolkit with circular refs
   **Expected**: Tool imported successfully; circular refs preserved or resolved
6. Send chat: "Add person John Doe, friend of Jane Smith"
   **Expected**: LLM generates circular structure: `{name: "John Doe", friendOf: {name: "Jane Smith"}}`
7. Verify MCP server processes circular structure
   **Expected**: Tool executes successfully; gpt-oss-120b handles circular refs (100% success per PoC)

---

#### Test Case: MCP + React-Intrinsic + gpt-oss-120b + Enums in Nested Schemas
**Test ID**: TC-P0-MCP-004  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- MCP toolkit with enum fields in nested schema:
  - Simple enums: `{status: "active" | "inactive" | "pending", priority: "low" | "medium" | "high"}`
  - Nested enums: `{customer: {type: "individual" | "corporate", address: {country: "US" | "CA" | "UK", state: "NY" | "CA" | "TX"}}}`
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Import MCP toolkit with enum fields in nested schema
   **Expected**: Tool imported successfully; enum constraints preserved
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. **Test Simple Enums**: Send chat "Create task with status active and priority high"
   **Expected**: LLM generates JSON with valid enum values: `{status: "active", priority: "high"}`
4. Verify MCP server receives valid enum values
   **Expected**: Tool executes successfully; enum validation passes
5. **Test Nested Enums**: Send chat "Add corporate customer in US, New York"
   **Expected**: LLM generates nested JSON with enums: `{customer: {type: "corporate", address: {country: "US", state: "NY"}}}`
6. Verify MCP server receives nested structure with valid enums
   **Expected**: Tool executes successfully; nested enum validation passes
7. **Test Invalid Enum (NEGATIVE)**: Send chat "Create task with status unknown"
   **Expected**: LLM attempts to use invalid enum value "unknown"
8. Verify error handling
   **Expected**: Tool execution fails with validation error; clear message about valid enum values

---

#### Test Case: MCP + React-Intrinsic + gpt-oss-120b + Multi-Field Slot Filling
**Test ID**: TC-P0-MCP-005  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Not Automated

**Preconditions**:
- MCP toolkit with nested schema requiring multiple fields
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Create agent and attach MCP tool
   **Expected**: Agent created successfully
2. Send partial chat: "Screen John Doe"
   **Expected**: Agent asks for missing required fields (e.g., address)
3. Provide additional info: "123 Main Street"
   **Expected**: Agent asks for city and state
4. Provide more info: "New York, NY"
   **Expected**: Agent has all required fields
5. Verify LLM maintains nested structure across 3 turns
   **Expected**: Final tool call has complete nested structure: `{name: "John Doe", address: {street: "123 Main Street", city: "New York", state: "NY"}}`
6. Verify tool executes with incrementally built structure
   **Expected**: MCP server receives complete nested JSON; 95%+ slot filling accuracy per PoC

---

### Section: Python Tools with React-Intrinsic + gpt-oss-120b

#### Test Case: Python + React-Intrinsic + gpt-oss-120b + Standard Nesting
**Test ID**: TC-P0-PY-001  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- Python tool with nested schema (basic + deep + $ref)
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Import Python tool with combined nested schema
   **Expected**: Tool imported successfully
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. **Test Basic Nesting**: Send chat with 3-level data
   **Expected**: Python function receives nested dict: `{"customer": {"name": "...", "address": {"street": "..."}}}`
4. Verify tool executes successfully
   **Expected**: Python processes 3-level nested dict correctly
5. **Test Deep Nesting**: Send chat with 5-level data
   **Expected**: Python function receives 5-level nested dict with all hierarchy
6. Verify tool executes successfully
   **Expected**: Python processes deep nesting correctly
7. **Test Schema References**: Send chat requiring reusable components
   **Expected**: Python function receives nested dict with resolved $ref references
8. Verify tool executes successfully
   **Expected**: Python processes resolved schema correctly

---

#### Test Case: Python + React-Intrinsic + gpt-oss-120b + Array Handling
**Test ID**: TC-P0-PY-002  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- Python tool with wrapped arrays and raw arrays (negative)
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. **Test Wrapped Arrays**: Import Python tool with wrapped arrays
   **Expected**: Tool imported successfully
2. Send chat with array data
   **Expected**: Python function receives list of dicts: `{"items": [{"name": "..."}, {"name": "..."}]}`
3. Verify tool executes successfully
   **Expected**: Python processes array correctly
4. **Test Raw Arrays (NEGATIVE)**: Attempt to import Python tool with raw array schema
   **Expected**: Import fails with error message about wrapping arrays
5. Verify no tool added to catalog
   **Expected**: Tool does not appear; clear error message provided

---

#### Test Case: Python + React-Intrinsic + gpt-oss-120b + Complex Scenarios
**Test ID**: TC-P0-PY-003  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- Python tool with complex schema (30+ fields) and circular references
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. **Test Complex Real-World**: Import Python tool with 30+ fields
   **Expected**: Tool imported successfully
2. Send comprehensive chat with 15-20 fields
   **Expected**: Python function receives large nested dict with 15-20 fields
3. Verify tool executes successfully
   **Expected**: Python processes large input correctly
4. **Test Circular References**: Import Python tool with circular refs
   **Expected**: Tool imported successfully
5. Send chat with circular data
   **Expected**: Python function receives circular dict: `{"person": {"name": "...", "friendOf": {"name": "..."}}}`
6. Verify tool executes successfully
   **Expected**: Python handles circular structure correctly

---

#### Test Case: Python + React-Intrinsic + gpt-oss-120b + Enums in Nested Schemas
**Test ID**: TC-P0-PY-004  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- Python tool with enum fields in nested schema using Python Enum or Literal types:
  - Simple enums: `status: Literal["active", "inactive", "pending"]`
  - Nested enums: `customer: {type: Literal["individual", "corporate"], address: {country: Literal["US", "CA", "UK"]}}`
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Import Python tool with enum fields in nested schema
   **Expected**: Tool imported successfully; enum constraints preserved
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. **Test Simple Enums**: Send chat "Create task with status active and priority high"
   **Expected**: Python function receives dict with valid enum values: `{"status": "active", "priority": "high"}`
4. Verify Python enum validation
   **Expected**: Tool executes successfully; Pydantic validates enum values
5. **Test Nested Enums**: Send chat "Add corporate customer in US"
   **Expected**: Python function receives nested dict with enums: `{"customer": {"type": "corporate", "address": {"country": "US"}}}`
6. Verify Python processes nested enums
   **Expected**: Tool executes successfully; nested enum validation passes
7. **Test Invalid Enum (NEGATIVE)**: Send chat "Create task with status unknown"
   **Expected**: LLM attempts to use invalid enum value
8. Verify error handling
   **Expected**: Pydantic validation fails; clear error message about valid enum values

---

#### Test Case: Python + React-Intrinsic + gpt-oss-120b + Multi-Field Slot Filling
**Test ID**: TC-P0-PY-005  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Not Automated

**Preconditions**:
- Python tool with nested schema requiring multiple fields
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Create agent and attach Python tool
   **Expected**: Agent created successfully
2. Send partial chat with incomplete data
   **Expected**: Agent asks for missing fields
3. Provide additional info incrementally
   **Expected**: Agent collects all required fields
4. Verify Python tool receives complete nested dict
   **Expected**: Python function receives complete nested structure built incrementally
5. Verify tool executes successfully
   **Expected**: Python processes complete input correctly

---

### Section: OpenAPI Tools with React-Intrinsic + gpt-oss-120b

#### Test Case: OpenAPI + React-Intrinsic + gpt-oss-120b + Standard Nesting
**Test ID**: TC-P0-API-001  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- OpenAPI tool with nested request body (basic + deep + $ref)
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Import OpenAPI tool with combined nested schema
   **Expected**: Tool imported successfully; references resolved
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. **Test Basic Nesting**: Send chat with 3-level data
   **Expected**: API receives nested request body: `{"customer": {"name": "...", "address": {"street": "..."}}}`
4. Verify API call succeeds
   **Expected**: API processes 3-level nested JSON correctly
5. **Test Deep Nesting**: Send chat with 5-level data
   **Expected**: API receives 5-level nested request body with all hierarchy
6. Verify API call succeeds
   **Expected**: API processes deep nesting correctly
7. **Test Schema References**: Send chat requiring reusable components
   **Expected**: API receives nested JSON with resolved $ref references
8. Verify API call succeeds
   **Expected**: API processes resolved schema correctly

---

#### Test Case: OpenAPI + React-Intrinsic + gpt-oss-120b + Array Handling
**Test ID**: TC-P0-API-002  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- OpenAPI spec with wrapped arrays and raw arrays (negative)
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. **Test Wrapped Arrays**: Import OpenAPI tool with wrapped arrays
   **Expected**: Tool imported successfully
2. Send chat with array data
   **Expected**: API receives array in request body: `{"items": [{"name": "..."}, {"name": "..."}]}`
3. Verify API call succeeds
   **Expected**: API processes array correctly
4. **Test Raw Arrays (NEGATIVE)**: Attempt to import OpenAPI spec with raw array
   **Expected**: Import fails with error message about wrapping arrays
5. Verify no tool added to catalog
   **Expected**: Tool does not appear; clear error message provided

---

#### Test Case: OpenAPI + React-Intrinsic + gpt-oss-120b + Complex Scenarios
**Test ID**: TC-P0-API-003  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- OpenAPI tool with complex request body (30+ fields) and circular references
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. **Test Complex Real-World**: Import OpenAPI tool with 30+ fields
   **Expected**: Tool imported successfully
2. Send comprehensive chat with 15-20 fields
   **Expected**: API receives large nested request body with 15-20 fields
3. Verify API call succeeds
   **Expected**: API processes large input correctly
4. **Test Circular References**: Import OpenAPI spec with circular refs
   **Expected**: Tool imported successfully
5. Send chat with circular data
   **Expected**: API receives circular request body with nested structure
6. Verify API call succeeds
   **Expected**: API handles circular structure correctly

---

#### Test Case: OpenAPI + React-Intrinsic + gpt-oss-120b + Enums in Nested Schemas
**Test ID**: TC-P0-API-004  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- OpenAPI spec with enum fields in nested schema:
  - Simple enums: `status: {type: string, enum: ["active", "inactive", "pending"]}`
  - Nested enums: `customer: {type: object, properties: {type: {enum: ["individual", "corporate"]}, address: {properties: {country: {enum: ["US", "CA", "UK"]}}}}}`
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Import OpenAPI tool with enum fields in nested schema
   **Expected**: Tool imported successfully; enum constraints preserved
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. **Test Simple Enums**: Send chat "Create task with status active"
   **Expected**: API receives request body with valid enum: `{"status": "active"}`
4. Verify API validates enum
   **Expected**: API call succeeds; enum validation passes
5. **Test Nested Enums**: Send chat "Add corporate customer in US"
   **Expected**: API receives nested request body with enums: `{"customer": {"type": "corporate", "address": {"country": "US"}}}`
6. Verify API processes nested enums
   **Expected**: API call succeeds; nested enum validation passes
7. **Test Invalid Enum (NEGATIVE)**: Send chat "Create task with status unknown"
   **Expected**: LLM attempts to use invalid enum value
8. Verify error handling
   **Expected**: API returns 400 error; clear message about valid enum values

---

#### Test Case: OpenAPI + React-Intrinsic + gpt-oss-120b + Multi-Field Slot Filling
**Test ID**: TC-P0-API-005  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Not Automated

**Preconditions**:
- OpenAPI tool with nested request body requiring multiple fields
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Create agent and attach OpenAPI tool
   **Expected**: Agent created successfully
2. Send partial chat with incomplete data
   **Expected**: Agent asks for missing fields
3. Provide additional info incrementally
   **Expected**: Agent collects all required fields
4. Verify API receives complete nested request body
   **Expected**: API receives complete nested structure built incrementally
5. Verify API call succeeds
   **Expected**: API processes complete input correctly

---

### Section: Langflow Tools with React-Intrinsic + gpt-oss-120b

#### Test Case: Langflow + React-Intrinsic + gpt-oss-120b + Standard Nesting
**Test ID**: TC-P0-LF-001  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- Langflow tool with nested input schema (basic + deep + $ref)
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Import Langflow tool with combined nested schema
   **Expected**: Tool imported successfully; references resolved
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. **Test Basic Nesting**: Send chat with 3-level data
   **Expected**: Langflow receives nested input: `{"customer": {"name": "...", "address": {"street": "..."}}}`
4. Verify flow executes successfully
   **Expected**: Langflow processes 3-level nested JSON correctly
5. **Test Deep Nesting**: Send chat with 5-level data
   **Expected**: Langflow receives 5-level nested input with all hierarchy
6. Verify flow executes successfully
   **Expected**: Langflow processes deep nesting correctly
7. **Test Schema References**: Send chat requiring reusable components
   **Expected**: Langflow receives nested JSON with resolved $ref references
8. Verify flow executes successfully
   **Expected**: Langflow processes resolved schema correctly

---

#### Test Case: Langflow + React-Intrinsic + gpt-oss-120b + Array Handling
**Test ID**: TC-P0-LF-002  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- Langflow tool with wrapped arrays and raw arrays (negative)
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. **Test Wrapped Arrays**: Import Langflow tool with wrapped arrays
   **Expected**: Tool imported successfully
2. Send chat with array data
   **Expected**: Langflow receives array input: `{"items": [{"name": "..."}, {"name": "..."}]}`
3. Verify flow executes successfully
   **Expected**: Langflow processes array correctly
4. **Test Raw Arrays (NEGATIVE)**: Attempt to import Langflow tool with raw array
   **Expected**: Import fails with error message about wrapping arrays
5. Verify no tool added to catalog
   **Expected**: Tool does not appear; clear error message provided

---

#### Test Case: Langflow + React-Intrinsic + gpt-oss-120b + Complex Scenarios
**Test ID**: TC-P0-LF-003  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- Langflow tool with complex schema (30+ fields) and circular references
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. **Test Complex Real-World**: Import Langflow tool with 30+ fields
   **Expected**: Tool imported successfully
2. Send comprehensive chat with 15-20 fields
   **Expected**: Langflow receives large nested input with 15-20 fields
3. Verify flow executes successfully
   **Expected**: Langflow processes large input correctly
4. **Test Circular References**: Import Langflow tool with circular refs
   **Expected**: Tool imported successfully
5. Send chat with circular data
   **Expected**: Langflow receives circular input with nested structure
6. Verify flow executes successfully
   **Expected**: Langflow handles circular structure correctly

---

#### Test Case: Langflow + React-Intrinsic + gpt-oss-120b + Enums in Nested Schemas
**Test ID**: TC-P0-LF-004  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Automated

**Preconditions**:
- Langflow tool with enum fields in nested input schema
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Import Langflow tool with enum fields in nested schema
   **Expected**: Tool imported successfully; enum constraints preserved
2. Create agent with react-intrinsic and gpt-oss-120b
   **Expected**: Agent created successfully
3. **Test Simple Enums**: Send chat "Process order with status pending"
   **Expected**: Langflow receives input with valid enum: `{"status": "pending"}`
4. Verify flow validates enum
   **Expected**: Flow executes successfully; enum validation passes
5. **Test Nested Enums**: Send chat "Process corporate customer from US"
   **Expected**: Langflow receives nested input with enums: `{"customer": {"type": "corporate", "address": {"country": "US"}}}`
6. Verify flow processes nested enums
   **Expected**: Flow executes successfully; nested enum validation passes
7. **Test Invalid Enum (NEGATIVE)**: Send chat "Process order with status unknown"
   **Expected**: LLM attempts to use invalid enum value
8. Verify error handling
   **Expected**: Flow execution fails; clear message about valid enum values

---

#### Test Case: Langflow + React-Intrinsic + gpt-oss-120b + Multi-Field Slot Filling
**Test ID**: TC-P0-LF-005  
**Priority**: Critical  
**Type**: Integration  
**Automation Status**: Not Automated

**Preconditions**:
- Langflow tool with nested schema requiring multiple fields
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Create agent and attach Langflow tool
   **Expected**: Agent created successfully
2. Send partial chat with incomplete data
   **Expected**: Agent asks for missing fields
3. Provide additional info incrementally
   **Expected**: Agent collects all required fields
4. Verify Langflow receives complete nested input
   **Expected**: Langflow receives complete nested structure built incrementally
5. Verify flow executes successfully
   **Expected**: Langflow processes complete input correctly

---

## Priority 1 (P1) - Other gpt-oss Styles (12 tests)

### Test Criteria:
- Agent Styles: **Default, React, Planner** (NOT react-intrinsic)
- Model: **gpt-oss-120b**
- Selected Tool Types × Selected Schema Groups

**Purpose**: Test backward compatibility with traditional flattening approach

---

### Section: Backward Compatibility with Other gpt-oss Styles

#### Test Case: MCP + Default + gpt-oss-120b + Standard Nesting
**Test ID**: TC-P1-001  
**Priority**: High  
**Type**: Regression  
**Automation Status**: Automated

**Preconditions**:
- MCP toolkit with standard nesting
- Agent configured with **default** style (NOT react-intrinsic) and gpt-oss-120b

**Test Steps**:
1. Create agent with default style and gpt-oss-120b
   **Expected**: Agent created successfully
2. Attach MCP tool with nested schema
   **Expected**: Tool attached successfully
3. Send chat with nested data
   **Expected**: Agent uses default style; schema is FLATTENED for parameter collection
4. Verify tool receives flattened input converted back to nested
   **Expected**: MCP server receives nested JSON (system converts flattened to nested)
5. Verify tool executes successfully
   **Expected**: Tool executes; backward compatibility maintained

---

#### Test Case: Python + React + gpt-oss-120b + Array Handling
**Test ID**: TC-P1-002  
**Priority**: High  
**Type**: Regression  
**Automation Status**: Automated

**Preconditions**:
- Python tool with wrapped arrays
- Agent configured with **react** style (NOT react-intrinsic) and gpt-oss-120b

**Test Steps**:
1. Create agent with react style and gpt-oss-120b
   **Expected**: Agent created successfully
2. Attach Python tool with wrapped arrays
   **Expected**: Tool attached successfully
3. Send chat with array data
   **Expected**: Agent uses react style; schema is FLATTENED
4. Verify Python tool receives nested dict with arrays (converted from flattened)
   **Expected**: Python function receives nested dict with arrays
5. Verify tool executes successfully
   **Expected**: Tool executes; backward compatibility maintained

---

#### Test Case: OpenAPI + Planner + gpt-oss-120b + Complex Scenarios
**Test ID**: TC-P1-003  
**Priority**: High  
**Type**: Regression  
**Automation Status**: Automated

**Preconditions**:
- OpenAPI tool with complex schemas
- Agent configured with **planner** style (NOT react-intrinsic) and gpt-oss-120b

**Test Steps**:
1. Create agent with planner style and gpt-oss-120b
   **Expected**: Agent created successfully
2. Attach OpenAPI tool with complex schema
   **Expected**: Tool attached successfully
3. Send chat requiring planning and tool execution
   **Expected**: Planner creates plan; schema is FLATTENED for tool call
4. Verify API receives nested request body (converted from flattened)
   **Expected**: API receives nested JSON
5. Verify tool executes successfully
   **Expected**: Tool executes; planner works with flattened schemas

---

**[Continue with 9 more P1 tests covering all combinations of 4 tools × 3 styles (Default, React, Planner) for selected schema groups]**

---

## Priority 2 (P2) - Other Models (24 tests)

### Test Criteria:
- Models: **Claude (Default), GPT-4 (React), Mistral (Planner), Llama (Default), WatsonX Granite (React), WatsonX Llama (Planner)**
- 1 style per model (mix and match)
- All 4 tool types × 6 models = 24 tests

**Purpose**: Verify backward compatibility with non-gpt-oss models

---

### Section: Backward Compatibility with Non-gpt-oss Models

#### Test Case: MCP + Default + Claude + Standard Nesting
**Test ID**: TC-P2-001  
**Priority**: Medium  
**Type**: Regression  
**Automation Status**: Automated

**Preconditions**:
- MCP toolkit with standard nesting
- Agent configured with **default** style and **Claude** model
- **NOTE**: React-intrinsic is NOT available for Claude

**Test Steps**:
1. Verify react-intrinsic style is NOT available for Claude
   **Expected**: UI/API does not show react-intrinsic option
2. Create agent with default style and Claude
   **Expected**: Agent created successfully
3. Test standard nesting (basic + deep + $ref)
   **Expected**: Schema is FLATTENED; system converts back to nested for MCP server
4. Verify backward compatibility
   **Expected**: Tool executes successfully; no breaking changes

---

#### Test Case: Python + React + GPT-4 + Array Handling
**Test ID**: TC-P2-002  
**Priority**: Medium  
**Type**: Regression  
**Automation Status**: Automated

**Preconditions**:
- Python tool with wrapped arrays
- Agent configured with **react** style and **GPT-4** model
- **NOTE**: React-intrinsic is NOT available for GPT-4

**Test Steps**:
1. Verify react-intrinsic style is NOT available for GPT-4
   **Expected**: UI/API does not show react-intrinsic option
2. Create agent with react style and GPT-4
   **Expected**: Agent created successfully
3. Test wrapped arrays
   **Expected**: Schema is FLATTENED; system converts back to nested for Python
4. Verify backward compatibility
   **Expected**: Tool executes successfully; arrays handled correctly

---

#### Test Case: OpenAPI + Planner + Mistral + Complex Scenarios
**Test ID**: TC-P2-003  
**Priority**: Medium  
**Type**: Regression  
**Automation Status**: Automated

**Preconditions**:
- OpenAPI tool with complex schemas
- Agent configured with **planner** style and **Mistral** model
- **NOTE**: React-intrinsic is NOT available for Mistral

**Test Steps**:
1. Verify react-intrinsic style is NOT available for Mistral
   **Expected**: UI/API does not show react-intrinsic option
2. Create agent with planner style and Mistral
   **Expected**: Agent created successfully
3. Test complex real-world schemas
   **Expected**: Schema is FLATTENED; system converts back to nested for API
4. Verify backward compatibility
   **Expected**: Tool executes successfully; planner works with flattening

---

#### Test Case: Langflow + Default + Llama + Enums in Nested Schemas
**Test ID**: TC-P2-004  
**Priority**: Medium  
**Type**: Regression  
**Automation Status**: Automated

**Preconditions**:
- Langflow tool with enum fields in nested schema
- Agent configured with **default** style and **Llama** model
- **NOTE**: React-intrinsic is NOT available for Llama

**Test Steps**:
1. Verify react-intrinsic style is NOT available for Llama
   **Expected**: UI/API does not show react-intrinsic option
2. Create agent with default style and Llama
   **Expected**: Agent created successfully
3. Test enums in nested schemas
   **Expected**: Schema is FLATTENED; enum constraints preserved; system converts back to nested
4. Verify backward compatibility
   **Expected**: Flow executes successfully; enum validation works with flattening

---

**[Continue with 20 more P2 tests covering all combinations of 4 tools × 6 models]**

---

## Priority 3 (P3) - Tool Flows and Edge Cases (24 tests)

### Section: Tool Flow Integration

#### Test Case: Tool Flow - MCP → Python (Both Nested, React-Intrinsic)
**Test ID**: TC-P3-001  
**Priority**: High  
**Type**: Integration  
**Automation Status**: Not Automated

**Preconditions**:
- Tool flow: MCP tool (nested output) → Python tool (nested input)
- Agent configured with **react-intrinsic** style and **gpt-oss-120b** model

**Test Steps**:
1. Create tool flow: MCP tool → Python tool
   **Expected**: Tool flow created successfully
2. Configure MCP tool to output nested JSON
   **Expected**: MCP tool configured with nested output schema
3. Configure Python tool to accept nested JSON input
   **Expected**: Python tool configured with nested input schema
4. Send chat triggering tool flow
   **Expected**: MCP tool executes first, outputs nested JSON
5. Verify Python tool receives MCP output as nested input (NO flattening)
   **Expected**: Python tool receives nested JSON from MCP tool directly
6. Verify tool flow completes successfully
   **Expected**: Both tools execute; final result returned to user

---

#### Test Case: Tool Flow - OpenAPI → Langflow (Nested, Default Style)
**Test ID**: TC-P3-002  
**Priority**: Medium  
**Type**: Integration  
**Automation Status**: Not Automated

**Preconditions**:
- Tool flow: OpenAPI tool (nested output) → Langflow tool (nested input)
- Agent configured with **default** style and **Claude** model

**Test Steps**:
1. Create tool flow: OpenAPI tool → Langflow tool
   **Expected**: Tool flow created successfully
2. Configure both tools with nested schemas
   **Expected**: Tools configured successfully
3. Send chat triggering tool flow
   **Expected**: OpenAPI tool executes; schema is FLATTENED
4. Verify Langflow tool receives converted nested input
   **Expected**: System converts flattened output to nested input for Langflow
5. Verify tool flow completes successfully
   **Expected**: Both tools execute; conversion works correctly

---

#### Test Case: Tool Flow - MCP → OpenAPI → Python (3-Tool Chain with Enums)
**Test ID**: TC-P3-003  
**Priority**: High  
**Type**: Integration  
**Automation Status**: Not Automated

**Preconditions**:
- Tool flow: MCP tool (nested output with enums) → OpenAPI tool (nested input/output with enums) → Python tool (nested input with enums)
- Agent configured with react-intrinsic style and gpt-oss-120b

**Test Steps**:
1. Create 3-tool flow with enum fields in nested schemas
   **Expected**: Tool flow created successfully
2. Send chat triggering entire flow
   **Expected**: MCP tool executes, outputs nested JSON with enums
3. Verify OpenAPI tool receives nested input with enums
   **Expected**: OpenAPI processes nested input, outputs nested JSON with enums
4. Verify Python tool receives nested input with enums
   **Expected**: Python processes nested input with enum validation
5. Verify entire flow completes successfully
   **Expected**: All 3 tools execute; enums preserved throughout chain

---

**[Continue with 21 more P3 tests covering various tool flows, edge cases, error handling, and extended scenarios]**

---

## Test Execution Strategy (FINAL)

### Phase 1: P0 Tests (20 tests) - CRITICAL
**Timeline**: Week 1-2 of QA (Dec 23 - Jan 5)
- **Focus**: React-intrinsic + gpt-oss-120b (PRIMARY FEATURE)
- **Coverage**: All 4 tool types × 5 schema groups = 20 tests
- **Goal**: Validate nested schema support including enums
- **Success Criteria**: ≥ 95% pass rate (19/20 tests)

### Phase 2: P1 Tests (12 tests) - HIGH
**Timeline**: Week 2-3 of QA (Jan 6 - Jan 12)
- **Focus**: Other gpt-oss styles (Default, React, Planner)
- **Coverage**: Backward compatibility with flattening
- **Goal**: Ensure no breaking changes
- **Success Criteria**: ≥ 90% pass rate (11/12 tests)

### Phase 3: P2 Tests (24 tests) - MEDIUM
**Timeline**: Week 3-4 of QA (Jan 13 - Jan 16)
- **Focus**: All other models (1 style each)
- **Coverage**: Backward compatibility verification
- **Goal**: Ensure all models continue to work
- **Success Criteria**: ≥ 85% pass rate (20/24 tests)

### Phase 4: P3 Tests (24 tests) - LOW
**Timeline**: Post-release or deferred
- **Focus**: Tool flows, edge cases, extended coverage
- **Goal**: Complete coverage
- **Success Criteria**: ≥ 80% pass rate (19/24 tests)

---

## Success Criteria (FINAL)

### Overall Release Criteria
- **P0 Pass Rate**: ≥ 95% (19/20 tests)
- **P1 Pass Rate**: ≥ 90% (11/12 tests)
- **P2 Pass Rate**: ≥ 85% (20/24 tests)
- **Critical Blockers**: 0
- **High Priority Issues**: ≤ 2
- **Performance**: Response time < 15 seconds for complex schemas
- **Model Success Rate**: gpt-oss-120b ≥ 94%

### Key Metrics
- **React-Intrinsic Adoption**: Available ONLY for gpt-oss models
- **Enum Support**: Validated in MCP, Python, OpenAPI, and Langflow tools
- **Backward Compatibility**: 100% for non-react-intrinsic styles
- **Tool Flow Success**: ≥ 90% for nested schema flows
- **Error Handling**: Clear messages for unsupported scenarios

---

## Test Automation Recommendations

### High Priority for Automation (16 tests)
- P0 tests with gpt-oss-120b (excluding slot filling)
- Focus on standard nesting, arrays, complex scenarios, enums
- All 4 tool types

### Medium Priority for Automation (12 tests)
- P1 tests with other gpt-oss styles
- P2 tests with selected models

### Manual Testing Required (52 tests)
- Multi-field slot filling (conversational) - 4 tests
- Tool flows (complex interactions) - 24 tests
- Error handling and edge cases
- UI validation (react-intrinsic option availability)

---

## Key Additions in Final Version

### 1. Enum Support Testing
- **MCP Tools**: Enum validation in nested schemas
- **Python Tools**: Literal types and Enum classes in nested schemas
- **OpenAPI Tools**: Enum constraints in OpenAPI spec
- **Langflow Tools**: Enum validation in input schemas

### 2. Removed gpt-oss-20b
- Focus exclusively on **gpt-oss-120b** (94% success rate, handles circular refs)
- Eliminates 20b's limitations (0% success on circular refs, 89% overall)

### 3. Consolidated Test Count
- **Total**: ~80 test scenarios (down from 120)
- **P0**: 20 tests (PRIMARY FEATURE)
- **P1**: 12 tests (backward compatibility)
- **P2**: 24 tests (other models)
- **P3**: 24 tests (tool flows, edge cases)

---

## Conclusion

**FINAL CONSOLIDATED TEST MATRIX**: ~80 test scenarios

**Key Features**:
1. **Focus on gpt-oss-120b**: Best performance, handles all schema types
2. **Enum Support**: Comprehensive testing across all tool types
3. **Logical Grouping**: Schema types grouped by similarity
4. **Tool Separation**: Each tool type tested independently
5. **Priority Focus**: P0 tests validate PRIMARY FEATURE (react-intrinsic + gpt-oss-120b)

**Expected Outcome**: Comprehensive validation of nested schema support including enum validation, with focused testing on the primary model (gpt-oss-120b) and complete backward compatibility verification.
