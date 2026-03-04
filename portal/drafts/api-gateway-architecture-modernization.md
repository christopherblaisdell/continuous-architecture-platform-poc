---
tags:
  - architecture
  - modernization
  - api-gateway
  - security
  - zero-trust
---

# API Gateway Architecture Modernization

> **Status:** Analysis — As-Is Assessment Complete, To-Be Evaluation Pending
>
> **Date:** 2026-03-04
>
> **Author:** Architecture Practice
>
> This document captures the formal classification of NovaTrek's current API gateway and authorization architecture, identifies its structural anti-patterns by industry name, and provides a ready-to-use prompt for continuing the modernization evaluation with any AI assistant.

---

## The Architectural Model: What It Is Called

The current setup is a combination of two distinct, highly rigid design patterns — one at the infrastructure layer and one at the application layer.

Collectively, this is best described as:

!!! warning "Current Architecture Classification"

    **A Siloed API Gateway Architecture with Tightly Coupled, Code-Bound Authorization**

The following sections break down the specific terminology for each layer.

---

## Layer-by-Layer Classification

### Infrastructure Layer: Infrastructure-Level Segmentation

**Industry name:** Gateway-per-Zone pattern

Instead of using logical routing based on identity, the current architecture uses physical/virtual infrastructure to draw hard boundaries. Every new compliance or trust zone (such as PCI) requires an entirely new IaaS footprint.

| Characteristic | Current State |
|----------------|---------------|
| **Pattern name** | Infrastructure-Level Segmentation |
| **Alias** | Gateway-per-Zone |
| **Routing mechanism** | Physical/virtual infrastructure boundaries |
| **Zone isolation** | Separate IaaS instances per consumer zone |
| **Scaling model** | Horizontal duplication of entire gateway stacks |
| **Primary risk** | **Infrastructure Sprawl** |

**How it manifests:** Multiple, completely separate IaaS instances of the API Gateway (Kraken) are deployed — one per consumer zone (Public/External, Internal, B2B/Partners). Each instance is independently provisioned, configured, monitored, and maintained.

---

### API Contract Layer: Topologically Bound Endpoints

**Industry name:** Topologically Bound Contracts

The Swagger/OpenAPI specifications are hardcoded to care about the physical network deployment rather than just defining the API's capabilities. Endpoint definitions carry awareness of *where* they are deployed, not just *what* they do.

| Characteristic | Current State |
|----------------|---------------|
| **Pattern name** | Topologically Bound Endpoints |
| **Contract concern** | Network topology embedded in API specs |
| **Portability** | Low — specs are pinned to specific gateway instances |
| **Reusability** | Low — same API served from different zones requires duplicate specs |
| **Primary risk** | **Specification drift and duplication** |

**How it manifests:** OpenAPI specifications explicitly define which specific gateway instance (network zone) an endpoint is permitted to live on. Moving an endpoint between zones requires modifying the specification itself.

---

### Code Layer: Invasive Security Routing

**Industry names:** Invasive Security Routing, Hardcoded Authorization

By forcing service methods to require a `{guest-id}` or token as a compiled argument, business logic is tightly coupled to security policies. Changing an access rule creates a **Lockstep Deployment**, forcing a full recompilation and release cycle.

| Characteristic | Current State |
|----------------|---------------|
| **Pattern name** | Invasive Security Routing / Hardcoded Authorization |
| **Authorization model** | Compiled into service method signatures |
| **Security parameter** | `{guest-id}` and token validation as required method arguments |
| **Change mechanism** | Code change, recompile, retest, redeploy |
| **Decoupling level** | None — security is fused with business logic |
| **Primary risk** | **Lockstep Deployments** |

**How it manifests:** If an endpoint needs to change its authorization requirements (e.g., no longer require a token), the only mechanism is to modify application source code, recompile, retest, and redeploy the backend service. A gateway policy change alone is insufficient.

---

## Anti-Pattern Summary

