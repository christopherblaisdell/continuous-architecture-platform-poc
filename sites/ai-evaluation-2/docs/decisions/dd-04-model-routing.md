<!-- CONFLUENCE-PUBLISH -->

# DD-04: Model Routing

| | |
|-----------|-------|
| **Status** | Resolved by DD-03 |
| **Date** | 2026-04-07 |
| **Scope** | How are different AI models selected and routed for different task types? |
| **Depends on** | DD-03 (AI Provider) |

---

## Problem Statement

Architecture work spans a range of task complexity — from quick triage and formatting to deep multi-service analysis and solution design. Different model tiers are appropriate for different tasks. The question is whether model routing requires custom infrastructure or is handled natively by the selected platform.

## Resolution

DD-04 is resolved by the provider selection in [DD-03](dd-03-ai-provider.md). Each option's model routing approach is inherent in the platform:

| Option | Model Routing Mechanism | Infrastructure Required |
|--------|------------------------|------------------------|
| **Option A (Copilot)** | Architect selects model per session. GPT-4o/4.1 (0x — free, unlimited) for routine tasks; Claude Opus 4.6 (3x) for architecture work. Built-in. | None |
| **Option B (Roo Code + Kong)** | Kong gateway routes requests to configured model providers. Operator configures routing rules. | Kong gateway provisioning and maintenance |
| **Option C (Bespoke Agent)** | Custom routing logic in the agent framework. Engineering team configures model tiers. | Custom development and ongoing maintenance |

With Option A selected as the recommended provider, model routing is a built-in capability requiring no additional infrastructure or decisions. The architect chooses the model when starting a session — frontier model for design work, routine model for everyday tasks.

---

**See also:**

- [DD-03: AI Provider](dd-03-ai-provider.md) — Provider selection that determines model routing
- [Platform Landscape](../evidence/platform-landscape.md) — Multi-model flexibility comparison (EF-07) across five platforms
