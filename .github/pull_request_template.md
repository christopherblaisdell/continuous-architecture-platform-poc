## Solution Design Review — [TICKET-ID]

### Summary

<!-- Brief description of the architectural change -->

### Affected Services

<!-- List all services impacted by this solution -->

- [ ] Service impact assessments included for each

### Checklist

#### Completeness

- [ ] Master document has Overview and Component Architecture
- [ ] All impacted services have impact assessment files
- [ ] At least 2 options considered in each decision (MADR format)

#### Capability Rollup

- [ ] Capability IDs declared in master document header
- [ ] `3.solution/c.capabilities/capabilities.md` exists with impact types
- [ ] New L3 capabilities identified and named (if applicable)
- [ ] `capability-changelog.yaml` entry drafted
- [ ] All affected metadata YAML files identified for update

#### Content Separation

- [ ] Impact files describe WHAT, not WHY or HOW
- [ ] Decision files describe WHY, not HOW
- [ ] Guidance files describe HOW (if present)
- [ ] User stories describe WHO benefits, not technical details

#### Metadata Consistency

- [ ] `architecture/metadata/tickets.yaml` updated
- [ ] `architecture/metadata/capabilities.yaml` updated (if new L3)
- [ ] `architecture/metadata/capability-changelog.yaml` entry appended
- [ ] `architecture/metadata/cross-service-calls.yaml` updated (if new integrations)
- [ ] Backward compatibility addressed for all API changes

#### Data Isolation

- [ ] No corporate identifiers introduced
- [ ] All synthetic data uses NovaTrek Adventures domain
- [ ] `scripts/audit-data-isolation.sh` passes clean
