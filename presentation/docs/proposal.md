# The Proposal

## Create a Shared Workspace for the Architecture Practice

Everyone in the organization uses VS Code. **This POC tested whether a shared Git workspace combined with Copilot subscriptions can serve as a shared solution for the entire solution architecture practice.**

It can. And the alternatives — building a custom platform or assembling an open-source stack — cost 13x to 243x more.

---

## The Recommendation

<div class="key-insight" markdown>
**Create a shared Git workspace for the architecture practice and add Copilot subscriptions.** The workspace contains specs, ADRs, standards, source code, and institutional knowledge — everything an architect needs. Copilot automatically indexes the entire workspace into a vector database. No MCP servers. No custom Copilot Extensions. No Azure AI Search pipelines. This is the standard pattern used by over 22 million engineers today. $39/seat/month, cancel anytime.
</div>

---

## Three Options Were Evaluated

This POC compared three approaches to AI-assisted architecture, all using the same underlying model (Claude Opus 4.6):

| Approach | Description | Year 1 Cost |
|----------|-------------|:-----------:|
| **Subscribe** | Add AI to VS Code — $39/mo, no infrastructure | **$468** |
| **Assemble open-source stack** | Roo Code + Kong AI Gateway + Qdrant vector DB | $6,084 + infrastructure |
| **Build custom agent** | Microsoft Azure AI Foundry with RAG pipeline | $113,450 |

<div class="hero-grid" markdown>

<div class="hero-card" markdown>
<div class="metric">$39/mo</div>
<div class="label">Subscribe ($39/mo)</div>
</div>

<div class="hero-card" markdown>
<div class="metric">$507/mo</div>
<div class="label">Assemble open-source stack</div>
</div>

<div class="hero-card dark" markdown>
<div class="metric">$9,454/mo</div>
<div class="label">Build custom agent</div>
</div>

</div>

The 13x and 243x cost gaps are not estimates — they come from actual billing data and Microsoft's published pricing. See [Cost Analysis](cost-evidence.md) and [Foundry Analysis](foundry-analysis.md) for the full breakdown.

---

## Why the Subscription Wins

The cost difference is not the main argument. The main argument is that a VS Code AI subscription **does everything we need**, and the alternatives introduce problems it does not have:

| Capability | VS Code + AI Subscription | Custom-Built Agent | Open-Source Stack |
|-----------|:-:|:-:|:-:|
| Reads all workspace files directly | Yes | No (chunked RAG) | Partial |
| Runs architecture tools autonomously | Yes | No (5-call limit) | Yes |
| Produces zero fabricated schema fields | Yes | Unknown | No (4 fabrications) |
| Requires custom infrastructure | No | Yes ($113k Year 1) | Yes (gateway + vector DB) |
| Works in VS Code (already installed) | Yes | No (browser-based) | Yes |
| Nothing to build or maintain | Yes | No | No |

The critical finding: **the subscription and the open-source stack used the same AI model.** The subscription produced zero fabrications. The open-source stack fabricated 4 OpenAPI schema elements. The difference was workspace context — the subscription reads all files in the workspace automatically; the open-source stack required manual file selection and missed critical context.

---

## What the AI Actually Produced

Across 5 architecture scenarios using a synthetic workspace (NovaTrek Adventures):

<div class="hero-grid" markdown>

<div class="hero-card" markdown>
<div class="metric">39</div>
<div class="label">Architecture files produced</div>
</div>

<div class="hero-card accent" markdown>
<div class="metric">301</div>
<div class="label">Portal artifacts auto-published</div>
</div>

<div class="hero-card dark" markdown>
<div class="metric">0</div>
<div class="label">Schema fabrications</div>
</div>

</div>

Each scenario produced a complete solution design following MADR, arc42, and C4 standards — including impact assessments, user stories, risk registers, and ADRs. The AI cited specific OpenAPI fields, Java source lines, and log entries because it could read them directly from the shared workspace.

See [Output Quality](quality-evidence.md) for the full head-to-head comparison.

---

## What Comes Free With Adoption

Because the shared workspace operates on plain-text files in a Git repository, using Copilot for architecture workflows unlocks three automation capabilities at no additional cost:

| Capability | How It Works | What It Replaces |
|-----------|-------------|-----------------|
| **Auto-published portal** | `git push` triggers generators that produce 301 artifacts in 30 seconds | Manual wiki page updates (currently skipped) |
| **Automated governance** | CALM topology generated from existing YAML metadata; CI validates architecture rules | Manual PR review for cross-service compliance |
| **Design-to-reality reconciliation** | AI compares what was designed against what was built after deployment | Nothing — this step does not exist today |

The portal, governance, and reconciliation capabilities are all built on the same foundation: architecture artifacts stored as code in version control. The shared workspace makes this practical because Copilot indexes all files in the workspace automatically — no MCP servers or custom integrations required.

---

## What This Does NOT Require

| Concern | Answer |
|---------|--------|
| New licenses | Copilot Pro+ at $39/seat/month — cancel anytime |
| Custom infrastructure | No — institutional knowledge lives in the workspace, Copilot indexes it automatically (standard pattern, 22M+ users) |
| New tools for architects to learn | No — same IDE, same Git workflow |
| Migration of existing specs | No — reads the OpenAPI specs and ADRs already in version control |
| Ongoing platform engineering | No — no custom code to maintain (unlike Foundry) |

<div class="cta-box" markdown>

### See the evidence in action

[The Proof: 301 Artifacts, Live Portal](proof.md)

</div>
