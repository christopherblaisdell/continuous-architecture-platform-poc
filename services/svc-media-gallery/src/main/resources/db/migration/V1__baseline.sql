CREATE SCHEMA IF NOT EXISTS media_gallery;

CREATE TABLE media_gallery.media_items (
    id                             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id                 UUID NOT NULL,
    trip_id                        UUID,
    uploader_type                  VARCHAR(30) NOT NULL,
    uploader_id                    UUID,
    media_type                     VARCHAR(30) NOT NULL,
    url                            VARCHAR(500) NOT NULL,
    thumbnail_url                  VARCHAR(500),
    file_size_bytes                INTEGER,
    captured_at                    TIMESTAMPTZ NOT NULL,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);

CREATE TABLE media_gallery.share_links (
    media_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token                          VARCHAR(255) NOT NULL,
    share_url                      VARCHAR(500) NOT NULL,
    expires_at                     TIMESTAMPTZ NOT NULL,
    download_count                 INTEGER,
    max_downloads                  INTEGER,
    created_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version                        INTEGER       NOT NULL DEFAULT 0
);
