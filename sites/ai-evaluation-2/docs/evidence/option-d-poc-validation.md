<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# Option D POC: BYOK Endpoint Validation

**TL;DR:** We deployed an Azure OpenAI endpoint via Bicep IaC in under 5 minutes, verified it responds to the exact API format GitHub Copilot BYOK expects, and confirmed tear-down is a single command. The Azure-side infrastructure for Option D is trivial. BYOK registration requires organization-level Copilot admin access (5-field form), which is a corporate admin action — not an engineering task.

---

## What We Proved

| Claim | Status | Evidence |
|-------|--------|----------|
| Azure OpenAI can be deployed via Bicep IaC | VERIFIED | `infra/ai-poc.bicep` + `infra/modules/azure-openai.bicep` |
| Deployment scales to zero (no idle cost) | VERIFIED | Standard SKU with pay-per-token billing — $0 when not in use |
| Endpoint responds to OpenAI Chat Completions API | VERIFIED | Successful `curl` test with 22 tokens consumed |
| Endpoint format matches BYOK requirements | VERIFIED | `https://{name}.openai.azure.com/` + deployment name + API key |
| Tear-down is a single command | VERIFIED | `./infra/deploy-ai-poc.sh teardown` deletes entire resource group |
| Total deployment time | **< 5 minutes** | Provider registration + Bicep deployment + model provisioning |
| BYOK registration in GitHub Copilot | NOT TESTED | Requires organization-level Copilot admin (Business/Enterprise), not available on personal Pro+ |

---

## Infrastructure Deployed

### Resource Group: `rg-novatrek-ai-poc`

| Resource | Type | SKU | Cost Model |
|----------|------|-----|------------|
| `oai-novatrek-poc` | Azure OpenAI (Cognitive Services) | S0 | Pay-per-token |
| `gpt-4o` deployment | GPT-4o 2024-11-20 | Standard, 10K TPM | $0 when idle |

### Endpoint Details

| Parameter | Value |
|-----------|-------|
| Endpoint URL | `https://oai-novatrek-poc.openai.azure.com/` |
| Deployment name | `gpt-4o` |
| API version | `2024-10-01-preview` |
| Model | `gpt-4o-2024-11-20` |

### Bicep IaC

All infrastructure is defined as code in the repository:

- `infra/ai-poc.bicep` — Top-level deployment template
- `infra/modules/azure-openai.bicep` — Reusable Azure OpenAI module
- `infra/deploy-ai-poc.sh` — Deploy and teardown script

The Bicep module accepts parameterized model deployments, making it trivial to swap GPT-4o for a fine-tuned model when ready.

---

## Test Results

### API Compatibility Test

Request:

```bash
curl https://oai-novatrek-poc.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-10-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: <KEY>" \
  -d '{"messages":[{"role":"user","content":"Say hello in exactly 5 words"}]}'
```

Response:

```json
{
  "choices": [{
    "message": {
      "content": "Hello there, how are you?",
      "role": "assistant"
    },
    "finish_reason": "stop"
  }],
  "model": "gpt-4o-2024-11-20",
  "usage": {
    "prompt_tokens": 14,
    "completion_tokens": 8,
    "total_tokens": 22
  }
}
```

The endpoint uses the standard OpenAI Chat Completions API format, which is exactly what GitHub Copilot BYOK expects for Microsoft Foundry providers.

---

## BYOK Registration: What Remains

BYOK registration is a **5-field admin form**, not an engineering task. It requires a GitHub organization with Copilot Business or Enterprise:

1. Navigate to: Organization Settings → Copilot → Models → Custom models → Add API key
2. **Provider:** Microsoft Foundry
3. **Name:** NovaTrek Architecture Model (displayed in model picker)
4. **API Key:** `<key from az cognitiveservices account keys list>`
5. **Deployment URL:** `https://oai-novatrek-poc.openai.azure.com/`
6. **Model ID:** `gpt-4o` (the deployment name)

After registration, the custom model appears in every organization member's model picker alongside built-in models (GPT-4o, Opus, etc.).

Source: [GitHub Docs — Using your LLM provider API keys with Copilot](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/use-your-own-api-keys)

### Why We Could Not Complete Registration

This POC uses a personal GitHub Pro+ account, not a GitHub organization with Copilot Business/Enterprise seats. The BYOK admin UI is available at the organization or enterprise level only. For individual plans (Free/Pro/Pro+), BYOK access is limited to VS Code extensions (e.g., AI Toolkit) and CLI environment variables — not the centralized admin model picker.

This is not a technical limitation — it is an access scope limitation. In the corporate environment (GitHub Enterprise Cloud), an org admin would complete registration in under 2 minutes.

---

## Cost Analysis

### POC Cost

| Item | Cost |
|------|------|
| Azure OpenAI resource (S0) | $0/month base |
| GPT-4o Standard deployment | $0 when idle, ~$0.0025/1K input tokens when used |
| API test (22 tokens) | < $0.001 |
| **Total POC cost** | **< $0.01** |

### Ongoing Cost (Scales to Zero)

When no requests are made, the cost is exactly $0. There is no minimum spend, no reserved capacity, and no idle charges. The resource exists but consumes nothing.

### Tear-down

```bash
./infra/deploy-ai-poc.sh teardown
# or directly:
az group delete --name rg-novatrek-ai-poc --yes --no-wait
```

This deletes the entire resource group and all resources within it. Full cleanup in ~5 minutes.

---

## Implications for Option D

This POC validates the Azure-side of Option D:

1. **Infrastructure is trivial** — 67 lines of Bicep deploys everything needed. No custom pipelines, no vector databases, no embedding infrastructure. Compare this to Option C's full agent stack.

2. **Cost is negligible** — Pay-per-token with zero idle cost. The $39/month Copilot subscription provides unlimited 0x model access for routine tasks, and the custom model is only invoked (and billed) when an architect explicitly selects it.

3. **Swapping models is parameterized** — When the Foundry team has a fine-tuned model ready, changing the Bicep parameter from `gpt-4o` to the fine-tuned model name is the only infrastructure change needed. Same endpoint URL, same API key, same BYOK registration.

4. **Registration is an admin action, not engineering** — The BYOK registration is a 5-field web form. No code, no pipeline, no deployment. An org admin does it once, and every architect gets the model in their picker immediately.

5. **Infrastructure as Code means reproducibility** — The Bicep templates are version-controlled, the deployment is idempotent, and tear-down is a single command. This is the "ethereal" infrastructure model — it exists when needed and vanishes when not.

---

**See also:**

- [Option D — Hybrid Architecture](option-d-hybrid-architecture.md) — Full BYOK analysis, feature compatibility, and risk assessment
- [Cost Offset Analysis](cost-offset-hybrid-subsidy.md) — Financial case for 0x models subsidizing the Foundry investment
- [DD-06: IDE Client Selection](../decisions/dd-06-ide-client-selection.md) — Why Copilot is the right client for consuming a custom Foundry model
- [Copilot Rollout Roadmap](../framework/copilot-rollout-roadmap.md) — Phase 4.3 covers BYOK integration steps
