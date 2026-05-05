# AI Customizations Index

This searchable index helps you quickly find specific standards, methodologies, and customizations.

## Universal Standards (All Modes)

### Corporate Standards
**File**: `universal/corporate-standards.md`
- No emojis policy
- Professional communication requirements
- Email formatting standards
- Meeting documentation
- Commit message guidelines

### Effort Estimation
**File**: `universal/effort-estimation.md`
- Sprint-based estimation (never dollars)
- Complexity assessment criteria
- Time-based estimates
- Story points and T-shirt sizing
- Confidence levels

### Markdown Formatting
**File**: `universal/markdown-formatting.md`
- Header rules (no special characters)
- Document structure standards
- Code block requirements
- Table formatting
- Link standards

### File Organization
**File**: `universal/file-organization.md`
- Standard project structure
- Language-specific layouts
- Naming conventions
- Directory organization
- Git ignore patterns

### Security and Uptime
**File**: `universal/security-uptime-basic.md`
- Security-first mindset
- Uptime requirements (99.9%, 99.99%, 99.999%)
- Common vulnerabilities
- Security documentation
- Monitoring requirements

## Methodologies

### 4-Phase Investigation Process
**File**: `methodologies/4-phase-investigation.md`
**Applicable Modes**: Solution Architect, Orchestrator, Ask
- Phase 1: Discovery and Context
- Phase 2: Analysis and Assessment
- Phase 3: Solution Design
- Phase 4: Recommendation and Roadmap

### Ticket Classification Framework
**File**: `methodologies/ticket-classification.md`
**Applicable Modes**: Solution Architect, Orchestrator
- Level 1-5 classification system
- Two-tier impact organization
- Complexity assessment
- Governance requirements

### BDD/TDD Methodology
**File**: `methodologies/bdd-tdd-methodology.md`
**Applicable Modes**: Code, Debug, VS Code Plugin
- Given-When-Then scenarios
- Red-Green-Refactor cycle
- Test organization
- Coverage standards

### Sequence Diagrams
**File**: `methodologies/sequence-diagrams.md`
**Applicable Modes**: Solution Architect, Orchestrator
- PlantUML syntax (never Mermaid)
- UDX linter compliance
- Participant declaration rules
- Message formatting

### PlantUML Standards
**File**: `methodologies/plantuml-standards.md`
**Applicable Modes**: Solution Architect, Orchestrator, Code (when documenting)
- Linter requirements
- Approved stereotypes
- Naming conventions
- Validation rules

### Guided Plan Execution
**File**: `methodologies/guided-plan-execution.md`
**Applicable Modes**: All modes executing a structured change plan
- Step-by-step interactive plan execution
- Present item, explain why, identify files
- Offer lettered options with recommendation
- Execute, commit, push, advance to next item
- Session state tracking for resume capability

### JIRA Ticket Extraction
**VS Code prompt**: `user-prompts/jira-extract.prompt.md` (symlinked to VS Code user prompts)
**Roo skill**: Installed at `~/.roo/skills/jira-extraction` (symlinked from `shared-ai-customizations/`)
**Script**: `scripts/jira/working_jira_client.py`
**Applicable Modes**: Solution Architect, Orchestrator, Code
- Browser cookie authentication (Chrome)
- JIRA REST API v3 ticket retrieval
- Atlassian Document Format (ADF) to markdown conversion
- Configurable JIRA instance via JIRA_BASE_URL env var

### Prompt Mirror — Context Capture
**File**: `methodologies/prompt-mirror.md`
**Instruction File**: `.github/instructions/prompt-mirror.instructions.md` (applyTo: `**`)
**Applicable Modes**: All modes
- Every AI chat interaction saved to `prompt-mirror/` as context-enriched markdown
- Files read as direct user requests with all context inlined
- No trace of prior AI processing — designed to be pasted directly into Roo Code
- Context gathering rules ensure self-contained completeness

### Architecture Backlog Management
**File**: `methodologies/architecture-backlog.md`
**Applicable Modes**: Solution Architect, Orchestrator
- Strategic initiatives
- Technical debt tracking
- Prioritization framework
- Progress tracking

## User Prompts (VS Code Global)

### JIRA Extract
**File**: `user-prompts/jira-extract.prompt.md`
**Symlinked to**: `~/Library/Application Support/Code/User/prompts/jira-extract.prompt.md`
- VS Code slash command: `/jira-extract`
- Lists assigned JIRA tickets or extracts a specific ticket to markdown
- Uses shared script at `scripts/jira/working_jira_client.py`
- Available from any VS Code workspace after symlink setup

