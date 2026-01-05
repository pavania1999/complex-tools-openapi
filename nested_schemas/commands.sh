orchestrate toolkits add --kind mcp --name nested_reference_api_local \
  --description "Process customer orders with nested address references demonstrating $ref pattern" \
  --package-root /Users/pavaniaddepalli/Documents/Cline/MCP/nested-reference-api/nested-reference-api.zip \
  --command "node build/index.js" \
  --tools '*'



orchestrate toolkits add --kind mcp --name moody-mcp-demo --description "Moody MCP" --package-root /Users/pavaniaddepalli/Documents/Docs/BOB/Complex_Tools/MCP_Servers/zod-mcp-fixed.zip --command "node server.js" --tools '*'    



orchestrate toolkits add --kind mcp --name customer_order_mcp --description "Customer Order MCP" --package-root /Users/pavaniaddepalli/Documents/Docs/BOB/Complex_Tools/MCP_Servers/customer-order-api.zip --command "node build/index.js" --tools '*'    

orchestrate toolkits add --kind mcp --name inventory_mcp_array --description "Customer Inventory MCP" --package-root /Users/pavaniaddepalli/Documents/Docs/BOB/Complex_Tools/MCP_Servers/array-handling-api.zip --command "node index.js" --tools '*'    



##Employee Registration

#Local
orchestrate toolkits add --kind mcp --name employee_registration_mcp --description "Employee Management MCP" --package-root /Users/pavaniaddepalli/Documents/Docs/BOB/Complex_Tools/MCP_Servers/employee-registration-api.zip --command "node build/index.js" --tools '*'    


#Remote
orchestrate toolkits add --kind mcp --name employee_registration_mcp_remote --description "Employee Management MCP" -u orchestrate toolkits add --kind mcp --name employee_registration_mcp_remote --description "Employee Management MCP" -u orchestrate toolkits add --kind mcp --name employee_registration_mcp_remote --description "Employee Management MCP" -u https://employee-registration-api-remote.onrender.com/sse --transport sse --tools '*'  --transport sse --tools '*'  --transport sse --tools '*'    
