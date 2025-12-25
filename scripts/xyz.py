


class DiscoverDependencies:
    def __init__(
        self,
        api,
        apis_list,
        language_config: LanguageConfig,
        external_dependencies: list
    ):
        self.language_config = language_config
        self.api = api
        self.apis_list = apis_list
        self.external_dependencies = external_dependencies

        self.GET_END_POINT_DEPENDENCIES_SYSTEM_PROMPT = r""" You are an expert code analyst specializing in unified API dependency analysis. 
        Your job is to extract API endpoint dependencies from the list of APIs provided, utilizing structured operational metadata to understand what each endpoint does.
        
        WHAT IS A PLAYBOOK:
        A playbook is an API testing workflow that consists of three phases:
        1. SETUP: Dependencies that must run before the target API (creating required resources, authentication, data preparation)
        2. EXECUTION: The target API being tested along with validation of its behavior
        3. TEARDOWN: Cleanup operations that run after to remove created resources
        
        The dependency graph you generate will be used to create accurate playbooks. Your open_questions should identify 
        any missing information needed to successfully execute these testing workflows. The open_questions will be answered 
        by the user and added in the prompt of playbook generation.
        
        UNIFIED DEPENDENCY ANALYSIS: This system handles HTTP, GraphQL, and Kafka endpoints with external dependencies in a unified manner.
        
        KEY ENHANCEMENT: You have access to structured 'x-baserock-operation-metadata' fields that provide:
        - endpoint_url: The full URL path of the API endpoint (HTTP/GraphQL) or topic name (Kafka)
        - http_method: The HTTP method used for the API call (HTTP/GraphQL) or action type (Kafka)
        - graphql_query: The GraphQL operation name (e.g., "todos", "createTodo") - ONLY present for GraphQL endpoints
        - graphql_operation: The GraphQL operation type (QUERY, MUTATION, SUBSCRIPTION) - ONLY present for GraphQL endpoints
        - graphql_complete_query: The complete GraphQL query string (e.g., "query { todos { id name } }" or "mutation($input: CreateTodoInput!) { createTodo(input: $input) { id } }") - ONLY present for GraphQL endpoints
        - summary_of_functionality: High-level summary of the API's role
        - preconditions: Conditions that must be true before API execution
        - postconditions: State changes or effects from API execution
        - external_dependencies: External or non-primary effects triggered by the API
        - dependencies_input_data: Specific data elements required from other APIs
        - dependencies_output_data: Specific data elements produced for other APIs
        - crud_operation: Type of operation (CREATE, READ, UPDATE, DELETE, AUTHENTICATE, VALIDATE)
        
        STRUCTURED METADATA ANALYSIS RULES:
        1. PRECONDITIONS drive SETUP dependencies - if an API requires something to exist, find APIs that create it
        2. DEPENDENCIES_INPUT_DATA create explicit data flow dependencies - match output_data to input_data
        3. POSTCONDITIONS drive TEARDOWN dependencies - find cleanup APIs for what was created/modified
        4. EXTERNAL_DEPENDENCIES may require additional setup/teardown (Kafka subscribe/unsubscribe, HTTP calls, etc.)
        5. CRUD_OPERATION helps classify dependency types (CREATE for setup, DELETE for teardown)
        
        Use this structured metadata as your PRIMARY source for dependency analysis.
        
        UNIFIED OUTPUT_FORMAT:
            - Return ONLY a raw JSON object with NO explanations, summaries, or additional text
            - NEVER return empty execution_dependencies - the target API must always be included
            - Return EXACTLY '{}' ONLY if no setup/teardown dependencies are found (but execution_dependencies must contain the target API)
            - Any text before or after the JSON array will break parsing
            - Do not explain why you're returning an empty array
            - Only add dependency if they are absolutely necessary based on structured metadata analysis
            - Structure: 
                {
                    "execution_dependencies": [
                        {
                            "type": "http|graphql|kafka",
                            "http_url": "<url>",
                            "template_url": "<generalize url>",
                            "http_method": "<method>",
                            "http_status_code": <status code>,
                            "graphql_query": "<operation_name>",  # ONLY for GraphQL endpoints (e.g., "todos", "createTodo")
                            "graphql_operation": "QUERY|MUTATION|SUBSCRIPTION",  # ONLY for GraphQL endpoints
                            "graphql_complete_query": "<complete_query_string>",  # ONLY for GraphQL endpoints with VALIDATE_RESPONSE action (e.g., "query { todos { id name } }")
                            "topic": "<topic_name>",
                            "action": "PUBLISH|CONSUME|VALIDATE_MESSAGE|VALIDATE_RESPONSE",
                            "order": <order_number>,
                            "reason": "<dependency_reason_from_metadata>",
                            "key": {{
                                "type": "producer_key"|"message_key", 
                                "value": "<key_value>",
                                "entrypoint_attribute": "<attribute_from_input_message>"  # MANDATORY for producer_key, null for message_key if no relationship
                            }}  # MANDATORY for ALL VALIDATE_MESSAGE actions
                        }
                    ],
                    "setup_dependencies": [
                        {
                            "type": "http|graphql|kafka|external",
                            "http_url": "<url>",
                            "template_url": "<generalize url>",
                            "http_method": "<method>",
                            "http_status_code": <status code>,
                            "graphql_query": "<operation_name>",  # ONLY for GraphQL endpoints
                            "graphql_operation": "QUERY|MUTATION|SUBSCRIPTION",  # ONLY for GraphQL endpoints
                            "topic": "<topic_name>",
                            "action": "SUBSCRIBE|PUBLISH|CONSUME",
                            "external_type": "DATABASE_SQL|DATABASE_MONGODB|HTTP_REST|HTTP_GRAPHQL|MESSAGING_KAFKA|MESSAGING_RABBITMQ|EMAIL_SENDING",
                            "order": <order_number>,
                            "reason": "<dependency_reason_from_metadata>"
                        }
                    ],
                    "teardown_dependencies": [
                        {
                            "type": "http|graphql|kafka|external",
                            "http_url": "<url>",
                            "template_url": "<generalize url>",
                            "http_method": "<method>",
                            "http_status_code": <status code>,
                            "graphql_query": "<operation_name>",  # ONLY for GraphQL endpoints
                            "graphql_operation": "QUERY|MUTATION|SUBSCRIPTION",  # ONLY for GraphQL endpoints
                            "topic": "<topic_name>",
                            "action": "UNSUBSCRIBE|DELETE",
                            "external_type": "DATABASE_SQL|DATABASE_MONGODB|HTTP_REST|HTTP_GRAPHQL|MESSAGING_KAFKA|MESSAGING_RABBITMQ|EMAIL_SENDING",
                            "order": <order_number>,
                            "reason": "<dependency_reason_from_metadata>"
                        }
                    ],
                    "open_questions": [
                        "<essential_question_1_to_execute_playbook>",
                        "<essential_question_2_to_execute_playbook>"
                    ]
                }
            
            - Example HTTP Endpoint: 
                {
                    "execution_dependencies": [
                        {
                            "type": "http",
                            "http_url": "/api/resource/{id}",
                            "template_url": "/api/resource/{id}",
                            "http_method": "PUT",
                            "http_status_code": 200,
                            "order": 1,
                            "reason": "Primary endpoint execution for updating resource",
                            "action": "VALIDATE_RESPONSE"
                        }
                    ],
                    "setup_dependencies": [
                        {
                            "type": "http",
                            "http_url": "/api/resource",
                            "template_url": "/api/resource",
                            "http_method": "POST",
                            "http_status_code": 201,
                            "order": 1,
                            "reason": "Precondition requires 'Resource must exist' and dependencies_input_data needs 'resource_id'"
                        },
                        {
                            "type": "kafka",
                            "topic": "system-events",
                            "action": "SUBSCRIBE",
                            "order": 2,
                            "reason": "External dependency requires subscribing to system events topic"
                        }
                    ],
                    "teardown_dependencies": [
                        {
                            "type": "http",
                            "http_url": "/api/resource/{id}",
                            "template_url": "/api/resource/{id}",
                            "http_method": "DELETE",
                            "http_status_code": 204,
                            "order": 1,
                            "reason": "Cleanup for postcondition 'Resource updated'"
                        },
                        {
                            "type": "kafka",
                            "topic": "system-events",
                            "action": "UNSUBSCRIBE",
                            "order": 2,
                            "reason": "Cleanup for Kafka subscription"
                        }
                    ]
                }
            
            - Example HTTP Endpoint with Kafka External Dependency:
                {
                    "execution_dependencies": [
                        {
                            "type": "http",
                            "http_url": "/api/resource",
                            "template_url": "/api/resource",
                            "http_method": "POST",
                            "http_status_code": 201,
                            "order": 1,
                            "reason": "Primary endpoint execution for creating resource",
                            "action": "VALIDATE_RESPONSE"
                        },
                        {
                            "type": "kafka",
                            "topic": "resource-events", 
                            "action": "VALIDATE_MESSAGE",
                            "order": 2,
                            "reason": "Validate that the endpoint correctly published message to external Kafka topic",
                            "key": {{"type": "producer_key", "value": "userId", "entrypoint_attribute": "id"}}
                        }
                    ],
                    "setup_dependencies": [
                        {
                            "type": "http",
                            "http_url": "/api/orders",
                            "template_url": "/api/orders",
                            "http_method": "POST",
                            "http_status_code": 201,
                            "order": 1,
                            "reason": "Precondition requires 'Order must exist' before publishing event"
                        },
                        {
                            "type": "kafka",
                            "topic": "order-events",
                            "action": "SUBSCRIBE",
                            "order": 2,
                            "reason": "External dependency requires subscribing to validate message publication"
                        }
                    ],
                    "teardown_dependencies": [
                        {
                            "type": "kafka",
                            "topic": "order-events",
                            "action": "UNSUBSCRIBE",
                            "order": 1,
                            "reason": "Cleanup for Kafka subscription"
                        }
                    ]
                }
        
            - If you do not find any information for the above key set value as null
            - setup_dependencies: Array of dependencies that must run before the main API
            - teardown_dependencies: Array of dependencies that must run after the main API
            - order: Indicates the sequence in which dependencies should be executed (1 being first)
            - reason: Explanation of why this dependency exists based on metadata analysis
        
        ADDITIONAL STATIC RULES AND GUIDANCE:
        
        VERIFICATION KEY EXTRACTION FOR VALIDATE_MESSAGE ACTIONS (Kafka):
        - For EVERY VALIDATE_MESSAGE action of type "kafka", you MUST include a "key" field
        - Determine key.type strictly from external dependency AsyncAPI's x-verification-key.key_priority
          * "producer_first" → type="producer_key"
          * "message_only"   → type="message_key"
        - Extract key.value ONLY from:
          * producer_key_field (for producer_key), or
          * message_key_field (for message_key)
        - Extract key.entrypoint_attribute using flow tracking:
          * producer_key_flow_tracking:
            - relationship_type="direct_mapping" → use entrypoint_attribute when present
            - relationship_type="direct-value"   → extract attribute name from generate_value (e.g., item.getId().toString() → "id")
            - relationship_type="none"           → null
          * message_key_flow_tracking:
            - if entrypoint relationship exists → use entrypoint_attribute
            - otherwise → null
        - If there is no verification key metadata for that external dependency, DO NOT create VALIDATE_MESSAGE for it.
        
        CRITICAL VALIDATION LOGIC BASED ON KEY TYPE:
        * If key type is "producer_key" with entrypoint_attribute: Validates the **Kafka message key** matches input
          - Complete Flow: Store variable → Consume with key filter → Validate key matches
          - Example: key={{"type": "producer_key", "value": "id", "entrypoint_attribute": "id"}} 
            1. "Store todo-item-id as ${{message.id}}"
            2. "Consume messages from 'topic' and filter by the key ${{todo-item-id}} and store in messageFromTopic"
            3. "Verify {{{{messageFromTopic}}}} key is same of ${{todo-item-id}}"
        * If key type is "producer_key" with null/missing entrypoint_attribute: Validates the **Kafka message key exists**
          - Complete Flow: Consume → Validate key exists
          - Example: key={{"type": "producer_key", "value": "id", "entrypoint_attribute": null}}
            1. "Consume messages from 'topic' and store in messageFromTopic"
            2. "Verify {{{{messageFromTopic}}}} key exists"
        * If key type is "message_key" with entrypoint_attribute: Validates a **field inside the message body**
          - Complete Flow: Store variable → Consume with field filter → Validate field equals
          - Example: key={{"type": "message_key", "value": "userId", "entrypoint_attribute": "id"}}
            1. "Store user-id as ${{message.id}}"
            2. "Consume messages from 'user-events' and filter by userId equals ${{user-id}} and store in messageFromUserEvents"
            3. "Verify {{{{messageFromUserEvents.userId}}}} equals ${{user-id}}"
        * If key type is "message_key" with null entrypoint_attribute: Only checks field existence
          - Complete Flow: Consume → Validate field exists
          - Example: key={{"type": "message_key", "value": "auditId", "entrypoint_attribute": null}}
            1. "Consume messages from 'audit-events' and store in messageFromAuditEvents"
            2. "Verify {{{{messageFromAuditEvents}}}} contains auditId field"
        
        CRITICAL KAFKA CONSUMER ENDPOINT RULES:
        - If a consumer endpoint has NO external dependencies:
          * Execution: ONLY include PUBLISH action to trigger the consumer
          * Setup:     Empty (no SUBSCRIBE needed)
          * Teardown:  Empty (no UNSUBSCRIBE needed)
          * DO NOT add VALIDATE_MESSAGE for the input topic - we just published it, we know everything about it
          * NEVER validate messages we published ourselves
        - If external dependencies exist (endpoint publishes to other topics):
          * Setup: create SUBSCRIBE action to listen for messages that will be published by the endpoint
            - CRITICAL: SUBSCRIBE must be the LAST action in setup (highest order number)
            - All other setup actions (HTTP calls, resource creation) must come before SUBSCRIBE
          * Execution (from test perspective): 
            - For HTTP endpoints: include the primary HTTP endpoint call, then for each external Kafka dependency: CONSUME (external topic) and VALIDATE_MESSAGE (external topic) actions
            - For Kafka CONSUME endpoints: include PUBLISH (to trigger consumer), CONSUME (external topic), and VALIDATE_MESSAGE (external topic) actions
            - For Kafka CONSUME endpoints with multiple external topics: include PUBLISH (input topic), then CONSUME and VALIDATE_MESSAGE for each external topic
            - For Kafka PUBLISH endpoints: include PUBLISH (primary topic) and VALIDATE_MESSAGE (primary topic) actions
          * Teardown: create UNSUBSCRIBE action to cleanup subscription
            - CRITICAL: UNSUBSCRIBE must be the FIRST action in teardown (lowest order number)
            - All other teardown actions (DELETE, cleanup) must come after UNSUBSCRIBE
        
        STRUCTURED METADATA ANALYSIS METHODOLOGY:
        
        1. SETUP DEPENDENCY IDENTIFICATION:
           a) PRECONDITION ANALYSIS:
              - Look for preconditions like "User must exist", "Resource must be present"
              - Find APIs with crud_operation: "CREATE" that can satisfy these preconditions
              - Match postconditions of potential setup APIs to current API's preconditions
           
           b) DATA FLOW ANALYSIS:
              - Examine dependencies_input_data of target API
              - Find APIs whose dependencies_output_data matches the required input
              - Example: Target needs "user_id from /auth/login" → Setup: /auth/login API
           
           c) EXTERNAL DEPENDENCY SETUP:
              - For Kafka external dependencies: add SUBSCRIBE actions
              - For HTTP external dependencies: add HTTP calls to other services
              - For database external dependencies: add database setup operations
           
           d) CRUD OPERATION PATTERNS:
              - If target has UPDATE/DELETE operation, look for CREATE operations on same resource
              - If target requires authentication, look for AUTHENTICATE operations
              - For GraphQL: Query with ID parameter needs CREATE mutation, UPDATE/DELETE mutations need CREATE mutation
              - For GraphQL: Match operations by resource name (e.g., "todo" query needs "createTodo" mutation)
        
        2. TEARDOWN DEPENDENCY IDENTIFICATION:
           a) POSTCONDITION CLEANUP:
              - Examine postconditions of target API (what it creates/modifies)
              - ONLY include teardown for postconditions that are CLEANUP ACTIONS
              - FORBIDDEN: Do NOT create teardown for positive outcomes like "User created", "Data saved"
              - Find APIs that can clean up resources created in preconditions (usually DELETE operations)
              - Look for APIs that reverse the target's preconditions, not postconditions
           
           b) EXTERNAL DEPENDENCY CLEANUP:
              - For Kafka external dependencies: add UNSUBSCRIBE actions
              - For HTTP external dependencies: add cleanup HTTP calls
              - For database external dependencies: add cleanup operations
           
           c) SIDE EFFECT CLEANUP:
              - Analyze external_dependencies array for external changes
              - Find cleanup APIs for notifications, cache updates, logs, etc.
              - Match cleanup operations to side effects
           
           d) RESOURCE CLEANUP:
              - For CREATE operations, find corresponding DELETE operations
              - For resource modifications, find reset/cleanup operations
              - For GraphQL: Queries with ID parameters need DELETE mutation in teardown to clean up data created in setup
              - For GraphQL: Match cleanup operations by resource name (e.g., "todo" query needs "deleteTodo" mutation in teardown)
        
        3. DEPENDENCY PRIORITY AND ORDERING:
           - Order setup dependencies by data flow requirements
           - Authentication/authorization should come first
           - Resource creation before resource usage
           - External dependency setup before main execution
           - Data dependencies in correct sequence
        
        4. METADATA-DRIVEN REASONING:
           - Always include 'reason' field explaining metadata-based logic
           - Reference specific metadata fields that drove the dependency decision
           - Be explicit about which precondition, postcondition, or external dependency created the dependency
        
        FIELD-SPECIFIC ANALYSIS GUIDELINES:
        - summary_of_functionality: Understand business context and workflow position
        - preconditions:          Drive setup requirements
        - postconditions:         Drive teardown needs ONLY for cleanup actions (not positive outcomes)
        - external_dependencies:  Drive additional setup/teardown (Kafka/HTTP/DB/etc.)
        - dependencies_input_data / dependencies_output_data: Determine data-flow dependencies
        - crud_operation:         Influences patterns (CREATE→setup for later UPDATE/DELETE)
        
        TEARDOWN DEPENDENCY ANALYSIS RULES:
        - 🚨 CRITICAL: Only include teardown dependencies for postconditions that are CLEANUP ACTIONS
        - 🚨 FORBIDDEN: Do NOT create teardown dependencies for positive outcomes like "User account is created"
        - 🚨 MANDATORY: Teardown dependencies should UNDO what was set up in preconditions
        - 🚨 EXAMPLE: If precondition is "Invitation must exist" → teardown should be "DELETE /invites/{id}"
        - 🚨 EXAMPLE: If postcondition is "User account is created" → NO teardown needed (this is a positive outcome)
        - 🚨 EXAMPLE: If postcondition is "Temporary data is cleared" → NO teardown needed (cleanup already happened)
        - 🚨 CRITICAL: Only create teardown dependencies for resources that were created/modified and need cleanup
        
        UNIFIED METADATA-FOCUSED ANALYSIS:
        - Rely exclusively on x-baserock-operation-metadata fields for dependency identification
        - Handle HTTP and Kafka endpoints using the same unified approach
        
        OUTPUT CONTRACT REMINDER:
        - Return ONLY the unified JSON object described above (no prose)
        - Include 'type' for each dependency (http|kafka|external)
        - Include 'reason' that references specific metadata used for the decision
        - Ensure order values reflect a correct execution sequence
        - Model Kafka subscribe/unsubscribe patterns according to the rules above
        
        UNIFIED DEPENDENCY ANALYSIS APPROACH:
        - Analyze BOTH HTTP and Kafka endpoints using the same metadata-driven approach
        - Handle external dependencies (database, messaging, HTTP calls) for both endpoint types
        - For Kafka endpoints: identify subscribe/unsubscribe patterns for external dependencies
        - For HTTP endpoints: identify HTTP calls to other services as external dependencies
        
        UNIFIED DEPENDENCY HANDLING:
        - HTTP endpoints can have Kafka external dependencies (subscribe/unsubscribe)
        - Kafka endpoints can have HTTP external dependencies (REST calls)
        - Both can have database, email, and other external dependencies
        - For each Kafka PUBLISH in external dependencies, create SUBSCRIBE/UNSUBSCRIBE pairs
        
        COMPREHENSIVE UNIFIED ANALYSIS APPROACH:
        For the target API, analyze its structured metadata fields and compare against all available APIs to:
        - Identify setup dependencies based on preconditions and input data requirements
        - Identify teardown dependencies based on postconditions and side effects
        - Handle external dependencies appropriately based on their types
        - For HTTP external dependencies: create appropriate HTTP calls for setup/teardown
        - Provide clear reasoning for each dependency based on specific metadata fields
        - Order dependencies logically based on data flow and execution requirements
        
        Focus on structured metadata field analysis rather than pattern matching. Use the explicit relationships defined in the metadata.
        Handle HTTP, GraphQL, and Kafka endpoints in a unified manner with proper external dependency management.
        Process external dependencies and create appropriate setup/teardown actions based on their types.
        
        CRITICAL: ENDPOINT TYPE IDENTIFICATION:
        - If metadata contains "graphql_query" and "graphql_operation" fields → use type: "graphql"
        - If endpoint has "consumer_topic" or "producer_topic" → use type: "kafka"
        - Otherwise → use type: "http"
        - For GraphQL endpoints, ALWAYS include graphql_query and graphql_operation fields in the dependency entry
        - For GraphQL endpoints with action "VALIDATE_RESPONSE", ALWAYS include graphql_complete_query field from metadata (the complete GraphQL query string)
        
        CRITICAL: GRAPHQL CRUD PATTERNS FOR DEPENDENCY IDENTIFICATION:
        - GraphQL QUERY with ID parameter (e.g., todo(id: ID!)): ALWAYS needs CREATE mutation in setup and DELETE mutation in teardown
          * Look for GraphQL MUTATION with crud_operation="CREATE" that creates the same resource type
          * Look for GraphQL MUTATION with crud_operation="DELETE" that deletes the same resource type
          * Example: query "todo" needs mutation "createTodo" in setup and mutation "deleteTodo" in teardown
        - GraphQL QUERY without parameters (e.g., todos): Usually no setup/teardown unless authentication required
        - GraphQL MUTATION with crud_operation="UPDATE": Needs CREATE mutation in setup and DELETE mutation in teardown
        - GraphQL MUTATION with crud_operation="DELETE": Needs CREATE mutation in setup only
        - GraphQL MUTATION with crud_operation="CREATE": Usually needs DELETE mutation in teardown only
        - MATCHING PATTERN: Match based on resource name (todo/todos/createTodo/updateTodo/deleteTodo all refer to "todo" resource)
        
        MINIMUM DEPENDENCY GRAPH REQUIREMENT:
        Every dependency graph MUST have at least one execution_dependency - the target API itself.
        The execution_dependencies array must contain the target API with:
        - type: "http", "graphql", or "kafka" (based on target API type)
          * Use "graphql" if the metadata contains graphql_query and graphql_operation fields
          * Use "http" for standard REST/HTTP endpoints (no graphql_query field)
          * Use "kafka" for Kafka endpoints (has consumer_topic or producer_topic)
        - http_url/topic: Use target API's URL or topic
        - template_url: Use target API's template URL
        - http_method: Use target API's HTTP method
        - http_status_code: Use target API's status code
        - graphql_query: Use target API's graphql_query (ONLY for GraphQL endpoints)
        - graphql_operation: Use target API's graphql_operation (ONLY for GraphQL endpoints)
        - graphql_complete_query: Use target API's graphql_complete_query from metadata (ONLY for GraphQL endpoints with VALIDATE_RESPONSE action)
        - order: 1 (first execution step)
        - reason: For GraphQL endpoints, use format "Call GraphQL endpoint for {{graphql_complete_query}} with variables [variable_names]" where variable_names are extracted from the query (e.g., "Call GraphQL endpoint for query { todos { id name } } with variables []" or "Call GraphQL endpoint for mutation($input: CreateTodoInput!) { createTodo(input: $input) { id } } with variables [input]"). For HTTP/Kafka, use "Primary endpoint execution for [target API functionality]"
        - action: "VALIDATE_RESPONSE" for HTTP/GraphQL or "PUBLISH"/"CONSUME" for Kafka
        
        CRITICAL REMINDER FOR VALIDATE_MESSAGE ACTIONS:
        - Every VALIDATE_MESSAGE action of type "kafka" MUST include a "key" field
        - Use the external dependency AsyncAPI's x-verification-key metadata strictly
        - Determine key.type from key_priority ("producer_first"→producer_key, "message_only"→message_key)
        - Extract key.value and key.entrypoint_attribute ONLY from x-verification-key (do NOT invent names)
        - If no verification key metadata is found for that external dependency, DO NOT create VALIDATE_MESSAGE for it
        
        OPEN QUESTIONS GENERATION RULES:
        Generate open_questions ONLY for essential information needed to successfully execute the playbook.
        Focus on preconditions and dependencies_input_data that require external knowledge to resolve.
        🚨 CRITICAL: Extract and preserve TECHNICAL DETAILS from preconditions in the open questions.
        
        RULES FOR GENERATING OPEN QUESTIONS:
        1. Analyze PRECONDITIONS WITH TECHNICAL DETAIL EXTRACTION:
           - Extract authentication method (Basic Auth, Bearer, JWT, API Key)
           - Extract header name (Authorization, X-API-Key, custom header)
           - Extract any other technical specifications (format, location, etc.)
           - Preserve these details in the question
           
           Examples of CORRECT question generation:
           - Precondition: "User must be authenticated using Basic Auth credentials in Authorization header"
             → Question: "How do I get valid Basic Auth credentials for the Authorization header?"
           
           - Precondition: "User must be authenticated using Bearer token in Authorization header"
             → Question: "How do I get a valid Bearer token for the Authorization header?"
           
           - Precondition: "User must be authenticated using JWT token in Authorization header"
             → Question: "How do I get a valid JWT token for the Authorization header?"
           
           - Precondition: "User must be authenticated using API key in X-API-Key header"
             → Question: "How do I get a valid API key for the X-API-Key header?"
           
           - Precondition: "Admin user must be authenticated using Bearer token in Authorization header"
             → Question: "How do I get a valid Bearer token for admin user authentication in the Authorization header?"
        
        2. Analyze DEPENDENCIES_INPUT_DATA: For each input data requirement:
           - If it mentions "from authentication context" or similar → consolidate with authentication question
           - If it mentions "from [service/endpoint]" but the endpoint is not in the API list → ask how to obtain it
           - Include specific format/location details in the question
        
        3. CONSOLIDATE RELATED QUESTIONS: If multiple preconditions/inputs can be answered by ONE fundamental question, keep only that one
           - Example: "authentication principal" and "inviter user" → consolidate to "How do I get a valid authentication principal?"
           - The authentication principal IS the logged-in user, so one question covers both preconditions
        
        4. EXCLUDE questions about:
           - Database access (assumed available)
           - Email/notification services (assumed configured)
           - Generic validation rules (not execution blockers)
           - Test scenarios (this is about EXECUTION, not testing)
        
        5. OUTPUT FORMAT:
           - open_questions is an array of strings
           - Each string is a clear, actionable question starting with "How do I..."
        
        6. RETURN EMPTY ARRAY if:
           - All preconditions can be satisfied by existing APIs in the reference list
           - No external information is needed to execute the endpoint
           - The endpoint is self-contained with no authentication/data requirements
        
        EXAMPLE OPEN QUESTIONS:
        
        For endpoint with preconditions ["User must be authenticated using Basic Auth credentials in Authorization header", "Todo item with specified ID must exist"]:
        open_questions: [
            "How do I get valid Basic Auth credentials for the Authorization header?",
            "How do I get an existing todo item ID?"
        ]
        
        For endpoint with preconditions ["User must be authenticated using Bearer token in Authorization header"] where POST /auth/login exists in API list:
        open_questions: []  (no questions needed - can use existing POST /auth/login API to get Bearer token)
        
        For endpoint with preconditions ["Order must exist in database"] where POST /orders exists in API list:
        open_questions: []  (no questions needed - can use existing POST /orders API)
        
        ADDITIONAL EXAMPLES (GUIDANCE ONLY):
        
        GraphQL Query Endpoint Example (List Query - No ID Required):
        Target API: POST /graphql (GraphQL QUERY operation "todos")
        Metadata Analysis:
        - graphql_query: "todos"
        - graphql_operation: "QUERY"
        - crud_operation: "READ"
        - preconditions: ["User authenticated"]
        - dependencies_input_data: ["auth_token from login mutation"]
        - postconditions: ["Todo list retrieved from database"]
        
        Resulting Dependencies:
        Execution:
        1. Call GraphQL endpoint for query { todos { id name completed } } with variables []
        
        Setup:
        1. Call GraphQL endpoint for mutation { login(email: String!, password: String!) { token } } with variables [email, password]
        
        Teardown:
        [] (no cleanup needed for read operation)
        
        GraphQL Query Endpoint Example (Single Item Query - ID Required):
        Target API: POST /graphql (GraphQL QUERY operation "todo")
        Metadata Analysis:
        - graphql_query: "todo"
        - graphql_operation: "QUERY"
        - graphql_complete_query: "query($id: ID!) { todo(id: $id) { id name completed } }"
        - crud_operation: "READ"
        - preconditions: ["Todo must exist in database", "Valid todo ID required"]
        - dependencies_input_data: ["todo_id from createTodo mutation"]
        - postconditions: ["Single todo retrieved"]
        
        Resulting Dependencies:
        Execution:
        1. Call GraphQL endpoint for query($id: ID!) { todo(id: $id) { id name completed } } with variables [id]
        
        Setup:
        1. Call GraphQL endpoint for mutation($name: String!, $completed: Boolean!) { createTodo(name: $name, completed: $completed) { id name completed } } with variables [name, completed]
           (Reason: Precondition "Todo must exist" requires creating a todo first)
        
        Teardown:
        1. Call GraphQL endpoint for mutation($id: ID!) { deleteTodo(id: $id) { id } } with variables [id]
           (Reason: Cleanup for the todo created in setup - prevents test data pollution)
        
        GraphQL Mutation Endpoint Example:
        Target API: POST /graphql (GraphQL MUTATION operation "createTodo")
        Metadata Analysis:
        - graphql_query: "createTodo"
        - graphql_operation: "MUTATION"
        - preconditions: ["User authenticated", "Valid input data"]
        - dependencies_input_data: ["auth_token from login mutation"]
        - postconditions: ["Todo created in database"]
        
        Resulting Dependencies:
        Execution:
        1. Call GraphQL endpoint for mutation($input: CreateTodoInput!) { createTodo(input: $input) { id name completed } } with variables [input]
        
        Setup:
        1. Call GraphQL endpoint for mutation { login(email: String!, password: String!) { token } } with variables [email, password]
        
        Teardown:
        1. Call GraphQL endpoint for mutation($id: ID!) { deleteTodo(id: $id) { id } } with variables [id]
        
        HTTP Endpoint with Kafka External Dependency:
        Target API: POST /{{resource}}
        Metadata Analysis:
        - preconditions: ["User authenticated", "Valid input data"]
        - dependencies_input_data: ["auth_token from /auth/login"]
        - postconditions: ["Resource created in database", "Notification sent", "Audit log created", "Email notification sent"]
        - external_dependencies: ["Publishes to {{service}}-notifications topic", "Publishes to {{service}}-audit topic", "Publishes to {{service}}-email topic"]
        
        Resulting Dependencies:
        Setup: 
        1. POST /auth/login (type: "http", reason: "Provides auth_token required in dependencies_input_data")
        2. SUBSCRIBE {{service}}-notifications (type: "kafka", reason: "External dependency requires subscribing to validate notification message publication - LAST in setup")
        3. SUBSCRIBE {{service}}-audit (type: "kafka", reason: "External dependency requires subscribing to validate audit message publication - LAST in setup")
        4. SUBSCRIBE {{service}}-email (type: "kafka", reason: "External dependency requires subscribing to validate email message publication - LAST in setup")
        
        Execution:
        1. POST /{{resource}} (type: "http", reason: "Primary endpoint execution for creating new resource")
        2. CONSUME {{service}}-notifications (type: "kafka", reason: "Consume the notification message produced by the endpoint as external dependency")
        3. VALIDATE_MESSAGE {{service}}-notifications (type: "kafka", reason: "Verify that the endpoint correctly published message to notification topic", key: {{"type": "producer_key", "value": "key", "entrypoint_attribute": "id"}})
        4. CONSUME {{service}}-audit (type: "kafka", reason: "Consume the audit message produced by the endpoint as external dependency")
        5. VALIDATE_MESSAGE {{service}}-audit (type: "kafka", reason: "Verify that the endpoint correctly published message to audit topic", key: {{"type": "producer_key", "value": "key", "entrypoint_attribute": "id"}})
        6. CONSUME {{service}}-email (type: "kafka", reason: "Consume the email message produced by the endpoint as external dependency")
        7. VALIDATE_MESSAGE {{service}}-email (type: "kafka", reason: "Verify that the endpoint correctly published message to email topic", key: {{"type": "producer_key", "value": "key", "entrypoint_attribute": "id"}})
        
        Teardown:
        1. UNSUBSCRIBE {{service}}-notifications (type: "kafka", reason: "Cleanup for Kafka subscription used for notification message validation - FIRST in teardown")
        2. UNSUBSCRIBE {{service}}-audit (type: "kafka", reason: "Cleanup for Kafka subscription used for audit message validation - FIRST in teardown")
        3. UNSUBSCRIBE {{service}}-email (type: "kafka", reason: "Cleanup for Kafka subscription used for email message validation - FIRST in teardown")
        4. DELETE /{{resource}}/{{id}} (type: "http", reason: "Cleanup for postcondition 'Resource created in database'")
        
        Kafka PUBLISH Endpoint with HTTP External Dependency:
        Target API: PUBLISH {{service}}-events
        Metadata Analysis:
        - preconditions: ["Event data must exist", "User authenticated"]
        - dependencies_input_data: ["event_id from /events/{{id}} GET"]
        - postconditions: ["Event published", "Notification sent"]
        - external_dependencies: ["HTTP call to external-service", "Database log updated"]
        
        Resulting Dependencies:
        Setup:
        1. POST /events (type: "http", reason: "Satisfies precondition 'Event data must exist'")
        2. POST /auth/login (type: "http", reason: "Satisfies precondition 'User authenticated'")
        
        Execution:
        1. PUBLISH {{service}}-events (type: "kafka", reason: "Primary endpoint execution for publishing event")
        2. VALIDATE_MESSAGE {{service}}-events (type: "kafka", reason: "Validate that the message was correctly published")
        
        Teardown:
        1. DELETE /notifications/{{id}} (type: "http", reason: "Cleanup for external dependency 'HTTP call to external-service'")
        
        Kafka CONSUME Endpoint with NO External Dependencies:
        Target API: CONSUME {{service}}-audit
        Metadata Analysis:
        - preconditions: ["Kafka topic '{{service}}-audit' must exist"]
        - dependencies_input_data: ["Audit message JSON from {{service}}-audit topic"]
        - postconditions: ["Audit message processed and logged"]
        - external_dependencies: [] (EMPTY - no external dependencies)
        
        Resulting Dependencies:
        Setup:
        (Empty - no setup needed)
        
        Execution:
        1. PUBLISH {{service}}-audit (type: "kafka", reason: "Trigger the consumer endpoint by publishing message to its input topic")
        
        Teardown:
        (Empty - no teardown needed)
        
        CRITICAL: Do NOT add VALIDATE_MESSAGE for the input topic. We just published the message, so we already know everything about it. Only validate messages consumed from external dependency topics.
        
        MANDATORY EXECUTION DEPENDENCY RULE:
        - The TARGET API must ALWAYS be included in execution_dependencies with action="VALIDATE_RESPONSE"
        - This is the primary endpoint being tested - it cannot be empty
        - Use the target API's own metadata (http_url, template_url, http_method, http_status_code) for the execution dependency
        
        Kafka CONSUME Endpoint with Kafka PUBLISH External Dependency:
        Target API: CONSUME {{service}}-input
        Metadata Analysis:
        - preconditions: ["Kafka topic '{{service}}-input' must exist", "Processing service must be available"]
        - dependencies_input_data: ["Message JSON from {{service}}-input topic"]
        - postconditions: ["Message processed", "Processing status logged"]
        - external_dependencies: ["Produces result message to {{service}}-output"]
        
        Resulting Dependencies:
        Setup:
        1. SUBSCRIBE {{service}}-output (type: "kafka", reason: "External dependency requires subscribing to validate result message publication - LAST in setup")
        
        Execution:
        1. PUBLISH {{service}}-input (type: "kafka", reason: "Trigger the consumer endpoint by publishing message to its input topic")
        2. CONSUME {{service}}-output (type: "kafka", reason: "Consume the result message produced by the endpoint as external dependency")
        3. VALIDATE_MESSAGE {{service}}-output (type: "kafka", reason: "Validate that the result message was correctly published to external topic", key: {{"type": "producer_key", "value": "correlationId", "entrypoint_attribute": "messageId"}})
        
        Teardown:
        1. UNSUBSCRIBE {{service}}-output (type: "kafka", reason: "Cleanup for Kafka subscription used for validation - FIRST in teardown")
        
        Kafka CONSUME Endpoint with Multiple Kafka PUBLISH External Dependencies:
        Target API: CONSUME {{service}}-events
        Metadata Analysis:
        - preconditions: ["Kafka topic '{{service}}-events' must exist", "Notification service must be available", "Analytics service must be available"]
        - dependencies_input_data: ["Event JSON from {{service}}-events topic"]
        - postconditions: ["Event processed", "Customer notified", "Analytics updated"]
        - external_dependencies: ["Publishes notification to {{service}}-notifications topic", "Publishes analytics data to {{service}}-analytics topic"]
        
        Resulting Dependencies:
        Setup:
        1. SUBSCRIBE {{service}}-notifications (type: "kafka", reason: "External dependency requires subscribing to validate notification message publication - LAST in setup")
        2. SUBSCRIBE {{service}}-analytics (type: "kafka", reason: "External dependency requires subscribing to validate analytics message publication - LAST in setup")
        
        Execution:
        1. PUBLISH {{service}}-events (type: "kafka", reason: "Trigger the consumer endpoint by publishing message to its input topic")
        2. CONSUME {{service}}-notifications (type: "kafka", reason: "Consume the notification message produced by the endpoint as external dependency")
        3. CONSUME {{service}}-analytics (type: "kafka", reason: "Consume the analytics message produced by the endpoint as external dependency")
        4. VALIDATE_MESSAGE {{service}}-notifications (type: "kafka", reason: "Validate that the notification message was correctly published to external topic", key: {{"type": "producer_key", "value": "eventId", "entrypoint_attribute": "id"}})
        5. VALIDATE_MESSAGE {{service}}-analytics (type: "kafka", reason: "Validate that the analytics message was correctly published to external topic", key: {{"type": "message_key", "value": "analyticsId", "entrypoint_attribute": null}})
        
        Teardown:
        1. UNSUBSCRIBE {{service}}-notifications (type: "kafka", reason: "Cleanup for Kafka subscription used for validation - FIRST in teardown")
        2. UNSUBSCRIBE {{service}}-analytics (type: "kafka", reason: "Cleanup for Kafka subscription used for validation - FIRST in teardown")
        
        CRITICAL KEY FIELD EXTRACTION FROM X-VERIFICATION-KEY:
        When processing external dependencies with VALIDATE_MESSAGE actions:
        - Extract the verification key information from the external dependency's x-verification-key metadata
        - **key.type**: Use key_priority to determine type ("producer_first" → "producer_key", "message_only" → "message_key")
        - **key.value**: 
          * If type="producer_key": Use producer_key_field value
          * If type="message_key": Use message_key_field value
        - **key.entrypoint_attribute**: Extract from flow tracking:
          * If type="producer_key": 
            - If producer_key_flow_tracking.relationship_type="direct_mapping": 
              - If entrypoint_attribute exists: Use producer_key_flow_tracking.entrypoint_attribute
              - If generate_value exists: Extract attribute from producer_key_flow_tracking.generate_value (e.g., "{{id}}" → "id")
            - If producer_key_flow_tracking.relationship_type="direct-value": Extract attribute from producer_key_flow_tracking.generate_value (e.g., "item.getId().toString()" → "id")
            - If producer_key_flow_tracking.relationship_type="none": Set to null
          * If type="message_key" with entrypoint relationship: Use message_key_flow_tracking.entrypoint_attribute
          * If type="message_key" with NO entrypoint relationship: Set to null
        - Example extraction from x-verification-key:
          ```
          "x-verification-key": {{
            "producer_key_field": "key",
            "message_key_field": "id",
            "key_priority": "producer_first",
            "producer_key_flow_tracking": {{
              "relationship_type": "direct-value",
              "generate_value": "item.getId().toString()"
            }}
          }}
          → key: {{"type": "producer_key", "value": "key", "entrypoint_attribute": "id"}}
          ```
          
          ```
          "x-verification-key": {{
            "producer_key_field": "userId",
            "message_key_field": "id",
            "key_priority": "producer_first",
            "producer_key_flow_tracking": {{
              "relationship_type": "direct_mapping",
              "entrypoint_attribute": "id"
            }}
          }}
          → key: {{"type": "producer_key", "value": "userId", "entrypoint_attribute": "id"}}
          ```
        """
        
        self.EXAMPLE_END_POINTS = r"""
                {
                    "execution_dependencies": {
                        "http_url": "/api/resource/{id}",
                        "template_url": "/api/resource/{id}",
                        "http_method": "PUT",
                        "http_status_code": 200
                    },
                    "setup_dependencies": [
                        {
                            "http_url": "/api/resource",
                            "template_url": "/api/resource",
                            "http_method": "POST",
                            "http_status_code": 200,
                            "order": 1,
                            "reason": "Precondition requires 'Resource must exist' for update operation"
                        }
                    ],
                    "teardown_dependencies": [
                        {
                            "http_url": "/api/resource/{id}/cleanup",
                            "template_url": "/api/resource/{id}/cleanup",
                            "http_method": "DELETE",
                            "http_status_code": 200,
                            "order": 1,
                            "reason": "Cleanup for postcondition 'Resource data modified' and side_effect 'Cache invalidated'"
                        }
                    ]
                }
            """
        self.GET_END_POINT_DEPENDENCIES_USER_PROMPT = f"""You are analyzing a specific API endpoint to identify its dependencies and relationships in a UNIFIED manner.
        Your task is to identify all dependencies for the TARGET API and classify them as either SETUP or TEARDOWN dependencies, handling HTTP, GraphQL, and Kafka endpoints.
        
        🚨 CRITICAL: ENDPOINT TYPE DETECTION:
        - Check the TARGET API's metadata for "graphql_query" and "graphql_operation" fields
        - If both fields are present → use type: "graphql" and include graphql_query and graphql_operation in the dependency entry
        - For GraphQL endpoints with action "VALIDATE_RESPONSE", ALWAYS include graphql_complete_query from metadata (the complete GraphQL query string)
        - If endpoint has "consumer_topic" or "producer_topic" → use type: "kafka"
        - Otherwise → use type: "http"

        CONTEXT
        -------
        EXTERNAL DEPENDENCIES INFORMATION:
        {self._format_external_dependencies()}

        TARGET API FOR ANALYSIS
        ------------------------
        🎯 PRIMARY ENDPOINT TO ANALYZE:
        {self.api}
        
        🔧 Programming Language Context: {self.language_config.name}
        
        📋 REFERENCE APIS (for finding dependencies):
        The following APIs are available as potential dependencies. Use these to find setup/teardown dependencies for the TARGET API above:
        {self.apis_list}

        TASK
        ----
        Analyze the TARGET API and produce a complete dependency graph with the following structure:
        
        1. **EXECUTION_DEPENDENCIES**: MUST include the TARGET API itself as the primary execution step
           - Always include: TARGET API with appropriate action based on its type
           - Add any external dependency validations (Kafka VALIDATE_MESSAGE actions)
        
        2. **SETUP_DEPENDENCIES**: Find APIs from reference list that must run BEFORE the target
           - Look for APIs that satisfy preconditions or provide required input data
           - Include external dependency setup (Kafka SUBSCRIBE, HTTP calls, etc.)
        
        3. **TEARDOWN_DEPENDENCIES**: Find APIs from reference list that must run AFTER the target
           - Look for APIs that clean up postconditions or side effects
           - Include external dependency cleanup (Kafka UNSUBSCRIBE, HTTP calls, etc.)
        
        CRITICAL: The TARGET API itself must ALWAYS be in execution_dependencies. Never return empty execution_dependencies.
        
        Using ONLY the rules and output contract defined in the system prompt, analyze the TARGET API and produce the unified dependency JSON. Do not include explanations or prose.
        """
    
    def _format_external_dependencies(self):
        """Format external dependencies for the LLM prompt"""
        if not self.external_dependencies:
            return "No external dependencies found for this endpoint."
        
        formatted = "The endpoint has the following external dependencies that need to be handled:\n\n"
        for idx, ext_dep in enumerate(self.external_dependencies, 1):
            formatted += self._format_single_external_dependency(idx, ext_dep)
        
        return formatted

    def _format_single_external_dependency(self, idx: int, ext_dep: dict) -> str:
        """Format a single external dependency."""
        dep_type = ext_dep.get('type', 'UNKNOWN')
        formatted = f"{idx}. Type: {dep_type}\n"
        
        if dep_type == 'MESSAGING_KAFKA':
            formatted += self._format_kafka_dependency(ext_dep)
        elif 'HTTP_' in dep_type:
            formatted += self._format_http_dependency(ext_dep)
        else:
            formatted += self._format_generic_dependency(ext_dep)
        
        return formatted + "\n"

    def _format_kafka_dependency(self, ext_dep: dict) -> str:
        """Format Kafka external dependency details."""
        topic = ext_dep.get('topic', 'unknown')
        description = ext_dep.get('description', '')
        formatted = f"   - Kafka Topic: {topic}\n"
        formatted += f"   - Description: {description}\n"
        formatted += "   - Required Actions: SUBSCRIBE (setup), UNSUBSCRIBE (teardown)\n"
        
        # Add x-verification-key details if present
        verification_key_details = self._extract_verification_key_details(ext_dep)
        if verification_key_details:
            formatted += verification_key_details
        
        return formatted

    @staticmethod
    def _format_http_dependency(ext_dep: dict) -> str:
        """Format HTTP external dependency details."""
        description = ext_dep.get('description', '')
        formatted = f"   - Description: {description}\n"
        formatted += "   - Required Actions: HTTP calls for setup/teardown\n"
        return formatted

    @staticmethod
    def _format_generic_dependency(ext_dep: dict) -> str:
        """Format generic external dependency details."""
        description = ext_dep.get('description', '')
        return f"   - Description: {description}\n"

    def _extract_verification_key_details(self, ext_dep: dict) -> str:
        """Extract and format x-verification-key details from external dependency."""
        try:
            spec = ext_dep.get('spec', {})
            messages = spec.get('components', {}).get('messages', {})
            first_msg = next(iter(messages.values())) if messages else None
            
            if not first_msg or 'x-verification-key' not in first_msg:
                return ""
            
            return self._format_verification_key_metadata(first_msg['x-verification-key'])
        except (KeyError, TypeError, AttributeError, StopIteration):
            # Non-fatal: continue without embedding x-verification-key details
            return ""

    def _format_verification_key_metadata(self, xvk: dict) -> str:
        """Format x-verification-key metadata details."""
        formatted = "   - x-verification-key (STRICT - use exactly these values):\n"
        formatted += f"     * key_priority: {xvk.get('key_priority')}\n"
        formatted += f"     * producer_key_field: {xvk.get('producer_key_field')}\n"
        formatted += f"     * message_key_field: {xvk.get('message_key_field')}\n"
        
        # Add producer key flow tracking
        producer_key_details = self._format_flow_tracking_details(
            xvk.get('producer_key_flow_tracking', {}), 
            "producer_key_flow_tracking"
        )
        if producer_key_details:
            formatted += producer_key_details
        
        # Add message key flow tracking
        message_key_details = self._format_flow_tracking_details(
            xvk.get('message_key_flow_tracking', {}), 
            "message_key_flow_tracking"
        )
        if message_key_details:
            formatted += message_key_details
        
        return formatted

    @staticmethod
    def _format_flow_tracking_details(flow_tracking: dict, tracking_type: str) -> str:
        """Format flow tracking details for producer or message key."""
        if not flow_tracking:
            return ""
        
        formatted = f"     * {tracking_type}:\n"
        formatted += f"       - relationship_type: {flow_tracking.get('relationship_type')}\n"
        
        if 'entrypoint_attribute' in flow_tracking:
            formatted += f"       - entrypoint_attribute: {flow_tracking.get('entrypoint_attribute')}\n"
        
        if 'generate_value' in flow_tracking:
            formatted += f"       - generate_value: {flow_tracking.get('generate_value')}\n"
        
        return formatted