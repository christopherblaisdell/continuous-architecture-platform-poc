# PlantUML Standards and Linter Compliance

**Applicable Modes**: Solution Architect, Orchestrator, Code (when documenting)

## Overview

This document defines the enterprise PlantUML standards enforced by the UDX PlantUML linter. All diagrams must comply with these standards to ensure consistency, quality, and maintainability across our architecture documentation.

## UDX PlantUML Linter Overview

The UDX PlantUML linter is a Java-based validation tool that:
- Builds complete object models of diagrams
- Validates structural integrity
- Enforces naming conventions
- Ensures architectural compliance
- Generates relationship inventories

## Diagram Types and Standards

### Component Diagrams

#### Required Elements
1. **Component Declaration**
   ```plantuml
   @startuml
   component "Order Service" as OS <<App>>
   component "Payment Gateway" as PG <<UPR>>
   interface "IPayment" as IPay
   
   OS --> IPay : uses
   PG -up- IPay : provides
   @enduml
   ```

2. **Interface Compliance**
   - All interfaces must be implemented
   - Required interfaces must have providers
   - No orphaned interfaces allowed

3. **Dependency Rules**
   - No circular dependencies
   - Dependencies must follow architectural layers
   - External dependencies must be clearly marked

### Sequence Diagrams

See [sequence-diagrams.md](./sequence-diagrams.md) for detailed sequence diagram standards.

## Approved Stereotypes

### System Stereotypes
- `<<Human>>` - Human actors or external users
- `<<App>>` - Application components
- `<<UPR>>` - UPR (Universal Parks & Resorts) specific components

### Component Stereotypes
- `<<Service>>` - Service components
- `<<Database>>` - Data storage components
- `<<Queue>>` - Message queue components
- `<<External>>` - External system components

### Usage Examples
```plantuml
participant "Guest" as G <<Human>>
participant "Mobile App" as MA <<App>>
participant "Reservation System" as RS <<UPR>>
database "Guest Database" as DB <<Database>>
```

## Naming Conventions

### Component Names
1. **Registered Names Required**
   - All component names must be in the registry
   - Exception: Components with exempt stereotypes
   - Registry maintained in `rules.json`

2. **Naming Format**
   ```plantuml
   ' Service components
   component "OrderService" as OS
   component "PaymentService" as PS
   
   ' UI components
   component "WebPortal" as WP
   component "MobileApp" as MA
   
   ' Infrastructure
   component "APIGateway" as GW
   component "MessageBus" as MB
   ```

3. **Alias Requirements**
   - All elements MUST have aliases
   - Aliases use PascalCase abbreviations
   - Keep aliases short but meaningful
   - Use consistent aliases across diagrams

## Validation Rules

### Strict Rules (Build Failures)

1. **Participant Declaration Rule**
   ```json
   {
     "name": "Participants in a message MUST be declared",
     "enforcement": "strict",
     "violationRegex": "\\w+\\s*->\\s*\\w+"
   }
   ```

2. **Type Validation Rule**
   ```json
   {
     "name": "Only valid types allowed",
     "enforcement": "strict",
     "invalid types": ["foo", "bar", "test"]
   }
   ```

3. **Stereotype Compliance Rule**
   ```json
   {
     "name": "Stereotypes must be from approved list",
     "enforcement": "strict",
     "valid stereotypes": {
       "participant": ["Human", "App", "UPR"],
       "component": ["Service", "Database", "Queue"]
     }
   }
   ```

### Guidance Rules (Warnings)

1. **Minimum Elements Rule**
   ```json
   {
     "name": "Diagrams should have meaningful content",
     "enforcement": "guidance",
     "lower": 2,
     "upper": -1
   }
   ```

2. **Documentation Rule**
   ```json
   {
     "name": "Diagrams should include descriptive notes",
     "enforcement": "guidance"
   }
   ```

## Linter Configuration

### Rules Configuration File (rules.json)
```json
{
  "valid stereotypes": [
    {
      "participant": ["Human", "App", "UPR"],
      "actor": ["Human", "System"],
      "component": ["Service", "Database", "Queue", "External"],
      "interface": ["REST", "SOAP", "GraphQL"]
    }
  ],
  "invalid types": ["test", "temp", "dummy"],
  "registered names": {
    "names": [
      "OrderService",
      "PaymentService",
      "GuestService",
      "ReservationSystem",
      "APIGateway",
      "MessageBus"
    ],
    "exempt stereotypes": ["Human", "External"]
  },
  "diagram rules": {
    "all": [
      {
        "name": "Minimum diagram elements",
        "rule": ".*",
        "lower": 2,
        "enforcement": "guidance"
      }
    ],
    "sequence": [
      {
        "name": "Participants must be declared",
        "rule": "^\\s*participant.*",
        "enforcement": "strict",
        "lower": 1
      }
    ],
    "component": [
      {
        "name": "Components must have relationships",
        "rule": ".*-->.*",
        "enforcement": "guidance",
        "lower": 1
      }
    ]
  }
}
```

## PlantUML File Organization

