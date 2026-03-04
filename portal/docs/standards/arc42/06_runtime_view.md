# 6. Runtime View

> **Help**: The runtime view describes concrete behavior and interactions of the system's building blocks in the form of scenarios from the following areas:
>
> - Important use cases or features: how do building blocks execute them?
> - Interactions at critical external interfaces: how do building blocks cooperate with users and neighboring systems?
> - Operation and administration: launch, start-up, stop
> - Error and exception scenarios
>
> **Motivation**: You should understand how (instances of) building blocks of your system perform their job and communicate at runtime. You will mainly capture scenarios in your documentation to communicate your architecture to stakeholders who are less willing or able to read and understand the static models (building block view, deployment view).
>
> **Form**: There are many notations for describing scenarios, e.g.:
> - Numbered list of steps (in natural language)
> - Activity diagrams or flow charts
> - Sequence diagrams
> - BPMN or EPCs (event process chains)
> - State machines

---

## 6.1 _\<Runtime Scenario 1: Key Use Case\>_

> **Help**: Describe the most important runtime scenario first -- typically the primary use case or "happy path" that stakeholders care about most.

### Description

_\<Describe the scenario in 2-3 sentences. What triggers it? What is the expected outcome?\>_

### Sequence Diagram

_\<Insert a sequence diagram. Consider using PlantUML or Mermaid.\>_

```
Actor       -> API Gateway   : 1. HTTP Request
API Gateway -> Service A     : 2. Route request
Service A   -> Database      : 3. Query data
Database    -> Service A     : 4. Return results
Service A   -> Service B     : 5. Enrich with additional data
Service B   -> Service A     : 6. Return enriched data
Service A   -> API Gateway   : 7. Response
API Gateway -> Actor         : 8. HTTP Response
```

### Step-by-Step

| Step | Component | Action | Notes |
|------|-----------|--------|-------|
| 1 | _\<Actor\>_ | _\<Initiates request\>_ | _\<Trigger condition\>_ |
| 2 | _\<API Gateway\>_ | _\<Routes and authenticates\>_ | _\<JWT validation\>_ |
| 3 | _\<Service A\>_ | _\<Processes business logic\>_ | _\<Validation rules applied\>_ |
| 4 | _\<Database\>_ | _\<Persists/retrieves data\>_ | _\<Transaction boundary\>_ |
| 5 | _\<Service A\>_ | _\<Returns response\>_ | _\<Response transformation\>_ |

---

## 6.2 _\<Runtime Scenario 2: Alternative/Error Path\>_

> **Help**: Describe an important alternative or error scenario. How does the system behave when things go wrong?

### Description

_\<Describe what triggers this error scenario and how the system handles it.\>_

### Error Handling Flow

```
Actor       -> API Gateway   : 1. HTTP Request
API Gateway -> Service A     : 2. Route request
Service A   -> Service B     : 3. Call dependent service
Service B   --X Service A    : 4. TIMEOUT / FAILURE
Service A   -> Service A     : 5. Circuit breaker opens
Service A   -> Cache         : 6. Fallback to cached data
Cache       -> Service A     : 7. Return stale data
Service A   -> API Gateway   : 8. Degraded response (200 + warning)
API Gateway -> Actor         : 9. Response with degradation notice
```

### Behavior

| Condition | System Response | Recovery |
|-----------|----------------|----------|
| _\<Downstream timeout\>_ | _\<Return cached/default response\>_ | _\<Retry with exponential backoff\>_ |
| _\<Invalid input\>_ | _\<Return 400 with validation errors\>_ | _\<N/A - client must correct\>_ |
| _\<Authentication failure\>_ | _\<Return 401 Unauthorized\>_ | _\<Redirect to login\>_ |
| _\<Rate limit exceeded\>_ | _\<Return 429 Too Many Requests\>_ | _\<Respect Retry-After header\>_ |

---

## 6.3 _\<Runtime Scenario 3: Asynchronous Processing\>_

> **Help**: Describe scenarios involving asynchronous or event-driven processing.

### Description

_\<Describe the async workflow, what triggers it, and how eventual consistency is achieved.\>_

### Event Flow

```
Service A   -> Message Broker : 1. Publish event
Message Broker -> Service B   : 2. Deliver event
Service B   -> Database B     : 3. Process and persist
Service B   -> Message Broker : 4. Publish completion event
Message Broker -> Service C   : 5. Deliver completion event
Service C   -> Notification   : 6. Notify user
```

---

## 6.4 _\<Runtime Scenario 4: Startup/Shutdown\>_

> **Help**: Describe the system startup and shutdown procedures if they are architecturally relevant.

### Startup Sequence

1. _\<Infrastructure provisioning / container orchestration readiness\>_
2. _\<Database migration check and execution\>_
3. _\<Configuration loading from config service\>_
4. _\<Health check endpoint becomes available\>_
5. _\<Service registers with service discovery\>_
6. _\<Traffic routing begins\>_

### Graceful Shutdown

1. _\<Stop accepting new requests\>_
2. _\<Complete in-flight requests (drain timeout: 30s)\>_
3. _\<Deregister from service discovery\>_
4. _\<Close database connections\>_
5. _\<Flush logs and metrics\>_
6. _\<Exit process\>_

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
