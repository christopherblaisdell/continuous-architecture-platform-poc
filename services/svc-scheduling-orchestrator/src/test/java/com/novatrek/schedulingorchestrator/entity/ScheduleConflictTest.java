package com.novatrek.schedulingorchestrator.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ScheduleConflictTest {

    @Test
    void gettersAndSetters() {
        ScheduleConflict c = new ScheduleConflict();
        UUID id = UUID.randomUUID();
        c.setId(id);
        c.setType(ScheduleConflict.ConflictType.GUIDE_DOUBLE_BOOKED);
        c.setSeverity(ScheduleConflict.ConflictSeverity.HIGH);
        c.setDescription("Guide assigned to two trips");
        c.setConflictDate(LocalDate.of(2025, 7, 1));
        UUID regionId = UUID.randomUUID();
        c.setRegionId(regionId);
        c.setResolved(false);
        OffsetDateTime now = OffsetDateTime.now();
        c.setResolvedAt(now);
        c.setDetectedAt(now);
        c.setVersion(1);

        assertEquals(id, c.getId());
        assertEquals(ScheduleConflict.ConflictType.GUIDE_DOUBLE_BOOKED, c.getType());
        assertEquals(ScheduleConflict.ConflictSeverity.HIGH, c.getSeverity());
        assertEquals("Guide assigned to two trips", c.getDescription());
        assertEquals(LocalDate.of(2025, 7, 1), c.getConflictDate());
        assertEquals(regionId, c.getRegionId());
        assertFalse(c.getResolved());
        assertEquals(now, c.getResolvedAt());
        assertEquals(now, c.getDetectedAt());
        assertEquals(1, c.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        ScheduleConflict c = new ScheduleConflict();
        c.onCreate();
        assertNotNull(c.getCreatedAt());
        assertNotNull(c.getUpdatedAt());

        c.onUpdate();
        assertNotNull(c.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(4, ScheduleConflict.ConflictType.values().length);
        assertEquals(4, ScheduleConflict.ConflictSeverity.values().length);
    }
}
