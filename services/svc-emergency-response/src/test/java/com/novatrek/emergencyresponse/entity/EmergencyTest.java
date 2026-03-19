package com.novatrek.emergencyresponse.entity;

import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class EmergencyTest {

    @Test
    void gettersAndSetters() {
        Emergency e = new Emergency();
        UUID id = UUID.randomUUID();
        e.setEmergencyId(id);
        UUID guestId = UUID.randomUUID();
        e.setGuestId(guestId);
        UUID resId = UUID.randomUUID();
        e.setReservationId(resId);
        e.setType("INJURY");
        e.setSeverity("HIGH");
        e.setStatus("ACTIVE");
        e.setDescription("Guest fell on trail");
        e.setReportedBy("guide-01");
        UUID dispatchId = UUID.randomUUID();
        e.setDispatchId(dispatchId);
        e.setResolutionNotes("Treated on site");
        OffsetDateTime now = OffsetDateTime.now();
        e.setResolvedAt(now);
        e.setRev("rev-1");
        e.setVersion(1);

        assertEquals(id, e.getEmergencyId());
        assertEquals(guestId, e.getGuestId());
        assertEquals(resId, e.getReservationId());
        assertEquals("INJURY", e.getType());
        assertEquals("HIGH", e.getSeverity());
        assertEquals("ACTIVE", e.getStatus());
        assertEquals("Guest fell on trail", e.getDescription());
        assertEquals("guide-01", e.getReportedBy());
        assertEquals(dispatchId, e.getDispatchId());
        assertEquals("Treated on site", e.getResolutionNotes());
        assertEquals(now, e.getResolvedAt());
        assertEquals("rev-1", e.getRev());
        assertEquals(1, e.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Emergency e = new Emergency();
        e.onCreate();
        assertNotNull(e.getCreatedAt());
        assertNotNull(e.getUpdatedAt());

        e.onUpdate();
        assertNotNull(e.getUpdatedAt());
    }
}
