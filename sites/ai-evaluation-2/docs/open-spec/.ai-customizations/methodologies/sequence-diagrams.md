# Sequence Diagram Methodology

**Applicable Modes**: Solution Architect, Orchestrator

## Overview

Sequence diagrams are essential for visualizing system interactions over time. They help communicate complex flows, identify integration points, and validate architectural designs. All sequence diagrams must be created using PlantUML per UDX standards and must pass the UDX PlantUML linter validation.

## Diagram Location Convention

Sequence diagrams live in two distinct locations based on scope:

| Location | Scope | Example |
|----------|-------|---------|
| `diagrams/Service/[service-name].puml` | Interactions **INSIDE** a single microservice — internal logic, data store access, 3rd-party API calls | `diagrams/Service/ms-ohip-reservations.puml` |
| `diagrams/Solution/[Domain]/[domain]-sequence.puml` | Interactions **BETWEEN** microservices — cross-service orchestration and data flow | `diagrams/Solution/Hotels/hotels-sequence.puml` |

**Rule**: If a diagram shows how multiple microservices coordinate to accomplish a workflow, it belongs in `Solution/`. If it shows what happens inside one microservice when an endpoint is called, it belongs in `Service/`.

## UDX PlantUML Linter Requirements

Our organization uses a PlantUML linter to ensure diagram quality and compliance. The linter enforces:
- Participant declaration requirements
- Message flow validation
- Naming convention compliance
- Stereotype usage standards
- Structural integrity rules

## PlantUML Basics for Sequence Diagrams

### Basic Syntax
```plantuml
@startuml
participant "Component A" as A
participant "Component B" as B
database "Database" as DB

A -> B: Request
B -> DB: Query
DB --> B: Result
B --> A: Response
@enduml
```

### Participant Types and Declaration

All participants MUST be declared before use. The linter enforces strict participant declaration:

```plantuml
@startuml
' REQUIRED: Declare all participants with aliases
participant "User Interface" as UI
participant "API Gateway" as GW
participant "Service Layer" as SVC
database "Database" as DB

' Optional: Add stereotypes for enterprise compliance
participant "User Service" as US <<App>>
participant "Payment Service" as PS <<UPR>>
participant "External System" as ES <<Human>>
@enduml
```

#### Participant Declaration Formats
```plantuml
' Format 1: Simple alias
participant ServiceName as SN

' Format 2: With display name
participant "Service Name" as SN

' Format 3: With stereotype
participant ServiceName as SN <<App>>

' Format 4: Full declaration with display name and stereotype
participant "Service Name" as SN <<App>>
```

## Sequence Diagram Standards

### 1. Naming Conventions (Linter Enforced)
- All participants MUST have aliases
- Names must be registered in the configuration
- Stereotypes must be from approved list: `<<Human>>`, `<<App>>`, `<<UPR>>`
- Use consistent naming across diagrams
- No special characters in aliases (only alphanumeric and underscore)

#### Naming Examples
```plantuml
' ✅ CORRECT - Proper declaration with alias
participant "Order Service" as OS
participant "Payment Gateway" as PG <<UPR>>

' ❌ INCORRECT - Missing alias (linter violation)
participant "Order Service"

' ❌ INCORRECT - Unregistered stereotype (linter violation)
participant "Service" as S <<Custom>>
```

### 2. Message Types and Formatting

The linter validates message formats and requires proper participant references:

```plantuml
@startuml
' Participants MUST be declared first
participant "Service A" as A
participant "Service B" as B

' Synchronous call with label and signature
A -> B: **Process Order** processOrder(orderId)

' Response with structured format
B --> A: **Order Processed** {status: "success"}

' Bold labels are recommended for clarity
A -> B: <b>Validate User</b> validateUser(userId)

' Self-calls are allowed (source != target)
A -> A: Process internally
@enduml
```

#### Message Label Standards
```plantuml
' Format 1: Bold with asterisks
A -> B: **Label Text** methodSignature()

' Format 2: HTML bold tags
A -> B: <b>Label Text</b> methodSignature()

' Format 3: Simple text (less preferred)
A -> B: methodCall()
```

