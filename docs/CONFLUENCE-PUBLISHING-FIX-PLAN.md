# Confluence Publishing Fix Plan

**Date**: 2026-03-11
**Status**: In Progress
**Goal**: Fix the broken Confluence publishing pipeline and add round-trip verification

---

## Current State Assessment

The Confluence publishing pipeline has 4 scripts but has never been tested end-to-end locally. The environment variables are not configured, and several scripts have design bugs.

### What Exists

| Script | Status | Issues |
|--------|--------|--------|
| `confluence-prepare.py` | Working | Generates staging output correctly (84 MD files + 240 SVGs) |
| `confluence-lock-pages.py` | Untested | N+1 API calls for label lookup (perf bug) |
| `confluence-drift-check.py` | Broken | Content hash compares Markdown vs XHTML (always differs); non-recursive file scan misses subdirectories |
| `confluence-delete-space-content.py` | Untested | Appears well-written |

### What's Missing

1. No `.env` file for local credentials
2. No Makefile targets for Confluence operations
3. No verification script to pull content back from Confluence and validate
4. No automated test for the transformation pipeline
5. `mark` is installed locally (v15.3.0) but no local publish workflow exists

---

## Execution Plan

### Phase 1: Local Environment Setup

**Goal**: Be able to publish to Confluence from the local machine.

- [ ] **1.1** Create `.env.example` with required Confluence variables (no secrets)
- [ ] **1.2** Create `.env` (gitignored) with actual credentials
- [ ] **1.3** Add Makefile targets: `confluence-prepare`, `confluence-publish`, `confluence-publish-dry-run`
- [ ] **1.4** Verify `.gitignore` excludes `.env`
- [ ] **1.5** Test `confluence-prepare.py` runs cleanly
- [ ] **1.6** Test `mark --dry-run` against the staging output

### Phase 2: Publish to Confluence

**Goal**: Successfully publish all portal content to Confluence.

- [ ] **2.1** Run `confluence-delete-space-content.py` to wipe stale pages (if any exist)
- [ ] **2.2** Run `mark` to publish all staging files
- [ ] **2.3** Verify pages appear in Confluence UI manually (spot check)

### Phase 3: Verification Script

**Goal**: Create `confluence-verify.py` that pulls content back from Confluence and validates it.

The script will:
1. Authenticate to Confluence REST API
2. Fetch all pages in the ARCH space with label `auto-generated`
3. For each page, extract:
   - Title (must match `<!-- Title: -->` header in staging)
   - Parent page (must match `<!-- Parent: -->` header)
   - Labels (must include all labels from `<!-- Label: -->` header)
   - Body content (Confluence Storage Format / XHTML)
   - Attachments list (SVG/PNG files)
4. Compare against the local staging directory (`portal/confluence/`)
5. Report:
   - Pages in staging but missing from Confluence (MISSING)
   - Pages in Confluence but not in staging (ORPHANED)
   - Title mismatches
   - Parent hierarchy mismatches
   - Missing labels
   - Missing attachments (SVG/PNG referenced in content but not attached)
   - Content presence checks (key headings and text fragments present in XHTML)

**Verification levels** (incremental):

| Level | What | How |
|-------|------|-----|
| **Structural** | Every staging file has a corresponding Confluence page | Title matching |
| **Hierarchy** | Parent-child relationships match | Parent title comparison |
| **Labels** | All derived labels present | Label set comparison |
| **Content** | Key content survived transformation | H1/H2 heading extraction from XHTML, text fragment search |
| **Attachments** | Images uploaded successfully | Attachment list vs referenced images |
| **Links** | Internal cross-references resolve | DEFERRED to future phase |

- [ ] **3.1** Create `portal/scripts/confluence-verify.py` with structural + hierarchy + labels checks
- [ ] **3.2** Add content presence checks (extract headings from XHTML, compare against Markdown headings)
- [ ] **3.3** Add attachment verification (list attachments per page, compare against staged images)
- [ ] **3.4** Add Makefile target: `confluence-verify`
- [ ] **3.5** Run verification and fix any issues found

### Phase 4: Fix Drift Check

**Goal**: Fix the broken `confluence-drift-check.py` so it actually works.

- [ ] **4.1** Replace content hash comparison with heading-based comparison (extract H1/H2 from XHTML)
- [ ] **4.2** Fix `load_staging_hashes()` to use `os.walk()` instead of `os.listdir()`
- [ ] **4.3** Add Makefile target: `confluence-drift-check`
- [ ] **4.4** Test drift check against live Confluence

### Phase 5: Commit and Validate

- [ ] **5.1** Run full cycle: prepare -> publish -> verify
- [ ] **5.2** Commit all changes
- [ ] **5.3** Push to main

---

## Deferred (Future Phase)

- Link verification (internal cross-references resolve to correct pages)
- Performance optimization (N+1 API calls in lock-pages and drift-check)
- Automated alerting on drift (GitHub Issue or Slack)
- Unit tests for regex transformations in `confluence-prepare.py`

---

## Commands Reference

```bash
# Environment setup
cp .env.example .env  # then edit with real credentials
source .env

# Prepare staging
make confluence-prepare

# Dry-run publish (validate without writing)
make confluence-publish-dry-run

# Publish to Confluence
make confluence-publish

# Verify published content
make confluence-verify

# Check for drift
make confluence-drift-check

# Nuclear option: wipe all pages
make confluence-wipe
```
