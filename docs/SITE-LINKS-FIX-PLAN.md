# Site Links Fix Plan — architecture.novatrek.cc

**Companion to:** [SITE-LINKS-ANALYSIS.md](SITE-LINKS-ANALYSIS.md)
**Goal:** Eliminate the 505 broken references identified in the analysis and prevent regression.
**Sequencing principle:** Fix highest-volume issues first; fix root causes (generators, configuration) before per-page edits; land regression detection (CI link check) before merging fixes so the green/red signal is reliable.

---

## Summary

| Step | Fixes | Issues resolved |
|---|---|---:|
| **A** | Land link checker as `portal/scripts/utilities/linkcheck.py` and wire into `bash portal/scripts/generate-all.sh` | (regression guard) |
| **B** | Fix favicon path in `mkdocs.yml` | 181 |
| **C** | Fix relative depth in `architect-guide/domain-model.md` and audit other nested pages | ~60 |
| **D** | Fix Swagger UI deep-link fragment generator | ~120 |
| **E** | Resolve dangling `.md` and out-of-portal references | ~147 |
| **F** | Fix solution-page `#architecture-decisions` anchor mismatch | 2 |
| **G** | Fix template-page placeholder `<img>` references | 3 |
| **H** | Accept or fix `pymdownx.footnotes` multi-cite back-references | 12 (or wontfix) |
| **I** | Rebuild, re-deploy, verify against live site | — |

---

## Step A — Land the link checker into CI

**Why first:** every subsequent step needs a reliable pass/fail. The current `/tmp/linkcheck.py` was undercounting until the regex was fixed; it must live in-repo so it cannot regress.

### Tasks

1. Move `/tmp/linkcheck.py` to `portal/scripts/utilities/linkcheck.py`. Keep it stdlib-only (no `requests`).
2. Wire the corrected anchor regex (handles `id="…"`, `id='…'`, and unquoted `id=…` from minified HTML).
3. Add an exit-non-zero mode (`--strict`) that fails the script if any category exceeds a threshold.
4. Add an invocation step to `portal/scripts/generate-all.sh` after `mkdocs build`:
   ```bash
   python3 portal/scripts/utilities/linkcheck.py portal/site --strict
   ```