### 3. Flow Control
```plantuml
@startuml
' Conditional
alt Success Case
    A -> B: Process
    B --> A: Success
else Failure Case
    A -> B: Process
    B --> A: Error
end

' Loop
loop Every 5 minutes
    A -> B: Health Check
    B --> A: Status
end

' Optional
opt Cache Available
    A -> Cache: Get Data
    Cache --> A: Cached Result
end
@enduml
```

## Common Patterns

### 1. API Request Flow
```plantuml
@startuml API Request Flow
actor Client
boundary "API Gateway" as GW
control "Auth Service" as Auth
control "Business Logic" as BL
database "Database" as DB

Client -> GW: HTTP Request
GW -> Auth: Validate Token
Auth --> GW: Token Valid

alt Token Valid
    GW -> BL: Forward Request
    BL -> DB: Query Data
    DB --> BL: Result Set
    BL --> GW: Process Response
    GW --> Client: HTTP 200 OK
else Token Invalid
    Auth --> GW: Invalid Token
    GW --> Client: HTTP 401 Unauthorized
end
@enduml
```

### 2. Event-Driven Flow
```plantuml
@startuml Event-Driven Architecture
participant "Service A" as A
queue "Event Bus" as Bus
participant "Service B" as B
participant "Service C" as C
database "Event Store" as Store

A -> Bus: Publish Event
Bus -> Store: Store Event
Bus ->> B: Notify (Async)
Bus ->> C: Notify (Async)

B -> Store: Get Event Details
Store --> B: Event Data
B -> B: Process Event

C -> Store: Get Event Details
Store --> C: Event Data
C -> C: Process Event
@enduml
```

### 3. Microservices Communication
```plantuml
@startuml Microservices Flow
actor User
boundary "API Gateway" as GW
participant "User Service" as US
participant "Order Service" as OS
participant "Inventory Service" as IS
participant "Payment Service" as PS

User -> GW: Place Order
GW -> US: Validate User
US --> GW: User Valid

GW -> OS: Create Order
activate OS
OS -> IS: Check Inventory
IS --> OS: Items Available

OS -> IS: Reserve Items
IS --> OS: Items Reserved

OS -> PS: Process Payment
PS --> OS: Payment Successful

OS -> IS: Confirm Reservation
IS --> OS: Confirmed

OS --> GW: Order Created
deactivate OS
GW --> User: Order Confirmation
@enduml
```

## Best Practices

### 1. Three-Column Comparison Table (Required in Solution Designs)

When presenting sequence diagrams in a solution design, ALWAYS use a 3-column markdown table to show Current State, Highlighted Target State, and Target State side by side. This provides immediate visual comparison of before/after and makes changes obvious.

**Table structure** (4 rows):

| Row | Purpose |
|-----|---------|
| 1 — Summary | Brief description of what each column represents |
| 2 — Diagram | Embedded SVG image (`![alt](path.svg)`) |
| 3 — Description | Detailed caption describing the flow shown |
| 4 — Source | PlantUML source file reference |

**Template**:

```markdown
| Current State | Target State — Changes Highlighted | Target State |
|:---:|:---:|:---:|
| [Brief current summary] | Same target-state with green highlighting on changed steps | [Brief target summary] |
| ![Current State](3.solution/current.svg) | ![Highlighted Target](3.solution/highlighted.svg) | ![Target State](3.solution/target.svg) |
| [Current flow description] | [What changed — reference green groups] | [Target flow description] |
| *Source: `diagrams/Service/[name].puml`* | *Ticket workspace only* | *Source: `diagrams/Service/[name].puml`* |
```

**Rules**:
- All three columns are center-aligned (`:---:`)
- The highlighted column is always the middle column
- The highlighted diagram exists only in the ticket workspace (not in the corporate repo)
- Current and target diagrams reference their corporate repo PlantUML source
- Keep descriptions concise — 1-2 sentences per cell

### 2. Diagram Organization (Linter Compliance)
- Declare ALL participants before first use
- One primary flow per diagram
- Include error handling paths
- Show security checkpoints
- Use proper stereotypes for participant types
- Maintain registered component names