### Directory Structure
```
architecture/
├── diagrams/
│   ├── component/
│   │   ├── system-overview.puml
│   │   ├── service-architecture.puml
│   │   └── data-flow.puml
│   ├── sequence/
│   │   ├── authentication-flow.puml
│   │   ├── order-processing.puml
│   │   └── payment-flow.puml
│   └── deployment/
│       ├── aws-infrastructure.puml
│       └── container-deployment.puml
├── generated/              # Linter output
│   ├── relationships.csv   # Component relationships
│   └── lint-results.csv    # Validation results
└── rules.json             # Linter configuration
```

### File Naming
- Use descriptive names with hyphens
- Include diagram type in name when helpful
- Examples:
  - `order-processing-sequence.puml`
  - `payment-service-component.puml`
  - `aws-deployment-architecture.puml`

## Running the Linter

### Command Line
```bash
# Lint single file
java -jar pumlint.jar rules.json relationships.csv lint-results.csv diagram.puml

# Lint directory
java -jar pumlint.jar rules.json relationships.csv lint-results.csv ./diagrams/

# With custom output location
java -jar pumlint.jar rules.json ~/output/relationships.csv ~/output/lint.csv ./diagrams/
```

### CI/CD Integration
```yaml
# Example GitLab CI configuration
plantuml-lint:
  stage: validate
  script:
    - java -jar pumlint.jar rules.json output/relationships.csv output/lint.csv diagrams/
    - if [ -s output/lint.csv ]; then exit 1; fi
  artifacts:
    reports:
      junit: output/lint.csv
    paths:
      - output/
```

## Common Violations and Resolutions

### 1. Undeclared Participant
**Violation**: `'API' in 'User -> API : Request'`
**Resolution**:
```plantuml
participant "User" as User
participant "API Gateway" as API  ' Add this line
User -> API : Request
```

### 2. Invalid Stereotype
**Violation**: `Invalid stereotype 'Service' for type 'participant'`
**Resolution**:
```plantuml
' Change from:
participant "OrderSvc" as OS <<Service>>
' To:
participant "OrderSvc" as OS <<App>>
```

### 3. Unregistered Name
**Violation**: `Name 'CustomService' not in registry`
**Resolution**:
- Add name to `rules.json` registered names
- OR use an exempt stereotype
- OR rename to registered name

### 4. Missing Interface Implementation
**Violation**: `Interface 'IPayment' has no provider`
**Resolution**:
```plantuml
interface "IPayment" as IPay
component "PaymentService" as PS
PS -up- IPay : provides  ' Add this line
```

## Quality Metrics

The linter provides quantitative analysis:
- **Relationship Inventory**: All component/participant interactions
- **Violation Count**: Number and severity of issues
- **Diagram Complexity**: Number of elements and relationships
- **Coverage Metrics**: Documented vs undocumented components

## PUML Change Protocol (MANDATORY)

Whenever a `.puml` file is modified, the following steps are **required** before considering the change complete:

### 1. Regenerate SVG

Use the known-good PlantUML version (see `/memories/repo/plantuml-version.md`):

```bash
java -jar /opt/homebrew/Cellar/plantuml/plantuml-1.2025.4.jar -tsvg <changed-file>.puml
```

- Do NOT use the bare `plantuml` command (Homebrew default may be a broken version)
- The SVG is generated in the same directory as the `.puml` file
- Commit the regenerated SVG alongside the `.puml` change

### 2. Update All Copies

If the diagram exists in multiple repositories (e.g., local workspace AND `udx-architecture-artifacts`), **update and commit to all copies**. Specifically:

- **Local workspace repo**: commit + push to air-gapped remote
- **udx-architecture-artifacts PR branch**: commit + push to GitHub

### 3. Checklist

Before marking a PUML change as done, verify:
- [ ] `.puml` file updated
- [ ] SVG regenerated with known-good PlantUML version
- [ ] SVG committed alongside `.puml`
- [ ] All repo copies updated (local + PR)
- [ ] Changes pushed to all remotes

## Best Practices

### Do's ✅
1. Run linter before committing
2. Fix all strict violations
3. Address guidance violations when possible
4. Keep rules.json updated
5. Document exemptions
6. **Always regenerate SVGs when changing PUML files**
7. **Always update all repo copies (local + PR) when changing PUML files**

### Don'ts ❌
1. Disable linter rules without approval
2. Use unregistered names without justification
3. Create diagrams without proper structure
4. Ignore linter warnings long-term
5. Bypass CI/CD linter checks
6. **Never commit PUML changes without regenerating SVGs**
7. **Never forget to update the PR when changing a diagram that exists in udx-architecture-artifacts**

## Troubleshooting

### Linter Not Finding Elements
- Check regex patterns in element declaration
- Ensure proper PlantUML syntax
- Verify file encoding (UTF-8)

### False Positives
- Review rules.json configuration
- Check for special characters in names
- Validate regex patterns

### Performance Issues
- Split large diagrams
- Limit directory depth for scanning
- Increase JVM heap size if needed

---

Remember: The PlantUML linter ensures our architectural documentation remains consistent, valid, and maintainable. Always validate diagrams before sharing or publishing.