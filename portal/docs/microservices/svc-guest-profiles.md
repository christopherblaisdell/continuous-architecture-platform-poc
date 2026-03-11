---
tags:
  - microservice
  - svc-guest-profiles
  - guest-identity
---

# svc-guest-profiles

**NovaTrek Adventures - Guest Profiles Service** &nbsp;|&nbsp; <span style="background: #7c3aed15; color: #7c3aed; border: 1px solid #7c3aed40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Guest Identity</span> &nbsp;|&nbsp; `v2.4.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages guest registration, profile management, preferences, medical

[:material-api: Swagger UI](../services/api/svc-guest-profiles.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-guest-profiles.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-guest-profiles.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-guest-profiles){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-guest-profiles){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 1 -- Guest Identity and Product Catalog

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :white_check_mark: complete |
| Database Schema (Flyway) | :white_check_mark: complete |
| CI Pipeline | :material-circle-outline: not-started |
| CD Pipeline | :material-circle-outline: not-started |
| Deployed to Dev | :white_check_mark: complete |
| Smoke Tested | :white_check_mark: complete |
| Deployed to Prod | :material-circle-outline: not-started |

**Azure Resources (Dev):**

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-guest-profiles)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/psql-novatrek-dev)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-guest-profiles C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-guest-profiles entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `guests` |
| **Tables** | `guest_profiles`, `certifications`, `medical_info`, `emergency_contacts`, `adventure_history` |
| **Estimated Volume** | ~800 new profiles/day peak season |
| **Connection Pool** | min 10 / max 30 / idle timeout 10min |
| **Backup Strategy** | Continuous WAL archiving, daily base backup, 90-day PITR (GDPR) |

### Key Features

- PII encrypted at rest (AES-256)
- Composite index on (last_name, date_of_birth)
- Soft delete with GDPR data retention policy

### Table Reference

#### `guest_profiles`

*Core guest identity records with PII encryption*

| Column | Type | Constraints |
|--------|------|-------------|
| `guest_id` | `UUID` | PK |
| `first_name` | `VARCHAR(100)` | NOT NULL, ENCRYPTED |
| `last_name` | `VARCHAR(100)` | NOT NULL, ENCRYPTED |
| `email` | `VARCHAR(255)` | NOT NULL, UNIQUE, ENCRYPTED |
| `phone` | `VARCHAR(30)` | NULL, ENCRYPTED |
| `date_of_birth` | `DATE` | NOT NULL |
| `loyalty_tier` | `VARCHAR(20)` | DEFAULT 'bronze' |
| `identity_verified` | `BOOLEAN` | NOT NULL, DEFAULT FALSE |
| `deleted_at` | `TIMESTAMPTZ` | NULL (soft delete) |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_guest_email` on `email` (UNIQUE)
- `idx_guest_name_dob` on `last_name, date_of_birth`
- `idx_guest_loyalty` on `loyalty_tier`

#### `certifications`

*Guest adventure certifications (scuba, climbing, etc.)*

| Column | Type | Constraints |
|--------|------|-------------|
| `cert_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL, FK -> guest_profiles |
| `cert_type` | `VARCHAR(50)` | NOT NULL |
| `issuer` | `VARCHAR(100)` | NOT NULL |
| `issued_date` | `DATE` | NOT NULL |
| `expiry_date` | `DATE` | NULL |
| `document_url` | `TEXT` | NULL |

**Indexes:**

- `idx_cert_guest` on `guest_id`
- `idx_cert_expiry` on `expiry_date`

#### `medical_info`

*Guest medical conditions and allergy records (encrypted PII)*

| Column | Type | Constraints |
|--------|------|-------------|
| `medical_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL, FK -> guest_profiles |
| `conditions` | `JSONB` | ENCRYPTED |
| `allergies` | `JSONB` | ENCRYPTED |
| `emergency_medications` | `JSONB` | ENCRYPTED |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_medical_guest` on `guest_id` (UNIQUE)

#### `emergency_contacts`

*Emergency contact information for each guest*