### Linter Validation Rules

#### Strict Rules (Must Fix)
1. **Participant Declaration**: All participants in messages must be declared
2. **Valid Types**: Only approved participant types allowed
3. **Registered Names**: Component names must be in registry
4. **Stereotype Compliance**: Only approved stereotypes permitted

#### Guidance Rules (Should Fix)
1. **Minimum Participants**: At least 2 participants recommended
2. **Message Clarity**: Use labeled messages for better documentation
3. **Consistent Formatting**: Follow enterprise styling standards

### 2. Level of Detail
```plantuml
@startuml
' High-Level (Architecture View)
participant "Frontend" as FE
participant "Backend" as BE
participant "Database" as DB

FE -> BE: User Request
BE -> DB: Data Operation
DB --> BE: Result
BE --> FE: Response

' Detailed (Implementation View)
note over FE: React Application
FE -> BE: POST /api/users\n{name, email}
note right: HTTPS TLS 1.3

BE -> BE: Validate Input
BE -> DB: INSERT INTO users\nVALUES (?, ?)
note right: Prepared Statement

DB --> BE: 1 row affected
BE --> FE: 201 Created\n{id: 123, name, email}
@enduml
```

### 3. Error Handling
```plantuml
@startuml Error Handling Pattern
participant "Client" as C
participant "Service" as S
participant "Database" as DB
participant "Error Handler" as EH

C -> S: Request
S -> DB: Query

alt Success
    DB --> S: Data
    S --> C: 200 OK
else Database Error
    DB --> S: Connection Failed
    S -> EH: Log Error
    S --> C: 503 Service Unavailable
else Validation Error
    S -> S: Validate Input
    S --> C: 400 Bad Request
end
@enduml
```

## Diagram Types by Use Case

### 1. Authentication Flow
```plantuml
@startuml OAuth2 Flow
actor User
participant "Client App" as App
participant "Auth Server" as Auth
participant "Resource Server" as RS

User -> App: Login Request
App -> Auth: Redirect to Auth
Auth -> User: Login Page
User -> Auth: Credentials
Auth -> App: Auth Code
App -> Auth: Exchange Code for Token
Auth --> App: Access Token
App -> RS: API Request + Token
RS -> Auth: Validate Token
Auth --> RS: Token Valid
RS --> App: Protected Resource
App --> User: Display Data
@enduml
```

### 2. Transaction Processing
```plantuml
@startuml Transaction Processing
participant "Client" as C
participant "Transaction Service" as TS
database "Transaction DB" as TDB
participant "Account Service" as AS
database "Account DB" as ADB

C -> TS: Initiate Transaction
TS -> TDB: BEGIN TRANSACTION

TS -> AS: Debit Account A
AS -> ADB: UPDATE balance
ADB --> AS: Success
AS --> TS: Debit Complete

TS -> AS: Credit Account B
AS -> ADB: UPDATE balance
ADB --> AS: Success
AS --> TS: Credit Complete

TS -> TDB: COMMIT
TDB --> TS: Transaction Complete
TS --> C: Transaction Successful
@enduml
```

### 3. Async Processing
```plantuml
@startuml Async Job Processing
participant "API" as API
queue "Job Queue" as Queue
participant "Worker" as Worker
database "Database" as DB
participant "Notification Service" as NS

API -> Queue: Enqueue Job
Queue --> API: Job ID: 123
API --> API: Return Job ID to Client

... Async Processing ...

Worker -> Queue: Poll for Jobs
Queue --> Worker: Job 123
Worker -> DB: Process Data
DB --> Worker: Processing Complete
Worker -> NS: Send Notification
NS --> Worker: Sent
Worker -> Queue: Mark Complete
@enduml
```

## Security Considerations in Diagrams

### Always Include:
1. Authentication steps
2. Authorization checks
3. Encryption indicators
4. Security boundaries
5. Token/credential handling

