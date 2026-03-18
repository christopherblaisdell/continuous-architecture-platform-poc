package com.novatrek.mediagallery.repository;

import com.novatrek.mediagallery.entity.MediaItem;
import com.novatrek.mediagallery.entity.ShareLink;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class MediaGalleryRepositoryTest {

    @Autowired
    private MediaItemRepository mediaItemRepository;

    @Autowired
    private ShareLinkRepository shareLinkRepository;

    @Test
    void saveAndFindMediaItem() {
        MediaItem item = new MediaItem();
        item.setReservationId(UUID.randomUUID());
        item.setTripId(UUID.randomUUID());
        item.setUploaderType(MediaItem.UploaderType.GUIDE);
        item.setUploaderId(UUID.randomUUID());
        item.setMediaType(MediaItem.MediaType.PHOTO);
        item.setUrl("https://cdn.novatrek.example.com/img/test.jpg");
        item.setThumbnailUrl("https://cdn.novatrek.example.com/thumb/test.jpg");
        item.setFileSizeBytes(2048000);
        item.setCapturedAt(OffsetDateTime.now());

        MediaItem saved = mediaItemRepository.save(item);
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);

        MediaItem found = mediaItemRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getMediaType()).isEqualTo(MediaItem.MediaType.PHOTO);
        assertThat(found.getUploaderType()).isEqualTo(MediaItem.UploaderType.GUIDE);
        assertThat(found.getFileSizeBytes()).isEqualTo(2048000);
    }

    @Test
    void mediaTypeEnumValues() {
        for (MediaItem.MediaType mt : MediaItem.MediaType.values()) {
            MediaItem item = new MediaItem();
            item.setReservationId(UUID.randomUUID());
            item.setMediaType(mt);
            item.setUrl("https://cdn.novatrek.example.com/" + mt.name());
            item.setCapturedAt(OffsetDateTime.now());

            MediaItem saved = mediaItemRepository.save(item);
            assertThat(mediaItemRepository.findById(saved.getId()).orElseThrow().getMediaType()).isEqualTo(mt);
        }
    }

    @Test
    void saveAndFindShareLink() {
        ShareLink link = new ShareLink();
        link.setToken("abc123token");
        link.setShareUrl("https://share.novatrek.example.com/abc123token");
        link.setExpiresAt(OffsetDateTime.now().plusDays(7));
        link.setDownloadCount(0);
        link.setMaxDownloads(10);

        ShareLink saved = shareLinkRepository.save(link);
        assertThat(saved.getMediaId()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);

        ShareLink found = shareLinkRepository.findById(saved.getMediaId()).orElseThrow();
        assertThat(found.getToken()).isEqualTo("abc123token");
        assertThat(found.getMaxDownloads()).isEqualTo(10);
    }
}
