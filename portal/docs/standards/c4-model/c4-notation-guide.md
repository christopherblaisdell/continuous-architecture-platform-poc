# C4 Model Notation Guide

## Element Shapes

### Person

Represents a user or actor that interacts with the software system. Drawn as a stick figure or a rounded rectangle with a person icon.

**Label format**: Name + Description

### Software System

Represents the highest level of abstraction -- an entire software system. Drawn as a simple rectangle with rounded corners.

**Label format**: Name + Description

### Container

A separately runnable/deployable unit within a software system (e.g., web application, API, database, message queue). Drawn as a rectangle.

**Label format**: Name + Technology + Description

### Component

A grouping of related functionality within a container, accessible via a well-defined interface. Drawn as a rectangle (often with a component icon or stereotype).

**Label format**: Name + Technology + Description

## Color Conventions

| Element | Color | Meaning |
|---------|-------|---------|
| Person | Blue | User/actor interacting with the system |
| Internal System | Blue/Dark Blue | System being described (in scope) |
| External System | Gray | Systems outside the boundary (out of scope) |
| Container | Blue (various shades) | Technical building blocks within the system |
| Component | Blue (lighter shade) | Logical groupings within a container |
| Database | Blue with cylinder shape | Persistent data store |

**Note**: The exact colors can be customized, but the key distinction is between internal (in-scope) and external (out-of-scope) elements.

## Relationship Arrows

- Arrows indicate the **direction of dependency or data flow**
- Every arrow must have a **verb label** describing the relationship (e.g., "Reads from", "Sends events to", "Authenticates via")
- Optionally include the **technology/protocol** (e.g., "REST/HTTPS", "JDBC", "AMQP")
- Use solid lines for synchronous communication
- Use dashed lines for asynchronous communication

**Format**: [Description] + [Technology/Protocol]

Example: `"Sends order events" / "Kafka/AVRO"`

## Level Descriptions

### Level 1 - System Context

- Shows the system under design at the center
- Surrounds it with users (persons) and other systems it interacts with
- Every element is a box or person shape with a name and brief description
- Relationships show high-level interactions
- Do NOT show internal details of the system

### Level 2 - Container

- Expands the system boundary to show containers inside
- External systems and persons remain visible for context
- Each container shows its name, technology choice, and responsibility
- Relationships between containers show protocols and data flow
- The system boundary is drawn as a dashed rectangle

### Level 3 - Component

- Expands a single container to show its internal components
- Other containers within the system are shown for context
- Components show their name, technology, and responsibility
- Relationships show how components interact and delegate

### Level 4 - Code

- Expands a single component to show implementation detail
- Typically uses UML class diagrams, entity relationship diagrams, or similar
- This level is optional -- only create when the detail adds value
- Consider auto-generating from source code

## Diagram Checklist Summary

- Every element has a name, type, technology (where applicable), and description
- Every relationship has a label describing the interaction
- The diagram has a title and a key/legend
- Internal vs external elements are visually distinguished
- The system boundary is clearly marked (Levels 2 and 3)
