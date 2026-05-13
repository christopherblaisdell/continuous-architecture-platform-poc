# Deep Research Prompt: Consuming an Azure AI Foundry Model in OpenCode

## Research Objective

Produce a **thorough, step-by-step, verified guide** for how to configure OpenCode to call a language model deployed in Azure AI Foundry. The guide must be actionable — every step must have a concrete command, configuration snippet, or verification test. Assume nothing works until proven.

Be skeptical of official documentation: Azure AI Foundry and OpenCode are both rapidly evolving products. Documentation is frequently stale, incomplete, or describes a UI that no longer exists. Where official docs and community evidence conflict, cite both and flag the discrepancy rather than silently preferring one.

---

## Target Products — Clarify These Before Writing Anything

### OpenCode

OpenCode (https://github.com/sst/opencode) is an open-source, terminal-based AI coding assistant built by SST. It is NOT Roo Code, not GitHub Copilot, not OpenRouter. It runs in the terminal and supports multiple AI providers via a `~/.config/opencode/config.json` (or equivalent) configuration file.

**CRITICAL**: Verify the current version of OpenCode before writing any configuration instructions. The project moves fast. Configuration schemas, provider names, and feature flags from blog posts written 6 months ago may no longer apply. Check the GitHub releases page and the actual source config schema — not the README marketing copy.

**Research tasks for OpenCode specifically:**
- What is the current stable version as of the research date?
- What is the exact configuration file format (location, schema, required vs optional fields)?
- Does OpenCode support custom base URL / OpenAI-compatible endpoints? If so, what is the exact configuration key?
- Does OpenCode support `azure` as a named provider, or does it use a generic `openai-compatible` provider type?
- What authentication mechanisms are supported: static API key in config, environment variable, Azure AD token (Bearer), Azure AD managed identity? Be explicit about which are actually implemented, not just theoretically possible.
- Does OpenCode support streaming (`stream: true`)? Is streaming required for the tool to function or optional?
- Does OpenCode support function calling / tool use for the models it calls? Is this auto-detected from the model's capabilities or must it be declared?
- Are there known open GitHub issues or community-reported problems with Azure-hosted endpoints specifically?

### Azure AI Foundry

Azure AI Foundry (formerly Azure AI Studio, formerly Azure ML model catalog, formerly Azure OpenAI Service — the naming history matters for understanding docs you may encounter) is Microsoft's platform for deploying AI models.

**Research tasks for Azure AI Foundry specifically:**
- What is the exact URL format for the inference endpoint produced when you deploy a model in Azure AI Foundry? Is it always OpenAI-compatible (`/v1/chat/completions`)? Or does it vary by model family (Phi vs GPT vs Llama vs Mistral)?
- What authentication does the inference endpoint require? Specifically:
  - Does it accept a static API key (set at deployment time)? Where is this key found in the portal?
  - Does it accept Azure AD bearer tokens? If so, what is the required scope (resource URI)?
  - Does it require both (double auth)?
  - Does the answer differ between "serverless API" deployments and "managed compute" deployments?
- What is the difference between a **serverless API deployment** and a **managed compute deployment** in the context of inference endpoint access? Which is easier to integrate with third-party tools?
- What does the response payload look like? Is it byte-for-byte OpenAI API compatible, or are there delta fields that might confuse a strict OpenAI-schema parser?
- Are there known streaming issues? Any models in Foundry that do not support streaming even though the endpoint claims to?
- What rate limits and quotas apply? Where are they configured and how are limit errors surfaced (HTTP 429 shape)?
- What is the correct model name to pass in the `model` field of the request body — the deployment name, the base model name, or something else?

---

## What the Final Guide Must Cover

Produce a **numbered, sequential step-by-step guide** with the following sections. Each section must contain concrete actions — no vague instructions like "configure your credentials." Every command must be copy-pasteable. Every configuration snippet must be a complete, minimal working example, not a template with placeholder-only fields.

### Part 1 — Prerequisites and Environment Verification

1. **Verify OpenCode is installed** — provide the install command for the current stable version (not `@latest` without first establishing what `latest` actually is). Include the version check command and the expected output format.

2. **Verify Azure CLI is installed and authenticated** — the guide should establish whether Azure CLI is needed at all for this workflow. If it is needed (e.g., for token retrieval), provide install instructions and the exact `az login` flow required. If it is not needed, say so explicitly.

3. **Azure subscription requirements** — what Azure subscription tier / region / quota is required to deploy a model? Are there models that are available in all regions vs only specific ones? Flag any model families (e.g., GPT-4o) that require capacity reservation or quota approval.

### Part 2 — Deploy a Model in Azure AI Foundry

4. **Create an Azure AI Foundry project** — exact portal navigation path or `az` CLI command sequence. Specify which resource type to create (AI Hub vs AI Project vs the old "AI Studio" workspace — these are different things). Include a working CLI command as the primary path; portal screenshots are acceptable as secondary context.

5. **Deploy a model for inference** — choose one specific model as the working example throughout the guide (suggest a small, widely available model like `Phi-3.5-mini-instruct` or `gpt-4o-mini` so the guide is reproducible without quota constraints). Walk through:
   - Navigating to the model catalog
   - Selecting serverless API deployment vs managed compute deployment — recommend one and justify why
   - The exact CLI command or portal steps to trigger the deployment
   - How to confirm the deployment is complete and healthy

6. **Retrieve the inference endpoint and API key** — exact steps to find:
   - The full base URL of the deployed model's inference endpoint
   - The API key (if applicable)
   - The exact model identifier to use in API requests
   - Include a `curl` command that proves the endpoint is live before OpenCode is involved at all

### Part 3 — Authenticate to the Endpoint

7. **API key authentication path** — if the deployment supports static API keys:
   - Where the key appears in the portal
   - How to store it securely (environment variable vs keychain vs config file)
   - Whether the key should be in the `Authorization: Bearer` header or an `api-key` header (these differ between Azure OpenAI Service and AI Foundry — flag this clearly)

8. **Azure AD token authentication path** — if the deployment requires or supports Entra ID tokens:
   - The correct Azure resource scope to request a token for
   - The exact `az account get-access-token` command
   - How token expiry is handled (tokens expire in ~1 hour — does OpenCode handle refresh, or does the user need to manually refresh?)
   - Whether managed identity is usable for local development or only for hosted workloads

9. **Verify authentication independently** — provide a `curl` command using the chosen auth method that performs a real chat completion against the deployed model. This is the smoke test before touching OpenCode config. Include the expected response shape and what a successful vs failed auth response looks like.

### Part 4 — Configure OpenCode

10. **Locate and create the OpenCode config file** — exact file path per OS (macOS, Linux, Windows). If the file does not exist, show the minimal skeleton to create it.

11. **Add the Azure Foundry model as a provider** — provide the complete configuration block. Specify:
    - The exact provider type name OpenCode uses for custom endpoints
    - The `baseUrl` field (note: does OpenCode expect the URL with or without `/v1` appended?)
    - The `apiKey` field — does it support reading from an environment variable (e.g., `$AZURE_FOUNDRY_API_KEY`) or must it be a literal string?
    - The model identifier field
    - Any Azure-specific headers that must be set (e.g., `api-key` header instead of `Authorization: Bearer`)
    - Any fields that control streaming, tool use, or context window size

12. **Verify OpenCode can reach the model** — show the exact OpenCode command or interactive flow that confirms the provider is wired up. What does a successful first response look like? What error messages indicate misconfiguration vs auth failure vs network failure?

### Part 5 — Known Failure Modes and Troubleshooting

13. **Authentication errors** — list the specific HTTP response codes and body shapes that indicate:
    - Wrong API key
    - Expired Azure AD token
    - Missing `api-key` header (Azure expects this header name, not `Authorization: Bearer`, in some configurations)
    - Insufficient RBAC permissions (what role is required on the Foundry resource?)

14. **Model name mismatch** — the `model` field in the request body must match what Azure expects. Describe what error is returned when the model name is wrong, and how to find the correct name.

15. **Streaming failures** — some Azure-hosted models return a streaming response with a non-standard termination sequence. Describe any known issues and how to disable streaming in OpenCode as a workaround.

16. **Tool call / function calling failures** — if the chosen model does not support function calling, OpenCode may fail silently or with a cryptic error. How to detect this and what to do.

17. **CORS / TLS / proxy issues** — are there any network-level gotchas for corporate proxy environments or VPNs?

### Part 6 — Maintenance and Operational Notes

18. **Rotating the API key** — how to update the key in both Azure Foundry (regenerate) and OpenCode config.

19. **Monitoring usage and cost** — where in the Azure portal to see token consumption and cost for the Foundry deployment.

20. **Model version updates** — when Microsoft updates the underlying model version, what changes at the endpoint level? Is the API key stable across model version updates?

---

## Research Methodology Requirements

- **Prioritize primary sources**: GitHub repository source code, Azure REST API specs, and official SDK changelogs over blog posts, tutorials, and StackOverflow answers.
- **Timestamp your sources**: For any source older than 6 months, flag it as potentially stale and note whether you found corroborating evidence from a recent source.
- **Test the curl commands yourself where possible**: Do not include a `curl` example unless you have verified the endpoint URL format is correct by cross-referencing the Azure REST API spec or a current official example.
- **Flag version-specific behavior**: If a step works in OpenCode 0.x but not 1.x (or vice versa), call that out explicitly rather than writing instructions that silently break for some users.
- **Distinguish "works" from "documented"**: If the official docs say X but community evidence suggests X does not actually work, report both and recommend the approach that has verified working examples.
- **Do not hallucinate configuration keys**: If you cannot confirm the exact configuration key name from source code or official documentation, say "the exact key name needs to be verified against the current OpenCode source at `src/config/schema.ts` (or equivalent)" rather than guessing.

---

## Output Format

Produce the guide as a single Markdown document structured as follows:

```
# How to Consume an Azure AI Foundry Model in OpenCode — Complete Guide

## Verified Against
- OpenCode version: [version]
- Azure AI Foundry: [as of date]
- Research date: [date]

## Quick Reference (TL;DR)
[5-bullet summary for experienced users who just need the config shape]

## Prerequisites
...

## Part 1 — [title]
### Step 1 — [title]
...

## Troubleshooting Reference
[table: symptom → likely cause → fix]

## Sources
[list with dates]
```

The guide must be self-contained. A user who has never used Azure AI Foundry before and who has OpenCode already installed should be able to follow it start-to-finish without referring to any other document.
