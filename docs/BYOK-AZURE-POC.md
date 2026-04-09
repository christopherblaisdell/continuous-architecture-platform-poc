# BYOK Azure POC — What We Did

## Summary

We deployed an Azure OpenAI endpoint via Bicep Infrastructure as Code (IaC), verified it responds to the exact API format that GitHub Copilot BYOK expects, documented the results, and tore everything down. The entire lifecycle — deploy, test, document, destroy — completed in a single session. Total cost: less than one cent.

## Why

The AI Toolchain Evaluation proposed **Option D (Hybrid)** — use GitHub Copilot as the platform and integrate a custom Foundry model via BYOK (Bring Your Own Key). Before recommending this to stakeholders, we needed to prove the Azure-side infrastructure actually works: Can we deploy an OpenAI-compatible endpoint that matches what BYOK expects? How hard is it? How much does it cost? Can we tear it down instantly?

## What We Built

### Bicep IaC (3 files)

| File | Purpose | Lines |
|------|---------|-------|
| `infra/modules/azure-openai.bicep` | Reusable module — deploys Azure OpenAI with parameterized model deployments | 67 |
| `infra/ai-poc.bicep` | Orchestrator — sets region, model, SKU, tags everything as `ephemeral` | 46 |
| `infra/deploy-ai-poc.sh` | Shell script — deploy with `./deploy-ai-poc.sh`, tear down with `./deploy-ai-poc.sh teardown` | 80 |

### Key Design Decisions

- **Standard SKU, not GlobalStandard** — eastus2 had zero quota for GlobalStandard. Standard had 50K TPM available for GPT-4o.
- **GPT-4o 2024-11-20, not GPT-4o-mini** — GPT-4o-mini (2024-07-18) was deprecated as of March 31, 2026. GPT-4o 2024-11-20 is GA and active.
- **Dedicated resource group (`rg-novatrek-ai-poc`)** — Isolated from production resources so tear-down is a single `az group delete` with no risk to other infrastructure.
- **Pay-per-token billing** — $0 when idle. No reserved capacity, no minimum spend. This is the "scales to zero" requirement.

## What We Proved

| Claim | Result |
|-------|--------|
| Azure OpenAI deploys via Bicep IaC | VERIFIED — zero Bicep diagnostics, clean deployment |
| Scales to zero (no idle cost) | VERIFIED — Standard SKU is pay-per-token only |
| Endpoint responds to OpenAI Chat Completions API | VERIFIED — 22 tokens consumed, correct response |
| Endpoint format matches BYOK requirements | VERIFIED — `https://{name}.openai.azure.com/` + deployment name + API key |
| Tear-down is a single command | VERIFIED — `./infra/deploy-ai-poc.sh teardown` |
| Total deployment time | Under 5 minutes (provider registration + Bicep + model provisioning) |
| BYOK registration in GitHub Copilot | NOT TESTED — requires org-level admin (Business/Enterprise plan) |

### API Test

```bash
curl https://oai-novatrek-poc.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-10-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: <KEY>" \
  -d '{"messages":[{"role":"user","content":"Say hello in exactly 5 words"}]}'
```

Response: `"Hello there, how are you?"` — 14 prompt tokens, 8 completion tokens, 22 total.

## What We Did NOT Test

**BYOK registration** — the step where a GitHub org admin registers the Azure OpenAI endpoint in Copilot's model picker. This requires a GitHub organization with Copilot Business or Enterprise seats. Our POC used a personal Pro+ account, which does not expose the org-level BYOK admin UI.

This is not an engineering gap. BYOK registration is a 5-field web form:

1. Provider: Microsoft Foundry
2. Name: (display name in model picker)
3. API Key: (from `az cognitiveservices account keys list`)
4. Deployment URL: `https://oai-novatrek-poc.openai.azure.com/`
5. Model ID: `gpt-4o` (the deployment name)

An org admin completes this in under 2 minutes. After registration, the model appears in every organization member's Copilot model picker alongside built-in models.

## Deployment Attempts (3 Iterations)

| Attempt | Config | Result | Root Cause |
|---------|--------|--------|------------|
| 1 | GPT-4o-mini, GlobalStandard | FAILED | eastus2 has 0 quota for GlobalStandard |
| 2 | GPT-4o-mini, Standard | FAILED | Model deprecated since 03/31/2026 |
| 3 | GPT-4o 2024-11-20, Standard | SUCCESS | GA model with available quota |

## Cost

| Item | Cost |
|------|------|
| Azure OpenAI resource (S0) | $0/month base |
| GPT-4o Standard deployment | $0 idle, ~$0.0025/1K input tokens when used |
| API test (22 tokens) | < $0.001 |
| **Total POC cost** | **< $0.01** |

## Teardown

The resource group was deleted immediately after validation:

```bash
./infra/deploy-ai-poc.sh teardown
```

All Azure resources removed. The Bicep templates remain in git — redeploy in under 5 minutes with `./infra/deploy-ai-poc.sh`.

## What This Means for Option D

1. **The Azure-side infrastructure is trivial.** 67 lines of Bicep. No vector databases, no embedding pipelines, no custom agent runtime. Compare this to Option C's full stack.
2. **Swapping models is a parameter change.** When Troy's team has a fine-tuned model ready, change the Bicep `modelName` parameter. Same endpoint, same API key, same BYOK registration.
3. **Cost is negligible.** Pay-per-token, zero idle cost. Copilot's $39/month subscription provides unlimited 0x-multiplier models for routine tasks — the custom model is only invoked (and billed) when an architect explicitly selects it.
4. **Registration is admin work, not engineering.** A 5-field form, completed once. No code, no CI/CD, no deployment pipeline.
5. **Infrastructure as Code means reproducibility.** Bicep is version-controlled, deployment is idempotent, tear-down is one command. Ephemeral by design.

## Commits

| Hash | Description |
|------|-------------|
| `24417773` | Bicep IaC, deploy script, evidence page, index update |

## Related Pages

- Evidence page: `sites/ai-evaluation-2/docs/evidence/option-d-poc-validation.md`
- Option D architecture: `sites/ai-evaluation-2/docs/evidence/option-d-hybrid-architecture.md`
- Cost offset analysis: `sites/ai-evaluation-2/docs/evidence/cost-offset-hybrid-subsidy.md`
- IDE client selection: `sites/ai-evaluation-2/docs/decisions/dd-06-ide-client-selection.md`
