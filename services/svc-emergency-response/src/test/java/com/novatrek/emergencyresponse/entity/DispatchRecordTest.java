package com.novatrek.emergencyresponse.entity;

import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class DispatchRecordTest {

    @Test
    void gettersAndSetters() {
        DispatchRecord d = new DispatchRecord();
        UUID id = UUID.randomUUID();
        d.setDispatchId(id);
        UUID emergencyId = UUID.randomUUID();
        d.setEmergencyId(emergencyId);
        UUID teamId = UUID.randomUUID();
        d.setRescueTeamId(teamId);
        d.setPriority("HIGH");
        d.setStatus(DispatchRecord.Status.dispatched);
        OffsetDateTime now = OffsetDateTime.now();
        d.setDispatchedAt(now);
        d.setEtaMinutes(25);
        d.setVersion(1);

        assertEquals(id, d.getDispatchId());
        assertEquals(emergencyId, d.getEmergencyId());
        assertEquals(teamId, d.getRescueTeamId());
        assertEquals("HIGH", d.getPriority());
        assertEquals(DispatchRecord.Status.dispatched, d.getStatus());
        assertEquals(now, d.getDispatchedAt());
        assertEquals(25, d.getEtaMinutes());
        assertEquals(1, d.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        DispatchRecord d = new DispatchRecord();
        d.onCreate();
        assertNotNull(d.getCreatedAt());
        assertNotNull(d.getUpdatedAt());

        d.onUpdate();
        assertNotNull(d.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(5, DispatchRecord.Status.values().length);
        assertNotNull(DispatchRecord.Status.valueOf("en_route"));
        assertNotNull(DispatchRecord.Status.valueOf("on_scene"));
        assertNotNull(DispatchRecord.Status.valueOf("returning"));
        assertNotNull(DispatchRecord.Status.valueOf("completed"));
    }
}
