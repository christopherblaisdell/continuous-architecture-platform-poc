# 1. Introduction and Goals

> **Help**: Describes the relevant requirements and the driving forces that software architects and the development team must consider. These include:
>
> - Underlying business goals, essential features, and functional requirements for the system
> - Quality goals for the architecture
> - Relevant stakeholders and their expectations
>
> This section should give readers a quick overview of the system's purpose and the key forces shaping architectural decisions.

---

## 1.1 Requirements Overview

> **Help**: Short description of the functional requirements, driving forces, and an extract of the requirements document (or a link to it). For most projects, a short excerpt of the most important requirements is sufficient. Link to more detailed requirements documents if they exist.
>
> **Motivation**: From the point of view of the end users, a system is created or modified to improve support of a business activity or improve the quality of that activity.
>
> **Form**: Short textual description, probably in tabular use-case format. If requirements documents exist, this overview should refer to those documents. Keep these excerpts as short as possible. Balance readability with redundancy.

### Purpose

_\<Describe the purpose of the system in 2-3 sentences\>_

### Essential Features

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| F-01 | _\<feature name\>_ | _\<brief description\>_ | _\<High/Medium/Low\>_ |
| F-02 | _\<feature name\>_ | _\<brief description\>_ | _\<High/Medium/Low\>_ |
| F-03 | _\<feature name\>_ | _\<brief description\>_ | _\<High/Medium/Low\>_ |

### Key Use Cases

_\<Describe or reference the most important use cases. Consider a use case diagram.\>_

---

## 1.2 Quality Goals

> **Help**: The top three to five quality goals for the architecture whose achievement is of highest importance to the major stakeholders. We really mean quality goals for the architecture, not project goals. They are not necessarily identical.
>
> **Motivation**: You should know the quality goals of your most important stakeholders, since they will influence fundamental architectural decisions. Make sure to be very concrete about these qualities, avoid buzzwords. If you as an architect do not know how the quality of your work will be judged, you will not be able to make effective decisions.
>
> **Form**: A table with quality goals and concrete scenarios, ordered by priorities. Consider using the ISO 25010 quality model as a reference.

| Priority | Quality Goal | Scenario |
|----------|-------------|----------|
| 1 | _\<e.g., Performance\>_ | _\<Concrete measurable scenario describing this quality goal\>_ |
| 2 | _\<e.g., Availability\>_ | _\<Concrete measurable scenario describing this quality goal\>_ |
| 3 | _\<e.g., Modifiability\>_ | _\<Concrete measurable scenario describing this quality goal\>_ |
| 4 | _\<e.g., Security\>_ | _\<Concrete measurable scenario describing this quality goal\>_ |
| 5 | _\<e.g., Usability\>_ | _\<Concrete measurable scenario describing this quality goal\>_ |

---

## 1.3 Stakeholders

> **Help**: Explicit overview of stakeholders of the system -- i.e., every person, role, or organization that:
>
> - Should know the architecture
> - Has to be convinced of the architecture
> - Has to work with the architecture or with the code
> - Needs the documentation of the architecture for their work
> - Has to come up with decisions about the system or its development
>
> **Motivation**: You should know all parties involved in the development of the system or affected by the system. Otherwise, you may get nasty surprises later during development. These stakeholders determine the extent and detail of your work and its results.
>
> **Form**: Table with role names, person names, and their expectations regarding the architecture and documentation.

| Role/Name | Contact | Expectations |
|-----------|---------|--------------|
| _\<Product Owner\>_ | _\<contact info\>_ | _\<What does this stakeholder expect from the architecture?\>_ |
| _\<Development Team\>_ | _\<contact info\>_ | _\<What does this stakeholder expect from the architecture?\>_ |
| _\<Operations Team\>_ | _\<contact info\>_ | _\<What does this stakeholder expect from the architecture?\>_ |
| _\<End Users\>_ | _\<contact info\>_ | _\<What does this stakeholder expect from the architecture?\>_ |
| _\<Architect\>_ | _\<contact info\>_ | _\<What does this stakeholder expect from the architecture?\>_ |
| _\<Management\>_ | _\<contact info\>_ | _\<What does this stakeholder expect from the architecture?\>_ |
| _\<Compliance/Security\>_ | _\<contact info\>_ | _\<What does this stakeholder expect from the architecture?\>_ |

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