| Anti-Pattern | Layer | Consequence |
|-------------|-------|-------------|
| **Infrastructure Sprawl** | Infrastructure | New compliance zones require entirely new gateway stacks — linear cost growth with each new trust boundary |
| **Topological Coupling** | API Contract | Specifications encode deployment topology, preventing portable or environment-agnostic API definitions |
| **Lockstep Deployment** | Code | Security policy changes trigger full SDLC cycles (code, build, test, deploy) instead of configuration changes |
| **Hardcoded Authorization** | Code | Business logic cannot be reasoned about independently from access control |
| **Zone Duplication** | Infrastructure + Contract | Same API capability served to different consumer zones requires duplicated infrastructure and specifications |

---

## Migration Evaluation Prompt

The following prompt can be copied and pasted directly into any AI assistant to continue evaluating modernization strategies for this architecture. It is written from the perspective of an Enterprise Architect looking to modernize a legacy cloud setup.

---

??? example "Copy-Paste AI Prompt — Click to expand"

    ```text
    Act as an expert Enterprise Cloud Architect specializing in API Gateway
    modernization, distributed systems, and modern security patterns (such as
    Zero Trust and Policy-as-Code).

    I need you to analyze my organization's current "As-Is" API and authorization
    architecture, identify the primary bottlenecks, and propose a modernized
    "To-Be" architecture.

    Current "As-Is" Architecture:

    1. Infrastructure-Level Segmentation: We currently run multiple, completely
       separate IaaS instances of an API Gateway (Kraken). Each instance is
       dedicated to a specific consumer zone (e.g., one for Public/External, one
       for Internal, one for B2B/Partners).

    2. Topologically Bound Contracts: In our Swagger/OpenAPI specifications, we
       explicitly define which specific gateway instance (network zone) an
       endpoint is permitted to live on.

    3. Tightly Coupled Authorization: Our backend services have hardcoded security
       parameters. For example, specific methods are compiled to strictly require
       a {guest-id} argument and validate a user token.

    4. Lockstep Deployments: If we want to change an endpoint so that it no longer
       requires a token, we cannot just change a gateway policy. We have to modify
       the application code, recompile, retest, and redeploy the backend service.

    5. Infrastructure Sprawl for New Contexts: If a new security context arises
       (e.g., we need a PCI-compliant zone), our only mechanism to handle this is
       to stand up a completely new, separate API Gateway infrastructure, update
       the Swagger specs to point to it, and write/deploy new code.

    What I need from you:

    A. What are the major risks, scalability issues, and anti-patterns present in
       this current model?

    B. What is the industry-standard "To-Be" architectural pattern to solve this?
       (Please discuss Centralized/Federated API Gateways and Externalized
       Authorization/Policy-as-Code).

    C. How do we decouple the security logic (the {guest-id} and token validation)
       from our compiled backend code so that routing and authorization can be
       handled dynamically?

    D. Provide a high-level, phased migration strategy to move from this siloed,
       code-bound architecture to a modern, configuration-driven architecture
       without causing massive downtime.
    ```

---

## Key Modernization Concepts to Evaluate

The following patterns and technologies represent the industry-standard "To-Be" alternatives to the current anti-patterns. These should be explored in the modernization evaluation.

| Current Anti-Pattern | Modernization Pattern | Key Technologies |
|---------------------|----------------------|-----------------|
| Gateway-per-Zone | **Centralized/Federated API Gateway** | Kong Enterprise, Apigee, AWS API Gateway, Azure APIM |
| Topologically Bound Contracts | **Topology-Agnostic API Specifications** | OpenAPI 3.1 with server variables, API-first design |
| Hardcoded Authorization | **Externalized Authorization (Policy-as-Code)** | Open Policy Agent (OPA), Cedar, Ory Keto, Azure AD RBAC |
| Lockstep Deployments | **Configuration-Driven Security** | Gateway-level policy engines, sidecar proxies (Envoy, Istio) |
| Infrastructure Sprawl | **Logical Segmentation via Policy** | Zero Trust Network Architecture, mTLS, SPIFFE/SPIRE |

---

## Next Steps

- [ ] Run the evaluation prompt against the selected AI toolchain
- [ ] Document the proposed "To-Be" architecture as a formal ADR
- [ ] Map the phased migration strategy to the NovaTrek roadmap
- [ ] Identify which NovaTrek services are most impacted by the current anti-patterns
- [ ] Assess ISO 25010 quality attribute impact (Security, Maintainability, Portability)