| Column | Type | Constraints |
|--------|------|-------------|
| `contact_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL, FK -> guest_profiles |
| `name` | `VARCHAR(200)` | NOT NULL, ENCRYPTED |
| `phone` | `VARCHAR(30)` | NOT NULL, ENCRYPTED |
| `relationship` | `VARCHAR(50)` | NOT NULL |
| `is_primary` | `BOOLEAN` | NOT NULL, DEFAULT TRUE |

**Indexes:**

- `idx_emg_guest` on `guest_id`

#### `adventure_history`

*Record of completed adventures per guest for profile display*

| Column | Type | Constraints |
|--------|------|-------------|
| `history_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL, FK -> guest_profiles |
| `trip_id` | `UUID` | NOT NULL |
| `trip_date` | `DATE` | NOT NULL |
| `adventure_category` | `VARCHAR(50)` | NOT NULL |
| `rating` | `SMALLINT` | NULL, CHECK (1-5) |
| `completed_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_hist_guest` on `guest_id, trip_date DESC`


---

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10008 | [Guest Reviews and Ratings Platform](../solutions/_NTK-10008-guest-reviews-and-ratings.md) | `CAP-1.7`, `CAP-1.2` | 2026-03-06 |

---

## :material-api: Endpoints (9 total)

---

### GET `/guests` -- Search guests { .endpoint-get }

> Search and filter the guest registry. Supports partial name matching,

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Guests/searchGuests){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--get-guests.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--get-guests.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests sequence diagram</object></div>

---

### POST `/guests` -- Register a new guest { .endpoint-post }

> Create a new guest profile. The email address must be unique across

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Guests/createGuest){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--post-guests.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--post-guests.svg" type="image/svg+xml" style="max-width: 100%;">POST /guests sequence diagram</object></div>

---

### GET `/guests/{guest_id}` -- Get guest profile { .endpoint-get }

> Retrieve the full profile for a specific guest by ID.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Guests/getGuest){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--get-guests-guest_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--get-guests-guest_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id} sequence diagram</object></div>

---

### PATCH `/guests/{guest_id}` -- Update guest profile { .endpoint-patch }

> Partially update a guest profile. Only the fields provided in the

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Guests/updateGuest){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--patch-guests-guest_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--patch-guests-guest_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /guests/{guest_id} sequence diagram</object></div>

---

### GET `/guests/{guest_id}/certifications` -- List guest certifications { .endpoint-get }

> Retrieve all certifications on file for a guest, including expired

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Certifications/listGuestCertifications){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--get-guests-guest_id-certifications.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--get-guests-guest_id-certifications.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/certifications sequence diagram</object></div>

---

### POST `/guests/{guest_id}/certifications` -- Add a certification { .endpoint-post }

> Record a new certification for a guest. Certification documents

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Certifications/addGuestCertification){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--post-guests-guest_id-certifications.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--post-guests-guest_id-certifications.svg" type="image/svg+xml" style="max-width: 100%;">POST /guests/{guest_id}/certifications sequence diagram</object></div>

---

### GET `/guests/{guest_id}/medical-info` -- Get guest medical information { .endpoint-get }

> Retrieve the medical information on file for a guest. Access to this

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Medical/getGuestMedicalInfo){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--get-guests-guest_id-medical-info.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--get-guests-guest_id-medical-info.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/medical-info sequence diagram</object></div>

---

### PUT `/guests/{guest_id}/medical-info` -- Update guest medical information { .endpoint-put }

> Replace the medical information record for a guest. This is a full

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Medical/updateGuestMedicalInfo){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--put-guests-guest_id-medical-info.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--put-guests-guest_id-medical-info.svg" type="image/svg+xml" style="max-width: 100%;">PUT /guests/{guest_id}/medical-info sequence diagram</object></div>

---

### GET `/guests/{guest_id}/adventure-history` -- Get guest adventure history { .endpoint-get }

> Retrieve the adventure participation history for a guest. Each entry

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/History/getGuestAdventureHistory){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-guest-profiles--get-guests-guest_id-adventure-history.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-guest-profiles--get-guests-guest_id-adventure-history.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/adventure-history sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Booking Flow, Guest Profile, Waiver Signing |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Check-In Station, Safety Incident Board |
| [Adventure App](../../applications/app-guest-mobile/) | Self Check-In, Earn Loyalty Points |

---

## :material-broadcast: Events Published

| Event | Channel | Trigger | Consumers |
|-------|---------|---------|-----------|
| [`guest.registered`](/events/#guestregistered) | `novatrek.guest-identity.guest.registered` | [`POST /guests`](#post-guests-register-a-new-guest) | [svc-loyalty-rewards](../svc-loyalty-rewards/), [svc-analytics](../svc-analytics/) |
