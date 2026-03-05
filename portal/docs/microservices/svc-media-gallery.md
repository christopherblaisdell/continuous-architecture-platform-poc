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

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 + S3-Compatible Object Store |
| **Schema** | `media` |
| **Primary Tables** | `media_items`, `share_links`, `albums` |
| **Key Features** | S3-compatible storage for photos and videos | Presigned URLs for secure direct upload and download | Automatic thumbnail generation on upload |
| **Estimated Volume** | ~500 uploads/day peak season |

---

## :material-api: Endpoints (5 total)

---

### GET `/media` -- List media by reservation or trip { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Media/listMedia){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="svg/svc-media-gallery--get-media.svg" type="image/svg+xml" style="max-width: 100%;">GET /media sequence diagram</object></div>

---

### POST `/media` -- Upload a media item { .endpoint-post }

> Uploads a new photo, video, or panorama. The media is associated with a

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Media/uploadMedia){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="svg/svc-media-gallery--post-media.svg" type="image/svg+xml" style="max-width: 100%;">POST /media sequence diagram</object></div>

---

### GET `/media/{media_id}` -- Get media item details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Media/getMedia){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="svg/svc-media-gallery--get-media-media_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /media/{media_id} sequence diagram</object></div>

---

### DELETE `/media/{media_id}` -- Delete a media item { .endpoint-delete }

> Soft-deletes the media item. Underlying storage is purged after 30 days.

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Media/deleteMedia){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="svg/svc-media-gallery--delete-media-media_id.svg" type="image/svg+xml" style="max-width: 100%;">DELETE /media/{media_id} sequence diagram</object></div>

---

### POST `/media/{media_id}/share` -- Create a shareable link for a media item { .endpoint-post }

> Generates a time-limited, tokenized URL for sharing with non-authenticated users.

[:material-open-in-new: View in Swagger UI](../services/api/svc-media-gallery.html#/Sharing/createShareLink){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="svg/svc-media-gallery--post-media-media_id-share.svg" type="image/svg+xml" style="max-width: 100%;">POST /media/{media_id}/share sequence diagram</object></div>