5. Optionally surface in `.github/workflows/docs-deploy.yml` as a separate `validate-links` job that runs before deploy. Treat as advisory (warn, don't block) until Step I confirms zero breakage; then flip to blocking.

### Validation

Running the script against the current build should reproduce the analysis numbers (181 / 160 / 147 / 14 / 3). Subsequent fix steps reduce these toward zero.

### Risk

None — read-only.

---

## Step B — Fix favicon (181 broken on every page)

### Option B1 (preferred — zero new files)

Edit [portal/mkdocs.yml](portal/mkdocs.yml) line 16:

```diff
 theme:
   name: material
   …
-  favicon: assets/favicon.png
+  favicon: assets/images/favicon.png
```

This points at the Material theme default, which is what the build copies into `site/assets/images/favicon.png` regardless. No source file to add. Same physical favicon every Material site uses.

### Option B2 (custom favicon)

If we want a NovaTrek-branded favicon:
1. Create `portal/docs/assets/favicon.png` (32×32 or 192×192 PNG).
2. Leave `mkdocs.yml` as-is (`favicon: assets/favicon.png`) — MkDocs will copy it to `site/assets/favicon.png` and the existing link tags will resolve.

### Validation

Re-run linkcheck. `missing_link` must drop from **181 → 0**.

### Risk

None.

---

## Step C — Fix `architect-guide/domain-model.md` and audit nested-page relative paths (~60 broken)

### Root cause

`portal/docs/architect-guide/domain-model.md` uses `../microservices/svc-X/` from a page that, due to `use_directory_urls: true`, renders one directory deeper than the source file. Needs `../../microservices/...`.

### Tasks

1. Patch [portal/docs/architect-guide/domain-model.md](portal/docs/architect-guide/domain-model.md) — bulk replace `../microservices/` with `../../microservices/`, and the same for `../domains/`, `../decisions/`, `../events/`, `../services/` if they appear:

   ```bash
   cd portal/docs/architect-guide
   sed -i.bak 's|](../microservices/|](../../microservices/|g; s|](../domains/|](../../domains/|g; s|](../decisions/|](../../decisions/|g' domain-model.md
   ```

2. **Audit every other page nested one level deep** under `portal/docs/`. The same bug is latent wherever a hand-authored page lives in a subdirectory and references siblings using one `..`. Enumerate candidates:
   ```bash
   find portal/docs -mindepth 2 -maxdepth 2 -name '*.md' -not -path '*/microservices/*' -not -path '*/solutions/*' -not -path '*/tickets/*' -not -path '*/capabilities/*'
   ```
   For each, grep for `](../` patterns and verify the target resolves.

3. **Generators** (`portal/scripts/generate-*.py`) already produce links from a known absolute root, so they are not affected — only hand-authored markdown.

### Validation

Re-run linkcheck. The 18 distinct `../microservices/svc-*/` entries under `missing_a` (count ~50) must drop to 0. Spot-check `/architect-guide/domain-model/` page-broken count drops from 43 → 0.

### Risk

Low — only edits markdown text; preview locally with `mkdocs serve` before commit.

---

## Step D — Fix Swagger UI deep-link fragments (~120 broken)

### Root cause

`portal/scripts/generate-microservice-pages.py` emits cross-references such as `services/api/svc-emergency-response.html#/Emergencies/triggerEmergency`, but the Swagger UI page rendered at that location uses a different fragment scheme.

### Tasks

1. Open `portal/site/services/api/svc-emergency-response.html` in a browser and inspect what fragment Swagger UI generates when an operation row is expanded. Likely formats:
   - `#/Emergencies/triggerEmergency` (Swagger UI ≤ 2.x)
   - `#operations-Emergencies-triggerEmergency` (Swagger UI ≥ 3.x default `deepLinking: true`)
   - `#tag/Emergencies/operation/triggerEmergency` (Redoc)

2. Once the actual format is confirmed, update the fragment template in `portal/scripts/generate-microservice-pages.py`. Search for the string emitting `services/api/...html#`. The likely fix is a single f-string change, e.g.:

   ```diff
   - link = f"services/api/{svc}.html#/{tag}/{op_id}"
   + link = f"services/api/{svc}.html#operations-{tag}-{op_id}"
   ```

3. Regenerate microservice pages:
   ```bash
   python3 portal/scripts/generate-microservice-pages.py
   ```

4. **Alternative:** if the viewer page itself can be configured (e.g., the HTML wrapper around Swagger UI sets `deepLinking: false`), changing it to emit the legacy `#/Tag/operationId` form would also work. Pick whichever side is one place to change.

### Validation

Re-run linkcheck. `fragment_missing` must drop from **160 → 0**. Manually click a couple of deep links from `/microservices/svc-emergency-response/` to confirm they scroll to the right operation.

### Risk

Medium — Swagger UI behavior depends on the viewer version. Verify in the browser first; do not guess.

---

## Step E — Resolve dangling `.md` and out-of-portal references (~147 broken)

This category has three sub-classes, each with a different fix.

### E1. Repo-relative paths leaked into portal docs

Examples (from the analysis):
- `../research/CONFLUENCE-PUBLISHING-PLAN.md` (in `portal/docs/roadmap.md`)
- `../docs/CALM-INTEGRATION-PLAN.md`
- `../architecture/reminders/CALM-EVALUATION.md`, `FIX-DEPLOY-FAILURES.md`
- `../phase-1-ai-tool-cost-comparison/...` paths

These point outside `portal/docs/`. Decide per-file:

- **Decision A — bring into portal:** copy/symlink the source under `portal/docs/research/`, `portal/docs/docs/`, etc., and add to `nav:` in `mkdocs.yml`. Then change the link to a portal-relative path.
- **Decision B — leave as external:** rewrite as a GitHub URL pointing at the file in the repo (`https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/blob/main/research/CONFLUENCE-PUBLISHING-PLAN.md`).
- **Decision C — remove:** delete the link if the referenced doc is obsolete.

Recommended default: **Decision B** for one-off references, **Decision A** for anything mentioned 2+ times.

### E2. `.md` references that should be in the nav

- `SYNTHETIC-EXEMPLAR-BACKLOG.md` (referenced from `everything-as-code/TRANSFORMATION-PLAN.md` and `everything-as-code/index.md`)
- `DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL-RESPONSE.md` (referenced from `everything-as-code/DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md`)
- `DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md`
- `TEST-METHODOLOGY-ROADMAP.md`
- `README.md` (twice)

For each: if the source `.md` exists somewhere in the repo, copy it into the appropriate `portal/docs/` subdirectory and add to `nav:`. If it doesn't exist, the link is aspirational — either remove or replace with placeholder text.

### E3. Stale references to renamed/deleted services

- `svc-referral-engine`, `svc-campaign-management` — services that no longer exist in `architecture/specs/`. Find and remove these references.
- `../services/svc-scheduling-orchestrator.md`, `../services/svc-check-in.md` — legacy paths from before the move to `microservices/`. Bulk replace `../services/svc-` with `../microservices/svc-` (verify trailing slash conventions).

### E4. Single-page absolute `/.ai-instructions/...` reference

- `/.ai-instructions/customizations/solution-design-optional-sections-standard.md` (3 occurrences) — `.ai-instructions` is not under `portal/docs/`. Convert to GitHub URL or remove.

### Validation

Re-run linkcheck. `missing_a` must drop from **147 → 0** (or near-zero if any links are deliberately kept as repo-relative GitHub URLs that the script doesn't follow).

### Risk

Medium — many small markdown edits across many files. Stage in 3–4 PRs grouped by sub-class to keep review manageable.

---

## Step F — Fix solution-page `#architecture-decisions` anchor (2 broken)

`/solutions/_NTK-10005-…/` and `/solutions/_NTK-10001-…/` link to `#architecture-decisions` but the heading slug rendered is different.

### Tasks

1. Inspect the rendered HTML of one solution page:
   ```bash
   grep -oE 'id=[a-z][^ >"]+' portal/site/solutions/_NTK-10005-wristband-rfid-field/index.html | grep -i decision
   ```
2. Find the corresponding emitter in `portal/scripts/generate-solution-pages.py` and align the link to the actual heading slug.
3. Regenerate and re-run linkcheck.

### Risk

None.

---

## Step G — Fix template-page placeholder `<img>` references (3 broken)

[portal/docs/standards/solution-design/solution-design-template.md](portal/docs/standards/solution-design/solution-design-template.md) embeds three placeholders:
- `3.solution/00.component.diagram.svg`
- `3.solution/01b.[component].[workflow].sequence.diagram.target.svg`
- `3.solution/02b.[component].[workflow].sequence.diagram.target.svg`

These are **template scaffolding** — they show what a real solution should contain. Two acceptable fixes:

### Option G1 — wrap in code blocks

```diff
- ![Component diagram](3.solution/00.component.diagram.svg)
+ `3.solution/00.component.diagram.svg` — component diagram of the proposed solution
```

### Option G2 — provide a single placeholder SVG

Create `portal/docs/standards/solution-design/3.solution/_placeholder.svg` (a "diagram goes here" visual) and rewrite all three references to point at it.

Recommend G1 — clearer intent.

---

## Step H — Footnote multi-cite back-references (12 broken — likely wontfix)

`pymdownx.footnotes` only emits one `fnref:N` anchor per footnote. When a footnote is cited 2+ times, the back-link from the footnote points only at the first citation; the others have no back-link target.

### Options

- **H1 — wontfix:** these are forward links from the footnote's "↩" back-arrow that just don't go everywhere. Users almost never click them. Document as a known limitation and exclude `#fnref:` from the link checker via `--ignore-fragment-pattern`.
- **H2 — fix:** consider switching to `markdown.extensions.footnotes` (built-in) or override the footnote template to emit `fnref:N:1`, `fnref:N:2` anchors. Likely more effort than it's worth.

Recommend H1.

---

## Step I — Rebuild, redeploy, verify against live site

1. Run the full pipeline:
   ```bash
   bash portal/scripts/generate-all.sh
   cd portal
   /usr/bin/python3 -m mkdocs build
   cp -r docs/services/api site/services/
   cp -r docs/specs site/
   cp -r docs/microservices/svg site/microservices/
   cp staticwebapp.config.json site/
   python3 scripts/utilities/linkcheck.py site --strict
   ```
2. Deploy:
   ```bash
   swa deploy site --deployment-token "<portal-token>" --env production
   ```
3. After deploy, smoke-test the live site by curling 5–10 representative pages and grepping for the previously-broken paths to confirm they have changed:
   ```bash
   for url in \
     "https://architecture.novatrek.cc/" \
     "https://architecture.novatrek.cc/architect-guide/domain-model/" \
     "https://architecture.novatrek.cc/microservices/svc-emergency-response/" \
     "https://architecture.novatrek.cc/everything-as-code/TRANSFORMATION-PLAN/" \
     "https://architecture.novatrek.cc/roadmap/"; do
       echo "==> $url"
       curl -s "$url" | grep -oE 'href="[^"]*"' | head -5
   done
   ```
4. Flip the `validate-links` GitHub Action job from advisory to blocking.

---

## Out of scope (intentionally)

- **Confluence mirror.** The Confluence pipeline transforms links via `confluence-prepare.py`; its broken-link surface is different and requires its own audit.
- **The 24-vs-19 microservice mismatch.** Five services (`svc-emergency-response`, `svc-wildlife-tracking`, `svc-reviews`, `svc-adventure-tracking`, plus one more) exist in the build but are not documented in [CLAUDE.md](CLAUDE.md). That is a documentation hygiene issue, not a broken link issue. File separately.
- **The `mkdocs-minify-plugin` decision.** The plugin emits unquoted HTML attributes that broke the original link checker's anchor regex. The corrected regex handles them, so the plugin can stay. If we ever want to drop the plugin for other reasons (debuggability, source-map fidelity), that's a separate decision.

---

## Estimated impact

After steps B–G land:

| Category | Before | After |
|---|---:|---:|
| `missing_link` | 181 | 0 |
| `fragment_missing` | 160 | 0 |
| `missing_a` | 147 | 0–5 (deliberate external refs) |
| `fragment_missing_self` | 14 | 2 (footnote backref artifacts, wontfix) |
| `missing_img` | 3 | 0 |
| **Total** | **505** | **~2** |

Then Step A (CI link checker) prevents regression.
