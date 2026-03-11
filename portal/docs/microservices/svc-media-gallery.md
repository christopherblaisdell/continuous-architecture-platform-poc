---
tags:
  - microservice
  - svc-media-gallery
  - support
---

# svc-media-gallery

**NovaTrek Media Gallery Service** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v1.0.2` &nbsp;|&nbsp; *NovaTrek Digital Experience Team*

> Manages trip photos, videos, and media content captured during NovaTrek adventures.

[:material-api: Swagger UI](../services/api/svc-media-gallery.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-media-gallery.yaml){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-media-gallery){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 5 -- Analytics, Loyalty, and Media

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :material-circle-outline: not-started |
| Database Schema (Flyway) | :material-circle-outline: not-started |
| CI Pipeline | :material-circle-outline: not-started |
| CD Pipeline | :material-circle-outline: not-started |
| Deployed to Dev | :material-circle-outline: not-started |
| Smoke Tested | :material-circle-outline: not-started |
| Deployed to Prod | :material-circle-outline: not-started |

**Azure Resources (Dev):**

- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/psql-novatrek-dev)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-media-gallery--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-media-gallery--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-media-gallery C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-media-gallery--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-media-gallery--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-media-gallery entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 + S3-Compatible Object Store |
| **Schema** | `media` |
| **Tables** | `media_items`, `share_links`, `albums` |
| **Estimated Volume** | ~500 uploads/day peak season |
| **Connection Pool** | min 3 / max 15 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, S3 cross-region replication |

### Key Features

- S3-compatible storage for photos and videos
- Presigned URLs for secure direct upload and download
- Automatic thumbnail generation on upload

### Table Reference

#### `media_items`

*Metadata for uploaded photos and videos (binary stored in S3)*

| Column | Type | Constraints |
|--------|------|-------------|
| `media_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL |
| `trip_id` | `UUID` | NULL |
| `media_type` | `VARCHAR(20)` | NOT NULL (photo/video) |
| `s3_key` | `VARCHAR(512)` | NOT NULL |
| `thumbnail_key` | `VARCHAR(512)` | NULL |
| `file_size_bytes` | `BIGINT` | NOT NULL |
| `width` | `INTEGER` | NULL |
| `height` | `INTEGER` | NULL |
| `gps_lat` | `DECIMAL(9,6)` | NULL |
| `gps_lng` | `DECIMAL(9,6)` | NULL |
| `uploaded_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_media_guest` on `guest_id, uploaded_at DESC`
- `idx_media_trip` on `trip_id`

#### `share_links`

*Shareable links for media items with expiry*

| Column | Type | Constraints |
|--------|------|-------------|
| `link_id` | `UUID` | PK |
| `media_id` | `UUID` | NOT NULL, FK -> media_items |
| `token` | `VARCHAR(128)` | NOT NULL, UNIQUE |
| `expires_at` | `TIMESTAMPTZ` | NOT NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_share_token` on `token` (UNIQUE)
- `idx_share_expiry` on `expires_at`

#### `albums`

*Guest-created photo albums grouping media items*

| Column | Type | Constraints |
|--------|------|-------------|
| `album_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL |
| `name` | `VARCHAR(200)` | NOT NULL |
| `cover_media_id` | `UUID` | NULL, FK -> media_items |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_album_guest` on `guest_id`


---

## :material-api: Endpoints (5 total)

---

### GET `/media` -- List media by reservation or trip { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Media/listMedia){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-media-gallery--get-media.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-media-gallery--get-media.svg" type="image/svg+xml" style="max-width: 100%;">GET /media sequence diagram</object></div>

---

### POST `/media` -- Upload a media item { .endpoint-post }

> Uploads a new photo, video, or panorama. The media is associated with a

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Media/uploadMedia){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-media-gallery--post-media.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-media-gallery--post-media.svg" type="image/svg+xml" style="max-width: 100%;">POST /media sequence diagram</object></div>

---

### GET `/media/{media_id}` -- Get media item details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Media/getMedia){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-media-gallery--get-media-media_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-media-gallery--get-media-media_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /media/{media_id} sequence diagram</object></div>

---

### DELETE `/media/{media_id}` -- Delete a media item { .endpoint-delete }

> Soft-deletes the media item. Underlying storage is purged after 30 days.

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Media/deleteMedia){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-media-gallery--delete-media-media_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-media-gallery--delete-media-media_id.svg" type="image/svg+xml" style="max-width: 100%;">DELETE /media/{media_id} sequence diagram</object></div>

---

### POST `/media/{media_id}/share` -- Create a shareable link for a media item { .endpoint-post }

> Generates a time-limited, tokenized URL for sharing with non-authenticated users.

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Sharing/createShareLink){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-media-gallery--post-media-media_id-share.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-media-gallery--post-media-media_id-share.svg" type="image/svg+xml" style="max-width: 100%;">POST /media/{media_id}/share sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Trip Browser, Trip Gallery |
| [Adventure App](../../applications/app-guest-mobile/) | Photo Upload |
