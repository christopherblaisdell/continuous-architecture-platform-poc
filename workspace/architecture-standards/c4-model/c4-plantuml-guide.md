# C4-PlantUML Guide

## Overview

C4-PlantUML combines the C4 model with PlantUML to create architecture diagrams as code. It provides a set of macros that map directly to C4 abstractions, enabling version-controllable, reproducible diagrams.

## Setup

Include the C4-PlantUML library at the top of your `.puml` file:

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
' Or for container diagrams:
' !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
' Or for component diagrams:
' !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml
@enduml
```

## Core Macros

| Macro | Purpose | Parameters |
|-------|---------|------------|
| `Person(alias, label, description)` | A user or actor | alias, display name, description |
| `System(alias, label, description)` | Internal software system | alias, display name, description |
| `System_Ext(alias, label, description)` | External software system | alias, display name, description |
| `Container(alias, label, technology, description)` | A container (app, DB, etc.) | alias, name, tech, description |
| `ContainerDb(alias, label, technology, description)` | Database container | alias, name, tech, description |
| `ContainerQueue(alias, label, technology, description)` | Message queue container | alias, name, tech, description |
| `Component(alias, label, technology, description)` | A component within a container | alias, name, tech, description |
| `Rel(from, to, label, technology)` | Relationship between elements | from alias, to alias, label, tech |

## System Context Diagram Example

```plantuml
@startuml C4_SystemContext
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

title System Context Diagram - Trail Management System

Person(guest, "NovaTrek Guest", "A visitor to the outdoor recreation platform")
Person(operator, "Park Operator", "Staff managing park operations")

System(trailMgmt, "Trail Management System", "Manages trail availability, conditions, and guest navigation")

System_Ext(weatherSvc, "Weather Service", "Provides real-time weather data")
System_Ext(mapProvider, "Map Provider", "Supplies base map tiles and geo data")
System_Ext(notificationSvc, "Notification Service", "Sends push notifications to guests")

Rel(guest, trailMgmt, "Views trail info, gets directions")
Rel(operator, trailMgmt, "Updates trail status, views reports")
Rel(trailMgmt, weatherSvc, "Fetches weather conditions", "REST/HTTPS")
Rel(trailMgmt, mapProvider, "Retrieves map data", "REST/HTTPS")
Rel(trailMgmt, notificationSvc, "Sends trail alerts", "REST/HTTPS")

@enduml
```

## Container Diagram Example

```plantuml
@startuml C4_Container
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

title Container Diagram - Trail Management System

Person(guest, "NovaTrek Guest", "A visitor to the outdoor recreation platform")

System_Boundary(trailMgmt, "Trail Management System") {
    Container(mobileApp, "Mobile App", "React Native", "Trail maps, navigation, and alerts")
    Container(webApp, "Web Dashboard", "React", "Operator dashboard for trail management")
    Container(apiGateway, "API Gateway", "Kong", "Routes and authenticates API requests")
    Container(trailApi, "Trail API", "Spring Boot", "Core trail management business logic")
    Container(geoService, "Geo Service", "Python/FastAPI", "Geospatial calculations and routing")
    ContainerDb(trailDb, "Trail Database", "PostgreSQL + PostGIS", "Trail data, conditions, geometry")
    ContainerQueue(eventBus, "Event Bus", "Apache Kafka", "Trail status change events")
}

System_Ext(weatherSvc, "Weather Service", "Provides weather data")

Rel(guest, mobileApp, "Uses")
Rel(mobileApp, apiGateway, "Makes API calls", "HTTPS")
Rel(webApp, apiGateway, "Makes API calls", "HTTPS")
Rel(apiGateway, trailApi, "Routes requests", "HTTP")
Rel(trailApi, geoService, "Requests routing", "gRPC")
Rel(trailApi, trailDb, "Reads/writes trail data", "JDBC")
Rel(trailApi, eventBus, "Publishes events", "Kafka protocol")
Rel(trailApi, weatherSvc, "Fetches weather", "REST/HTTPS")

@enduml
```

## Component Diagram Example

```plantuml
@startuml C4_Component
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Component Diagram - Trail API

Container_Boundary(trailApi, "Trail API") {
    Component(trailController, "Trail Controller", "Spring MVC", "Handles trail CRUD REST endpoints")
    Component(conditionController, "Condition Controller", "Spring MVC", "Handles trail condition updates")
    Component(trailService, "Trail Service", "Spring Bean", "Core trail business logic and validation")
    Component(conditionService, "Condition Service", "Spring Bean", "Trail condition assessment logic")
    Component(trailRepo, "Trail Repository", "Spring Data JPA", "Data access for trail entities")
    Component(eventPublisher, "Event Publisher", "Spring Kafka", "Publishes trail status events")
}

ContainerDb(trailDb, "Trail Database", "PostgreSQL + PostGIS", "Trail data storage")
ContainerQueue(eventBus, "Event Bus", "Kafka", "Trail events")
Container(geoService, "Geo Service", "Python/FastAPI", "Geospatial routing")

Rel(trailController, trailService, "Delegates to")
Rel(conditionController, conditionService, "Delegates to")
Rel(trailService, trailRepo, "Uses")
Rel(conditionService, trailRepo, "Uses")
Rel(conditionService, eventPublisher, "Publishes events via")
Rel(trailService, geoService, "Requests routing", "gRPC")
Rel(trailRepo, trailDb, "Reads/writes", "JDBC")
Rel(eventPublisher, eventBus, "Sends events", "Kafka")

@enduml
```

## Tips

- Use `LAYOUT_WITH_LEGEND()` at the end of a diagram to auto-generate a legend
- Use `LAYOUT_LEFT_RIGHT()` or `LAYOUT_TOP_DOWN()` to control layout direction
- Use `Boundary()` to group related elements visually
- Keep descriptions concise: aim for one sentence per element
- Store `.puml` files alongside source code for version control
