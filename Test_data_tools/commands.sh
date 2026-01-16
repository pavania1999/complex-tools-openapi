##Nested reference API TC01
orchestrate toolkits add --kind mcp --name nested_reference_api_tc_01 \
  --description "Process customer orders with nested address references demonstrating $ref pattern" \
  --package-root /Users/pavaniaddepalli/Documents/Docs/BOB/Complex_Tools/MCP_Servers/nested-reference-api_fix.zip \
  --command "node build/index.js" \
  --tools '*'