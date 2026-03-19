package com.novatrek.emergencyresponse.entity;

import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class TimelineEntryTest {

    @Test
    void gettersAndSetters() {
        TimelineEntry e = new TimelineEntry();
        UUID id = UUID.randomUUID();
        e.setEntryId(id);
        UUID emergencyId = UUID.randomUUID();
        e.setEmergencyId(emergencyId);
        e.setEventType(TimelineEntry.EventType.created);
        e.setDescription("Emergency reported at trailhead");
        e.setActor("ranger-01");
        OffsetDateTime now = OffsetDateTime.now();
        e.setTimestamp(now);
        e.setVersion(1);

        assertEquals(id, e.getEntryId());
        assertEquals(emergencyId, e.getEmergencyId());
        assertEquals(TimelineEntry.EventType.created, e.getEventType());
        assertEquals("Emergency reported at trailhead", e.getDescription());
        assertEquals("ranger-01", e.getActor());
        assertEquals(now, e.getTimestamp());
        assertEquals(1, e.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        TimelineEntry e = new TimelineEntry();
        e.onCreate();
        assertNotNull(e.getCreatedAt());
        assertNotNull(e.getUpdatedAt());

        e.onUpdate();
        assertNotNull(e.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(6, TimelineEntry.EventType.values().length);
        assertNotNull(TimelineEntry.EventType.valueOf("status_change"));
        assertNotNull(TimelineEntry.EventType.valueOf("dispatch"));
        assertNotNull(TimelineEntry.EventType.valueOf("escalation"));
        assertNotNull(TimelineEntry.EventType.valueOf("resolution"));
    }
}
