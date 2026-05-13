# OpenSpec: Greenfield vs Brownfield — Our Context

This document describes where greenfield vs brownfield concerns apply to this specific OpenSpec adoption, and what to do about each one.

## Our Starting Position

| Axis | Our State | Notes |
|------|-----------|-------|
| AI instruction infrastructure | **Greenfield** | No existing tool-native instruction files to reconcile. Follow MIGRATION-GUIDE.md directly. |
| OpenAPI / Swagger specs | **Brownfield** | Existing specs must be imported before the AI can propose non-conflicting API changes. |
| Component diagrams | **Brownfield** | Existing diagrams in a non-PlantUML format; must be converted or replaced. |
| Sequence diagrams | **Brownfield** | Same as component diagrams. |
| ADRs | **Institutional knowledge** | No formal ADR registry exists. Key decisions are in people's heads. Treat as greenfield for the artifact registry; surface institutional knowledge as retroactive ADRs. |
| Capability model | **Institutional knowledge** | No formal capability taxonomy. Derive from the service portfolio during bootstrap. |
| Solution designs | **Confluence (out of scope)** | Extensive knowledge exists in Confluence but ingesting it into AI is a separate future exercise. Treat as greenfield for the `architecture/solutions/` registry. |
| Test standards | **Institutional knowledge** | Conventions exist in practice; write `config/test-standards.yaml` to match what actually exists, not the aspirational standard. |
| AsyncAPI / event specs | **Institutional knowledge** | Event schemas live in code. Out of scope unless an event-driven change proposal requires them. |
| CI/CD pipeline | **Existing** | Wire the generator check gate carefully into the existing pipeline — see MIGRATION-GUIDE.md Step 9. |

---

## AI Instruction Infrastructure — Greenfield

No action required beyond following MIGRATION-GUIDE.md. There are no existing tool-native instruction files to reconcile. The generator runs cleanly from the first bootstrap.

---

## Brownfield Artifacts: What to Do

Three artifact types exist today and must be handled before the AI can reason about them accurately.

---

### OpenAPI / Swagger Specifications

**What this covers:** REST API contracts, gRPC proto files, Swagger 2.0 JSON files, OpenAPI 3.x YAML files, WSDL/SOAP contracts, GraphQL schema files. In OpenSpec, these live in `architecture/specs/`.

Existing Swagger files must be imported into `architecture/specs/` before the AI can reason about them. Without them, the AI will propose API changes that conflict with contracts consumers already depend on.

**The import rule:** Copy existing specs verbatim into `architecture/specs/` first. Do not normalize or clean them up in the same step. Import first, then normalize service by service in subsequent changes. This keeps the prior-art registry accurate while avoiding breaking changes.

**The normalization decision:** Existing specs almost certainly do not conform to your new OpenSpec design rules — inconsistent naming, missing descriptions, wrong HTTP semantics. When a spec is touched for the first time, make an explicit decision: normalize the whole spec to the standard (potentially breaking consumers) or apply new rules only to new fields and leave existing fields as-is. This decision is worth capturing as an ADR.

**Auto-generated specs:** If specs are generated from code annotations (e.g., springdoc, Django REST Framework), the file in `architecture/specs/` will drift from reality unless the generation pipeline keeps it updated. Before treating an imported spec as authoritative, confirm it reflects the current codebase — not the codebase as it was when the spec was last manually updated.

**First move:** Import all existing Swagger files into `architecture/specs/` verbatim. Verify each one against the actual service behavior before the first proposal that touches it.

---

### Component Diagrams and Sequence Diagrams

Existing diagrams are not in PlantUML/C4 format and cannot be read by the generator. The AI also cannot read image files (PNG, PDF) or proprietary formats (Visio, Lucidchart, Miro).

**The authority question:** When an existing diagram disagrees with the imported Swagger spec (common in brownfield), the spec wins. Diagrams are outputs derived from specs and metadata — they are not an independent source of truth. Establish this explicitly: if a diagram and a spec conflict, the spec is authoritative and the diagram needs to be regenerated.

**Conversion approach:** Do not convert all existing diagrams upfront. Convert only the diagrams for services under active development. For everything else, link to the legacy diagram from the portal as a historical reference and note its status as unverified. Retire legacy diagrams as each service's PlantUML equivalents are generated and reviewed.

**Accuracy check first:** Many existing diagrams show the system as it was designed, not as it currently operates. Before converting a diagram to PlantUML, verify it against actual service behavior. Converting an inaccurate diagram makes the inaccuracy more official-looking without improving it.

**First move:** For any service touched by a new proposal, generate its PlantUML C4 diagram from the imported Swagger spec rather than converting the existing diagram. The generator output will be more accurate than a conversion of a potentially stale source.

