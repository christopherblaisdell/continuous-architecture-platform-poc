# The Ask: What's Required to Adopt This

## Build on Existing Strengths

Many architecture teams already source-control specs and diagrams with production gating. This platform builds on that foundation. The POC measured cost and quality using NovaTrek Adventures as a synthetic case study. Here's what organizations need to adopt it.

---

## Four Approvals

### 1. GitHub Copilot Pro+ Licenses

<div class="hero-card" markdown>
<div class="metric">$39</div>
<div class="label">per seat / per month</div>
</div>

- Fixed subscription — no variable costs, no runaway billing
- Includes Claude Opus 4.6 access with unlimited autonomous tool calls
- Native VS Code integration — no infrastructure to manage
- Proven: 39 architecture files produced across 5 scenarios, 208x cheaper than per-token alternatives

**Pilot scope:** Start with the architecture practice team. Measure quality and adoption for 1 month before expanding.

---

### 2. Solution Designs in Markdown (Extending Version Control)

Many teams already author specs and diagrams in text formats and version-control them. This extends that practice:

- **New** solution designs and ADRs are authored in Markdown in the architecture repository
- **Existing** specs, diagrams, and wiki content stay exactly where they are
- The AI generates correctly formatted Markdown automatically — architects don't need to learn syntax

**What this enables:** Version-controlled designs alongside specs, pull request reviews on architecture decisions, AI context for future sessions, automated publishing that replaces manual wiki updates.

---

### 3. Automated Publishing Pipeline

- Azure Static Web Apps deployment (free tier — $0/month)
- GitHub Actions workflow triggered on version control push
- Builds MkDocs site + copies non-Markdown assets
- Deploys in under 30 seconds

**What this replaces:** The voluntary manual wiki update step — the one that gets skipped, causing documentation to fall behind version-controlled artifacts.

---

### 4. Optional: Wiki API Access

For organizations that require wiki integration:

- Same Markdown source publishes to both MkDocs and wiki platform
- Version control remains the source of truth
- Wiki pages become read-only mirrors
- Requires wiki REST API access (write permission to architecture space)

**This is optional.** The platform works without wiki sync.

---

## Total Cost

| Component | Monthly Cost | Notes |
|-----------|:---:|-------|
| Copilot Pro+ (per seat) | $39 | Fixed subscription |
| Azure Static Web Apps | $0 | Free tier |
| MkDocs Material | $0 | Open source |
| GitHub Actions | $0 | Included with repository |
| Material Insiders (optional) | $15 | Premium features |
| **Total per architect** | **$39** | |

---

## Risk Profile

| Concern | Answer |
|---------|--------|
| "What if the AI output isn't usable?" | 39 complete architecture files produced in 5 scenarios, all following MADR/arc42/C4 standards. Start with a 1-month pilot. |
| "What if costs increase?" | Fixed $39/month subscription. Even at 2x, cheaper than alternatives. |
| "What if architects don't adopt it?" | Architects already work in Git with text-format specs. The AI handles Markdown formatting. The workflow extends what they already do. |
| "What if we need to go back?" | Markdown is portable. Export to any format. No vendor lock-in. |
| "What about existing Confluence content?" | Stays in place. Only new work moves to Markdown-first. |
| "Is the data secure?" | All data stays in the git repository. Copilot processes context server-side. No data leaves the GitHub/Azure ecosystem. |

---

## Return on Investment

| Investment | Return |
|-----------|--------|
| $39/month per architect | 20-100 minutes saved per re-investigation (eliminated by PROMOTE) |
| 0 minutes manual publishing | 15-30 minutes saved per publication cycle (automated by CI/CD) |
| 0 infrastructure management | Kong Gateway + Qdrant + monitoring eliminated |
| 1 month pilot | Definitive quality data for scale-up decision |

---

## Next Step

<div class="cta-box" markdown>

### Approve Copilot Pro+ licenses for the architecture practice.

Start a 1-month pilot. Measure quality and adoption. Scale based on data.

**Total commitment: $39/seat/month. Cancel anytime.**

</div>

---

## Summary of Evidence

| Claim | Source |
|-------|--------|
| 208x cheaper per run | Actual billing data from Phase 1 execution |
| 39 architecture files produced | 5 evaluated scenarios following MADR/arc42/C4 standards |
| 301 artifacts published automatically | Live portal at mango-sand-083b8ce0f.4.azurestaticapps.net |
| 95%+ knowledge gap rate | Phase 1 post-execution analysis (CLOSING-THE-LOOP.md) |
| $0 publishing infrastructure cost | Azure Static Web Apps free tier + open source MkDocs |
| Zero fabrication (Copilot) | Head-to-head comparison vs Roo Code |

**Every number in this presentation comes from measured results, not projections.**
