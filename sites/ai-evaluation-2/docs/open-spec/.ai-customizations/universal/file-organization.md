# File Organization Standards - Universal Application

All modes MUST follow these file organization standards to maintain consistency, discoverability, and professional structure across UDX projects.

## Naming Conventions

### File Names
**Format**: `lowercase-hyphenated-descriptive-name.extension`

✅ **CORRECT**:
- `api-design-document.md`
- `user-authentication-flow.puml`
- `2024-03-15-release-notes.md`
- `database-schema-v2.sql`

❌ **INCORRECT**:
- `APIDesignDocument.md` (no camelCase)
- `user_authentication_flow.puml` (no underscores)
- `api design document.md` (no spaces)
- `api-doc.md` (too abbreviated)

### Directory Names
**Format**: `lowercase-hyphenated-descriptive-name/`

✅ **CORRECT**:
- `architecture-decisions/`
- `api-documentation/`
- `test-results/`
- `deployment-configs/`

❌ **INCORRECT**:
- `ArchitectureDecisions/` (no camelCase)
- `API_Docs/` (no underscores or caps)
- `test results/` (no spaces)
- `configs/` (too abbreviated)

## Directory Structure Standards

### Project Root Organization
```
project-root/
├── .ai-customizations/          # AI customization configs
├── documentation/               # All documentation
│   ├── architecture/           # Architecture docs
│   ├── api/                    # API documentation
│   ├── guides/                 # User/dev guides
│   └── decisions/              # ADRs and decisions
├── src/                        # Source code
├── tests/                      # Test files
├── configs/                    # Configuration files
├── scripts/                    # Utility scripts
├── templates/                  # Document templates
└── plans/                      # Project plans
    ├── integration-plans/      # Integration planning
    └── migration-plans/        # Migration planning
```

### Documentation Organization
```
documentation/
├── architecture/
│   ├── system-overview.md
│   ├── component-design/
│   │   ├── api-gateway.md
│   │   └── service-mesh.md
│   └── diagrams/
│       ├── system-context.puml
│       └── deployment-view.puml
├── api/
│   ├── rest/
│   │   ├── endpoints.md
│   │   └── examples/
│   └── graphql/
│       ├── schema.md
│       └── queries.md
├── guides/
│   ├── getting-started.md
│   ├── installation.md
│   └── troubleshooting.md
└── decisions/
    ├── 2024-03-15-database-selection.md
    └── 2024-03-20-api-versioning.md
```

## Date-Prefixed Files

### When to Use Date Prefixes
Use ISO 8601 date format (YYYY-MM-DD) for:
- Release notes
- Meeting minutes  
- Decision records
- Time-sensitive plans
- Changelog entries
- Incident reports

### Format
`YYYY-MM-DD-descriptive-name.md`

Examples:
- `2024-03-15-release-notes.md`
- `2024-03-20-architecture-decision.md`
- `2024-03-22-incident-report.md`

## Special Directories

### Hidden Directories
- `.ai-customizations/` - AI configuration
- `.github/` - GitHub specific files
- `.vscode/` - VS Code settings
- `.idea/` - IDE settings

### Reserved Directory Names
Never use these names for custom directories:
- `bin/` - Reserved for binaries
- `lib/` - Reserved for libraries
- `node_modules/` - Package dependencies
- `vendor/` - Third-party code
- `tmp/` or `temp/` - Temporary files

## File Organization Rules

### Grouping Strategy
1. **By Type**: Group similar file types together
2. **By Feature**: For feature-specific documentation
3. **By Timeline**: For time-sensitive documents
4. **By Audience**: Separate internal/external docs

### Depth Limits
- Maximum directory depth: 4 levels
- Exception: Generated files (e.g., node_modules)
- Keep frequently accessed files shallow

### File Size Considerations
- Split large documents > 1000 lines
- Use sub-documents with clear naming
- Maintain index/navigation files
- Link between related documents

## Configuration Files

### Standard Locations
```
configs/
├── development/
│   ├── app-config.yaml
│   └── db-config.yaml
├── staging/
│   ├── app-config.yaml
│   └── db-config.yaml
└── production/
    ├── app-config.yaml
    └── db-config.yaml
```

### Naming Patterns
- Environment-specific: `{environment}-config.yaml`
- Service-specific: `{service}-config.yaml`
- Version-specific: `config-v{version}.yaml`

## Template Organization

### Template Directory Structure
```
templates/
├── documentation/
│   ├── architecture-decision-record.md
│   ├── api-specification.md
│   └── design-document.md
├── code/
│   ├── service-template.py
│   └── test-template.py
└── configs/
    ├── service-config-template.yaml
    └── deployment-template.yaml
```

## Version Control Considerations

### Files to Track
- All documentation
- Source code
- Configuration templates
- Scripts and tools
- Test files

### Files to Ignore
- Generated files
- Temporary files
- Local environment configs
- Sensitive credentials
- Build artifacts

### .gitignore Patterns
```gitignore
# Dependencies
node_modules/
vendor/

# Build outputs
dist/
build/
*.exe

# Temporary files
*.tmp
*.temp
.DS_Store

# Local configs
.env.local
config.local.yaml

# IDE files
.idea/
*.swp
```

## Migration Guidelines

### When Reorganizing
1. Document current structure
2. Plan target structure
3. Create migration script
4. Update all references
5. Verify functionality
6. Archive old structure

### Maintaining Links
- Use relative paths
- Update documentation
- Implement redirects
- Communicate changes

## Validation Checklist

Before committing:
- [ ] All files use lowercase-hyphenated names
- [ ] No spaces in file or directory names
- [ ] Date prefixes in ISO 8601 format
- [ ] Appropriate directory structure
- [ ] No files in root (except necessary)
- [ ] Templates in templates/ directory
- [ ] Documentation in documentation/
- [ ] Configs properly organized
- [ ] No deeply nested structures (>4 levels)

## Common Violations

### File Naming
- ❌ `UserGuide.pdf` → ✅ `user-guide.pdf`
- ❌ `API_Spec_v2.md` → ✅ `api-specification-v2.md`
- ❌ `test results.xlsx` → ✅ `test-results.xlsx`

### Directory Structure
- ❌ Files scattered in root
- ❌ Mixed naming conventions
- ❌ Unclear organization
- ❌ Too many levels deep

---

**Remember**: Consistent file organization enables efficient collaboration, reduces confusion, and maintains professional standards across all UDX projects.