### Example with Security:
```plantuml
@startuml Secure API Flow
actor Client
boundary "WAF" as WAF
boundary "API Gateway" as GW
participant "Auth Service" as Auth
participant "Service" as Svc
database "Database" as DB

Client -> WAF: HTTPS Request
note right: TLS 1.3
WAF -> WAF: Check Rules
WAF -> GW: Forward Request

GW -> Auth: Validate JWT
note right: RS256 Signature
Auth -> Auth: Verify Claims
Auth --> GW: Token Valid + Roles

GW -> Svc: Request + User Context
note right: Internal TLS
Svc -> Svc: Check Permissions
Svc -> DB: Query (Encrypted)
note right: AES-256
DB --> Svc: Encrypted Data
Svc -> Svc: Decrypt
Svc --> GW: Response
GW --> Client: HTTPS Response
@enduml
```

## Common Mistakes to Avoid

1. **Too Much Detail** - Keep diagrams focused
2. **Missing Error Paths** - Always show failure scenarios
3. **Unclear Timing** - Use activation bars for long operations
4. **No Return Messages** - Show both request and response
5. **Mixing Concerns** - Separate different flows

## Integration with Architecture Documentation

### Diagram Placement
```
docs/
└── architecture/
    ├── overview.md
    ├── sequence-diagrams/
    │   ├── authentication-flow.puml
    │   ├── order-processing.puml
    │   ├── payment-flow.puml
    │   └── README.md
    └── images/
        └── generated/  # PlantUML output
```

### Linking in Documents
```markdown
## Order Processing Flow

The order processing involves multiple services working together:

![Order Processing](./images/generated/order-processing.png)

See [order-processing.puml](./sequence-diagrams/order-processing.puml) for source.
```

## Tools and Generation

### PlantUML Generation Commands
```bash
# Generate PNG
java -jar plantuml.jar sequence-diagram.puml

# Generate SVG (preferred for documentation)
java -jar plantuml.jar -tsvg sequence-diagram.puml

# Batch generation
java -jar plantuml.jar "sequence-diagrams/*.puml"
```

### VS Code Integration
- Install PlantUML extension
- Preview diagrams while editing
- Auto-generate on save
- Export to multiple formats

## Checklist for Sequence Diagrams

Before finalizing any sequence diagram:
- [ ] All participants declared with proper aliases
- [ ] Participant names are registered in configuration
- [ ] Stereotypes are from approved list
- [ ] No undeclared participants in messages
- [ ] Message types (sync/async) indicated
- [ ] Error paths included
- [ ] Security checkpoints shown
- [ ] Timing/activation bars used appropriately
- [ ] Notes explain complex logic
- [ ] Diagram has a clear title
- [ ] Source file uses .puml extension
- [ ] **Diagram passes PlantUML linter validation**
- [ ] Generated images in correct location
- [ ] Diagram referenced in documentation

## Running the PlantUML Linter

### Command Line Usage
```bash
# Basic linting
java -jar pumlint.jar rules.json relationships.csv lint-results.csv diagram.puml

# Lint entire directory
java -jar pumlint.jar rules.json relationships.csv lint-results.csv /path/to/diagrams/
```

### Integration with Development
1. Run linter before committing diagrams
2. Fix all "strict" violations
3. Address "guidance" violations when possible
4. Include linter reports in documentation

### Common Linter Violations and Fixes

#### Undeclared Participant
```plantuml
' ❌ VIOLATION: 'API' not declared
User -> API: Request

' ✅ FIX: Declare all participants
participant "User" as User
participant "API Gateway" as API
User -> API: Request
```

#### Invalid Stereotype
```plantuml
' ❌ VIOLATION: '<<Service>>' not in approved list
participant "OrderSvc" as OS <<Service>>

' ✅ FIX: Use approved stereotype
participant "OrderSvc" as OS <<App>>
```

#### Unregistered Name
```plantuml
' ❌ VIOLATION: 'CustomService' not in registry
participant "CustomService" as CS

' ✅ FIX: Use registered name or add to registry
participant "OrderService" as OS
```

---

Remember: Sequence diagrams are communication tools. They should clarify, not complicate. Keep them focused, accurate, and up-to-date with implementation.