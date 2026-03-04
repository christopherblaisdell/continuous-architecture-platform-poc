# C4 Model Reference

## Overview

The C4 model is a lean graphical notation technique for modelling the architecture of software systems, created by Simon Brown. It provides a set of hierarchical abstractions (software systems, containers, components, and code) that enable different audiences to understand a software architecture at different levels of detail.

## The Four Levels

### Level 1: System Context Diagram

Shows the software system in scope and its relationships with users and other systems. This is the most zoomed-out view, providing the big picture.

**Audience**: Everyone -- technical and non-technical stakeholders.

### Level 2: Container Diagram

Zooms into the software system to show the high-level technical building blocks (containers): applications, data stores, microservices, message brokers, etc. Each container is a separately deployable/runnable unit.

**Audience**: Technical people inside and outside the development team.

### Level 3: Component Diagram

Zooms into an individual container to show the components inside it. A component is a grouping of related functionality behind a well-defined interface.

**Audience**: Software architects and developers.

### Level 4: Code Diagram

Zooms into a component to show how it is implemented. Typically a UML class diagram or similar. This level is optional and often auto-generated from code.

**Audience**: Developers working on the component.

## Key Principles

- **Abstraction first**: Start with the big picture and zoom in
- **Notation independence**: C4 is about abstraction levels, not specific notation
- **Supplementary diagrams**: Use deployment diagrams, dynamic diagrams as needed
- **Keep it simple**: Every element should have a name, technology choice, and description

## Resources

- Official website: [https://c4model.com](https://c4model.com)
- C4-PlantUML: [https://github.com/plantuml-stdlib/C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML)
- Simon Brown's book: "Software Architecture for Developers"

## License

The C4 model is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
