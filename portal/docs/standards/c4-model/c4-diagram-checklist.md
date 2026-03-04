# C4 Diagram Review Checklist

Use this checklist when creating or reviewing C4 diagrams to ensure quality and consistency.

## Completeness

- [ ] All key software systems relevant to the scope are shown
- [ ] All significant users/actors are represented
- [ ] External systems and dependencies are included
- [ ] No orphaned elements (every element has at least one relationship)
- [ ] System boundary is clearly defined (Levels 2 and 3)
- [ ] The diagram has a descriptive title

## Clarity

- [ ] Every element has a meaningful name (not abbreviations or codenames alone)
- [ ] Every element has a brief description explaining its responsibility
- [ ] Technology choices are labeled on containers and components
- [ ] Relationship arrows have verb labels describing the interaction
- [ ] Communication protocols/technologies are noted on relationships
- [ ] Text is readable at the intended display size
- [ ] A legend or key is included (or use `LAYOUT_WITH_LEGEND()`)

## Consistency

- [ ] Element names are consistent across all diagram levels
- [ ] Technology labels match actual implementation
- [ ] Color coding follows team conventions (internal vs external)
- [ ] Arrow direction consistently represents dependency or data flow
- [ ] Naming conventions are applied uniformly (e.g., "Service" suffix, "DB" suffix)

## Audience Appropriateness

- [ ] **Level 1 (Context)**: Understandable by non-technical stakeholders
- [ ] **Level 2 (Container)**: Appropriate for technical leads and architects
- [ ] **Level 3 (Component)**: Appropriate for developers working on the system
- [ ] **Level 4 (Code)**: Only created when it adds value beyond reading the source
- [ ] Detail level matches the intended audience -- not too much, not too little

## Accuracy

- [ ] Diagram reflects the current state of the system (or clearly labeled as target/future state)
- [ ] No stale elements from previous versions of the architecture
- [ ] Data flows match actual runtime behavior
- [ ] Deployment boundaries match actual infrastructure

## Maintainability

- [ ] Diagram source is stored in version control (`.puml` files preferred)
- [ ] Diagram is generated from code, not manually drawn (when possible)
- [ ] Last-updated date is noted or version-controlled
- [ ] Diagram is referenced from relevant documentation (README, wiki, ADR)
