# 5. Building Block View

> **Help**: The building block view shows the static decomposition of the system into building blocks (modules, components, subsystems, classes, interfaces, packages, libraries, frameworks, layers, partitions, tiers, functions, macros, operations, data structures, ...) as well as their dependencies (relationships, associations, ...).
>
> This view is mandatory for every architecture documentation. It is the analogy to the floor plan of a building.
>
> **Motivation**: Maintain an overview of your source code by making its structure understandable through abstraction. This allows you to communicate with stakeholders on an abstract level without disclosing implementation details.
>
> **Form**: The building block view is a hierarchical collection of black boxes and white boxes and their descriptions.
>
> - **Level 1** is the white box description of the overall system together with black box descriptions of all contained building blocks.
> - **Level 2** zooms into some building blocks of Level 1 (i.e., contains the white box description of selected building blocks of Level 1, together with black box descriptions of their internal building blocks).
> - **Level 3** zooms into selected building blocks of Level 2, and so on.

---

## 5.1 Whitebox Overall System (Level 1)

> **Help**: Here you describe the decomposition of the overall system using the following white box template. It contains:
>
> - An overview diagram
> - A motivation for this decomposition
> - Black box descriptions of the contained building blocks
> - (Optional) important interfaces

### Overview Diagram

_\<Insert an overview diagram of the system decomposition. Consider using C4 Container diagram, UML component diagram, or similar.\>_

```
┌──────────────────────────────────────────────────────────┐
│                  <<System Name>>                          │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Building  │  │Building  │  │Building  │  │Building  │ │
│  │Block A   │──│Block B   │──│Block C   │──│Block D   │ │
│  │          │  │          │  │          │  │          │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│       │                           │                      │
│       ▼                           ▼                      │
│  ┌──────────┐              ┌──────────┐                  │
│  │Building  │              │Building  │                  │
│  │Block E   │              │Block F   │                  │
│  └──────────┘              └──────────┘                  │
└──────────────────────────────────────────────────────────┘
```

### Motivation

_\<Explain why you chose this particular decomposition. What was the driving factor -- domain boundaries, team structure, technical layers, or deployment units?\>_

### Contained Building Blocks

| Building Block | Responsibility | Interface(s) |
|---------------|---------------|--------------|
| _\<Block A\>_ | _\<What is this block responsible for?\>_ | _\<Key interfaces it exposes\>_ |
| _\<Block B\>_ | _\<What is this block responsible for?\>_ | _\<Key interfaces it exposes\>_ |
| _\<Block C\>_ | _\<What is this block responsible for?\>_ | _\<Key interfaces it exposes\>_ |
| _\<Block D\>_ | _\<What is this block responsible for?\>_ | _\<Key interfaces it exposes\>_ |
| _\<Block E\>_ | _\<What is this block responsible for?\>_ | _\<Key interfaces it exposes\>_ |
| _\<Block F\>_ | _\<What is this block responsible for?\>_ | _\<Key interfaces it exposes\>_ |

### Important Interfaces

_\<Describe the most important interfaces between building blocks. Focus on interfaces that are architecturally significant.\>_

| Interface | From | To | Description | Technology |
|-----------|------|-----|-------------|------------|
| _\<Interface 1\>_ | _\<Block A\>_ | _\<Block B\>_ | _\<What is communicated?\>_ | _\<REST/gRPC/Event\>_ |
| _\<Interface 2\>_ | _\<Block B\>_ | _\<Block C\>_ | _\<What is communicated?\>_ | _\<REST/gRPC/Event\>_ |

---

## 5.2 Level 2

> **Help**: Here you can specify the inner structure of (some) building blocks from Level 1 as white boxes. You have to decide which building blocks of your system are important enough to justify a detailed description. Please prefer relevance over completeness. Specify important, surprising, risky, complex, or volatile building blocks. Leave out normal, simple, boring, or standardized parts.

### 5.2.1 _\<Building Block A\>_ (White Box)

> _\<Purpose/Responsibility\>_

#### Overview Diagram

_\<Insert a diagram showing the internal structure of this building block.\>_

#### Contained Building Blocks

| Building Block | Responsibility |
|---------------|---------------|
| _\<Sub-Block A.1\>_ | _\<Describe responsibility\>_ |
| _\<Sub-Block A.2\>_ | _\<Describe responsibility\>_ |
| _\<Sub-Block A.3\>_ | _\<Describe responsibility\>_ |

#### Internal Interfaces

_\<Describe important internal interfaces of this building block.\>_

---

### 5.2.2 _\<Building Block B\>_ (White Box)

> _\<Purpose/Responsibility\>_

#### Overview Diagram

_\<Insert a diagram showing the internal structure of this building block.\>_

#### Contained Building Blocks

| Building Block | Responsibility |
|---------------|---------------|
| _\<Sub-Block B.1\>_ | _\<Describe responsibility\>_ |
| _\<Sub-Block B.2\>_ | _\<Describe responsibility\>_ |

---

## 5.3 Level 3

> **Help**: Here you can specify the inner structure of (some) building blocks from Level 2 as white boxes. Only detail Level 3 when strictly necessary for understanding or when the building block is particularly complex, risky, or volatile.

### 5.3.1 _\<Building Block A.1\>_ (White Box)

> _\<Purpose/Responsibility\>_

#### Overview Diagram

_\<Diagram of internal structure\>_

#### Contained Building Blocks

| Building Block | Responsibility |
|---------------|---------------|
| _\<Sub-Block A.1.1\>_ | _\<Describe responsibility\>_ |
| _\<Sub-Block A.1.2\>_ | _\<Describe responsibility\>_ |

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
