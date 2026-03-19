package com.novatrek.guidemanagement.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class AvailabilityWindowTest {

    @Test
    void gettersAndSetters() {
        AvailabilityWindow w = new AvailabilityWindow();
        UUID id = UUID.randomUUID();
        w.setId(id);
        UUID guideId = UUID.randomUUID();
        w.setGuideId(guideId);
        w.setStartDate(LocalDate.of(2025, 6, 1));
        w.setEndDate(LocalDate.of(2025, 6, 30));
        w.setAvailable(true);
        w.setNotes("Summer availability");
        w.setVersion(1);

        assertEquals(id, w.getId());
        assertEquals(guideId, w.getGuideId());
        assertEquals(LocalDate.of(2025, 6, 1), w.getStartDate());
        assertEquals(LocalDate.of(2025, 6, 30), w.getEndDate());
        assertTrue(w.getAvailable());
        assertEquals("Summer availability", w.getNotes());
        assertEquals(1, w.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        AvailabilityWindow w = new AvailabilityWindow();
        w.onCreate();
        assertNotNull(w.getCreatedAt());
        assertNotNull(w.getUpdatedAt());

        w.onUpdate();
        assertNotNull(w.getUpdatedAt());
    }
}
