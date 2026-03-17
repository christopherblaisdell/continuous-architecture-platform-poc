# How an Index Change Flows to Production

There are **three artifacts** involved, each with a clear owner:

## Step 1 — Architect edits the architectural source of truth

The architect opens `architecture/metadata/data-stores.yaml` and adds or modifies an index entry. For example, adding a new index to `svc-check-in`:

```yaml
indexes:
  - name: idx_checkins_guest_id
    columns: guest_id
  - name: idx_checkins_status_date    # ← new index
    columns: status, check_in_date    # ← new index
    type: composite                   # ← new index
```

## Step 2 — Portal regenerates automatically

On push to `main`, the CI pipeline runs `portal/scripts/generate-microservice-pages.py`, which:

1. Reads `data-stores.yaml`
2. Generates an **ERD diagram** (PlantUML → SVG) showing the updated table structure
3. Renders the **Data Store** section on the service page with the new index listed
4. Deploys to [architecture.novatrek.cc](https://architecture.novatrek.cc) — the portal now shows the new index

## Step 3 — Developer writes the Flyway migration

A developer (or the architect) authors a versioned SQL migration file:

```
services/svc-check-in/src/main/resources/db/migration/V2__add_status_date_index.sql
```

```sql
CREATE INDEX idx_checkins_status_date ON checkin.check_ins (status, check_in_date);
```

Naming convention: `V{version}__{description}.sql` — forward-only, never destructive.

## Step 4 — PR validation

On pull request, CI runs `flyway validate` against a disposable PostgreSQL instance to verify the migration is syntactically correct and compatible with the existing schema history.

## Step 5 — Production deployment

After merge, the per-service CD pipeline calls the reusable workflow `.github/workflows/db-migrate.yml`, which:

1. **Dev/Ephemeral**: Runs `flyway migrate` via Docker container against Neon Serverless Postgres (connection URL from `NEON_DATABASE_URL` secret)
2. **Prod**: Authenticates to Azure via OIDC and runs `flyway migrate` against Azure PostgreSQL Flexible Server

## Visual summary

```
data-stores.yaml ─► generate-microservice-pages.py ─► Portal (documentation)
       │
       │  (architect intent, reviewed by developers)
       ▼
V{N}__*.sql ─► PR (flyway validate) ─► merge ─► CD (flyway migrate) ─► Neon (dev) / Azure PostgreSQL (prod)
```

## Known gaps

**1. No drift detection between YAML and SQL.** There is currently no automated sync validation between `data-stores.yaml` and the Flyway SQL files. They are maintained independently — the YAML is the architectural design target, and the SQL files are the executable schema. If an architect adds an index to the YAML but nobody writes the corresponding Flyway migration (or vice versa), the two will drift silently. A CI check that diffs the two and flags drift is a potential Phase 3 enhancement.

**2. Two-step coordination gap.** The architect and developer are different people editing different files at different times. There is no mechanism ensuring a Flyway migration actually gets written after the YAML is updated. Linking the YAML change to a required migration via a ticket or automated issue would close this loop.
