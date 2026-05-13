# OpenSpec: Greenfield vs Brownfield — Corporate Workspace Context

> **This document is a stub for the corporate workspace.**
> All state assessments marked `PENDING DISCOVERY` must be populated by running
> `.openspec/prompts/corp-discovery.prompt.md` in the corporate workspace.
> Rewrite each PENDING DISCOVERY block in-place based on the discovery findings.
> When all blocks are replaced, remove this banner.

This document describes where greenfield vs brownfield concerns apply to this specific OpenSpec adoption, and what to do about each one.

---

## Our Starting Position

> **PENDING DISCOVERY** — All state assessments in this table must be populated by running
> `.openspec/prompts/corp-discovery.prompt.md`. Replace each row's State and Notes cells
> with findings from the corporate workspace audit before treating this table as authoritative.

| Axis | Our State | Notes |
|------|-----------|-------|
| AI instruction infrastructure | **PENDING DISCOVERY** | Determine: do tool-native instruction files exist in `.github/`, `.cursor/`, `.roo/`? Are they current? Was OpenSpec already bootstrapped? |
| OpenAPI / Swagger specs | **PENDING DISCOVERY** | Determine: where do specs live? Are they in `architecture/specs/`? Are there existing Swagger/OpenAPI files outside that path? Are any auto-generated from code? |
| Component diagrams | **PENDING DISCOVERY** | Determine: what format are existing diagrams? (PlantUML, Miro, Lucidchart, Visio, draw.io, other). Are any in `architecture/diagrams/`? |
| Sequence diagrams | **PENDING DISCOVERY** | Same as component diagrams — determine format and location. |
| ADRs | **PENDING DISCOVERY** | Determine: does a formal ADR registry exist? Where do ADRs live? Are they in MADR format? How many exist? |
| Capability model | **PENDING DISCOVERY** | Determine: does a formal capability taxonomy exist? Is `architecture/metadata/capabilities.yaml` populated? |
| Solution designs | **PENDING DISCOVERY** | Determine: where do solution designs live? Are they in `architecture/solutions/`? Is there a legacy documentation system (Confluence, Notion, SharePoint, wiki) with historical designs? |
| Test standards | **PENDING DISCOVERY** | Determine: is `config/test-standards.yaml` populated? What test infrastructure exists (unit, integration, BDD/Gherkin, contract tests)? |
| AsyncAPI / event specs | **PENDING DISCOVERY** | Determine: does an event-driven architecture exist? Are event schemas documented? Where? |
| CI/CD pipeline | **PENDING DISCOVERY** | Determine: what CI/CD system is in use? Is the OpenSpec generator check gate already wired in? |

---

## AI Instruction Infrastructure

> **PENDING DISCOVERY** — Determine whether this axis is greenfield or brownfield in the corporate workspace.
> Replace this section with findings for the "AI instruction infrastructure" axis from
> `.openspec/prompts/corp-discovery.prompt.md`.
>
> **If greenfield (no existing instruction files):** No reconciliation needed. The generator runs cleanly.
>
> **If brownfield (existing instruction files found):** Review each file for conflicts with the generator
> output. Files produced by `scripts/generate-tool-instructions.py` will overwrite any manually
> maintained versions. Decide which axes to preserve before running the generator.

---

## Brownfield Artifacts: What to Do

> **PENDING DISCOVERY** — Determine which of the following artifact categories contain brownfield
> content in the corporate workspace. Update each sub-section header with the correct state label
> (Brownfield / Institutional knowledge / Greenfield / Not applicable) after running discovery.

---

### OpenAPI / Swagger Specifications

**What this covers:** REST API contracts, gRPC proto files, Swagger 2.0 JSON files, OpenAPI 3.x YAML files, WSDL/SOAP contracts, GraphQL schema files. In OpenSpec, these live in `architecture/specs/`.

> **PENDING DISCOVERY** — Determine the actual state of API specs in this workspace:
> - Are specs already in `architecture/specs/`? If so, are they current?
> - Are there existing Swagger/OpenAPI files elsewhere in the repo or in a separate specs repository?
> - Are specs auto-generated from code annotations? If so, which framework generates them?
> - Do specs reflect current service behavior, or an earlier design state?
>
> Replace this block with a concrete description of what was found and what the first-move action is.

**The import rule:** If specs exist outside `architecture/specs/`, copy them verbatim before normalizing. Import first, then normalize service by service in subsequent changes. This keeps the prior-art registry accurate while avoiding breaking changes.

