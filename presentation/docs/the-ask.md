# The Ask: What We Need to Move Forward

## Build on Our Existing Strengths

We already source-control specs and diagrams in Git with production gating. We've proven the platform works by building on that foundation. We've measured the cost and quality. We've built a live demonstration. Here's what we need to adopt it.

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
- Proven: 96.1% quality, 208x cheaper than per-token alternatives

**Pilot scope:** Start with the architecture practice team. Measure quality and adoption for 1 month before expanding.

---

### 2. Solution Designs in Markdown (Extending Our Git-First Practice)

We already author specs and diagrams in text formats and check them into Git. This extends that practice:

- **New** solution designs and ADRs are authored in Markdown in the same architecture repo
- **Existing** specs, diagrams, and Confluence content stay exactly where they are
- The AI generates correctly formatted Markdown automatically — architects don't need to learn syntax

**What this enables:** Version-controlled designs alongside specs, pull request reviews on architecture decisions, AI context for future sessions, automated publishing that replaces the manual Confluence step.

---

### 3. Automated Publishing Pipeline

- Azure Static Web Apps deployment (free tier — $0/month)
- GitHub Actions workflow triggered on push to main
- Builds MkDocs site + copies non-Markdown assets
- Deploys in under 30 seconds

**What this replaces:** The voluntary manual Confluence update step — the one that gets skipped, causing documentation to fall behind the artifacts already in Git.

---

### 4. Optional: Confluence API Access

For organizations that require Confluence:

- Same Markdown source publishes to both MkDocs and Confluence
- Git remains the source of truth
- Confluence pages become read-only mirrors
- Requires Confluence REST API access (write permission to architecture space)

**This is optional.** The platform works without Confluence sync.

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
| "What if the AI quality isn't good enough?" | 96.1% measured across 5 scenarios. Start with a 1-month pilot. |
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
| 96.1% quality score | 149/155 across 5 evaluated scenarios |
| 301 artifacts published automatically | Live portal at mango-sand-083b8ce0f.4.azurestaticapps.net |
| 95%+ knowledge gap rate | Phase 1 post-execution analysis (CLOSING-THE-LOOP.md) |
| $0 publishing infrastructure cost | Azure Static Web Apps free tier + open source MkDocs |
| Zero fabrication (Copilot) | Head-to-head comparison vs Roo Code |

**Every number in this presentation comes from measured results, not projections.**
