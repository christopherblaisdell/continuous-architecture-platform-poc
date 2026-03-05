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

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `guests` |
| **Primary Tables** | `guest_profiles`, `certifications`, `medical_info`, `emergency_contacts`, `adventure_history` |
| **Key Features** | PII encrypted at rest (AES-256) | Composite index on (last_name, date_of_birth) | Soft delete with GDPR data retention policy |
| **Estimated Volume** | ~800 new profiles/day peak season |

---

## :material-api: Endpoints (9 total)

---

### GET `/guests` -- Search guests { .endpoint-get }

> Search and filter the guest registry. Supports partial name matching,

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Guests/searchGuests){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--get-guests.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests sequence diagram</object></div>

---

### POST `/guests` -- Register a new guest { .endpoint-post }

> Create a new guest profile. The email address must be unique across

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Guests/createGuest){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--post-guests.svg" type="image/svg+xml" style="max-width: 100%;">POST /guests sequence diagram</object></div>

---

### GET `/guests/{guest_id}` -- Get guest profile { .endpoint-get }

> Retrieve the full profile for a specific guest by ID.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Guests/getGuest){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--get-guests-guest_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id} sequence diagram</object></div>

---

### PATCH `/guests/{guest_id}` -- Update guest profile { .endpoint-patch }

> Partially update a guest profile. Only the fields provided in the

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Guests/updateGuest){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--patch-guests-guest_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /guests/{guest_id} sequence diagram</object></div>

---

### GET `/guests/{guest_id}/certifications` -- List guest certifications { .endpoint-get }

> Retrieve all certifications on file for a guest, including expired

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Certifications/listGuestCertifications){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--get-guests-guest_id-certifications.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/certifications sequence diagram</object></div>

---

### POST `/guests/{guest_id}/certifications` -- Add a certification { .endpoint-post }

> Record a new certification for a guest. Certification documents

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Certifications/addGuestCertification){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--post-guests-guest_id-certifications.svg" type="image/svg+xml" style="max-width: 100%;">POST /guests/{guest_id}/certifications sequence diagram</object></div>

---

### GET `/guests/{guest_id}/medical-info` -- Get guest medical information { .endpoint-get }

> Retrieve the medical information on file for a guest. Access to this

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Medical/getGuestMedicalInfo){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--get-guests-guest_id-medical-info.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/medical-info sequence diagram</object></div>

---

### PUT `/guests/{guest_id}/medical-info` -- Update guest medical information { .endpoint-put }

> Replace the medical information record for a guest. This is a full

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/Medical/updateGuestMedicalInfo){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--put-guests-guest_id-medical-info.svg" type="image/svg+xml" style="max-width: 100%;">PUT /guests/{guest_id}/medical-info sequence diagram</object></div>

---

### GET `/guests/{guest_id}/adventure-history` -- Get guest adventure history { .endpoint-get }

> Retrieve the adventure participation history for a guest. Each entry

[:material-open-in-new: View in Swagger UI](../services/api/svc-guest-profiles.html#/History/getGuestAdventureHistory){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-guest-profiles--get-guests-guest_id-adventure-history.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/adventure-history sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../applications/web-guest-portal/) | Booking Flow, Guest Profile, Waiver Signing |
| [Operations Dashboard](../applications/web-ops-dashboard/) | Check-In Station, Safety Incident Board |
| [Adventure App](../applications/app-guest-mobile/) | Self Check-In, Earn Loyalty Points |