**The normalization decision:** Existing specs may not conform to the OpenSpec design rules — inconsistent naming, missing descriptions, wrong HTTP semantics. When a spec is touched for the first time, make an explicit decision: normalize the whole spec to the standard (potentially breaking consumers) or apply new rules only to new fields and leave existing fields as-is. This decision is worth capturing as an ADR.

**Auto-generated specs:** If specs are generated from code annotations, the file in `architecture/specs/` will drift from reality unless the generation pipeline keeps it updated. Before treating an imported spec as authoritative, confirm it reflects the current codebase — not the codebase as it was when the spec was last manually updated.

> **PENDING DISCOVERY — First move:** Describe the specific first-move action here after discovery.
> Example: "Import all existing OpenAPI files from `services/*/api/openapi.yaml` into `architecture/specs/` verbatim."

---

### Component Diagrams and Sequence Diagrams

> **PENDING DISCOVERY** — Determine the actual format and location of existing diagrams:
> - Are diagrams already in PlantUML/C4 format in `architecture/diagrams/`?
> - Are they in a non-PlantUML format (Visio, Miro, Lucidchart, draw.io, PNG exports)?
> - Where are they stored (repo, wiki, shared drive, portal)?
> - Are they current or stale relative to the actual services?
>
> Replace this block with the specific format and location found, then update the guidance below.

**The authority question:** When an existing diagram disagrees with an imported Swagger spec (common in brownfield), the spec wins. Diagrams are outputs derived from specs and metadata — they are not an independent source of truth. Establish this explicitly: if a diagram and a spec conflict, the spec is authoritative and the diagram needs to be regenerated.

**If diagrams are in non-PlantUML format:** Do not convert all existing diagrams upfront. Convert only the diagrams for services under active development. For everything else, link to the legacy diagram from the portal as a historical reference and note its status as unverified. Retire legacy diagrams as each service's PlantUML equivalents are generated and reviewed.

**If diagrams are already in PlantUML/C4 format:** Verify they were generated from the current specs, not manually authored. Manually authored PlantUML diagrams may conflict with generator output — the generator must be treated as the authoritative source.

**Accuracy check first:** Many existing diagrams show the system as it was designed, not as it currently operates. Before converting a diagram to PlantUML, verify it against actual service behavior. Converting an inaccurate diagram makes the inaccuracy more official-looking without improving it.

> **PENDING DISCOVERY — First move:** Describe the specific first-move action here after discovery.

---

## Institutional Knowledge: Handling What Is Not Yet Documented

> **PENDING DISCOVERY** — This section covers architectural knowledge that may exist in people's heads rather than formal artifacts. Verify which of the following sub-sections apply to the corporate workspace. Mark any axis as "Not applicable" if it is already formally documented and current.

---

### ADRs

> **PENDING DISCOVERY** — Determine the state of the ADR registry:
> - Does a formal ADR registry exist? Where does it live?
> - Are ADRs in MADR format? Another format? Mixed?
> - How many ADRs exist? What is the highest ADR number?
> - Is `decisions/` populated? Are ADRs referenced in solution designs?
>
> Replace this block with a concrete description of the current state. Then apply the appropriate guidance below.

**If the ADR registry is empty (institutional knowledge only):** The AI will propose trade-off analysis for questions that have already been settled — it does not know what has been decided unless an ADR exists. The practical approach is triage, not comprehensive retroactive documentation:

1. Before the first proposal, identify the 5-10 decisions that a new change is most likely to contradict. Common examples: authentication strategy, inter-service communication style, data ownership rules, error handling conventions, naming conventions.
2. Write retroactive ADRs for those decisions using MADR format with `Status: Accepted` and an approximate date.
3. Assign ADR numbers starting from the next available slot. Each new decision made through the OpenSpec workflow adds the next number in sequence.
4. Do not attempt to document all institutional decisions upfront. The retroactive ADR registry grows naturally as proposals surface questions that need to be settled.

**If an ADR registry exists:** Review existing ADRs for format compatibility with MADR. Determine the current highest ADR number so new decisions continue the sequence rather than creating conflicts.

---

### Capability Model

> **PENDING DISCOVERY** — Determine the state of the capability model:
> - Does `architecture/metadata/capabilities.yaml` exist and is it populated?
> - Is there any existing capability taxonomy (L1/L2 business capabilities)?
> - What vocabulary do engineering teams actually use to describe service groupings?
>
> Replace this block with findings. Then apply the appropriate guidance below.

**If no formal capability taxonomy exists:** The practical approach is bottom-up derivation:

