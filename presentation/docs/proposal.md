# The Proposal

## Extend Your Existing IDE AI Assistant to Architecture Workflows

Your developers already use AI assistants in their IDEs for code completion and generation. **This POC tested whether that same class of tool — an off-the-shelf IDE AI assistant — can produce compliant architecture designs.**

The answer is yes. And the alternatives are significantly more expensive.

---

## The Recommendation

<div class="key-insight" markdown>
**Adopt an off-the-shelf IDE AI assistant.** Extend its use from code generation to architecture workflows — solution designs, ADRs, impact assessments, and automated portal publishing. No custom platforms. No custom builds. One license at $39/month.
</div>

---

## Three Options Were Evaluated

This POC compared three approaches to AI-assisted architecture, all using the same underlying model (Claude Opus 4.6):

| Approach | Description | Year 1 Cost |
|----------|-------------|:-----------:|
| **Adopt off-the-shelf tool** | Use an IDE AI assistant — one license, no infrastructure | **$468** |
| **Assemble open-source stack** | Roo Code + Kong AI Gateway + Qdrant vector DB | $6,084 + infrastructure |
| **Build custom agent** | Microsoft Azure AI Foundry with RAG pipeline | $113,450 |

<div class="hero-grid" markdown>

<div class="hero-card" markdown>
<div class="metric">$39/mo</div>
<div class="label">Off-the-shelf tool</div>
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

## Why the Existing Tool Wins

The cost difference is not the main argument. The main argument is that the existing tool **already does what we need**, and the alternatives introduce problems the existing tool does not have:

| Capability | Existing IDE Tool | Custom-Built Agent | Open-Source Stack |
|-----------|:-:|:-:|:-:|
| Reads all workspace files directly | Yes | No (chunked RAG) | Partial |
| Runs mock tools autonomously | Yes | No (5-call limit) | Yes |
| Produces zero fabricated schema fields | Yes | Unknown | No (4 fabrications) |
| Requires custom infrastructure | No | Yes ($113k Year 1) | Yes (gateway + vector DB) |
| Off-the-shelf (no custom build) | Yes | No | No |
| Iterates in architect's own IDE | Yes | No (browser-based) | Yes |

The critical finding: **both the existing tool and the open-source stack used the same AI model.** The existing tool produced zero fabrications. The open-source stack fabricated 4 OpenAPI schema elements. The difference was workspace context — the existing tool reads all files automatically; the open-source stack required manual file selection and missed critical context.

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

Each scenario produced a complete solution design following MADR, arc42, and C4 standards — including impact assessments, user stories, risk registers, and ADRs. The AI cited specific OpenAPI fields, Java source lines, Elasticsearch log entries, and GitLab merge requests because it could read them directly from the workspace.

See [Output Quality](quality-evidence.md) for the full head-to-head comparison.

---

## What Comes Free With Adoption

Because the existing tool operates on plain-text files in a Git repository, adopting it for architecture workflows unlocks three automation capabilities at no additional cost:

| Capability | How It Works | What It Replaces |
|-----------|-------------|-----------------|
| **Auto-published portal** | `git push` triggers generators that produce 301 artifacts in 30 seconds | Manual wiki page updates (currently skipped) |
| **Automated governance** | CALM topology generated from existing YAML metadata; CI validates architecture rules | Manual PR review for cross-service compliance |
| **Design-to-reality reconciliation** | AI compares what was designed against what was built after deployment | Nothing — this step does not exist today |

The portal, governance, and reconciliation capabilities are all built on the same foundation: architecture artifacts stored as code in version control. The existing tool makes this practical because it reads all files in the workspace automatically.

---

## What This Does NOT Require

| Concern | Answer |
|---------|--------|
| New licenses | One license at $39/month — cancel anytime |
| Custom infrastructure | No — runs in the architect's existing IDE |
| New tools for architects to learn | No — same IDE, same Git workflow |
| Migration of existing specs | No — reads the OpenAPI specs and ADRs already in version control |
| Ongoing platform engineering | No — no custom code to maintain (unlike Foundry) |

<div class="cta-box" markdown>

### See the evidence in action

[The Proof: 301 Artifacts, Live Portal](proof.md)

</div>