## Standards

### Testing Standards
**File**: `standards/testing-standards.md`
**Applicable Modes**: Code, Debug, VS Code Plugin
- Unit test requirements (80% coverage)
- Integration testing
- E2E testing
- Test patterns (AAA)
- Mock/stub patterns

### Impact Organization
**File**: `standards/impact-organization.md`
**Applicable Modes**: Solution Architect, Orchestrator
- Two-tier classification (Simple vs Complex)
- Component resource hierarchy
- One impact per resource
- Documentation requirements by tier

### Email Writing
**File**: `standards/email-writing.md`
**Applicable Modes**: Solution Architect, Orchestrator, Ask, Corporate Compliance
- Subject line format
- Professional templates
- Stakeholder communication
- Incident communication

### Component Hierarchy
**File**: `standards/component-hierarchy.md`
**Applicable Modes**: Solution Architect, Code
- System/Service/Component/Module levels
- Dependency direction rules
- Single responsibility principle
- Interface contracts

### Documentation Dates
**File**: `standards/documentation-dates.md`
**Applicable Modes**: Corporate Compliance, Solution Architect
- ISO 8601 format requirements
- Historical document naming
- Version history tracking
- Retention periods

### Swagger/YAML Locations
**File**: `standards/swagger-yaml-locations.md`
**Applicable Modes**: Solution Architect, Code, Orchestrator
- Primary location: `external-repos/architecture/udx-architecture-artifacts/services/`
- UDX microservice API specifications
- Directory structure and organization
- Usage guidelines

### PlantUML Diagram Locations
**File**: `standards/plantuml-diagram-locations.md`
**Applicable Modes**: Solution Architect, Orchestrator, Code (when documenting)
- Service diagrams: `external-repos/architecture/udx-architecture-artifacts/diagrams/Service/`
- Solution diagrams: `external-repos/architecture/udx-architecture-artifacts/diagrams/Solution/`
- Component library: `external-repos/architecture/udx-architecture-artifacts/diagrams/Components/`
- Reusability guidelines and best practices

## Mode-Specific Customizations

### All Modes
**File**: `mode-customizations/all-modes.md`
- Universal standards reference
- Mandatory requirements
- Quick reference checklist

### Solution Architect
**File**: `mode-customizations/solution-architect.md`
- UDX Solution Design Template usage
- Swagger/OpenAPI ownership
  - Primary location: `external-repos/architecture/udx-architecture-artifacts/services/[service-name]/`
  - Contains all UDX microservice API specifications
- PlantUML diagrams (not Mermaid)
- Architecture governance

### Code
**File**: `mode-customizations/code.md`
- BDD/TDD implementation
- Test-first development
- Error handling patterns
- Security implementation

### Debug
**File**: `mode-customizations/debug.md`
- Systematic investigation
- Reproduction tests
- Performance debugging
- Root cause analysis

### Ask
**File**: `mode-customizations/ask.md`
- Technical explanations
- Code analysis
- Best practice guidance
- No implementation

### Orchestrator
**File**: `mode-customizations/orchestrator.md`
- Project decomposition
- Mode coordination
- Progress tracking
- Handoff management

### Corporate Compliance
**File**: `mode-customizations/corporate-compliance.md`
- Air-gapped requirements
- Compliance documentation
- Audit trails
- Data classification

### VS Code Plugin Developer
**File**: `mode-customizations/vscode-plugin-dev.md`
- Extension structure
- VS Code API usage
- Testing extensions
- Publishing guidelines

## Quick Reference by Topic

### Security
- `universal/security-uptime-basic.md` - Basic awareness
- `methodologies/sequence-diagrams.md` - Security in diagrams
- `standards/testing-standards.md` - Security testing

### Testing
- `methodologies/bdd-tdd-methodology.md` - Test methodologies
- `standards/testing-standards.md` - Testing requirements
- Mode-specific: Code, Debug, VS Code Plugin

### Documentation
- `universal/markdown-formatting.md` - Formatting standards
- `standards/documentation-dates.md` - Date requirements
- `standards/email-writing.md` - Communication standards

### Architecture
- `methodologies/4-phase-investigation.md` - Investigation process
- `methodologies/architecture-backlog.md` - Backlog management
- `standards/component-hierarchy.md` - Component organization

### Compliance
- `mode-customizations/corporate-compliance.md` - Compliance mode
- `standards/documentation-dates.md` - Audit requirements
- `universal/corporate-standards.md` - Professional standards

---

Use Ctrl+F (Cmd+F on Mac) to search this index for specific topics or requirements.