---

## Institutional Knowledge: Handling What Is Not Yet Documented

Most of the architecture practice exists in institutional knowledge rather than formal artifacts. The sections below describe how to handle each area pragmatically — the goal is not to document everything before starting, but to document enough that the AI produces accurate proposals.

### ADRs — Start Greenfield, Surface Key Decisions First

The ADR registry starts empty. The AI will propose trade-off analysis for questions that have already been settled in institutional knowledge — it does not know what has been decided unless an ADR exists.

The practical approach is triage, not comprehensive retroactive documentation:

1. Before the first proposal, identify the 5-10 decisions that a new change is most likely to contradict. Common examples: authentication strategy, inter-service communication style, data ownership rules, error handling conventions, naming conventions.
2. Write retroactive ADRs for those decisions using MADR format with `Status: Accepted` and an approximate date.
3. Start at ADR-001. Each new decision made through the OpenSpec workflow adds the next number in sequence.
4. Do not attempt to document all institutional decisions upfront. The retroactive ADR registry grows naturally as proposals surface questions that need to be settled.

### Capability Model — Derive from the Service Portfolio

No formal capability taxonomy exists. The practical approach is bottom-up derivation:

1. List all existing services.
2. Group them by business function — this grouping becomes the L2 capability layer.
3. Group the L2 capabilities into business domains — this becomes the L1 layer.
4. Populate `architecture/metadata/capabilities.yaml` with this initial model.
5. Use the language engineering teams actually use, not enterprise architecture vocabulary. A capability model in the wrong vocabulary will be ignored.

L3 capabilities emerge from solution designs as proposals are made — they are not pre-defined. The initial L1/L2 model is sufficient to start. Expect to refine it as the first few proposals expose gaps.

### Solution Designs — Start Fresh, Acknowledge Confluence Exists

The existing Confluence instance contains substantial solution design history. Ingesting this into AI-accessible artifacts is a separate future exercise and is out of scope for the initial OpenSpec bootstrap.

For the `architecture/solutions/` registry: start fresh. Every new change from the first proposal forward creates a solution design using the standard folder structure. The prior art is in Confluence — reference it by URL in the requirements section of new proposals rather than migrating it.

When the AI performs prior-art discovery, instruct it to note that Confluence contains historical designs that have not been migrated. This prevents the AI from concluding that no prior art exists when it may exist but is not yet accessible.

### Test Standards — Document What Actually Exists

Write `config/test-standards.yaml` to describe the actual test infrastructure in place, not the aspirational standard. If BDD/Gherkin infrastructure does not exist, do not mark it as the standard — the AI will propose Gherkin acceptance criteria that cannot be executed.

If there is a gap between current and target test practice, document both explicitly. This gives the AI the ability to write proposals that acknowledge the gap and suggest incremental steps toward the target state.

---

## Workflow Adjustments for This Context

The core propose → explore → apply → archive workflow is unchanged. Two specific adjustments apply given the brownfield artifacts.

### Proposals Touching Existing API Contracts

Any proposal that modifies a service with an imported Swagger spec must include:

- A "Current State" section describing the existing contract
- A backward compatibility assessment — which consumers depend on the existing shape
- A migration strategy if fields are being removed, renamed, or made required

The AI will not produce these sections by default on the first few proposals — they must be explicitly requested or added to the proposal prompt template.

### Proposals Requiring Diagram Updates

When a proposal changes service structure in a way that invalidates an existing diagram:

- The apply task list must include regenerating the affected PlantUML diagrams from the updated spec
- Do not update legacy diagrams — generate new PlantUML replacements instead
- If the existing diagram contains information not yet captured in the spec (e.g., a component structure not yet reflected in any OpenAPI operation), capture that information in `architecture/metadata/` before generating the replacement diagram

---

## Confluence — Out of Scope for Now

The Confluence instance contains the majority of the documented architecture history including solution designs, meeting notes, and decision rationale. Ingesting this content into AI-accessible artifacts is a deliberate future exercise and is not part of the current OpenSpec bootstrap.

This means the AI will operate without visibility into historical context stored in Confluence. In practice:

- The AI may re-propose patterns that were tried and rejected — flag these when they occur and use them as the trigger for writing a retroactive ADR
- Prior-art discovery will return incomplete results until Confluence content is migrated — acknowledge this explicitly in proposals rather than treating empty prior-art discovery as confirmation that no prior art exists
- As institutional knowledge is surfaced through proposals and discussions, capture it as ADRs and solution designs in the repo rather than in Confluence — this builds the AI-accessible registry incrementally without requiring a bulk migration

