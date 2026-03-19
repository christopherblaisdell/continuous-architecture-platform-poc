package com.novatrek.guidemanagement.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GuideRatingTest {

    @Test
    void gettersAndSetters() {
        GuideRating r = new GuideRating();
        UUID id = UUID.randomUUID();
        r.setId(id);
        UUID guideId = UUID.randomUUID();
        r.setGuideId(guideId);
        UUID resId = UUID.randomUUID();
        r.setReservationId(resId);
        UUID guestId = UUID.randomUUID();
        r.setGuestId(guestId);
        r.setRating(5);
        r.setReviewText("Amazing guide!");
        r.setDate(LocalDate.of(2025, 5, 1));
        r.setVersion(1);

        assertEquals(id, r.getId());
        assertEquals(guideId, r.getGuideId());
        assertEquals(resId, r.getReservationId());
        assertEquals(guestId, r.getGuestId());
        assertEquals(5, r.getRating());
        assertEquals("Amazing guide!", r.getReviewText());
        assertEquals(LocalDate.of(2025, 5, 1), r.getDate());
        assertEquals(1, r.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        GuideRating r = new GuideRating();
        r.onCreate();
        assertNotNull(r.getCreatedAt());
        assertNotNull(r.getUpdatedAt());

        r.onUpdate();
        assertNotNull(r.getUpdatedAt());
    }
}
