package com.novatrek.guidemanagement.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GuideScheduleEntryTest {

    @Test
    void gettersAndSetters() {
        GuideScheduleEntry e = new GuideScheduleEntry();
        UUID id = UUID.randomUUID();
        e.setId(id);
        UUID guideId = UUID.randomUUID();
        e.setGuideId(guideId);
        UUID tripId = UUID.randomUUID();
        e.setTripId(tripId);
        e.setTripName("Alpine Summit Trek");
        e.setDepartureDate(LocalDate.of(2025, 7, 1));
        e.setReturnDate(LocalDate.of(2025, 7, 5));
        e.setRole(GuideScheduleEntry.GuideRole.LEAD);
        e.setGroupSize(10);
        e.setVersion(1);

        assertEquals(id, e.getId());
        assertEquals(guideId, e.getGuideId());
        assertEquals(tripId, e.getTripId());
        assertEquals("Alpine Summit Trek", e.getTripName());
        assertEquals(LocalDate.of(2025, 7, 1), e.getDepartureDate());
        assertEquals(LocalDate.of(2025, 7, 5), e.getReturnDate());
        assertEquals(GuideScheduleEntry.GuideRole.LEAD, e.getRole());
        assertEquals(10, e.getGroupSize());
        assertEquals(1, e.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        GuideScheduleEntry e = new GuideScheduleEntry();
        e.onCreate();
        assertNotNull(e.getCreatedAt());
        assertNotNull(e.getUpdatedAt());

        e.onUpdate();
        assertNotNull(e.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(3, GuideScheduleEntry.GuideRole.values().length);
    }
}
