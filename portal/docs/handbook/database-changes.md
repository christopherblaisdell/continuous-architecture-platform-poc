---
tags:
  - handbook
  - database
  - schema
---

<!-- PUBLISH -->

<div class="hero" markdown>

# Database Changes

<p class="subtitle">How to add tables, columns, indexes, and foreign key relationships — and keep the architectural metadata in sync</p>

</div>

Database changes in NovaTrek involve two separate artifacts maintained in parallel:

1. **`architecture/metadata/data-stores.yaml`** — the architectural model of the schema (source of truth for portal generation)
2. **Flyway migration files** — executable SQL that applies the change to the actual database

The architect owns the first. Developers own the second. Both must reflect the same intent.

---

## How Changes Flow

```
Architect edits data-stores.yaml
     │
     ▼
CI runs generate-microservice-pages.py
  → Portal page updated (ERD, data store section, tables, indexes)
  → Architecture.novatrek.cc reflects the change

Developer writes Flyway migration (V{N}__description.sql)
     │
     ▼
PR validation: flyway validate against disposable PostgreSQL
     │
     ▼
Merge: flyway migrate → Azure PostgreSQL Flexible Server
```

The two steps are intentionally separate. The YAML captures the architectural intent; the SQL file is the executable change. See [Known Gaps](#known-gaps) for limitations of this two-track approach.

---

## Adding a Table

### 1. Edit `data-stores.yaml`

Open `architecture/metadata/data-stores.yaml` and add the table under the relevant service:

```yaml
svc-check-in:
  engine: PostgreSQL 15
  schema: checkin
  tables:
    - check_ins
    - gear_verifications
    - wristband_assignments
    - rfid_audit_log         # ← new table
  table_details:
    # ... existing table_details ...
    rfid_audit_log:
      description: Audit log of all RFID wristband scan events
      columns:
        - name: audit_id
          type: UUID
          constraints: PK, DEFAULT gen_random_uuid()
        - name: check_in_id
          type: UUID
          constraints: NOT NULL, FK -> check_ins
        - name: wristband_id
          type: VARCHAR(50)
          constraints: NOT NULL
        - name: event_type
          type: VARCHAR(20)
          constraints: NOT NULL
        - name: scanned_at
          type: TIMESTAMPTZ
          constraints: NOT NULL, DEFAULT NOW()
        - name: created_at
          type: TIMESTAMPTZ
          constraints: NOT NULL, DEFAULT NOW()
      indexes:
        - name: idx_rfid_audit_checkin
          columns: check_in_id
        - name: idx_rfid_audit_scanned
          columns: scanned_at DESC
```

**Column constraint conventions:**

| Pattern | Example |
|---|---|
| Primary key | `PK, DEFAULT gen_random_uuid()` |
| Foreign key | `NOT NULL, FK -> {table_name}` |
| Not null with default | `NOT NULL, DEFAULT NOW()` |
| Nullable | `NULL` |
| Unique constraint | `UNIQUE` |
| Check constraint | `NOT NULL, CHECK (1-3)` |

### 2. Write the Flyway Migration

Create a versioned SQL file in the service's migration directory:

```
services/svc-check-in/src/main/resources/db/migration/V3__add_rfid_audit_log.sql
```

```sql
CREATE TABLE checkin.rfid_audit_log (
    audit_id      UUID         NOT NULL DEFAULT gen_random_uuid(),
    check_in_id   UUID         NOT NULL REFERENCES checkin.check_ins(check_in_id),
    wristband_id  VARCHAR(50)  NOT NULL,
    event_type    VARCHAR(20)  NOT NULL,
    scanned_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_rfid_audit PRIMARY KEY (audit_id)
);

CREATE INDEX idx_rfid_audit_checkin ON checkin.rfid_audit_log (check_in_id);
CREATE INDEX idx_rfid_audit_scanned ON checkin.rfid_audit_log (scanned_at DESC);
```

**Flyway naming convention:** `V{version}__{description}.sql`

- Version number increments from the last migration in the directory
- Description uses underscores (not hyphens)
- Migrations are forward-only — never edit a migration that has already been applied

---

## Adding a Column

### 1. Edit `data-stores.yaml`

Add the column to the appropriate table's `columns:` list:

```yaml
    check_ins:
      columns:
        - name: check_in_id
          type: UUID
          constraints: PK, DEFAULT gen_random_uuid()
        # ... existing columns ...
        - name: wristband_id       # ← new column
          type: VARCHAR(50)
          constraints: NULL
```

### 2. Write the Flyway Migration

```sql
-- V4__add_wristband_id_to_check_ins.sql
ALTER TABLE checkin.check_ins
    ADD COLUMN wristband_id VARCHAR(50) NULL;
```

!!! warning "Adding NOT NULL columns to existing tables"
    Adding a `NOT NULL` column without a default value will fail on a table that already has rows. Either supply a default, or add the column as nullable and apply `NOT NULL` in a separate migration after back-filling data.

---

## Adding an Index

### 1. Edit `data-stores.yaml`

Add the index to the table's `indexes:` list:

```yaml
    check_ins:
      indexes:
        - name: idx_checkin_reservation
          columns: reservation_id
        - name: idx_checkin_status_date    # ← new index
          columns: status, check_in_date
          type: composite
```

**Index type values:** omit for single-column B-tree (default), `composite`, `unique`, `partial`

### 2. Write the Flyway Migration

```sql
-- V5__add_checkin_status_date_index.sql
CREATE INDEX idx_checkin_status_date
    ON checkin.check_ins (status, check_in_date);
```

For detailed guidance on the full index change flow, see [How an Index Change Flows to Production](../database-change-workflow.md).

---

## Adding a Foreign Key Relationship

Foreign keys enforce referential integrity between tables. In NovaTrek, foreign keys exist within a service's own schema — they do NOT cross service boundaries (cross-service relationships use API calls, not database constraints).

### 1. Document the Relationship in `data-stores.yaml`

Use the `FK -> {table}` constraint notation to make the relationship explicit in the architectural model:

```yaml
    gear_verifications:
      columns:
        - name: verification_id
          type: UUID
          constraints: PK
        - name: check_in_id
          type: UUID
          constraints: NOT NULL, FK -> check_ins     # ← FK to parent table
        - name: gear_assignment_id
          type: UUID
          constraints: NOT NULL
```

### 2. Write the Flyway Migration

```sql
-- V6__add_gear_verification_fk.sql
ALTER TABLE checkin.gear_verifications
    ADD CONSTRAINT fk_gear_verification_checkin
    FOREIGN KEY (check_in_id)
    REFERENCES checkin.check_ins(check_in_id)
    ON DELETE CASCADE;
```

**ON DELETE behavior options:**

| Option | Use when |
|---|---|
| `ON DELETE CASCADE` | Child records have no meaning without the parent (e.g., gear verifications without a check-in) |
| `ON DELETE RESTRICT` | Child records must be manually cleaned up before parent deletion |
| `ON DELETE SET NULL` | Child records remain valid but lose the parent reference |

!!! warning "Cross-service foreign keys are prohibited"
    Never create a database-level foreign key that references a table owned by a different service. Cross-service relationships are enforced via API contracts, not database constraints. This is the core **bounded context** rule — see [Platform Principles](index.md#platform-principles).

---

## Removing a Column or Table

Removing schema elements requires careful coordination with consumers.

### Safe removal process

1. Verify no application code references the column/table (check service code and cross-service-calls.yaml)
2. If an API field corresponds to the column, mark the field `deprecated: true` in the OpenAPI spec first
3. After a grace period (at minimum one release cycle), write the drop migration:

```sql
-- V7__drop_legacy_code_column.sql
ALTER TABLE checkin.check_ins DROP COLUMN IF EXISTS legacy_code;
```

4. Remove the column from `data-stores.yaml`

!!! warning "Destructive migrations cannot be undone"
    Once a `DROP COLUMN` or `DROP TABLE` migration runs in production, data cannot be recovered unless there is a backup/restore. Always verify before merging.

---

## Updating the Data Store Metadata (Non-Schema)

You can also update non-schema metadata in `data-stores.yaml` without a Flyway migration — this only affects the portal documentation:

```yaml
svc-check-in:
  volume: ~6,000 check-ins/day peak season    # ← updated estimate
  connection_pool:
    min: 5
    max: 25                                    # ← increased pool size
    idle_timeout: 10min
  backup: Continuous WAL archiving, daily base backup, 14-day PITR    # ← updated retention
```

These metadata-only changes regenerate the portal service page but do not require a Flyway migration.

---

## Running the Generators

After editing `data-stores.yaml`, regenerate locally:

```bash
# Full regeneration
bash portal/scripts/generate-all.sh

# Microservice pages only (faster for data store changes)
python3 portal/scripts/generate-microservice-pages.py
```

Review the updated service page at `portal/docs/microservices/svc-{name}.md` to confirm the data store section reflects your changes.

---

## Known Gaps

**No drift detection between YAML and SQL.** There is no automated check that `data-stores.yaml` and the Flyway migration files are consistent. If an architect adds a column to the YAML but no migration is written, they will drift silently. A CI diff check is a planned Phase 3 enhancement.

**Two-step coordination gap.** The YAML change (architect) and the Flyway migration (developer) are coordinated via ticket and PR process, not automated tooling. The impact assessment in the solution design should explicitly list all required Flyway migrations.

---

## Checklist

- [ ] `data-stores.yaml` updated (table, columns, indexes, constraints)
- [ ] Flyway migration file written with correct naming convention
- [ ] `NOT NULL` columns have defaults or are added as nullable with a back-fill plan
- [ ] Cross-service foreign keys not introduced
- [ ] Destructive changes verified against API specs and service code
- [ ] Generators run without errors

---

!!! tip "Related guides"
    - [Database Change Workflow](../database-change-workflow.md) — detailed index change flow with CI steps
    - [API Contract Changes](api-contracts.md) — when schema changes affect a public API field
    - [Adding a Service](adding-a-service.md) — when the database is for a new service
    - [Metadata Registry](../standards/metadata-registry/index.md) — full reference for `data-stores.yaml` structure