1. List all existing services.
2. Group them by business function — this grouping becomes the L2 capability layer.
3. Group the L2 capabilities into business domains — this becomes the L1 layer.
4. Populate `architecture/metadata/capabilities.yaml` with this initial model.
5. Use the language engineering teams actually use, not enterprise architecture vocabulary. A capability model in the wrong vocabulary will be ignored.

L3 capabilities emerge from solution designs as proposals are made — they are not pre-defined. The initial L1/L2 model is sufficient to start. Expect to refine it as the first few proposals expose gaps.

**If a capability taxonomy already exists:** Import the existing taxonomy into `architecture/metadata/capabilities.yaml`. Verify the vocabulary aligns with what engineering teams actually use before including it in proposals.

---

### Solution Designs

> **PENDING DISCOVERY** — Determine where historical solution designs live:
> - Is `architecture/solutions/` already populated?
> - Is there a legacy documentation system (Confluence, Notion, SharePoint, Google Docs, wiki)?
> - How much historical design content exists? Is it accessible to the AI?
> - Is bulk migration in scope, or will historical designs be referenced by URL?
>
> Replace this block with findings. Then apply the appropriate guidance below.

**For the `architecture/solutions/` registry:** Start fresh for new work regardless of legacy content. Every new change from the first proposal forward creates a solution design using the standard folder structure. Reference historical designs by URL in the requirements section of new proposals rather than migrating them in bulk.

When the AI performs prior-art discovery, instruct it to note that historical designs may exist in a legacy documentation system that has not been migrated. This prevents the AI from concluding that no prior art exists when prior art may be present but is not yet AI-accessible.

---

### Test Standards

> **PENDING DISCOVERY** — Determine the actual test infrastructure in place:
> - Is `config/test-standards.yaml` populated?
> - What test frameworks and types exist (unit, integration, BDD/Gherkin, contract tests, e2e)?
> - Is there a gap between current test practice and the aspirational standard?
>
> Replace this block with findings.

**The general rule:** Write `config/test-standards.yaml` to describe the actual test infrastructure in place, not the aspirational standard. If a test type does not exist, do not mark it as the standard — the AI will propose acceptance criteria that cannot be executed.

If there is a gap between current and target test practice, document both explicitly. This gives the AI the ability to write proposals that acknowledge the gap and suggest incremental steps toward the target state.

---

## Workflow Adjustments for This Context

The core propose → explore → apply → archive workflow is unchanged. The following adjustments apply to brownfield contexts and remain valid regardless of the specific state found during discovery.

### Proposals Touching Existing API Contracts

Any proposal that modifies a service with an existing Swagger spec must include:

- A "Current State" section describing the existing contract
- A backward compatibility assessment — which consumers depend on the existing shape
- A migration strategy if fields are being removed, renamed, or made required

The AI will not produce these sections by default on the first few proposals — they must be explicitly requested or added to the proposal prompt template.

### Proposals Requiring Diagram Updates

When a proposal changes service structure in a way that invalidates an existing diagram:

- The apply task list must include regenerating the affected PlantUML diagrams from the updated spec
- Do not update legacy diagrams — generate new PlantUML replacements instead
- If the existing diagram contains information not yet captured in the spec (e.g., a component structure not reflected in any OpenAPI operation), capture that information in `architecture/metadata/` before generating the replacement diagram

---

## Historical Design Repository

> **PENDING DISCOVERY** — Determine where historical architecture documentation lives and whether
> it is in scope for the current OpenSpec bootstrap:
> - What system(s) contain historical designs? (Confluence, Notion, SharePoint, Google Docs, wiki, other)
> - Is the content accessible to the AI (API, file export, URL reference)?
> - Is bulk migration in scope, or will historical designs be referenced by URL in new proposals?
>
> Replace this section with a concrete description of the legacy documentation system and the
> ingestion strategy. If no legacy documentation system exists, replace with "Not applicable."
>
> **If a legacy documentation system exists:** The AI will operate without visibility into historical
> context stored there. In practice:
> - The AI may re-propose patterns that were tried and rejected — flag these when they occur and
>   use them as the trigger for writing a retroactive ADR
> - Prior-art discovery will return incomplete results until legacy content is migrated — acknowledge
>   this explicitly in proposals rather than treating empty prior-art discovery as confirmation that
>   no prior art exists
> - As institutional knowledge is surfaced through proposals and discussions, capture it as ADRs and
>   solution designs in the repo rather than in the legacy system — this builds the AI-accessible
>   registry incrementally without requiring a bulk migration
